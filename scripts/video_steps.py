"""Extract step keyframes (and narration) from a Home Assistant screen recording.

Usage:
    python scripts/video_steps.py user-import/clip.mp4 [--out DIR] [--no-audio]

Output (default DIR = user-import/steps/<clip-stem>/):
    keyframes/NN_post_<t>.png   settled screen after each UI change  (the still for the step)
    keyframes/NN_pre_<t>.png    last frame before the change          (cursor shows what was clicked)
    sheet_N.png                 contact sheets of post frames, 12 per sheet, timestamp burned in
    events.json                 [{idx, t_pre, t_post, click_xy?}]
    transcript.txt              narration with timestamps (faster-whisper), if the clip has audio
    fps1/tNNNN.jpg              plain 1 fps sample at 640 px, the same safety net as
                                video-pipeline/scripts/sample_frames.py, so nothing is missed
                                if settle detection skips an event

Detection: sample ~4 fps, grayscale, downscale; a "change" starts when the fraction of pixels
that moved by more than PIX_T between consecutive samples exceeds CHANGE_T, and the event closes
on the first sample after which the screen stays still (fraction < STILL_T) for STILL_N samples.
A pixel-count metric (not the mean difference) is what lets a small dropdown or dialog register
while cursor motion does not. Screen recordings have no camera noise, so thresholds are low.
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

SAMPLE_FPS = 4
PIX_T = 25          # a pixel "changed" if its gray value moved by more than this
CHANGE_T = 0.0025   # fraction of changed pixels that counts as "something changed"
                    # (a 4-item dropdown is ~3 %, typing a number ~0.08 %, the cursor ~0.05 %)
STILL_T = 0.001     # below this fraction the screen is considered static (cursor drift allowed)
STILL_N = 3         # consecutive still samples (=0.75 s at 4 fps) to close an event
MIN_GAP_S = 0.4     # ignore changes closer than this to the previous event's post frame
DOWNSCALE_W = 480   # analysis width; frames are saved at native resolution


def analyse(path: Path, out: Path):
    cap = cv2.VideoCapture(str(path))
    if not cap.isOpened():
        sys.exit(f"cannot open {path}")
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    stride = max(1, round(fps / SAMPLE_FPS))
    print(f"{path.name}: {w}x{h} @ {fps:.2f} fps, {n_frames / fps:.1f} s, sampling every {stride} frames")

    kf = out / "keyframes"
    kf.mkdir(parents=True, exist_ok=True)
    fps1 = out / "fps1"
    fps1.mkdir(exist_ok=True)
    next_fps1_t = 0.0

    def small(frame):
        g = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        s = DOWNSCALE_W / g.shape[1]
        return cv2.resize(g, (DOWNSCALE_W, int(g.shape[0] * s)), interpolation=cv2.INTER_AREA).astype(np.int16)

    events = []
    prev = None          # (t, frame, small)
    pre = None           # frame just before the current change started
    in_change = False
    still_run = 0
    last_post_t = -1e9
    i = 0
    # Always record the opening screen as event 0.
    first_saved = False

    while True:
        ok = cap.grab()
        if not ok:
            break
        if i % stride:
            i += 1
            continue
        ok, frame = cap.retrieve()
        i += 1
        if not ok:
            break
        t = (i - 1) / fps
        sm = small(frame)

        if t >= next_fps1_t:
            r = 640 / frame.shape[1]
            cv2.imwrite(str(fps1 / f"t{t:07.2f}.jpg"),
                        cv2.resize(frame, (640, int(frame.shape[0] * r)), interpolation=cv2.INTER_AREA),
                        [cv2.IMWRITE_JPEG_QUALITY, 85])
            next_fps1_t += 1.0

        if not first_saved:
            events.append({"idx": 0, "t_pre": None, "t_post": round(t, 2)})
            cv2.imwrite(str(kf / f"00_post_{t:06.2f}.png"), frame)
            first_saved = True

        if prev is not None:
            d = float((np.abs(sm - prev[2]) > PIX_T).mean())
            if not in_change:
                if d > CHANGE_T and t - last_post_t > MIN_GAP_S:
                    in_change = True
                    still_run = 0
                    pre = prev
            else:
                if d < STILL_T:
                    still_run += 1
                    if still_run >= STILL_N:
                        # settled: current frame is the post frame
                        idx = len(events)
                        t_pre = pre[0]
                        cv2.imwrite(str(kf / f"{idx:02d}_pre_{t_pre:06.2f}.png"), pre[1])
                        cv2.imwrite(str(kf / f"{idx:02d}_post_{t:06.2f}.png"), frame)
                        events.append({"idx": idx, "t_pre": round(t_pre, 2), "t_post": round(t, 2)})
                        print(f"  event {idx:02d}: pre {t_pre:6.2f}s  post {t:6.2f}s")
                        in_change = False
                        last_post_t = t
                else:
                    still_run = 0
        prev = (t, frame, sm)
    cap.release()

    (out / "events.json").write_text(json.dumps(events, indent=1), encoding="utf-8")
    contact_sheets(out, kf, events)
    return events


def contact_sheets(out: Path, kf: Path, events, per_sheet=12, cols=3, thumb_w=640):
    posts = sorted(kf.glob("*_post_*.png"))
    if not posts:
        return
    try:
        font = ImageFont.truetype("arial.ttf", 28)
    except OSError:
        font = ImageFont.load_default()
    for s in range(0, len(posts), per_sheet):
        batch = posts[s:s + per_sheet]
        thumbs = []
        for p in batch:
            im = Image.open(p).convert("RGB")
            r = thumb_w / im.width
            im = im.resize((thumb_w, int(im.height * r)), Image.LANCZOS)
            d = ImageDraw.Draw(im)
            label = p.stem.split("_post_")[0] + "  t=" + p.stem.split("_post_")[1] + "s"
            d.rectangle([0, 0, 320, 40], fill=(0, 0, 0))
            d.text((8, 4), label, fill=(255, 255, 0), font=font)
            thumbs.append(im)
        th = max(t.height for t in thumbs)
        rows = (len(thumbs) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * thumb_w + (cols + 1) * 8, rows * th + (rows + 1) * 8), (60, 60, 60))
        for k, t in enumerate(thumbs):
            x = 8 + (k % cols) * (thumb_w + 8)
            y = 8 + (k // cols) * (th + 8)
            sheet.paste(t, (x, y))
        dest = out / f"sheet_{s // per_sheet + 1}.png"
        sheet.save(dest)
        print(f"  wrote {dest.name} ({len(thumbs)} frames)")


def has_audio(path: Path) -> bool:
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=codec_type",
         "-of", "csv=p=0", str(path)],
        capture_output=True, text=True)
    return "audio" in r.stdout


def enable_cuda_dlls() -> None:
    """Same as video-pipeline/scripts/asr_pass.py: CTranslate2 needs the cuBLAS + cuDNN DLLs
    from the nvidia-*-cu12 pip wheels on the DLL search path, which Windows does not add.
    Without this the model silently falls back to CPU."""
    import glob
    import os
    import site
    roots = list(site.getsitepackages())
    try:
        roots.append(site.getusersitepackages())
    except Exception:
        pass
    for sp in roots:
        for sub in ("cublas", "cudnn"):
            for d in glob.glob(os.path.join(sp, "nvidia", sub, "bin")):
                if os.path.isdir(d):
                    os.add_dll_directory(d)
                    os.environ["PATH"] = d + os.pathsep + os.environ.get("PATH", "")


def wordless_gaps(segs, duration_s: float, min_gap_s: float = 6.0):
    """Dropout guard from asr_pass.py: any stretch >= min_gap_s with no recognised speech."""
    gaps, prev = [], 0.0
    for s in segs:
        if s.start - prev >= min_gap_s:
            gaps.append((prev, s.start))
        prev = max(prev, s.end)
    if duration_s - prev >= min_gap_s:
        gaps.append((prev, duration_s))
    return gaps


def transcribe(path: Path, out: Path, model_name: str, language: str, device: str = "auto"):
    """ASR config ported verbatim from video-pipeline/scripts/asr_pass.py (the proven Thai
    settings, KSM video-editing-pipeline v3): sequential decoding, Whisper temperature
    fallback ON, Silero VAD OFF, beam 5, condition_on_previous_text=False, cuda float16
    with cpu int8 fallback, wordless-gap warning."""
    if not has_audio(path):
        print("  no audio stream; skipping transcript")
        return
    enable_cuda_dlls()
    from faster_whisper import WhisperModel
    wav = out / "audio.wav"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(path), "-vn", "-ac", "1", "-ar", "16000",
                    "-c:a", "pcm_s16le", str(wav)], check=True)
    # CUDA init can die with a hard access violation (seen 2026-09-08 after NVIDIA driver
    # 616.64; the proven asr_pass.py crashes the same way), which no try/except catches.
    # So probe CUDA in a child process first and fall back to CPU if that child dies.
    model = None
    if device in ("auto", "cuda"):
        probe = subprocess.run(
            [sys.executable, "-c",
             "import sys; sys.path.insert(0, %r); import video_steps as v; v.enable_cuda_dlls(); "
             "from faster_whisper import WhisperModel; WhisperModel(%r, device='cuda', compute_type='float16'); "
             "print('cuda-ok')" % (str(Path(__file__).resolve().parent), model_name)],
            capture_output=True, text=True)
        if "cuda-ok" in probe.stdout:
            model = WhisperModel(model_name, device="cuda", compute_type="float16")
            print(f"  whisper '{model_name}' on cuda")
        else:
            print(f"  cuda probe failed (exit {probe.returncode}); falling back to cpu int8")
    if model is None:
        if device == "cuda":
            sys.exit("cuda requested but unusable")
        model = WhisperModel(model_name, device="cpu", compute_type="int8")
        print(f"  whisper '{model_name}' on cpu")
    segments, info = model.transcribe(
        str(wav),
        language=language,
        word_timestamps=True,
        vad_filter=False,
        beam_size=5,
        condition_on_previous_text=False,
    )
    segs = list(segments)
    lines = [f"# model={model_name} language={info.language} (p={info.language_probability:.2f}) "
             f"duration={info.duration:.1f}s"]
    for seg in segs:
        lines.append(f"[{seg.start:6.2f} - {seg.end:6.2f}] {seg.text.strip()}")
    for s, e in wordless_gaps(segs, info.duration):
        lines.append(f"!! NO WORDS {s:.1f}-{e:.1f}s ({e - s:.1f}s) - ASR dropout or long pause")
        print(f"  !! NO WORDS {s:.1f}-{e:.1f}s - verify by ear")
    (out / "transcript.txt").write_text("\n".join(lines), encoding="utf-8")
    print(f"  transcript: {len(segs)} segments -> transcript.txt")
    wav.unlink(missing_ok=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("clip", type=Path)
    ap.add_argument("--out", type=Path)
    ap.add_argument("--no-audio", action="store_true")
    ap.add_argument("--model", default="medium", help="faster-whisper model (proven default: medium)")
    ap.add_argument("--lang", default=None,
                    help="narration language (th, en); default lets Whisper detect it. Forcing the "
                         "wrong language mangles the text AND is several times slower, because every "
                         "window falls through the temperature ladder (seen 2026-09-08, English clip as th)")
    ap.add_argument("--device", default="auto", choices=["auto", "cuda", "cpu"])
    a = ap.parse_args()
    out = a.out or (a.clip.parent / "steps" / a.clip.stem)
    out.mkdir(parents=True, exist_ok=True)
    events = analyse(a.clip, out)
    print(f"{len(events)} events -> {out}")
    if not a.no_audio:
        transcribe(a.clip, out, a.model, a.lang, a.device)


if __name__ == "__main__":
    main()
