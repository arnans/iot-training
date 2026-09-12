#!/usr/bin/env python3
"""Render root-level Markdown documents into standalone HTML for docs/.

The Markdown at the repo root stays the single source of truth. This script
produces a self-contained, print-ready page per language, styled for handing to
the venue's network provider rather than for the participant worksheet site.

MkDocs copies non-Markdown files in docs/ through to the built site verbatim, so
the output lands at <site>/network-requirements.html without picking up the
worksheet theme.

    python scripts/render-network-doc.py

Requires the `markdown` package, which arrives with mkdocs (requirements.txt).
"""

from __future__ import annotations

import datetime as _dt
import pathlib
import re
import sys


try:
    import markdown
except ImportError:  # pragma: no cover
    sys.exit("markdown is not installed. Run: pip install -r requirements.txt")

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from network_figures import FIGURES  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "docs"
IMG_DIR = OUT_DIR / "images"

# source markdown -> (output file, <html lang>, document kicker)
DOCUMENTS = [
    # The kicker sits above the title, so keep it clear of the opening sentence,
    # which already names the audience in both editions.
    ("NETWORK-REQUIREMENTS-th.md", "network-requirements.html", "th",
     "เอกสารข้อกำหนดทางเทคนิค"),
    ("NETWORK-REQUIREMENTS.md", "network-requirements-en.html", "en",
     "Vendor specification"),
    # Not a vendor document, but the same shape: one standalone page, no worksheet
    # theme, readable by anyone with the link. Its links are absolute so the page
    # works from the repository and from GitHub Pages alike.
    ("INSTRUCTOR-RESOURCES.md", "instructor-resources.html", "en",
     "Instructor & TA handbook"),
]

EXTENSIONS = ["tables", "attr_list", "sane_lists", "md_in_html"]

TEMPLATE = """<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{kicker}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Sarabun:wght@400;600;700&family=IBM+Plex+Mono:wght@400;600&display=swap" rel="stylesheet">
<style>
{css}
</style>
</head>
<body>
<article class="doc">
  <header class="doc-head">
    <p class="kicker">{kicker}</p>
    <h1>{title}</h1>
    <p class="meta">{meta}</p>
    <p class="disclosure">{disclosure}</p>
  </header>
{body}
  <footer class="doc-foot">
    <p>{footer}</p>
  </footer>
</article>
</body>
</html>
"""

