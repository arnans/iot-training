"""MkDocs hook: an image whose source is an .mp4 becomes a looping walkthrough video.

The Markdown keeps plain image syntax, so alt text, width and path handling stay the same
as for pictures:

    ![ขั้นตอนสร้างกฎ ...](images/walkthroughs/a5-1-low-water.mp4){ width="85%" }

MkDocs has already rewritten the src to the right relative path by on_page_content, so the
poster (the clip's title card, <name>.png next to the .mp4) is derived from it. The video is
muted and loops; it has controls for pause and scrubbing, and loads nothing until
extra.js starts it when it scrolls into view (preload="none").
scripts/render-worksheets.py applies the same function to the standalone renders.
Registered in mkdocs.yml under `hooks:`. No dependencies beyond MkDocs itself.
"""
import html as _html
import re

MP4_IMG = re.compile(r'<img\b([^>]*?)\bsrc="([^"]+\.mp4)"([^>]*)>')


def _attr(attrs, name):
    m = re.search(r'\b' + name + r'="([^"]*)"', attrs)
    return m.group(1) if m else ""


def walkthrough_videos(page_html):
    def repl(m):
        attrs, src = m.group(1) + m.group(3), m.group(2)
        alt, width = _attr(attrs, "alt"), _attr(attrs, "width")
        poster = "" if src.startswith("data:") else f' poster="{src[:-4]}.png"'
        style = f' style="width:{width}"' if width else ""
        return (f'<video class="walkthrough" src="{src}"{poster} aria-label="{alt}"{style} '
                f'controls muted loop playsinline preload="none">{_html.escape(_html.unescape(alt))}</video>')
    return MP4_IMG.sub(repl, page_html)


def on_page_content(html, page, config, files):
    return walkthrough_videos(html)
