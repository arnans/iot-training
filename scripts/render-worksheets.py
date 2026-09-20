#!/usr/bin/env python3
"""Render the participant worksheets into self-contained HTML, for dry runs off the site.

The Markdown in docs/ stays the single source of truth. This script reuses the site's
own pieces, so a render behaves like the live worksheet:

  - hooks/fields.py expands the {{f:...}} markers into the same form fields
  - docs/stylesheets/extra.css supplies the design (its light/dark blocks are
    re-keyed from Material's colour-scheme attribute to prefers-color-scheme)
  - docs/javascripts/extra.js saves answers to localStorage and adds the toolbar

Images are linked as ../images/..., which GitHub Pages serves next to the renders, so
the committed files stay small. --offline inlines every image as a data URI instead, for
a render that must open on its own: attached to a message or opened from a USB stick.
Links to pages that are not rendered (index, record sheet, reference) become plain text.

    python scripts/render-worksheets.py                    # docs/renders/<page>.html
    python scripts/render-worksheets.py --offline          # same, images inlined (~30 MB in all)
    python scripts/render-worksheets.py --combined out.html # also one page with all as tabs (always inlined)

The combined file is an HTML fragment (no <html>/<head>), written for publishing as a
claude.ai Artifact; it asks the host for its download capability so the
"download answers" button still works inside the artifact viewer.

Requires the `markdown` and `pymdownx` packages, which arrive with mkdocs-material
(requirements.txt). GitHub Pages serves docs/ from main, so the committed files are public
at https://arnans.github.io/iot-training/renders/<page>.html -- re-run this script and
commit after editing a worksheet.
"""

from __future__ import annotations

import argparse
import base64
import html
import importlib.util
import mimetypes
import pathlib
import re
import sys

try:
    import markdown
    from pymdownx import slugs
except ImportError:  # pragma: no cover
    sys.exit("markdown / pymdownx not installed. Run: pip install -r requirements.txt")

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
OUT_DIR = DOCS / "renders"

# (source, slug, group, eyebrow, label) -- the group is a heading row in the sidebar and the
# first words of the chip on a phone; the label is the page title cut to what fits a chip.
# Keep them in step with mkdocs.yml's nav and each page's own # heading.
PAGES = [
    ("install.md", "install", "ก่อนการอบรม", "", "เตรียมแล็ปท็อป"),
    ("session-1-start.md", "session-1-start", "ช่วงที่ 1", "", "เตรียมพร้อมก่อนเริ่ม"),
    ("activity-1.md", "activity-1", "ช่วงที่ 1", "กิจกรรม 1", "อ่านค่าเซนเซอร์ (Sense)"),
    ("activity-2.md", "activity-2", "ช่วงที่ 1", "กิจกรรม 2", "ต่อวงจรและสั่งงานหลอดไฟ (Act)"),
    ("activity-3.md", "activity-3", "ช่วงที่ 1", "กิจกรรม 3", "สร้างกฎควบคุมระบบ (Logic)"),
    ("activity-4.md", "activity-4", "ช่วงที่ 2", "กิจกรรม 4", "ตั้งกฎอัตโนมัติ (Think)"),
    ("activity-5.md", "activity-5", "ช่วงที่ 2", "กิจกรรม 5", "จำลองปัญหาและป้องกัน (Failure lab)"),
    ("activity-6.md", "activity-6", "ช่วงที่ 3", "กิจกรรม 6", "อ่านข้อมูลย้อนหลัง (History)"),
    ("activity-7.md", "activity-7", "ช่วงที่ 3", "กิจกรรม 7", "สร้างแดชบอร์ด (Dashboard)"),
    ("activity-8.md", "activity-8", "ช่วงที่ 3", "กิจกรรม 8", "ออกแบบระบบฟาร์ม (Design)"),
    ("resources.md", "resources", "อ้างอิง", "", "รวมไฟล์และลิงก์"),
    ("reference.md", "reference", "อ้างอิง", "", "เมนูและวิธีแก้ปัญหา"),
    ("record-sheet.md", "record-sheet", "อ้างอิง", "", "ใบบันทึกของกลุ่ม"),
]
SLUGS = {p[1] for p in PAGES}
# the switcher ends at activity 8: the reference pages are reached from docs/index.html, so the
# course structure stays readable. They are still rendered (and linked from the front door).
NAV_PAGES = [p for p in PAGES if p[2] != "อ้างอิง"]
# the session pages became one page per activity; the old render names forward to the session's first page
REDIRECTS = {"session-1": "session-1-start", "session-2": "activity-4", "session-3": "activity-6", "session-3-history": "activity-6"}

