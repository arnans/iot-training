#!/usr/bin/env python3
"""Render the participant worksheets into self-contained HTML, for dry runs off the site.

The Markdown in docs/ stays the single source of truth. This script reuses the site's
own pieces, so a render behaves like the live worksheet:

  - hooks/fields.py expands the {{f:...}} markers into the same form fields
  - docs/stylesheets/extra.css supplies the design (its light/dark blocks are
    re-keyed from Material's colour-scheme attribute to prefers-color-scheme)
  - docs/javascripts/extra.js saves answers to localStorage and adds the toolbar

Every image is inlined as a data URI, so each file opens on its own: attach it to a
message, open it from a USB stick, or publish it. Links to pages that are not
rendered (index, record sheet, reference) become plain text.

    python scripts/render-worksheets.py                    # docs/renders/<page>.html
    python scripts/render-worksheets.py --combined out.html # also one page with all four as tabs

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
import datetime as _dt
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

# (source, slug, switcher eyebrow, switcher label) -- the label is the session title cut
# to what fits a chip on a phone; keep it in step with the page's own # heading
PAGES = [
    ("install.md", "install", "ก่อนการอบรม", "เตรียมแล็ปท็อป"),
    ("session-1.md", "session-1", "ช่วงที่ 1", "รับรู้ ตัดสินใจ สั่งการ"),
    ("session-2.md", "session-2", "ช่วงที่ 2", "ควบคุมอัตโนมัติและ Fail-safe"),
    ("session-3.md", "session-3", "ช่วงที่ 3", "แดชบอร์ดและออกแบบระบบ"),
    ("resources.md", "resources", "อ้างอิง", "รวมไฟล์และลิงก์"),
    ("reference.md", "reference", "อ้างอิง", "เมนูและวิธีแก้ปัญหา"),
    ("record-sheet.md", "record-sheet", "อ้างอิง", "ใบบันทึกของกลุ่ม"),
]
SLUGS = {p[1] for p in PAGES}

SITE_NAME = "IoT ในฟาร์มอัจฉริยะ"
FONTS = ("https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;500;600;700"
         "&family=IBM+Plex+Mono:wght@400;600&display=swap")


def _load_fields_hook():
    spec = importlib.util.spec_from_file_location("fields_hook", ROOT / "hooks" / "fields.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


FIELDS = _load_fields_hook()


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
.ws-draft {
  font-size: 0.76rem;
  padding: 0.1rem 0.75rem;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.16);
  border: 1px solid rgba(255, 255, 255, 0.28);
}

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
.ws-n::after { content: " · "; }
.ws-pages > li.is-current .ws-n { opacity: 0.85; }
.ws-toc { display: none; }
.ws-side a:focus-visible, .ws-top a:focus-visible { outline: 2px solid var(--ag-marigold); outline-offset: 2px; }

@media (min-width: 64rem) {
  .ws-shell { grid-template-columns: 15rem minmax(0, 47rem); }
  .ws-side {
    position: sticky;
    top: 0;
    align-self: start;
    max-height: 100vh;
    overflow-y: auto;
    padding-block: 2rem;
  }
  .ws-pages { display: block; }
  .ws-pages > li { margin-bottom: 0.3rem; }
  .ws-pages > li > a {
    display: block;
    border: 0;
    border-radius: 0.5rem;
    padding: 0.35rem 0.7rem;
    font-weight: 600;
  }
  .ws-pages > li.is-current > a { background: var(--ag-panel); color: var(--md-typeset-a-color); }
  /* sidebar: session number as a small eyebrow over the session's name */
  .ws-n {
    display: block;
    font-size: 0.72rem;
    font-weight: 500;
    letter-spacing: 0.03em;
    color: var(--md-default-fg-color--lighter);
  }
  .ws-n::after { content: none; }
  .ws-pages > li.is-current .ws-n { color: var(--ag-marigold-deep); opacity: 1; }
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
  .ws-top, .ws-side, #shot-box { display: none !important; }
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
    items.forEach(function (li) {
      var on = li.dataset.page === slug;
      li.classList.toggle("is-current", on);
      var a = li.querySelector("a");
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
        if path.suffix == ".svg":
            mime = "image/svg+xml"
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


def render_page(src: str, slug: str, combined: bool) -> dict:
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
    body = md.convert(text)

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
    body = re.sub(r'(src|href)="(images/[^"]+)"', lambda m: f'{m.group(1)}="{data_uri(m.group(2))}"', body)
    body = body.replace("<table>", '<div class="table-wrap"><table>').replace("</table>", "</table></div>")
    body = YOUTUBE_LINE.sub(youtube_embed, body)

    sections = [(prefix + t["id"], html.escape(html.unescape(t["name"])))
                for t in _h2_tokens(md.toc_tokens)]
    return {"slug": slug, "title": title, "body": body, "sections": sections}


def _h2_tokens(tokens):
    out = []
    for t in tokens:
        if t["level"] == 2:
            out.append(t)
        elif t["level"] < 2:
            out.extend(_h2_tokens(t["children"]))
    return out


def switcher(pages: list[dict], current: str | None, combined: bool) -> str:
    rows = []
    for (_, slug, eyebrow, name), p in zip(PAGES, pages):
        cur = slug == current
        label = f'<span class="ws-n">{eyebrow}</span><span class="ws-t">{html.escape(name)}</span>'
        if combined:
            head = f'<a href="#{slug}" data-goto="{slug}">{label}</a>'
            toc = "".join(
                f'<li><a href="#{sid}" data-goto="{slug}" data-anchor="{sid}">{name}</a></li>'
                for sid, name in p["sections"]
            )
        else:
            aria = ' aria-current="page"' if cur else ""
            head = f'<a href="{slug}.html"{aria}>{label}</a>'
            toc = "".join(f'<li><a href="#{sid}">{name}</a></li>' for sid, name in p["sections"]) if cur else ""
        cls = ' class="is-current"' if cur else ""
        rows.append(
            f'<li data-page="{slug}"{cls}>{head}'
            + (f'<ul class="ws-toc">{toc}</ul>' if toc else "")
            + "</li>"
        )
    return f'<nav class="ws-side" aria-label="หน้าในชุดใบงาน"><ul class="ws-pages">{"".join(rows)}</ul></nav>'


def page_shell(title: str, nav: str, main: str, scripts: str, stamp: str) -> str:
    css = BASE_CSS + site_css() + LATE_CSS
    return f"""<title>{html.escape(title)}</title>
