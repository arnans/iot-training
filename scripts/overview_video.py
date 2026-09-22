"""Build the three pre-workshop overview videos from one talking-head take.

Usage:
    python scripts/overview_video.py planning/overview-video-edit.json [--check] [--only V1 V2]
        [--render preview|h264|h265]

Reads the edit JSON (see OVERVIEW-VIDEO-PLAN.md) and, per video:

1. Resolves every insert and chapter cue against the ASR word stream (Thai, no spaces:
   the words are joined into one string and substring-searched, forward from the previous
   cue, so repeated phrases resolve in order).
2. Snaps the video's in/out to the quietest 30 ms of audio within ±0.12 s, so a cut never
   clips a syllable.
3. Times each insert: starts `lead_s` before its phrase, ends at the first of its hold, the
   next insert or zoom, or the end of the talk. An insert starting inside a zoom is an error.
4. Prepares every insert as 1920×1080 media in <work_dir>/inserts/: photos fill the frame,
   diagrams and screenshots sit on the concept-art cream, pairs go side by side, screen
   recordings are speed-fitted to their slot (capped at `max_speed`; beyond that the clip's
   last stretch is used, which is where the finished result is). Anything not yet on disk
   becomes a grey PLACEHOLDER still so the cut can be reviewed before all art exists.
5. Writes <work_dir>/xml/<V>.xml (FCP7 XML for Premiere), <V>-chapters.txt (YouTube
   description format) and <V>-report.md.

Speaker zooms are a razor on V1 plus a Basic Motion scale on the zoomed piece, centre 0,0.
A centred 115% crop was checked against every zoom span before choosing it: eyes sit on the
upper-third line and no gesture leaves the frame, so no centre offset is needed (Premiere's
normalised Center units are then irrelevant). Audio stays one unbroken clip on A1.

--render also encodes the finished video with ffmpeg + NVENC straight from the same
decisions: `preview` is 960×540 for review, `h264`/`h265` are 1080p deliverables.
"""

import argparse
import json
import subprocess
import sys
import time
import wave
from pathlib import Path
from urllib.parse import quote
from xml.sax.saxutils import escape

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
CREAM = (248, 244, 232)
W, H = 1920, 1080
FONT_TH = r"C:\Windows\Fonts\LeelawUI.ttf"
FONT_TH_BOLD = r"C:\Windows\Fonts\LeelaUIb.ttf"
FONT_DIR = ROOT / "scripts" / "fonts"  # Prompt (SIL OFL), kept in the repo so any machine has it


def find_chrome() -> str:
    """$CHROME if set, else Chrome on PATH or in its usual Windows install folders."""
    import os
    import shutil
    cands = [os.environ.get("CHROME"), shutil.which("chrome"), shutil.which("google-chrome")]
    for base in ("PROGRAMFILES", "PROGRAMFILES(X86)", "LOCALAPPDATA"):
        if os.environ.get(base):
            cands.append(str(Path(os.environ[base]) / "Google/Chrome/Application/chrome.exe"))
    return next((c for c in cands if c and Path(c).exists()), "chrome")


CHROME = find_chrome()
PHOTO_EXT = {".jpg", ".jpeg", ".webp"}
VIDEO_EXT = {".mp4", ".mov", ".mkv", ".webm"}


# ---------------------------------------------------------------- helpers

def run(cmd: list, **kw) -> str:
    r = subprocess.run([str(c) for c in cmd], capture_output=True, text=True,
                       encoding="utf-8", errors="replace", **kw)
    if r.returncode != 0:
        sys.exit(f"command failed (exit {r.returncode}): {str(cmd[0])} ... {str(cmd[-1])}\n"
                 f"{(r.stderr or r.stdout)[-2500:]}")
    return r.stdout


def probe(path: Path) -> dict:
    d = json.loads(run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                        "stream=width,height,r_frame_rate:format=duration", "-of", "json", path]))
    n, m = d["streams"][0]["r_frame_rate"].split("/")
    return {"width": d["streams"][0]["width"], "height": d["streams"][0]["height"],
            "fps": float(n) / float(m), "duration_s": float(d["format"]["duration"])}


_NVENC = None


def nvenc_ok() -> bool:
    """NVENC crashes ffmpeg outright (0xC0000005) on driver 616.92 + RTX 5060 Ti, as of Sep 2026,
    so probe it on a 1 s test pattern in a child process and fall back to x264/x265 on the CPU."""
    global _NVENC
    if _NVENC is None:
        r = subprocess.run(["ffmpeg", "-v", "error", "-f", "lavfi", "-i",
                            "testsrc2=s=1280x720:r=30:d=1", "-c:v", "h264_nvenc", "-f", "null", "-"],
                           capture_output=True)
        _NVENC = r.returncode == 0
        if not _NVENC:
            print("   (NVENC unavailable, encoding on the CPU)")
    return _NVENC


def fmt(t: float) -> str:
    return f"{int(t // 60)}:{t % 60:05.2f}"


def yt(t: float) -> str:
    t = int(t)
    return f"{t // 3600}:{t // 60 % 60:02d}:{t % 60:02d}" if t >= 3600 else f"{t // 60}:{t % 60:02d}"


def pathurl(p: Path) -> str:
    return "file://localhost/" + quote(p.resolve().as_posix(), safe="/:")


# ---------------------------------------------------------------- word stream

class Words:
    def __init__(self, asr_path: Path):
        d = json.loads(asr_path.read_text(encoding="utf-8"))
        self.words = d["words"]
        chars, self.cs, self.ce = [], [], []
        for w in self.words:
            for _ in w["w"]:
                self.cs.append(w["s"])
                self.ce.append(w["e"])
            chars.append(w["w"])
        self.text = "".join(chars)

    def find(self, needle: str, after: float) -> float | None:
        """Start time of the first occurrence of `needle` that starts at or after `after`."""
        i = self.text.find(needle)
        while i >= 0:
            if self.cs[i] >= after - 1e-6:
                return self.cs[i]
            i = self.text.find(needle, i + 1)
        return None


class Audio:
    def __init__(self, wav_path: Path):
        with wave.open(str(wav_path)) as w:
            self.sr = w.getframerate()
            self.x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32)

    def quietest(self, t: float, radius: float = 0.12, win: float = 0.03) -> float:
        n = int(win * self.sr)
        a = max(0, int((t - radius) * self.sr))
        b = min(len(self.x) - n, int((t + radius) * self.sr))
        if b <= a:
            return t
        best, best_e = t, None
        for s in range(a, b, n // 3 or 1):
            e = float(np.mean(self.x[s:s + n] ** 2))
            if best_e is None or e < best_e:
                best, best_e = (s + n / 2) / self.sr, e
        return best


# ---------------------------------------------------------------- media prep

def font(size: int, bold=False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_TH_BOLD if bold else FONT_TH, size)


def resolve_src(spec: str, work: Path) -> list[tuple[str, Path | None]]:
    """-> [(label, path or None if missing)]"""
    spec = spec.strip()
    if spec.startswith("pair:"):
        inner = spec[5:].strip().strip("[]")
        return [resolve_src(p, work)[0] for p in inner.split(",")]
    kind, _, name = spec.partition(":")
    name = name.strip()
    if kind == "have":
        p = ROOT / name
        return [(spec, p if p.exists() else None)]
    folder = {"make": work / "make", "shoot": work / "shoot", "source": work / "sourced"}[kind]
    hits = sorted(q for q in folder.glob(f"{name}.*")
                  if q.suffix.lower() not in {".md", ".txt", ".json"}) if folder.exists() else []
    return [(spec, hits[0] if hits and readable(hits[0]) else None)]


def readable(p: Path) -> bool:
    """False for a file still being written or broken, so it becomes a placeholder, not a crash."""
    if p.stat().st_size == 0:
        return False
    if p.suffix.lower() in VIDEO_EXT:
        return True
    try:
        with Image.open(p) as im:
            im.verify()
        return True
    except Exception:
        return False


def fit(img: Image.Image, box_w: int, box_h: int, cover: bool) -> Image.Image:
    r = (max if cover else min)(box_w / img.width, box_h / img.height)
    img = img.resize((max(1, round(img.width * r)), max(1, round(img.height * r))), Image.LANCZOS)
    if cover:
        x, y = (img.width - box_w) // 2, (img.height - box_h) // 2
        img = img.crop((x, y, x + box_w, y + box_h))
    return img


GEN_NOTE = "Image generated with Claude Fable 5.1"
AI_NOTE = "AI-generated illustration"
ART_DIR = ROOT / "planning" / "slide-reference" / "assets"  # made earlier with another image tool
RADIUS = 28  # px, photo and screen-recording corners


def load_credits(work: Path) -> dict[str, str]:
    """src id -> attribution line, from the Wikimedia sourcing table in sourced/CREDITS.md."""
    p = work / "sourced" / "CREDITS.md"
    out = {}
    if p.exists():
        for line in p.read_text(encoding="utf-8").splitlines():
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) == 7 and cells[0].startswith("src-"):
                out[cells[0]] = cells[6]
    return out


