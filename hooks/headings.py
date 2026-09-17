"""MkDocs hook: sub-activity headings get their number as a badge.

A sub-activity is an H3 whose text starts with its number, "### 4.4 เพิ่ม Trigger ...".
extra.css draws that number as a small badge so the heading reads as a section start;
this hook (on_page_content, the rendered HTML) wraps it:

    <h3 id="a4-3b">4.4 เพิ่ม ...  ->  <h3 id="a4-3b"><span class="sub-num">4.4</span>เพิ่ม ...

The nav is built from the Markdown before this runs, so its entries keep the plain text.
scripts/render-worksheets.py applies the same function to the standalone renders.
Registered in mkdocs.yml under `hooks:`. No dependencies beyond MkDocs itself.
"""
import re

SUB_HEADING = re.compile(r'(<h3 id="[^"]*">)(\d+\.\d+)\s+')


def number_badges(html):
    return SUB_HEADING.sub(r'\1<span class="sub-num">\2</span>', html)


def on_page_content(html, page, config, files):
    return number_badges(html)