SITE_NAME = "IoT ในฟาร์มอัจฉริยะ"
# shown at the foot of every page, on screen and in print; the site footer carries the same line (mkdocs.yml)
AI_DISCLOSURE = "เอกสารนี้เรียบเรียงขึ้นด้วย AI (Fable 5.1 และ GPT-6 Astra) ภายใต้การกำกับอย่างใกล้ชิดของผู้จัดทำ และรับรองว่าเนื้อหาเป็นไปตามเจตนาของผู้จัดทำทุกประการ"
FONTS = ("https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;500;600;700"
         "&family=IBM+Plex+Mono:wght@400;600&display=swap")


def _load_hook(name: str):
    spec = importlib.util.spec_from_file_location(f"{name}_hook", ROOT / "hooks" / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


FIELDS = _load_hook("fields")
STEPS = _load_hook("steps")
HEADINGS = _load_hook("headings")
CALLOUTS = _load_hook("callouts")
VIDEOS = _load_hook("videos")


# ---------------------------------------------------------------- styles

def site_css() -> str:
    """extra.css with Material's scheme attributes swapped for the three-state theme pattern."""
    css = (DOCS / "stylesheets" / "extra.css").read_text(encoding="utf-8")
    css = re.sub(r"^@import .*$\n?", "", css, flags=re.M)  # fonts arrive via <link>; the URL itself holds ";"
    m = re.search(r'\[data-md-color-scheme="slate"\]\s*\{(.*?)\n\}', css, re.S)
    if not m:
        sys.exit("extra.css: dark (slate) block not found; update site_css()")
    dark = m.group(1) + "\n  color-scheme: dark;"
    css = css.replace(m.group(0), "")
    css = css.replace('[data-md-color-scheme="default"]', ":root")
    css += (
        "\n/* dark: follows the OS unless the viewer picked light; an explicit dark pick always wins */\n"
        f'@media (prefers-color-scheme: dark) {{\n  :root:not([data-theme="light"]) {{{dark}\n  }}\n}}\n'
        f':root[data-theme="dark"] {{{dark}\n}}\n'
    )
    return css


# What Material's own stylesheet normally provides, trimmed to what the worksheets use.
BASE_CSS = """
:root { color-scheme: light; }
[hidden] { display: none !important; }
*, *::before, *::after { box-sizing: border-box; }
html { -webkit-text-size-adjust: 100%; scroll-padding-top: 1rem; }
body {
  margin: 0;
  background: var(--md-default-bg-color);
  color: var(--md-default-fg-color);
  font: 400 16px/1.6 "Prompt", "Segoe UI", Tahoma, sans-serif;
}

/* ---- top band ---- */
.ws-top {
  background: linear-gradient(90deg, var(--md-primary-fg-color--dark), var(--md-primary-fg-color));
  color: #ffffff;
  padding-block: 0.75rem;
  padding-inline: 16px;
}
.ws-top__inner {
  max-width: 76rem;
  margin: 0 auto;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 0.4rem 1rem;
}
.ws-brand { font-weight: 600; font-size: 1.05rem; letter-spacing: 0.01em; }

/* ---- shell: page switcher + reading column ---- */
.ws-shell {
  max-width: 76rem;
  margin: 0 auto;
  padding-inline: 16px;
  display: grid;
  grid-template-columns: minmax(0, 1fr);
  column-gap: 2.75rem;
}
.ws-side { padding-block: 1rem 0; font-size: 0.86rem; line-height: 1.5; }
.ws-pages { list-style: none; margin: 0; padding: 0; display: flex; flex-wrap: wrap; gap: 0.4rem; }
.ws-pages > li > a {
  display: inline-block;
  padding: 0.3rem 0.9rem;
  border-radius: 999px;
  border: 1px solid var(--ag-chip-border);
  color: var(--md-default-fg-color--light);
  text-decoration: none;
  font-weight: 500;
}
.ws-pages > li > a:hover { border-color: var(--ag-green); color: var(--md-typeset-a-color); }
.ws-pages > li.is-current > a {
  background: var(--ag-green);
  border-color: var(--ag-green);
  color: #ffffff;
}
.ws-g::after, .ws-n::after { content: " · "; }
.ws-pages > li > a::before { display: none; }   /* the number badge is a sidebar thing */
.ws-pages > li.is-current .ws-n, .ws-pages > li.is-current .ws-g { opacity: 0.85; }
.ws-toc { display: none; }
/* phones: the current group's pages as chips, every other group as one chip (its first page) */
.ws-pages > li[data-page]:not(.in-group) { display: none; }
.ws-pages > li.ws-group.in-group { display: none; }
.ws-pages > li.in-group .ws-g { display: none; }
/* previous / next: two buttons, the next one filled so it reads as the way forward */
.ws-pager { display: flex; flex-wrap: wrap; gap: 0.8rem; margin: 3.5rem 0 0; font-size: 0.92rem; }
.ws-pager a {
  flex: 1 1 14rem;
  display: block;
  padding: 0.7rem 1rem;
  border: 2px solid var(--ag-green);
  border-radius: 0.6rem;
  color: var(--ag-green-deep);
  text-decoration: none;
  line-height: 1.4;
}
.ws-pager .ws-next { margin-left: auto; text-align: right; background: var(--ag-green); color: #ffffff; }
.ws-pager__k { display: block; font-size: 0.74rem; font-weight: 500; opacity: 0.85; }
.ws-pager__t { display: block; font-weight: 700; }
.ws-pager a:hover, .ws-pager a:focus-visible { border-color: var(--ag-green-deep); box-shadow: 0 2px 8px var(--ag-shadow); }
.ws-pager .ws-next:hover, .ws-pager .ws-next:focus-visible { background: var(--ag-green-deep); }
.ws-disclosure { margin: 4rem 0 0; padding-top: 0.8rem; border-top: 1px solid var(--ag-rule); font-size: 0.74rem; line-height: 1.5; color: var(--md-default-fg-color--lighter); }
.ws-side a:focus-visible, .ws-top a:focus-visible { outline: 2px solid var(--ag-marigold); outline-offset: 2px; }

@media (min-width: 64rem) {
  .ws-shell { grid-template-columns: 15rem minmax(0, 47rem); }
  .ws-side {
    position: sticky;
    top: 0;
    align-self: start;
    min-height: 100vh;
    max-height: 100vh;
    overflow-y: auto;
    padding: 2rem 1rem 2rem 0.5rem;
    background: var(--ag-nav-bg);   /* its own surface, apart from the page */
  }
  .ws-pages { display: block; }
  /* sidebar: a session is a heading with a rule above; under it each activity with its number
     as a badge, the unnumbered pages with a hollow one; only the open page's sub-activity
     list gets a tree line */
  .ws-g, .ws-n { display: none; }
  .ws-pages > li[data-page]:not(.in-group), .ws-pages > li.ws-group.in-group { display: block; }
  .ws-pages > li.ws-group > a, .ws-pages > li.ws-group > a:hover {
    display: block;
    margin: 1.5rem 0 0.4rem 0;
    padding: 0.6rem 0.2rem 0;
    border: 0;
    border-top: 2px solid var(--ag-rule);
    border-radius: 0;
    font-size: 0.92rem;
    font-weight: 700;
    color: var(--ag-green-deep);
  }
  .ws-pages > li.ws-group:first-child > a { margin-top: 0; padding-top: 0; border-top: 0; }
  .ws-pages > li[data-page] { margin: 0 0 0.15rem 0.2rem; }
  .ws-pages > li[data-page] > a {
    display: flex;
    align-items: baseline;
    gap: 0.5rem;
    border: 0;
    border-radius: 0.4rem;
    padding: 0.3rem 0.5rem;
    font-weight: 500;
  }
  .ws-pages > li[data-page] > a::before {
    content: attr(data-n);
    display: block;
    flex: none;
    width: 1.45rem;
    height: 1.45rem;
    border-radius: 50%;
    background: var(--ag-badge-bg);
    color: var(--ag-badge-fg);
    font-size: 0.72rem;
    font-weight: 700;
    line-height: 1.45rem;
    text-align: center;
    align-self: center;
  }
  .ws-pages > li[data-page] > a:not([data-n])::before {
    content: "";
    width: 1.05rem;
    height: 1.05rem;
    margin: 0 0.2rem;
    background: transparent;
    border: 2px solid var(--ag-rule);
  }
  .ws-pages > li.is-current > a { background: var(--md-default-bg-color); color: var(--md-typeset-a-color); font-weight: 700; }
  .ws-t { display: block; }
  .ws-pages > li.is-current .ws-toc {
    display: block;
    list-style: none;
    margin: 0.3rem 0 0.8rem 0.9rem;
    padding: 0 0 0 0.75rem;
    border-left: 2px solid var(--ag-rule);
  }
  .ws-toc a {
    display: block;
    padding: 0.22rem 0;
    color: var(--md-default-fg-color--light);
    text-decoration: none;
    font-size: 0.8rem;
  }
  .ws-toc a:hover { color: var(--md-typeset-a-color); }
}

/* ---- the worksheet itself ---- */
.md-typeset { padding-block: 1rem 5rem; overflow-wrap: break-word; min-width: 0; }
.md-typeset > section > h1:first-child, .md-typeset > h1:first-child { margin-top: 0.6em; }
.md-typeset p, .md-typeset ul, .md-typeset ol, .md-typeset blockquote { margin: 0 0 1em; }
.md-typeset ul { padding-left: 1.4em; }
.md-typeset li > ul, .md-typeset li > ol { margin: 0.4em 0 0.4em; }
.md-typeset a { color: var(--md-typeset-a-color); text-underline-offset: 0.18em; }
.md-typeset code {
  font-family: "IBM Plex Mono", Consolas, monospace;
  background: var(--md-code-bg-color);
  color: var(--md-code-fg-color);
}
.md-typeset pre {
  background: var(--md-code-bg-color);
  padding: 0.8em 1em;
  border-radius: 0.6em;
  overflow-x: auto;
  margin: 0.4em 0 1em;
}
.md-typeset pre code { padding: 0; background: none; font-size: 0.88em; }
.md-typeset hr { border: 0; }
.md-typeset blockquote > :last-child { margin-bottom: 0; }
.md-typeset img { max-width: 100%; height: auto; display: inline-block; }
.md-typeset .table-wrap { overflow-x: auto; margin: 0 0 1.3em; }
.md-typeset .video { margin: 0.4em 0 1.2em; max-width: 42rem; }
.md-typeset .video-frame { position: relative; aspect-ratio: 16 / 9; border-radius: 0.6em; overflow: hidden; background: #000; }
.md-typeset .video-frame iframe { position: absolute; inset: 0; width: 100%; height: 100%; border: 0; }
.md-typeset .video-link { font-size: 0.85em; margin: 0.35em 0 0; }
.md-typeset table { border-collapse: separate; border-spacing: 0; width: 100%; }
.md-typeset th, .md-typeset td { padding: 0.55em 0.9em; text-align: left; }
.md-typeset td { font-variant-numeric: tabular-nums; }
.md-typeset .admonition {
  margin: 1.2em 0;
  padding: 0.6em 1em;
  border-left: 4px solid var(--ag-sky);
  background: var(--ag-panel);
}
.md-typeset .admonition-title { font-weight: 600; margin-bottom: 0.3em; }
"""

# Loaded after extra.css: pieces of extra.css that assumed Material's markup around them.
LATE_CSS = """
.md-typeset ul.task-list { padding-left: 0; }
.md-typeset .task-list-item { position: relative; }
.md-typeset .task-list-control .task-list-indicator { position: absolute; display: block; left: 0; top: 0.3em; }
.md-typeset .task-list-control .task-list-indicator::after {
  content: "";
  position: absolute;
  left: 0.36em;
  top: 0.1em;
  width: 0.34em;
  height: 0.68em;
  border: solid #ffffff;
  border-width: 0 0.16em 0.16em 0;
  transform: rotate(45deg);
  opacity: 0;
}
.md-typeset .task-list-control [type="checkbox"] {
  position: absolute;
  left: 0;
  top: 0.3em;
  width: 1.3em;
  height: 1.3em;
  margin: 0;
  opacity: 0;
  cursor: pointer;
  z-index: 1;
}
.md-typeset .task-list-control [type="checkbox"]:checked + .task-list-indicator::after { opacity: 1; }
.md-typeset .task-list-control [type="checkbox"]:focus-visible + .task-list-indicator {
  outline: 2px solid var(--ag-marigold);
  outline-offset: 2px;
}
.md-typeset input.fld:focus-visible, .md-typeset textarea.fld-ta:focus-visible { outline: 2px solid var(--ag-green); }

/* lightbox for the ดูภาพ chips (the site uses glightbox) */
#shot-box {
  border: 0;
  padding: 0.6rem;
  max-width: min(96vw, 1100px);
  border-radius: 0.8rem;
  background: var(--md-default-bg-color);
  color: var(--md-default-fg-color);
  box-shadow: 0 20px 60px var(--ag-shadow);
}
#shot-box::backdrop { background: rgba(10, 20, 12, 0.72); }
#shot-box img { display: block; max-width: 100%; max-height: 80vh; margin: 0 auto; border-radius: 0.5rem; }
#shot-box p { margin: 0.5rem 0.2rem 0; font-size: 0.85rem; color: var(--md-default-fg-color--light); }

@media print {
  .ws-top, .ws-side, .ws-pager, #shot-box { display: none !important; }
  .ws-shell { display: block; max-width: none; padding: 0; }
}
"""


# ---------------------------------------------------------------- scripts

def extra_js() -> str:
    """extra.js, with its <a download> save swapped for a hook that also works in a sandbox."""
    js = (DOCS / "javascripts" / "extra.js").read_text(encoding="utf-8")
    js, n = re.subn(
        r"var blob = new Blob\(\[JSON\.stringify\(out, null, 2\)\].*?\}, 1500\);",
        "window.wsSaveFile(name, JSON.stringify(out, null, 2));",
        js,
        flags=re.S,
    )
    if n != 1:
        sys.exit("extra.js: export block not found; update extra_js()")
    return js


SAVE_SHIM_JS = r"""
(function () {
  var downloads = null;
  if (window.claude && typeof window.claude.use === "function") {
    window.claude.use("downloads").then(function (d) { downloads = d; }, function () {});
  }
  function anchorSave(name, text) {
    var a = document.createElement("a");
    a.href = URL.createObjectURL(new Blob([text], { type: "application/json" }));
    a.download = name;
    document.body.appendChild(a);
    a.click();
    setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 1500);
  }
  window.wsSaveFile = function (name, text) {
    if (!downloads) { anchorSave(name, text); return; }
    downloads.save({ filename: name, data: text }).catch(function (e) {
      if (e && e.code === "declined") return;
      window.alert("ดาวน์โหลดไม่สำเร็จ (" + ((e && (e.message || e.code)) || "unknown") + ")");
    });
  };
})();
"""

LIGHTBOX_JS = r"""
(function () {
  var box = document.getElementById("shot-box");
  if (!box || typeof box.showModal !== "function") return;
  var img = box.querySelector("img"), cap = box.querySelector("p");
  document.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest("a.glightbox");
    if (!a) return;
    e.preventDefault();
    img.src = a.getAttribute("href");
    cap.textContent = a.getAttribute("data-title") || "";
    box.showModal();
  });
  box.addEventListener("click", function () { box.close(); });
})();
"""

# Combined file only: one page visible at a time, switcher remembered per viewer.
TABS_JS = r"""
(function () {
  var TAB = "farm-worksheet.tab";
  var pages = Array.prototype.slice.call(document.querySelectorAll(".ws-page"));
  var items = Array.prototype.slice.call(document.querySelectorAll(".ws-pages > li"));

  function regrow(root) {
    root.querySelectorAll("textarea.fld-ta").forEach(function (t) {
      t.style.height = "auto";
      t.style.height = (t.scrollHeight + 2) + "px";
    });
  }

  function show(slug, anchor) {
    if (!pages.some(function (p) { return p.dataset.page === slug; })) slug = pages[0].dataset.page;
    pages.forEach(function (p) { p.hidden = p.dataset.page !== slug; });
    var group = (items.filter(function (li) { return li.dataset.page === slug; })[0] || {}).dataset;
    group = group ? group.group : "";
    items.forEach(function (li) {
      var on = li.dataset.page === slug;
      li.classList.toggle("is-current", on);
      li.classList.toggle("in-group", li.dataset.group === group);
      var a = li.querySelector("a");
      if (!a) return;                              /* a group row */
      if (on) a.setAttribute("aria-current", "page"); else a.removeAttribute("aria-current");
    });
    regrow(document.querySelector('.ws-page[data-page="' + slug + '"]'));
    try { localStorage.setItem(TAB, slug); } catch (e) { /* storage blocked: start on page 1 next time */ }
    var target = anchor && document.getElementById(anchor);
    if (target) target.scrollIntoView(); else window.scrollTo(0, 0);
  }

  document.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest("[data-goto]");
    if (!a) return;
    e.preventDefault();
    show(a.dataset.goto, a.dataset.anchor);
  });

  document.addEventListener("DOMContentLoaded", function () {
    var bar = document.getElementById("ws-bar"), main = document.getElementById("ws-main");
    if (bar && main) main.insertBefore(bar, main.firstChild);  /* one toolbar for all four pages */
  });

  var start = null;
  try { start = localStorage.getItem(TAB); } catch (e) { /* no storage */ }
  show(start || pages[0].dataset.page);
})();
"""


# ---------------------------------------------------------------- pages

_uri_cache: dict[str, str] = {}


def data_uri(rel: str) -> str:
    if rel not in _uri_cache:
        path = DOCS / rel
        mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        # Windows answers from the registry, where .svg and .webp are often missing or wrong
        mime = {".svg": "image/svg+xml", ".webp": "image/webp"}.get(path.suffix, mime)
        _uri_cache[rel] = f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode("ascii")
    return _uri_cache[rel]


# a YouTube link alone on its own line (bare, or as a Markdown link) becomes a player; the link stays
# underneath, because the player needs internet and a page opened from a local file may refuse to play
YOUTUBE_LINE = re.compile(
    r'<p>\s*(?:<a href="[^"]*">)?\s*'
    r'(https?://(?:www\.)?(?:youtu\.be/|youtube\.com/watch\?v=|youtube\.com/shorts/)([A-Za-z0-9_-]{11})[^\s<"]*)'
    r'\s*(?:</a>)?\s*</p>'
)


def youtube_embed(m: re.Match) -> str:
    url, vid = html.unescape(m.group(1)), m.group(2)
    return (f'<div class="video"><div class="video-frame">'
            f'<iframe src="https://www.youtube-nocookie.com/embed/{vid}?rel=0" title="วิดีโอสาธิต" loading="lazy" '
            f'allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" '
            f'referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe></div>'
            f'<p class="video-link"><a href="{html.escape(url)}" target="_blank" rel="noopener">▶ เปิดวิดีโอใน YouTube</a></p></div>')


def render_page(src: str, slug: str, combined: bool, inline: bool = False) -> dict:
    text = (DOCS / src).read_text(encoding="utf-8")
    title = re.search(r"^# (.+)$", text, re.M).group(1).strip()
    text = FIELDS.MARKER.sub(FIELDS._render, text)
    md = markdown.Markdown(
        extensions=["admonition", "attr_list", "md_in_html", "tables", "sane_lists", "toc", "pymdownx.tasklist"],
        extension_configs={
            "toc": {"slugify": slugs.slugify(case="lower")},
            "pymdownx.tasklist": {"custom_checkbox": True, "clickable_checkbox": True},
        },
    )
    body = VIDEOS.walkthrough_videos(CALLOUTS.classify(HEADINGS.number_badges(STEPS.continue_steps(md.convert(text)))))

    prefix = f"{slug}--" if combined else ""
    if prefix:  # ids (headings, and paragraphs given one with attr_list) must stay unique once four pages share one document
        body = re.sub(r'(<(?:h[1-6]|p|div) id=")', r"\1" + prefix, body)
        body = body.replace('href="#', 'href="#' + prefix)

    # links to the other worksheets; anything else in docs/ is not rendered, so unwrap it
    def link(m):
        target, anchor, inner = m.group(1), m.group(2) or "", m.group(3)
        if target not in SLUGS:
            return inner
        if combined:
            a = f' data-anchor="{target}--{anchor[1:]}"' if anchor else ""
            return f'<a href="#{target}" data-goto="{target}"{a}>{inner}</a>'
        return f'<a href="{target}.html{anchor}">{inner}</a>'

    body = re.sub(r'<a href="([a-z0-9-]+)\.md(#[^"]*)?">(.*?)</a>', link, body, flags=re.S)
    body = re.sub(r'(src|href|poster)="(images/[^"]+)"',
                  lambda m: f'{m.group(1)}="{data_uri(m.group(2)) if inline else "../" + m.group(2)}"', body)
    body = body.replace("<table>", '<div class="table-wrap"><table>').replace("</table>", "</table></div>")
    body = YOUTUBE_LINE.sub(youtube_embed, body)

    sections = [(prefix + t["id"], html.escape(html.unescape(t["name"])))
                for t in _toc_tokens(md.toc_tokens)]
    return {"slug": slug, "title": title, "body": body + pager(slug, combined), "sections": sections}


SUB_ID = re.compile(r"^(?:[a-z0-9-]+--)?(?:a\d+|hist)(?:-|$)")   # sub-activity ids: a4, a4-1, hist-2 (combined: prefixed)


def _toc_tokens(tokens):
    """The page's own nav: its H2s, and on an activity page the sub-activities (H3s under the H1)."""
    out = []
    for t in tokens:
        if t["level"] == 1:
            out.extend(_toc_tokens(t["children"]))
        elif t["level"] == 2 or (t["level"] == 3 and SUB_ID.match(t["id"])):
            out.append(t)
    return out


def switcher(pages: list[dict], current: str | None, combined: bool) -> str:
    rows, group = [], None
    by_slug = {p["slug"]: p for p in pages}
    cur_group = next((g for _, s, g, *_ in NAV_PAGES if s == current), None)
    for _, slug, grp, eyebrow, name in NAV_PAGES:
        p = by_slug[slug]
        ingrp = ' in-group' if grp == cur_group else ""
        num = f' data-n="{eyebrow.split()[-1]}"' if eyebrow else ""    # "กิจกรรม 4" -> the badge shows 4
        if grp != group:
            group = grp
            first = f'<a href="#{slug}" data-goto="{slug}">' if combined else f'<a href="{slug}.html">'
            rows.append(f'<li class="ws-group{ingrp}" data-group="{grp}">{first}{grp}</a></li>')
        cur = slug == current
        label = (f'<span class="ws-g">{grp.replace("ช่วงที่", "ช่วง")}</span>'
                 + (f'<span class="ws-n">{eyebrow}</span>' if eyebrow else "")
                 + f'<span class="ws-t">{html.escape(name)}</span>')
        if combined:
            head = f'<a href="#{slug}" data-goto="{slug}"{num}>{label}</a>'
            toc = "".join(
                f'<li><a href="#{sid}" data-goto="{slug}" data-anchor="{sid}">{name}</a></li>'
                for sid, name in p["sections"]
            )
        else:
            aria = ' aria-current="page"' if cur else ""
            head = f'<a href="{slug}.html"{aria}{num}>{label}</a>'
            toc = "".join(f'<li><a href="#{sid}">{name}</a></li>' for sid, name in p["sections"]) if cur else ""
        cls = ' class="is-current in-group"' if cur else (' class="in-group"' if ingrp else "")
        rows.append(
            f'<li data-page="{slug}" data-group="{grp}"{cls}>{head}'
            + (f'<ul class="ws-toc">{toc}</ul>' if toc else "")
            + "</li>"
        )
    return f'<nav class="ws-side" aria-label="หน้าในชุดใบงาน"><ul class="ws-pages">{"".join(rows)}</ul></nav>'


COURSE = [p for p in PAGES if p[2].startswith("ช่วงที่")]   # the pages a group works through in order


def pager(slug: str, combined: bool) -> str:
    """Previous / next links along the course pages; nothing on the reference pages."""
    idx = next((i for i, p in enumerate(COURSE) if p[1] == slug), None)
    if idx is None:
        return ""
    def link(p, cls, kicker):
        _, s, grp, eyebrow, name = p
        text = f"{eyebrow} · {html.escape(name)}" if eyebrow else html.escape(name)
        href = f'href="#{s}" data-goto="{s}"' if combined else f'href="{s}.html"'
        return f'<a class="{cls}" {href}><span class="ws-pager__k">{kicker}</span><span class="ws-pager__t">{text}</span></a>'
    prev = link(COURSE[idx - 1], "ws-prev", "← ก่อนหน้า") if idx > 0 else ""
    nxt = link(COURSE[idx + 1], "ws-next", "ถัดไป →") if idx + 1 < len(COURSE) else ""
    return f'<nav class="ws-pager" aria-label="หน้าก่อนหน้าและถัดไป">{prev}{nxt}</nav>' if prev or nxt else ""


def page_shell(title: str, nav: str, main: str, scripts: str) -> str:
    css = BASE_CSS + site_css() + LATE_CSS
    return f"""<title>{html.escape(title)}</title>
<meta name="description" content="ใบงานผู้เข้าร่วม {html.escape(SITE_NAME)}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<style>
{css}
</style>
<header class="ws-top">
  <div class="ws-top__inner">
    <span class="ws-brand">{html.escape(SITE_NAME)}</span>
  </div>
</header>
<div class="ws-shell">
{nav}
<main class="md-content__inner md-typeset" id="ws-main">
{main}
<footer class="ws-disclosure">{AI_DISCLOSURE}</footer>
</main>
</div>
<dialog id="shot-box" aria-label="ภาพหน้าจอ"><img alt=""><p></p></dialog>
<script>{SAVE_SHIM_JS}</script>
<script>{extra_js()}</script>
<script>{LIGHTBOX_JS}</script>
{scripts}"""


def full_document(fragment: str) -> str:
    return ('<!DOCTYPE html>\n<html lang="th">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            "</head>\n<body>\n" + fragment + "\n</body>\n</html>\n")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--combined", metavar="PATH", help="also write all pages as one tabbed fragment (images inlined)")
    ap.add_argument("--offline", action="store_true", help="inline images as data URIs so each render opens on its own")
    args = ap.parse_args()

    OUT_DIR.mkdir(exist_ok=True)

    pages = [render_page(src, slug, combined=False, inline=args.offline) for src, slug, *_ in PAGES]
    for p in pages:
        doc = full_document(page_shell(p["title"], switcher(pages, p["slug"], False), p["body"], ""))
        out = OUT_DIR / f"{p['slug']}.html"
        out.write_text(doc, encoding="utf-8")
        print(f"wrote {out.relative_to(ROOT)}  ({out.stat().st_size / 1e6:.1f} MB)")
    for old, new in REDIRECTS.items():
        (OUT_DIR / f"{old}.html").write_text(
            f'<!DOCTYPE html>\n<html lang="th"><head><meta charset="utf-8">\n<meta http-equiv="refresh" content="0; url={new}.html">\n'
            f'<title>{html.escape(SITE_NAME)}</title></head>\n<body><p>ใบงานช่วงนี้แยกเป็นหน้าละกิจกรรมแล้ว: '
            f'<a href="{new}.html">{new}.html</a></p></body></html>\n', encoding="utf-8")

    if args.combined:
        cpages = [render_page(src, slug, combined=True, inline=True) for src, slug, *_ in NAV_PAGES]
        main_html = "\n".join(
            f'<section class="ws-page" data-page="{p["slug"]}">\n{p["body"]}\n</section>' for p in cpages
        )
        frag = page_shell(SITE_NAME, switcher(cpages, cpages[0]["slug"], True), main_html,
                          f"<script>{TABS_JS}</script>")
        out = pathlib.Path(args.combined)
        out.write_text(frag, encoding="utf-8")
        print(f"wrote {out}  ({out.stat().st_size / 1e6:.1f} MB)")


if __name__ == "__main__":
    main()