CSS = """
:root {
  --ink: #14181d;
  --ink-soft: #4a545f;
  --rule: #d9dee4;
  --rule-soft: #eaeef2;
  --paper: #ffffff;
  --wash: #f5f7f9;
  --accent: #0f6b63;
  --accent-wash: #e8f3f1;
  --flag: #8a5a00;
  --flag-wash: #fdf4e3;
  --mono: "IBM Plex Mono", ui-monospace, "Cascadia Mono", Consolas, monospace;
}

*, *::before, *::after { box-sizing: border-box; }

html { -webkit-text-size-adjust: 100%; }

body {
  margin: 0;
  padding: 3.5rem 1.25rem 5rem;
  background: var(--wash);
  color: var(--ink);
  font-family: Sarabun, "Leelawadee UI", "Noto Sans Thai", -apple-system,
               BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif;
  font-size: 16px;
  line-height: 1.85;
}

.doc {
  max-width: 54rem;
  margin: 0 auto;
  padding: 3.5rem clamp(1.5rem, 5vw, 4rem) 3rem;
  background: var(--paper);
  border: 1px solid var(--rule);
  border-radius: 4px;
  box-shadow: 0 1px 2px rgba(20, 24, 29, .04), 0 12px 32px rgba(20, 24, 29, .06);
}

/* ---- masthead ---------------------------------------------------------- */

.doc-head { border-bottom: 3px solid var(--accent); padding-bottom: 1.5rem; margin-bottom: 2.5rem; }

.kicker {
  margin: 0 0 .6rem;
  font-size: .78rem;
  font-weight: 600;
  letter-spacing: .14em;
  text-transform: uppercase;
  color: var(--accent);
}

.doc-head h1 { margin: 0; font-size: clamp(1.7rem, 4vw, 2.3rem); line-height: 1.3; font-weight: 700; }

.meta { margin: .75rem 0 0; font-size: .9rem; color: var(--ink-soft); }

.disclosure {
  margin: 1.1rem 0 0;
  padding-top: .85rem;
  border-top: 1px solid var(--rule-soft);
  font-size: .82rem;
  line-height: 1.7;
  color: var(--ink-soft);
}

/* ---- headings ---------------------------------------------------------- */

h2 {
  margin: 3rem 0 1rem;
  padding-bottom: .5rem;
  border-bottom: 1px solid var(--rule);
  font-size: 1.4rem;
  line-height: 1.4;
  font-weight: 700;
}

h3 {
  margin: 2rem 0 .75rem;
  font-size: 1.12rem;
  line-height: 1.5;
  font-weight: 700;
  color: var(--accent);
}

h2 + h3 { margin-top: 1.25rem; }

p { margin: 0 0 1.15rem; }

a { color: var(--accent); text-underline-offset: 2px; }

strong { font-weight: 700; }

hr { height: 0; margin: 3rem 0; border: 0; border-top: 1px solid var(--rule-soft); }

/* ---- lists ------------------------------------------------------------- */

ul, ol { margin: 0 0 1.15rem; padding-left: 1.35rem; }
li { margin-bottom: .5rem; }
li > ul, li > ol { margin-top: .5rem; margin-bottom: .25rem; }

/* ---- tables ------------------------------------------------------------ */

.table-scroll { overflow-x: auto; margin: 0 0 1.6rem; -webkit-overflow-scrolling: touch; }

table {
  width: 100%;
  border-collapse: collapse;
  font-size: .92rem;
  line-height: 1.65;
}

th, td {
  padding: .6rem .8rem;
  border: 1px solid var(--rule);
  text-align: left;
  vertical-align: top;
}

thead th {
  background: var(--wash);
  font-weight: 700;
  white-space: nowrap;
}

tbody tr:nth-child(even) { background: #fbfcfd; }

/* ---- callouts (blockquotes carry the load-bearing asks) ---------------- */

blockquote {
  margin: 0 0 1.6rem;
  padding: 1.1rem 1.35rem .35rem;
  background: var(--flag-wash);
  border: 1px solid #f0dfba;
  border-left: 4px solid var(--flag);
  border-radius: 3px;
}

blockquote p { margin-bottom: .8rem; }

/* ---- code -------------------------------------------------------------- */

code {
  padding: .12em .38em;
  background: var(--accent-wash);
  border-radius: 3px;
  font-family: var(--mono);
  font-size: .88em;
  font-weight: 600;
  white-space: nowrap;
}

blockquote code { background: #fff; border: 1px solid #ecdcb8; }

figure {
  margin: 0 0 1.9rem;
  padding: 1.25rem 1.25rem .9rem;
  background: #fcfdfd;
  border: 1px solid var(--rule);
  border-radius: 4px;
}

figure svg { display: block; width: 100%; height: auto; }

figcaption {
  margin-top: .9rem;
  padding-top: .7rem;
  border-top: 1px solid var(--rule-soft);
  font-size: .82rem;
  line-height: 1.6;
  color: var(--ink-soft);
  text-align: center;
}

/* ---- footer ------------------------------------------------------------ */

.doc-foot {
  margin-top: 3.5rem;
  padding-top: 1.25rem;
  border-top: 1px solid var(--rule);
  font-size: .82rem;
  color: var(--ink-soft);
}

.doc-foot p { margin: 0; }

/* ---- print ------------------------------------------------------------- */

@media print {
  @page { size: A4; margin: 16mm 14mm; }
  body { padding: 0; background: #fff; font-size: 10.5pt; line-height: 1.6; }
  .doc { max-width: none; padding: 0; border: 0; border-radius: 0; box-shadow: none; }
  a { color: inherit; text-decoration: none; }
  h2 { break-after: avoid; page-break-after: avoid; }
  h3 { break-after: avoid; page-break-after: avoid; }
  table, blockquote, .table-scroll, figure { break-inside: avoid; page-break-inside: avoid; }
  tr, li { break-inside: avoid; page-break-inside: avoid; }
  thead { display: table-header-group; }
  .doc-foot { break-before: avoid; }
}
"""