def classify(spec: str) -> str:
    """generated (made in this project by Claude) | art (older AI illustration) | photo."""
    kind, _, name = spec.partition(":")
    if kind == "make":
        return "generated"
    if kind == "have" and (ROOT / name.strip()).resolve().is_relative_to(ART_DIR.resolve()):
        return "art"
    return "photo"  # photos and screenshots alike: rounded card, label, credit


def page(body: str, extra_css: str = "") -> str:
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face {{ font-family: Prompt; font-weight: 400; src: url("{(FONT_DIR / 'Prompt-Regular.ttf').as_uri()}"); }}
@font-face {{ font-family: Prompt; font-weight: 700; src: url("{(FONT_DIR / 'Prompt-Bold.ttf').as_uri()}"); }}
html, body {{ margin: 0; width: {W}px; height: {H}px; overflow: hidden; }}
body {{ background: rgb{CREAM}; font-family: Prompt, sans-serif; color: #2b2b2b; position: relative; }}
.note {{ position: absolute; left: 40px; bottom: 20px; font-size: 22px; color: #8a7f6a; }}
{extra_css}</style></head><body>{body}</body></html>"""


def compose_generated(path: Path, out: Path, note: str) -> None:
    """A full-frame image made for the video, with its generation footnote bottom-left."""
    html_to_png(page(f'<img src="{path.resolve().as_uri()}" style="position:absolute;inset:0;'
                     f'width:{W}px;height:{H}px"><div class="note">{escape(note)}</div>'), out)


def compose_art(path: Path, out: Path) -> None:
    """Older concept art: contained on the cream, disclosed as AI-generated."""
    html_to_png(page(f'<img src="{path.resolve().as_uri()}" style="position:absolute;left:50%;'
                     f'top:50%;transform:translate(-50%,-50%);max-width:1728px;max-height:900px">'
                     f'<div class="note">{AI_NOTE}</div>'), out)


def compose_cards(paths: list[Path], labels: list[str], credits: list[str], out: Path) -> None:
    """One or two photos/screenshots as rounded cards, each with its label and credit beneath."""
    n = len(paths)
    max_w, max_h = (1500, 740) if n == 1 else (820, 660)
    cols = "".join(
        f'<div class="col"><div class="box"><img src="{p.resolve().as_uri()}"></div>'
        + (f'<div class="lbl">{escape(lbl)}</div>' if lbl else "")
        + (f'<div class="cr">{escape(cr)}</div>' if cr else "")
        + "</div>"
        for p, lbl, cr in zip(paths, labels, credits))
    html_to_png(page(f'<div class="row">{cols}</div>', f"""
.row {{ position: absolute; inset: 0; display: flex; align-items: center; justify-content: center;
        gap: 72px; padding-bottom: 20px; }}
.col {{ display: flex; flex-direction: column; align-items: center; max-width: {max_w}px; }}
.box {{ height: {max_h if n > 1 else 'auto'}{'px' if n > 1 else ''}; display: flex; align-items: center; }}
.col img {{ max-width: {max_w}px; max-height: {max_h}px; border-radius: {RADIUS}px; display: block;
            outline: 2px solid rgba(43,43,43,.08); }}
.lbl {{ margin-top: 26px; font-size: 52px; font-weight: 700; line-height: 1.2; text-align: center; }}
.cr {{ margin-top: 10px; font-size: 20px; color: #8a7f6a; text-align: center; line-height: 1.35; }}
"""), out)


def placeholder(ins: dict, missing: list[str]) -> Image.Image:
    im = Image.new("RGB", (W, H), (58, 58, 58))
    d = ImageDraw.Draw(im)
    for i in range(0, W, 40):
        d.line([(i, 30), (i + 20, 30)], fill=(150, 150, 150), width=4)
        d.line([(i, H - 30), (i + 20, H - 30)], fill=(150, 150, 150), width=4)
    d.text((W // 2, 330), "PLACEHOLDER", font=font(90, True), fill=(255, 200, 60), anchor="mm")
    d.text((W // 2, 470), f"{ins['id']}  ·  {ins['desc']}", font=font(52), fill="white", anchor="mm")
    d.text((W // 2, 580), "missing: " + ", ".join(missing), font=font(40), fill=(200, 200, 200),
           anchor="mm")
    return im


def prep_video(src: Path, out: Path, slot: float, max_speed: float, pad_rgb=CREAM) -> str:
    """Speed-fit a screen recording into `slot` seconds at 1920×1080, 30 fps, no audio."""
    dur = probe(src)["duration_s"]
    speed = dur / slot
    if speed > max_speed:
        start, speed = dur - slot * max_speed, max_speed
    else:
        start = 0.0
    speed = max(speed, 1.0)
    hexc = "0x%02X%02X%02X" % pad_rgb
    # Exact content box (even sizes) so the rounded-corner mask lines up with the picture.
    m = probe(src)
    r = min(1728 / m["width"], 972 / m["height"])
    cw, ch = int(m["width"] * r) // 2 * 2, int(m["height"] * r) // 2 * 2
    x0, y0 = (W - cw) // 2, (H - ch) // 2
    mask = out.with_name(f"_mask_{cw}x{ch}.png")
    if not mask.exists():
        mk = Image.new("RGBA", (W, H), CREAM + (255,))
        ImageDraw.Draw(mk).rounded_rectangle([x0, y0, x0 + cw - 1, y0 + ch - 1], RADIUS,
                                             fill=(0, 0, 0, 0))
        mk.save(mask)
    fg = (f"[0:v]trim=start={start:.3f},setpts=(PTS-STARTPTS)/{speed:.4f},"
          f"scale={cw}:{ch}:flags=lanczos,pad={W}:{H}:{x0}:{y0}:color={hexc},fps=30,"
          f"tpad=stop_mode=clone:stop_duration={slot:.3f}[v];"
          f"[v][1:v]overlay=0:0,format=yuv420p")
    run(["ffmpeg", "-v", "error", "-y", "-i", src, "-loop", "1", "-i", mask,
         "-filter_complex", fg, "-t", f"{slot:.3f}", "-an",
         "-c:v", "libx264", "-preset", "fast", "-crf", "16", out])
    return f"{speed:.1f}x from {start:.1f}s" if start else f"{speed:.1f}x"


def prep_insert(ins: dict, slot: float, work: Path, cfg: dict, credits: dict) -> dict:
    parts = resolve_src(ins["src"], work)
    missing = [lbl for lbl, p in parts if p is None]
    outdir = work / "inserts"
    outdir.mkdir(parents=True, exist_ok=True)
    frames = round(slot * 30)
    if missing:
        out = outdir / f"{ins['id']}.png"
        placeholder(ins, missing).save(out)
        return {"path": out, "kind": "still", "status": "PLACEHOLDER", "note": ", ".join(missing)}
    paths = [p for _, p in parts]
    if len(paths) == 1 and paths[0].suffix.lower() in VIDEO_EXT:
        out = outdir / f"{ins['id']}_{frames}f_r{RADIUS}.mp4"  # radius in name: restyle = re-prep
        if not out.exists() or out.stat().st_mtime < paths[0].stat().st_mtime:
            note = prep_video(paths[0], out, slot, cfg["max_speed"])
        else:
            note = "cached"
        return {"path": out, "kind": "video", "status": "ok", "note": note}
    out = outdir / f"{ins['id']}.png"
    specs = [lbl for lbl, _ in parts]
    kinds = [classify(s) for s in specs]
    if len(paths) == 1 and kinds[0] == "generated":
        compose_generated(paths[0], out, ins.get("note", GEN_NOTE))  # "note": "" for photo composites
        return {"path": out, "kind": "still", "status": "ok", "note": "generated footnote"}
    if len(paths) == 1 and kinds[0] == "art":
        compose_art(paths[0], out)
        return {"path": out, "kind": "still", "status": "ok", "note": "AI-illustration footnote"}
    labels = list(ins.get("labels", [])) + [""] * len(paths)
    cred = [("Photo: " + credits[s.split(":", 1)[1].strip()])
            if s.startswith("source:") and s.split(":", 1)[1].strip() in credits else ""
            for s in specs]
    compose_cards(paths, labels[:len(paths)], cred, out)
    return {"path": out, "kind": "still", "status": "ok",
            "note": "credited" if any(cred) else ""}


def html_to_png(html: str, out: Path) -> None:
    """Render a 1920×1080 page with headless Chrome.

    Anything with Thai text goes through here, not PIL: this Pillow build has no raqm, so it
    drops a tone mark stacked on an upper vowel (เมื่อ -> เมือ, ที่ -> ที).
    """
    page = out.with_suffix(".html")
    page.write_text(html, encoding="utf-8")
    run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
         "--force-device-scale-factor=1", f"--window-size={W},{H}",
         f"--screenshot={out}", page.resolve().as_uri()])
    got = Image.open(out)
    if got.size != (W, H):
        sys.exit(f"Chrome rendered {out.name} at {got.size}, expected {(W, H)}")


def callout_png(big: str, small: str, out: Path) -> None:
    """A number callout beside the speaker (the reference puts "256 GB" / "$1099" there): a small
    label card on a transparent 1920×1080 frame, right of centre, clear of Roger at 132-140%.
    Anchored from the right edge so a longer number grows inward, never off the frame."""
    page_ = out.with_suffix(".html")
    page_.write_text(f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face {{ font-family: Prompt; font-weight: 400; src: url("{(FONT_DIR / 'Prompt-Regular.ttf').as_uri()}"); }}
@font-face {{ font-family: Prompt; font-weight: 700; src: url("{(FONT_DIR / 'Prompt-Bold.ttf').as_uri()}"); }}
html, body {{ margin: 0; width: {W}px; height: {H}px; overflow: hidden; background: transparent; }}
.c {{ position: absolute; right: 70px; top: 300px; min-width: 300px; padding: 24px 38px 26px;
      background: rgba(255,253,248,.96); border-radius: 26px; font-family: Prompt, sans-serif;
      box-shadow: 0 10px 34px rgba(0,0,0,.28); text-align: center; }}
.b {{ font-size: 84px; font-weight: 700; color: #2b2b2b; line-height: 1.05; white-space: nowrap; }}
.s {{ margin-top: 8px; font-size: 30px; color: #7a705c; white-space: nowrap; }}
</style></head><body><div class="c"><div class="b">{escape(big)}</div>
<div class="s">{escape(small)}</div></div></body></html>""", encoding="utf-8")
    run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
         "--force-device-scale-factor=1", "--default-background-color=00000000",
         f"--window-size={W},{H}", f"--screenshot={out}", page_.resolve().as_uri()])
    im = Image.open(out)
    if im.size != (W, H) or im.mode != "RGBA" or im.getpixel((10, 10))[3] != 0:
        sys.exit(f"callout {out.name}: expected a transparent {W}x{H} RGBA frame, got {im.mode} {im.size}")


def two_line(title: str) -> str:
    """Break a long "Topic: explanation" title after the colon for the cards."""
    return title.replace(": ", ":\n", 1) if len(title) > 24 else title


def card(path: Path, lines: list[tuple[str, int, bool, str]], picture: Path | None) -> None:
    pic = (f'<img src="{picture.resolve().as_uri()}">' if picture and picture.exists() else "")
    note = (f'<div style="position:absolute;left:40px;bottom:20px;font-size:22px;color:#8a7f6a">'
            f'{GEN_NOTE}</div>') if pic else ""
    text = "".join(f'<div style="font-size:{s}px;font-weight:{700 if b else 400};color:{c}">'
                   f'{escape(t).replace(chr(10), "<br>")}</div>' for t, s, b, c in lines)
    html_to_png(f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face {{ font-family: Prompt; font-weight: 400; src: url("{(FONT_DIR / 'Prompt-Regular.ttf').as_uri()}"); }}
@font-face {{ font-family: Prompt; font-weight: 700; src: url("{(FONT_DIR / 'Prompt-Bold.ttf').as_uri()}"); }}
html, body {{ margin: 0; width: {W}px; height: {H}px; overflow: hidden; }}
body {{ background: rgb{CREAM}; font-family: Prompt, sans-serif; display: flex;
        flex-direction: column; justify-content: center; padding: 0 140px; box-sizing: border-box; }}
.t {{ line-height: 1.3; }} .t div {{ white-space: nowrap; }} .t div + div {{ margin-top: 10px; }}
.p {{ flex: 1; min-height: 0; margin: 20px -60px 40px; display: flex; justify-content: center; }}
.p img {{ max-width: 100%; max-height: 100%; object-fit: contain; }}
body.nopic {{ justify-content: center; }}
</style></head><body class="{'' if pic else 'nopic'}" style="{'padding-top:90px' if pic else ''}">
<div class="t">{text}</div>{f'<div class="p">{pic}</div>' if pic else ''}{note}</body></html>""", path)


# ---------------------------------------------------------------- resolve

def resolve_zooms(v: dict, cfg: dict, words: Words, v_in: float, v_out: float, inserts: list,
                  errs: list, warns: list) -> list[dict]:
    """Zooms, MKBHD-style (see planning/STYLE-STUDY-MKBHD.md).

    Each zoom names the phrase it starts on (`in_cue`, or a number `in`) and ends at `out_cue`
    (the start of that phrase), a number `out`, or — by default — the next insert or the end of
    the video. `level` is the scale (% of the source frame; base is `base_scale`); `style` is
    "cut" (instant, the default) or "push" (a fast smoothstep ease over `push_s`), used for
    each video's signature lines. A zoom whose in-point is another zoom's out-point is a second
    tier: it starts from that zoom's level instead of the base. Every zoom ends with an instant
    cut back to the base, and never runs into an insert: it is clipped at the insert's start.
    """
    base = cfg.get("base_scale", 100)
    ins_starts = sorted(i["start"] for i in inserts)
    out, after = [], v_in
    for z in v["zooms"]:
        z = dict(z)
        s = z.get("in")
        if s is None:
            s = words.find(z["in_cue"], after)
            if s is None:
                errs.append(f"{z['id']}: in_cue not found after {fmt(after)}: {z['in_cue']}")
                continue
        e = z.get("out")
        if e is None and z.get("out_cue"):
            e = words.find(z["out_cue"], s + 0.05)
            if e is None:
                errs.append(f"{z['id']}: out_cue not found after {fmt(s)}: {z['out_cue']}")
                continue
        nxt = min([t for t in ins_starts if t > s + 1e-6] + [v_out])
        if any(i["start"] - 1e-6 <= s < i["end"] for i in inserts if "end" in i):
            errs.append(f"{z['id']} starts at {fmt(s)} under an insert")
        if e is None or e > nxt:
            e = nxt  # a cutaway (or the end card) resets the framing, as in the reference
        if not v_in <= s < e <= v_out + 0.01:
            errs.append(f"{z['id']}: {fmt(s)}–{fmt(e)} is empty or outside the video")
            continue
        if e - s < 1.5:
            warns.append(f"{z['id']}: only {e - s:.1f}s long")
        z.update({"in": s, "out": e, "level": z.get("level", cfg["zoom_scale"]),
                  "style": z.get("style", "cut")})
        out.append(z)
        after = s + 0.05
    out.sort(key=lambda z: z["in"])
    for a, b in zip(out, out[1:]):
        if b["in"] < a["out"] - 0.02:
            warns.append(f"{a['id']} cut short at {fmt(b['in'])} by {b['id']}")
            a["out"] = b["in"]
    for k, z in enumerate(out):
        prev = out[k - 1] if k else None
        tier = prev is not None and abs(prev["out"] - z["in"]) < 0.02
        z["from"] = prev["level"] if tier else base
        z["tier2"] = tier
    return out


def resolve_video(v: dict, cfg: dict, words: Words, audio: Audio, work: Path) -> dict:
    errs, warns = [], []
    v_in = audio.quietest(v["in"]) if v["in"] > 0 else 0.0
    v_out = audio.quietest(v["out"])

    chapters, after = [], v_in
    for i, (cue, title) in enumerate(v["chapters"]):
        t = v_in if i == 0 else (float(cue) if not isinstance(cue, str) else words.find(cue, after))
        if t is None:
            errs.append(f"chapter '{title}': cue not found after {fmt(after)}: {cue}")
            continue
        chapters.append((t, title))
        after = t + 0.1

    inserts, after = [], v_in
    for ins in v["inserts"]:
        t = words.find(ins["cue"], after)
        if t is None:
            errs.append(f"{ins['id']}: cue not found after {fmt(after)}: {ins['cue']}")
            continue
        inserts.append({**ins, "t": t, "start": max(v_in, t - cfg["lead_s"])})
        after = t + 0.1

    zooms = resolve_zooms(v, cfg, words, v_in, v_out, inserts, errs, warns)
    callouts = []
    for k, z in enumerate(zooms):
        if z.get("callout"):
            # shown from just after the punch until the zoom chain (incl. a 2nd tier) cuts back
            end, j = z["out"], k
            while j + 1 < len(zooms) and zooms[j + 1]["tier2"]:
                j += 1
                end = zooms[j]["out"]
            callouts.append({"id": f"C{z['id']}", "big": z["callout"]["big"],
                             "small": z["callout"].get("small", ""), "start": z["in"] + 0.25,
                             "end": end})

    events = sorted([i["start"] for i in inserts] + [z["in"] for z in zooms])
    for ins in inserts:
        s = ins["start"]
        is_video = any(p and p.suffix.lower() in VIDEO_EXT for _, p in resolve_src(ins["src"], work))
        hold = ins.get("hold", cfg["hold_video_s"] if is_video else cfg["hold_still_s"])
        nxt = min([e for e in events if e > s + 1e-6] + [v_out])
        ins["end"] = min(s + hold, nxt - 0.3, v_out - 0.3)
        if ins["end"] - s < 2.5:
            warns.append(f"{ins['id']}: only {ins['end'] - s:.1f}s on screen before the next event")

    hook = resolve_hook(v, cfg, audio, zooms, inserts, callouts, v_in, v_out, errs, warns)
    return {"in": v_in, "out": v_out, "chapters": chapters, "zooms": zooms, "hook": hook,
            "inserts": inserts, "callouts": callouts, "errors": errs, "warnings": warns}


def resolve_hook(v: dict, cfg: dict, audio: Audio, zooms: list, inserts: list, callouts: list,
                 v_in: float, v_out: float, errs: list, warns: list) -> dict | None:
    """The cold open: a few quick shots lifted from later in the video, each its own fragment of
    speech over its own picture, hard-cut together. Then the picture fades to black, and the title
    banner fades in with the intro music and back out to black before the talk starts.

    A shot is {in, out, show}: `show` is "talk" (the speaker, at the zoom the edit has there, or
    `level`, plus any callout the edit shows there) or an insert id (that insert's picture, from
    the middle of it). in/out are source seconds on a pause where there is one; they snap to the
    quietest 30 ms within ±0.06 s."""
    if not v.get("hook"):
        return None
    base = cfg.get("base_scale", 100)
    by_id = {i["id"]: i for i in inserts}
    shots = []
    for k, sh in enumerate(v["hook"]["shots"], 1):
        a, b = audio.quietest(sh["in"], 0.06), audio.quietest(sh["out"], 0.06)
        if not v_in <= a < b <= v_out:
            errs.append(f"hook shot {k}: {fmt(a)}–{fmt(b)} is empty or outside the video")
            continue
        shot = {**sh, "in": a, "out": b, "frames": round(b * 30) - round(a * 30)}
        mid = (a + b) / 2
        if sh["show"] == "talk":
            live = [z for z in zooms if z["in"] <= mid < z["out"]]
            shot["level"] = sh.get("level", live[0]["level"] if live else base)
            shot["callout"] = next((c for c in callouts if c["start"] <= mid < c["end"]), None)
        elif sh["show"] not in by_id:
            errs.append(f"hook shot {k}: no insert '{sh['show']}' in this video")
            continue
        shots.append(shot)
    n = sum(s["frames"] for s in shots)
    if not 3.5 * 30 <= n <= 7 * 30:
        warns.append(f"hook shots run {n / 30:.1f}s (aim for ~5)")
    return {"shots": shots, "frames": n, "tail": round(cfg.get("hook_tail_s", 0.5) * 30)}


# ---------------------------------------------------------------- XML

def smoothstep(u: float) -> float:
    u = min(1.0, max(0.0, u))
    return u * u * (3 - 2 * u)


def push_frames(n: int, cfg: dict) -> int:
    return max(1, min(round(cfg.get("push_s", 0.4) * 30), n))


def zoom_curve(n: int, z: dict, cfg: dict) -> list[tuple[int, float]]:
    """(frame offset, scale %) keys for a "push" zoom segment of n frames: ease from the level it
    starts at to its own level over push_s, then hold. One key per ramp frame, so the ease
    survives whatever interpolation the NLE applies between keys. (A "cut" zoom needs no keys.)"""
    a, t = z["from"], z["level"]
    rf = push_frames(n, cfg)
    return [(k, round(a + (t - a) * smoothstep(k / rf), 3)) for k in range(rf + 1)] + [(n, t)]


def basic_motion(scale: float, keys: list[tuple[int, float]] | None = None, when0: int = 0) -> str:
    """Basic Motion at a fixed scale, or keyframed when `keys` is given. `when0` is added to each
    key's frame offset: the source in-point if <when> counts from the start of the media, 0 if it
    counts from the clip's in-point (see --zoom-keys)."""
    kf = "".join(f"""
                <keyframe><when>{when0 + k}</when><value>{v}</value></keyframe>"""
                 for k, v in (keys or []))
    return f"""        <filter>
          <effect>
            <name>Basic Motion</name>
            <effectid>basic</effectid>
            <effectcategory>Motion</effectcategory>
            <effecttype>motion</effecttype>
            <mediatype>video</mediatype>
            <parameter>
              <parameterid>scale</parameterid>
              <name>Scale</name>
              <valuemin>0</valuemin>
              <valuemax>1000</valuemax>
              <value>{scale}</value>{kf}
            </parameter>
            <parameter>
              <parameterid>rotation</parameterid>
              <name>Rotation</name>
              <valuemin>-3600</valuemin>
              <valuemax>3600</valuemax>
              <value>0</value>
            </parameter>
            <parameter>
              <parameterid>center</parameterid>
              <name>Center</name>
              <value>
                <horiz>0</horiz>
                <vert>0</vert>
              </value>
            </parameter>
          </effect>
        </filter>
"""


def file_block(fid: str, path: Path, seen: set, dur_f: int, w: int, h: int, audio=False) -> str:
    if fid in seen:
        return f'<file id="{fid}"/>'
    seen.add(fid)
    a = ("\n            <audio><samplecharacteristics><depth>16</depth><samplerate>48000"
         "</samplerate></samplecharacteristics><channelcount>2</channelcount></audio>") if audio else ""
    return f"""<file id="{fid}">
          <name>{escape(path.name)}</name>
          <pathurl>{pathurl(path)}</pathurl>
          <rate><timebase>30</timebase><ntsc>FALSE</ntsc></rate>
          <duration>{dur_f}</duration>
          <media>
            <video><samplecharacteristics><width>{w}</width><height>{h}</height>
              <rate><timebase>30</timebase><ntsc>FALSE</ntsc></rate></samplecharacteristics></video>{a}
          </media>
        </file>"""


def clipitem(cid: str, name: str, start: int, end: int, in_f: int, out_f: int, fblock: str,
             filt: str = "") -> str:
    return f"""      <clipitem id="{cid}">
        <name>{escape(name)}</name>
        <enabled>TRUE</enabled>
        <duration>{out_f - in_f}</duration>
        <rate><timebase>30</timebase><ntsc>FALSE</ntsc></rate>
        <start>{start}</start>
        <end>{end}</end>
        <in>{in_f}</in>
        <out>{out_f}</out>
        {fblock}
{filt}      </clipitem>
"""


def build_xml(v: dict, r: dict, media: dict, cover: Path, endc: Path, src: Path,
              src_meta: dict, cfg: dict, music: Path | None = None) -> str:
    fr = lambda s: round(s * 30)  # noqa: E731
    C, E = fr(cfg["cover_s"]), fr(cfg["end_s"])
    in_f, out_f = fr(r["in"]), fr(r["out"])
    hook = r.get("hook")
    K = hook["frames"] + hook["tail"] if hook else 0  # the cold open plays before the cover
    tl = lambda s: K + C + fr(s) - in_f  # noqa: E731  source seconds -> timeline frame
    talk_end = K + C + out_f - in_f
    src_dur = fr(src_meta["duration_s"])
    seen, n = set(), [0]

    def cid():
        n[0] += 1
        return f"clipitem-{n[0]}"

    def segments(zooms: list) -> list[tuple[int, int, dict | None]]:
        cuts = [in_f]
        for z in zooms:
            cuts += [fr(z["in"]), fr(z["out"])]
        cuts.append(out_f)
        zoomed = {(fr(z["in"]), fr(z["out"])): z for z in zooms}
        return [(a, b, zoomed.get((a, b))) for a, b in zip(cuts, cuts[1:]) if b > a]

    def talk(wa: int, wb: int, at: int, zooms: list) -> tuple[list, list]:
        """V1 pieces and the A1 clip for source frames [wa, wb) placed at timeline frame `at`."""
        v = []
        for a, b, z in segments(zooms):
            x, y = max(a, wa), min(b, wb)
            if y <= x:
                continue
            if z and z["style"] == "push":
                # keys are laid out from the zoom's own in-point, so a window that starts
                # partway through a push still lands on the same curve
                filt = basic_motion(z["level"], zoom_curve(b - a, z, cfg),
                                    a if cfg.get("zoom_keys") == "media" else a - x)
            elif z:
                filt = basic_motion(z["level"])
            else:
                base = cfg.get("base_scale", 100)
                filt = basic_motion(base) if base != 100 else ""
            v.append(clipitem(cid(), src.name, at + x - wa, at + y - wa, x, y,
                              file_block("file-src", src, seen, src_dur, src_meta["width"],
                                         src_meta["height"], audio=True), filt))
        a1 = clipitem(cid(), src.name, at, at + wb - wa, wa, wb,
                      file_block("file-src", src, seen, src_dur, 0, 0, audio=True))
        return v, [a1]

    def overlays(spans: list, wa: int, at: int) -> tuple[list, list]:
        """V2 inserts and V3 callouts for (start s, end s, item) spans, the item's media entered
        at its own offset so a clipped insert shows the right part."""
        v2, v3 = [], []
        for s, e, it in spans:
            x, y = fr(s), fr(e)
            if "callout" in it:  # a callout record
                c = it["callout"]
                v3.append(clipitem(cid(), c["path"].name, at + x - wa, at + y - wa, 0, y - x,
                                   file_block(f"file-{c['id']}", c["path"], seen,
                                              fr(c["end"]) - fr(c["start"]), W, H)))
            else:
                m, off = media[it["id"]], x - fr(it["start"])
                full = max(fr(it["end"]) - fr(it["start"]), off + y - x)  # a held still
                v2.append(clipitem(cid(), f"{it['id']} {m['path'].name}", at + x - wa,
                                   at + y - wa, off, off + y - x,
                                   file_block(f"file-{it['id']}", m["path"], seen, full, W, H)))
        return v2, v3

    body_spans = ([(i["start"], i["end"], i) for i in r["inserts"]]
                  + [(c["start"], c["end"], {"callout": c}) for c in r["callouts"]])
    v1, a1, v2, v3 = [], [], [], []
    a2 = []
    if hook:
        # Quick shots, hard-cut; then a gap of black for the fade-out. The fades themselves (out of
        # the last shot, in and out of the banner) are marked, not built: add Dip to Black there.
        at = 0
        by_id = {i["id"]: i for i in r["inserts"]}
        for sh in hook["shots"]:
            a, nf = fr(sh["in"]), sh["frames"]
            if sh["show"] == "talk":
                v1.append(clipitem(cid(), src.name, at, at + nf, a, a + nf,
                                   file_block("file-src", src, seen, src_dur, src_meta["width"],
                                              src_meta["height"], audio=True),
                                   basic_motion(sh["level"])))
                if sh["callout"]:
                    c = sh["callout"]
                    v3.append(clipitem(cid(), c["path"].name, at, at + nf, 0, nf,
                                       file_block(f"file-{c['id']}", c["path"], seen,
                                                  max(nf, fr(c["end"]) - fr(c["start"])), W, H)))
            else:
                ins, m = by_id[sh["show"]], media[sh["show"]]
                full = fr(ins["end"]) - fr(ins["start"])
                off = max(0, (full - nf) // 2)
                v2.append(clipitem(cid(), f"{ins['id']} {m['path'].name}", at, at + nf, off, off + nf,
                                   file_block(f"file-{ins['id']}", m["path"], seen,
                                              max(full, off + nf), W, H)))
            a1.append(clipitem(cid(), src.name, at, at + nf, a, a + nf,
                               file_block("file-src", src, seen, src_dur, 0, 0, audio=True)))
            at += nf
        if music:  # from the fade to black through the banner
            a2.append(clipitem(cid(), music.name, hook["frames"], K + C, 0, K + C - hook["frames"],
                               file_block("file-music", music, seen, K + C - hook["frames"], 0, 0,
                                          audio=True)))
    v1.append(clipitem(cid(), cover.name, K, K + C, 0, C,
                       file_block("file-cover", cover, seen, C, W, H)))
    pv, pa = talk(in_f, out_f, K + C, r["zooms"])
    pv2, pv3 = overlays(body_spans, in_f, K + C)
    v1 += pv
    a1 += pa
    v2 += pv2
    v3 += pv3
    v1.append(clipitem(cid(), endc.name, talk_end, talk_end + E, 0, E,
                       file_block("file-end", endc, seen, E, W, H)))

    markers = "".join(
        f"""    <marker><name>{escape(title)}</name><comment></comment>
      <in>{0 if k == 0 else tl(t)}</in><out>-1</out></marker>
""" for k, (t, title) in enumerate(r["chapters"]))
    if hook:
        fi, fo = fr(cfg.get("banner_fade_in_s", 0.4)), fr(cfg.get("banner_fade_out_s", 0.6))
        markers += "".join(
            f"""    <marker><name>{escape(name)}</name><comment>add Dip to Black</comment>
      <in>{a}</in><out>{b}</out></marker>
""" for name, a, b in [("fade out of the hook", hook["frames"], K),
                       ("banner fades in", K, K + fi), ("banner fades out", K + C - fo, K + C)])
    total = talk_end + E
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE xmeml>
<xmeml version="5">
  <sequence>
    <name>{escape(v['id'] + ' ' + v['title'])}</name>
    <duration>{total}</duration>
    <rate><timebase>30</timebase><ntsc>FALSE</ntsc></rate>
{markers}    <media>
      <video>
        <format><samplecharacteristics><width>{W}</width><height>{H}</height>
          <pixelaspectratio>Square</pixelaspectratio>
          <rate><timebase>30</timebase><ntsc>FALSE</ntsc></rate></samplecharacteristics></format>
        <track>
{''.join(v1)}        </track>
        <track>
{''.join(v2)}        </track>
        <track>
{''.join(v3)}        </track>
      </video>
      <audio>
        <track>
{''.join(a1)}        </track>
        <track>
{''.join(a2)}        </track>
      </audio>
    </media>
  </sequence>
</xmeml>
"""


# ---------------------------------------------------------------- render

def render(v: dict, r: dict, media: dict, cover: Path, endc: Path, src: Path, cfg: dict,
           mode: str, out: Path, max_seconds: float | None = None,
           music: Path | None = None) -> None:
    ow, oh = (960, 540) if mode == "preview" else (W, H)
    norm = f"scale={ow}:{oh}:flags=lanczos,fps=30,format=yuv420p,setsar=1"

    def zoom_filter(zooms: list[dict], t0: float) -> str:
        """One zoompan over the whole talk. Its zoom is a function of the input time: base scale
        everywhere, eased up to the zoom scale inside each zoom span (zoom_curve's smoothstep).

        Deliberately one linear chain. The first version razored the talk with split -> trim ->
        zoompan -> concat; split fed nine branches and decoded frames queued up behind the ones
        not being read, reaching 119 GB and crashing the machine (21 Sep 2026)."""
        b = cfg.get("base_scale", 100) / 100

        def ease(u: str) -> str:
            c = f"clip({u},0,1)"
            return f"({c}*{c}*(3-2*{c}))"

        terms = []
        for z in zooms:
            s, e = z["in"] - t0, z["out"] - t0
            fr_, to = z["from"] / 100, z["level"] / 100
            if z["style"] == "push":
                rs = push_frames(round((e - s) * 30), cfg) / 30
                level = f"({fr_ - b:.4f}+{to - fr_:.4f}*{ease(f'(it-{s:.4f})/{rs:.4f}')})"
            else:
                level = f"{to - b:.4f}"
            # half-open [s, e): contiguous tiers must not both count at their shared instant
            terms.append(f"gte(it,{s:.4f})*lt(it,{e:.4f})*{level}")
        z_expr = f"{b}+({'+'.join(terms) or '0'})"
        # setpts rebuilds timestamps from the frame count: zoompan's output timestamps are in a
        # different time base, and an fps filter after it saw gaps and duplicated frames ~533x
        # (3 s in -> 48,000 frames out; the 7.6-min talk ran for two hours without finishing).
        return (f"zoompan=z='{z_expr}':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2'"
                f":d=1:s={W}x{H}:fps=30,setpts=N/(30*TB),")

    # Three stages, each reading one file at a time so memory stays flat:
    #   1. the talk alone (zoom applied), keyframes forced at every insert boundary;
    #   2. each insert, the cover and the end card as a clip of exactly its frame count;
    #   3. the concat demuxer strings them in order and the talk audio goes underneath.
    # Inserts cover the whole frame, so "talk, insert, talk, ..." is the same picture as
    # overlaying them. The first design overlaid 10-27 inserts in one filtergraph, and ffmpeg
    # decoded them ahead into memory while they waited for their slot (8.7 GB and rising on V2).
    q = lambda t: round(t * 30) / 30  # noqa: E731  everything on the 30 fps grid
    r = {**r, "in": q(r["in"]), "out": q(r["out"]),
         "zooms": [{**z, "in": q(z["in"]), "out": q(z["out"])} for z in r["zooms"]],
         "inserts": [{**i, "start": q(i["start"]), "end": q(i["end"])} for i in r["inserts"]]}
    talk_f = round((r["out"] - r["in"]) * 30)
    if max_seconds:
        talk_f = min(talk_f, round(max_seconds * 30))

    parts = out.parent / f"_parts_{v['id']}"
    parts.mkdir(parents=True, exist_ok=True)
    mem = cfg.get("render_mem_gb", 8)
    gpu = cfg.get("gpu_intermediates", True) and nvenc_ok()
    # Intermediates only need to be clean and cut exactly: NVENC with forced IDR frames (so the
    # concat demuxer's in-points land on real keyframes) spares the CPU for decode + zoompan.
    venc_mid = (["-c:v", "h264_nvenc", "-preset", "p4", "-rc", "vbr", "-cq", "16", "-b:v", "0",
                 "-forced-idr", "1"] if gpu else
                ["-c:v", "libx264", "-preset", "veryfast", "-crf", "12"])
    mid = ["-an", *venc_mid, "-pix_fmt", "yuv420p", "-r", "30", "-video_track_timescale", "15360"]
    hw = ["-hwaccel", "cuda"] if gpu else []  # decode the source on the GPU (frames come back to RAM)

    def clip(srcfile: Path, frames: int, dst: Path, still: bool, skip: int = 0,
             post: str = "") -> Path:
        """A fixed-length clip; `skip` frames into the media first (a hook shot taken from the
        middle of an insert); `post` is appended to the filter chain (fades)."""
        inp = ["-loop", "1", "-framerate", "30", "-i", srcfile] if still else ["-i", srcfile]
        pre = f"trim=start_frame={skip},setpts=PTS-STARTPTS," if skip and not still else ""
        run_guarded(["ffmpeg", "-v", "error", "-y", *inp, "-vf",
                     f"{pre}{norm},tpad=stop_mode=clone:stop_duration=2"
                     + (f",{post}" if post else ""), "-frames:v", str(frames), *mid, dst], mem)
        return dst

    def picture(t0: float, n: int, tag: str, spans: list, zooms: list) -> list[str]:
        """Render source window [t0, t0 + n frames) as the finished picture and return its concat
        lines. `spans` are the (start s, end s, insert) inside it, already clipped to it.

        1. the talk alone (zoom and callouts applied), keyframes forced at every insert boundary;
        2. each insert as a clip of exactly its frame count;
        and the concat demuxer (stage 3) strings them in order. Inserts cover the whole frame,
        so "talk, insert, talk, ..." is the same picture as overlaying them. The first design
        overlaid 10-27 inserts in one filtergraph, and ffmpeg decoded them ahead into memory while
        they waited for their slot (8.7 GB and rising on V2)."""
        fspans = [(round((s - t0) * 30), round((e - t0) * 30), ins) for s, e, ins in spans]
        fspans = [(a, min(b, n), ins) for a, b, ins in fspans if a < n and b > a]
        talk_v = parts / f"{tag}.mp4"
        cuts = sorted({f for a, b, _ in fspans for f in (a, b) if 0 < f < n})
        # Callouts are few and short, so they are overlaid here: each is a still looped at 2 fps
        # for only its own (clipped) duration and shifted to its start, so almost nothing is
        # decoded ahead. Input seek, so decoding starts at the window's in-point.
        ins_ = [*hw, "-ss", f"{t0:.4f}", "-t", f"{n / 30:.4f}", "-i", src]
        fc = [f"[0:v]{zoom_filter(zooms, t0)}"
              f"scale={ow}:{oh}:flags=lanczos,setsar=1[v0]"]  # no fps filter after zoompan
        last, k = "v0", 0
        for c in r.get("callouts", []):
            a, e = max(c["start"], t0) - t0, min(c["end"], t0 + n / 30) - t0
            if e <= a:
                continue
            ins_ += ["-loop", "1", "-framerate", "2", "-t", f"{e - a:.3f}", "-i", c["path"]]
            fc.append(f"[{k + 1}:v]scale={ow}:{oh},format=rgba,setpts=PTS-STARTPTS+{a:.3f}/TB[c{k}]")
            fc.append(f"[{last}][c{k}]overlay=eof_action=pass:repeatlast=0[v{k + 1}]")
            last, k = f"v{k + 1}", k + 1
        fc.append(f"[{last}]format=yuv420p[vout]")
        run_guarded(["ffmpeg", "-v", "error", "-y", *ins_, "-filter_complex", ";".join(fc),
                     "-map", "[vout]", "-frames:v", str(n),
                     "-force_key_frames", ",".join(f"{c / 30:.4f}" for c in cuts) or "0",
                     *mid, talk_v], mem)
        lines, pos = [], 0
        for a, b, ins in fspans:
            if a > pos:
                lines += [f"file '{talk_v.as_posix()}'", f"inpoint {pos / 30:.6f}",
                          f"outpoint {a / 30:.6f}"]
            m = media[ins["id"]]
            skip = round((t0 - ins["start"]) * 30) + a  # frames into the insert's own media
            name = f"{ins['id']}.mp4" if tag == "talk" else f"{tag}-{ins['id']}.mp4"
            lines.append(f"file '{clip(m['path'], b - a, parts / name, m['kind'] != 'video', skip).as_posix()}'")
            pos = b
        if pos < n:
            lines += [f"file '{talk_v.as_posix()}'", f"inpoint {pos / 30:.6f}",
                      f"outpoint {n / 30:.6f}"]
        return lines

    def audio_of(t0: float, n: int, dst: Path, fade_in: float = 0, fade_out: float = 0) -> Path:
        # hook shots are lifted out of running speech: fade their edges so no cut clicks
        af = [f"afade=t=in:d={fade_in}"] if fade_in else []
        af += [f"afade=t=out:st={n / 30 - fade_out:.3f}:d={fade_out}"] if fade_out else []
        af = ["-af", ",".join(af)] if af else []
        run_guarded(["ffmpeg", "-v", "error", "-y", "-ss", f"{t0:.4f}", "-t", f"{n / 30:.4f}",
                     "-i", src, "-vn", *af, "-ac", "2", "-ar", "48000", "-c:a", "pcm_s16le", dst],
                    mem)
        return dst

    cf, ef = round(cfg["cover_s"] * 30), round(cfg["end_s"] * 30)
    lines, K = [], 0
    hook = r.get("hook")
    if hook:
        # The cold open: each shot an exact-length clip, hard-cut. Then the last frame freezes
        # and fades to black, and the banner (the cover card) fades in from black and back out.
        by_id = {i["id"]: i for i in r["inserts"]}
        shot_a = []
        for k, sh in enumerate(hook["shots"]):
            n, t0, dst = sh["frames"], q(sh["in"]), parts / f"hook-{k + 1}.mp4"
            if sh["show"] == "talk":
                z = sh["level"] / 100
                ins_ = [*hw, "-ss", f"{t0:.4f}", "-t", f"{n / 30 + 0.2:.4f}", "-i", src]
                fc = [f"[0:v]crop=iw/{z}:ih/{z},scale={ow}:{oh}:flags=lanczos,setsar=1,fps=30[v0]"]
                last = "v0"
                if sh["callout"]:
                    ins_ += ["-loop", "1", "-framerate", "30", "-t", f"{n / 30:.4f}",
                             "-i", sh["callout"]["path"]]
                    fc += [f"[1:v]scale={ow}:{oh},format=rgba[c]",
                           "[v0][c]overlay=eof_action=pass[v1]"]
                    last = "v1"
                fc.append(f"[{last}]format=yuv420p[vout]")
                run_guarded(["ffmpeg", "-v", "error", "-y", *ins_, "-filter_complex", ";".join(fc),
                             "-map", "[vout]", "-frames:v", str(n), *mid, dst], mem)
            else:
                ins, m = by_id[sh["show"]], media[sh["show"]]
                full = round((ins["end"] - ins["start"]) * 30)
                clip(m["path"], n, dst, m["kind"] != "video", max(0, (full - n) // 2))
            lines.append(f"file '{dst.as_posix()}'")
            end = k + 1 == len(hook["shots"])
            shot_a.append(audio_of(t0, n, parts / f"hook-{k + 1}.wav", 0.03, 0.12 if end else 0.03))
        tail_f = hook["tail"]
        tail = parts / "hook-tail.mp4"  # the last frame held, fading to black
        run_guarded(["ffmpeg", "-v", "error", "-y", "-i", dst, "-vf",
                     f"tpad=stop_mode=clone:stop_duration={tail_f / 30 + 1:.3f},"
                     f"trim=start_frame={hook['shots'][-1]['frames']},setpts=PTS-STARTPTS,"
                     f"fade=t=out:st=0:d={tail_f / 30:.3f}", "-frames:v", str(tail_f), *mid, tail],
                    mem)
        lines.append(f"file '{tail.as_posix()}'")
        K = hook["frames"] + tail_f

        # intro audio: the shots back to back, then the music from the fade through the banner
        D, fo = (tail_f + cf) / 30, cfg.get("banner_fade_out_s", 0.6)
        fmt_a = "aresample=48000,aformat=sample_fmts=s16:channel_layouts=stereo"
        ins_, fc = [], []
        for k, wav in enumerate(shot_a):
            ins_ += ["-i", wav]
            fc.append(f"[{k}:a]{fmt_a}[s{k}]")
        fc.append("".join(f"[s{k}]" for k in range(len(shot_a)))
                  + f"concat=n={len(shot_a)}:v=0:a=1,apad=whole_dur={hook['frames'] / 30:.4f},"
                  f"atrim=0:{hook['frames'] / 30:.4f}[h]")
        if music:
            ins_ += ["-i", music]
            fc.append(f"[{len(shot_a)}:a]atrim=0:{D:.4f},asetpts=PTS-STARTPTS,"
                      f"loudnorm=I={cfg.get('music_lufs', -22)}:TP=-2,{fmt_a},"
                      f"afade=t=in:d=0.15,afade=t=out:st={D - fo - 0.2:.3f}:d={fo + 0.2:.3f},"
                      f"apad=whole_dur={D:.4f},atrim=0:{D:.4f}[m]")
        else:
            fc.append(f"aevalsrc=0|0:s=48000:d={D:.4f},{fmt_a}[m]")
        fc.append("[h][m]concat=n=2:v=0:a=1[intro]")
        intro_a = parts / "intro.wav"
        run_guarded(["ffmpeg", "-v", "error", "-y", *ins_, "-filter_complex", ";".join(fc),
                     "-map", "[intro]", "-c:a", "pcm_s16le", intro_a], mem)
        fi = cfg.get("banner_fade_in_s", 0.4)
        banner = f"fade=t=in:st=0:d={fi},fade=t=out:st={cf / 30 - fo:.3f}:d={fo}"
    else:
        banner = ""
    lines.append(f"file '{clip(cover, cf, parts / 'cover.mp4', True, post=banner).as_posix()}'")
    lines += picture(r["in"], talk_f, "talk",
                     [(i["start"], i["end"], i) for i in r["inserts"]], r["zooms"])
    talk_a = audio_of(r["in"], talk_f, parts / "talk.wav")
    if not max_seconds:
        lines.append(f"file '{clip(endc, ef, parts / 'end.mp4', True).as_posix()}'")
    listing = parts / "concat.txt"
    listing.write_text("ffconcat version 1.0\n" + "\n".join(lines) + "\n", encoding="utf-8")

    # 3. join: the intro audio (or silence under the cover), then the talk, padded through the end
    if nvenc_ok():
        venc = {"preview": ["-c:v", "h264_nvenc", "-preset", "p4", "-cq", "30"],
                "h264": ["-c:v", "h264_nvenc", "-preset", "p6", "-tune", "hq", "-rc", "vbr",
                         "-cq", "19", "-b:v", "0", "-profile:v", "high"],
                "h265": ["-c:v", "hevc_nvenc", "-preset", "p6", "-tune", "hq", "-rc", "vbr",
                         "-cq", "22", "-b:v", "0", "-tag:v", "hvc1"]}[mode]
    else:
        venc = {"preview": ["-c:v", "libx264", "-preset", "veryfast", "-crf", "28"],
                "h264": ["-c:v", "libx264", "-preset", "slow", "-crf", "18", "-profile:v", "high"],
                "h265": ["-c:v", "libx265", "-preset", "medium", "-crf", "22", "-tag:v", "hvc1"]}[mode]
    total = (K + cf + talk_f + (0 if max_seconds else ef)) / 30
    if hook:
        aud = ["-i", talk_a, "-i", intro_a, "-filter_complex",
               "[2:a][1:a]concat=n=2:v=0:a=1,apad[a]"]
    else:
        aud = ["-i", talk_a, "-filter_complex",
               f"[1:a]adelay={round(cfg['cover_s'] * 1000)}:all=1,apad[a]"]
    run_guarded(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", listing,
                 *aud,
                 "-map", "0:v", "-map", "[a]", *venc, "-r", "30", "-c:a", "aac", "-b:a", "192k",
                 "-t", f"{total:.4f}", "-movflags", "+faststart", out], mem)


def run_guarded(cmd: list, ceiling_gb: float) -> None:
    """Run ffmpeg with a memory watchdog: kill it if its memory passes `ceiling_gb`, rather than
    let it exhaust the machine (a runaway render crashed VS Code and forced a reboot on
    21 Sep 2026). Prints the peak so a graph change can be judged on a short slice first."""
    import psutil
    p = subprocess.Popen([str(c) for c in cmd], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
                         text=True, encoding="utf-8", errors="replace")
    proc, peak = psutil.Process(p.pid), 0
    try:
        while p.poll() is None:
            try:
                mem = proc.memory_info()
                peak = max(peak, mem.rss, getattr(mem, "private", 0) or mem.vms)
            except psutil.NoSuchProcess:
                break
            if peak > ceiling_gb * 1024 ** 3:
                p.kill()
                p.wait()
                sys.exit(f"render stopped by watchdog: ffmpeg passed {ceiling_gb} GB "
                         f"(peak {peak / 1024 ** 3:.1f} GB)")
            time.sleep(0.5)
    except KeyboardInterrupt:
        p.kill()
        raise
    err = p.stderr.read()
    print(f"   ffmpeg peak memory {peak / 1024 ** 3:.2f} GB")
    if p.returncode != 0:
        sys.exit(f"ffmpeg failed (exit {p.returncode}):\n{err[-2500:]}")


# ---------------------------------------------------------------- preflight

def check(cfg: dict, work: Path) -> int:
    """Report what the build needs and what's missing. Returns the exit code (0 = all present)."""
    import shutil
    bad = 0

    def line(ok: bool, what: str, note: str = "") -> None:
        nonlocal bad
        bad += not ok
        print(f"  {'ok     ' if ok else 'MISSING'}  {what}{'  ' + note if note else ''}")

    print("tools")
    for tool in ("ffmpeg", "ffprobe"):
        line(bool(shutil.which(tool)), tool, "(on PATH)")
    line(Path(CHROME).exists(), "Chrome", CHROME if Path(CHROME).exists() else "(set $CHROME)")
    print("fonts")
    for f in (FONT_TH, FONT_TH_BOLD, FONT_DIR / "Prompt-Regular.ttf", FONT_DIR / "Prompt-Bold.ttf"):
        line(Path(f).exists(), str(f))
    print("source take, ASR, audio")
    for key in ("source", "asr", "wav"):
        line((ROOT / cfg[key]).exists(), cfg[key])
    print("inserts (a missing one becomes a grey PLACEHOLDER in the cut)")
    seen = set()
    for v in cfg["videos"]:
        for ins in v["inserts"]:
            for lbl, p in resolve_src(ins["src"], work):
                if lbl not in seen:
                    seen.add(lbl)
                    if p is None:
                        line(False, lbl, f"({v['id']} {ins['id']})")
    print(f"  {len(seen)} distinct sources referenced")
    music = work / "music"
    print("intro music: " + (", ".join(m.name for m in music.glob("intro.*")) if music.exists()
                             and any(music.glob("intro.*")) else "none (banner is silent)"))
    if not bad:
        words = Words(ROOT / cfg["asr"])
        audio = Audio(ROOT / cfg["wav"])
        errs = [f"{v['id']}: {e}" for v in cfg["videos"]
                for e in resolve_video(v, cfg, words, audio, work)["errors"]]
        print("cues: " + ("all resolve" if not errs else "\n  " + "\n  ".join(errs)))
        bad += len(errs)
    print("\nready to build" if not bad else f"\n{bad} problem(s)")
    return 1 if bad else 0


# ---------------------------------------------------------------- main

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("edit", type=Path)
    ap.add_argument("--only", nargs="*")
    ap.add_argument("--render", choices=["preview", "h264", "h265"])
    ap.add_argument("--cpu-intermediates", action="store_true",
                    help="encode render intermediates with x264 on the CPU instead of NVENC")
    ap.add_argument("--max-seconds", type=float,
                    help="render only the first N seconds (test a graph change on a slice)")
    ap.add_argument("--zoom-keys", choices=["media", "clip"], default="media",
                    help="what a keyframe <when> counts from in the XML: the start of the source "
                         "media (default) or the clip's in-point; switch if Premiere puts the "
                         "zoom ramps in the wrong place")
    ap.add_argument("--check", action="store_true",
                    help="list every input the build needs and whether it is on this machine; "
                         "writes nothing (run this first on a new computer)")
    args = ap.parse_args()

    cfg = json.loads(args.edit.read_text(encoding="utf-8"))
    cfg["zoom_keys"] = args.zoom_keys
    if args.cpu_intermediates:
        cfg["gpu_intermediates"] = False
    work = ROOT / cfg["work_dir"]
    if args.check:
        sys.exit(check(cfg, work))
    credits = load_credits(work)
    src = ROOT / cfg["source"]
    words = Words(ROOT / cfg["asr"])
    audio = Audio(ROOT / cfg["wav"])
    src_meta = probe(src)
    xml_dir = work / "xml"
    xml_dir.mkdir(parents=True, exist_ok=True)
    cards = work / "cards"
    cards.mkdir(exist_ok=True)

    videos = [v for v in cfg["videos"] if not args.only or v["id"] in args.only]
    resolved = {v["id"]: resolve_video(v, cfg, words, audio, work) for v in videos}
    bad = [f"{vid}: {e}" for vid, r in resolved.items() for e in r["errors"]]
    if bad:
        sys.exit("edit JSON did not resolve:\n  " + "\n  ".join(bad))

    all_ids = [v["id"] for v in cfg["videos"]]
    # intro music under the banner: <work_dir>/music/intro.<any audio ext>; silent if absent
    music = next((m for m in sorted((work / "music").glob("intro.*"))
                  if m.suffix.lower() in {".mp3", ".wav", ".m4a", ".aac", ".ogg", ".flac"}), None) \
        if (work / "music").exists() else None
    print(f"intro music: {music.name if music else 'none (banner is silent)'}")
    for v in videos:
        r = resolved[v["id"]]
        media = {ins["id"]: prep_insert(ins, ins["end"] - ins["start"], work, cfg, credits)
                 for ins in r["inserts"]}
        for c in r["callouts"]:
            c["path"] = cards / f"callout-{c['id']}.png"
            callout_png(c["big"], c["small"], c["path"])

        k = all_ids.index(v["id"])
        cover_pic = {"V1": "spine", "V2": "float-two-ways", "V3": "do-vs-temperature"}.get(v["id"])
        cover_pic = next(iter(sorted((work / "make").glob(f"{cover_pic}.*"))), None) \
            if (work / "make").exists() else None
        cover = cards / f"{v['id']}-cover.png"
        card(cover, [(v["subtitle"], 44, False, "#8a7f6a"),
                     (two_line(v["title"]), 112 if len(v["title"]) <= 24 else 92, True, "#2b2b2b")],
             cover_pic)
        endc = cards / f"{v['id']}-end.png"
        if k + 1 < len(cfg["videos"]):
            nxt = cfg["videos"][k + 1]
            card(endc, [("ตอนต่อไป", 48, False, "#8a7f6a"),
                        (two_line(nxt["title"]), 100, True, "#2b2b2b")], None)
        else:  # the series ends here; no event or link, so the videos stand on their own
            card(endc, [("ขอบคุณที่รับชม", 100, True, "#2b2b2b")], None)

        (xml_dir / f"{v['id']}.xml").write_text(
            build_xml(v, r, media, cover, endc, src, src_meta, cfg, music), encoding="utf-8")

        C = cfg["cover_s"]
        h = r["hook"]
        K = (h["frames"] + h["tail"]) / 30 if h else 0.0
        L = K + C  # the body starts after the hook and the cover
        chap = [f"{yt(0 if i == 0 else L + t - r['in'])} {title}"
                for i, (t, title) in enumerate(r["chapters"])]
        (xml_dir / f"{v['id']}-chapters.txt").write_text("\n".join(chap) + "\n", encoding="utf-8")

        length = L + r["out"] - r["in"] + cfg["end_s"]
        rep = [f"# {v['id']} — {v['title']}", "",
               f"Source {fmt(r['in'])}–{fmt(r['out'])} (snapped from {fmt(v['in'])}–{fmt(v['out'])}); "
               f"finished length {yt(length)} including "
               + (f"a {h['frames'] / 30:.1f}s hook, {h['tail'] / 30:.1f}s fade to black, "
                  if h else "")
               + f"{C:.0f}s {'banner' if h else 'cover'} and {cfg['end_s']:.0f}s end card.", "",
               *(["## Hook", "", "| # | video | source | length | picture | line |",
                  "|---|---|---|---|---|---|",
                  *[f"| {k} | {sum(x['frames'] for x in h['shots'][:k - 1]) / 30:.1f}s "
                    f"| {fmt(sh['in'])}–{fmt(sh['out'])} | {sh['frames'] / 30:.1f}s | "
                    + (f"talk {sh['level']:g}%" + (f" + callout {sh['callout']['big']}"
                                                   if sh["callout"] else "")
                       if sh["show"] == "talk" else f"insert {sh['show']}")
                    + f" | {sh.get('line', '')} |" for k, sh in enumerate(h["shots"], 1)], ""]
                 if h else []),
               "## Chapters", "", *[f"- {c}" for c in chap], "",
               "## Zooms", "", "| id | source | video | length | move | line | why |",
               "|---|---|---|---|---|---|---|",
               *[f"| {z['id']} | {fmt(z['in'])}–{fmt(z['out'])} | {yt(L + z['in'] - r['in'])} "
                 f"| {z['out'] - z['in']:.1f}s | {z['from']:g}→{z['level']:g}% {z['style']}"
                 f"{' (2nd tier)' if z['tier2'] else ''} | {z.get('line', '')} | {z.get('why', '')} |"
                 for z in r["zooms"]], "",
               "## Inserts", "", "| id | video | on screen | status | src | note |",
               "|---|---|---|---|---|---|",
               *[f"| {i['id']} | {yt(L + i['start'] - r['in'])} | {i['end'] - i['start']:.1f}s "
                 f"| {media[i['id']]['status']} | `{i['src']}` | {media[i['id']]['note']} |"
                 for i in r["inserts"]]]
        if r["warnings"]:
            rep += ["", "## Warnings", "", *[f"- {w}" for w in r["warnings"]]]
        (xml_dir / f"{v['id']}-report.md").write_text("\n".join(rep) + "\n", encoding="utf-8")

        ph = sum(1 for m in media.values() if m["status"] == "PLACEHOLDER")
        print(f"{v['id']}: {yt(length)}, {len(r['inserts'])} inserts ({ph} placeholder), "
              f"{len(r['zooms'])} zooms, {len(r['chapters'])} chapters -> xml/{v['id']}.xml")
        for w in r["warnings"]:
            print(f"   ! {w}")

        if args.render:
            out = work / "render" / f"{v['id']}-{args.render}.mp4"
            out.parent.mkdir(exist_ok=True)
            render(v, r, media, cover, endc, src, cfg, args.render, out, args.max_seconds, music)
            print(f"   rendered {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