<meta name="description" content="ใบงานผู้เข้าร่วม {html.escape(SITE_NAME)} (ฉบับร่างสำหรับทดลองใช้)">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<style>
{css}
</style>
<header class="ws-top">
  <div class="ws-top__inner">
    <span class="ws-brand">{html.escape(SITE_NAME)}</span>
    <span class="ws-draft">ฉบับร่างสำหรับทดลองใช้ · {stamp}</span>
  </div>
</header>
<div class="ws-shell">
{nav}
<main class="md-content__inner md-typeset" id="ws-main">
{main}
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
    ap.add_argument("--combined", metavar="PATH", help="also write all four pages as one tabbed fragment")
    args = ap.parse_args()

    stamp = _dt.date.today().isoformat()
    OUT_DIR.mkdir(exist_ok=True)

    pages = [render_page(src, slug, combined=False) for src, slug, *_ in PAGES]
    for p in pages:
        doc = full_document(page_shell(p["title"], switcher(pages, p["slug"], False), p["body"], "", stamp))
        out = OUT_DIR / f"{p['slug']}.html"
        out.write_text(doc, encoding="utf-8")
        print(f"wrote {out.relative_to(ROOT)}  ({out.stat().st_size / 1e6:.1f} MB)")

    if args.combined:
        cpages = [render_page(src, slug, combined=True) for src, slug, *_ in PAGES]
        main_html = "\n".join(
            f'<section class="ws-page" data-page="{p["slug"]}">\n{p["body"]}\n</section>' for p in cpages
        )
        frag = page_shell(SITE_NAME, switcher(cpages, cpages[0]["slug"], True), main_html,
                          f"<script>{TABS_JS}</script>", stamp)
        out = pathlib.Path(args.combined)
        out.write_text(frag, encoding="utf-8")
        print(f"wrote {out}  ({out.stat().st_size / 1e6:.1f} MB)")


if __name__ == "__main__":
    main()