FOOTERS = {
    "th": "เอกสารนี้สร้างจากไฟล์ต้นทาง {src} ในคลัง iot-training "
          "หากต้องการแก้ไข ขอให้แก้ที่ไฟล์ต้นทางแล้วสร้างใหม่",
    "en": "Generated from {src} in the iot-training repository. "
          "Edit the Markdown source and re-render rather than this file.",
}

METAS = {
    "th": "โครงการอบรม IoT ในฟาร์มอัจฉริยะ · ปรับปรุงล่าสุด {date}",
    "en": "IoT in Smart Farming workshop · Last updated {date}",
}

# AI authorship disclosure, carried in the masthead of every rendered page.
# Roger's wording, which names the tool and credits the preparing team; it is a
# deliberate variant of the canonical disclaimer in roger-ksm
# knowledge/ai-disclaimer-bilingual.md.
DISCLOSURES = {
    "th": "เอกสารนี้เรียบเรียงด้วย Claude AI เนื้อหาได้รับการออกแบบและตรวจทานโดยผู้รับผิดชอบแล้ว "
          "ขอรับรองว่าเป็นไปตามเจตนาของคณะจัดทำทุกประการ",
    "en": "This document was compiled with Claude AI. Its content was designed and reviewed by "
          "those responsible, who certify that it reflects the intent of the preparing team in "
          "every respect.",
}


def render(md_name: str, out_name: str, lang: str, kicker: str) -> pathlib.Path:
    src = ROOT / md_name
    text = src.read_text(encoding="utf-8")

    # The H1 becomes the masthead title, so lift it out of the body.
    lines = text.splitlines()
    title = out_name
    for i, line in enumerate(lines):
        if line.startswith("# "):
            title = line[2:].strip()
            del lines[i]
            break
    text = "\n".join(lines).lstrip("\n")

    # Drop the cross-language pointer: each rendered page stands alone.
    text = re.sub(r"^\*(?:ฉบับภาษา|English version)[^\n]*\*\n+", "", text,
                  flags=re.MULTILINE)

    html = markdown.markdown(text, extensions=EXTENSIONS, output_format="html5")

    # Inline each figure so the page stays self-contained and prints as one
    # piece. The Markdown keeps a plain image link, which renders on GitHub.
    def _inline(match: re.Match) -> str:
        alt, name = match.group(1), match.group(2)
        svg = (IMG_DIR / f"{name}-{lang}.svg").read_text(encoding="utf-8")
        svg = "\n".join("    " + ln for ln in svg.splitlines())
        return ("<figure>\n" + svg + "\n    <figcaption>" + alt
                + "</figcaption>\n  </figure>")

    html = re.sub(
        r'<p><img alt="([^"]*)" src="docs/images/([a-z-]+)-' + lang + r'\.svg"\s*/?></p>',
        _inline, html)

    # Wrap tables so wide ones scroll instead of breaking the page.
    html = html.replace("<table>", '<div class="table-scroll"><table>')
    html = html.replace("</table>", "</table></div>")

    # Indent the body so the generated file reads like hand-written HTML.
    body = "\n".join("  " + line if line else "" for line in html.splitlines())

    date = _dt.date.today().isoformat()
    page = TEMPLATE.format(
        lang=lang,
        title=title,
        kicker=kicker,
        css=CSS.strip(),
        body=body,
        disclosure=DISCLOSURES[lang],
        meta=METAS[lang].format(date=date),
        footer=FOOTERS[lang].format(src=md_name),
    )

    out = OUT_DIR / out_name
    out.write_text(page, encoding="utf-8", newline="\n")
    return out


def build_figures() -> None:
    """Write one SVG per figure per language into docs/images/."""
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    for name, build in FIGURES.items():
        for lang in ("th", "en"):
            path = IMG_DIR / f"{name}-{lang}.svg"
            path.write_text(build(lang) + "\n", encoding="utf-8", newline="\n")
            print(f"figure -> {path.relative_to(ROOT)}")


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    build_figures()
    for md_name, out_name, lang, kicker in DOCUMENTS:
        out = render(md_name, out_name, lang, kicker)
        print(f"{md_name} -> {out.relative_to(ROOT)}  ({out.stat().st_size:,} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
