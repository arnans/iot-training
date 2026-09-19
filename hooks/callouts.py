"""MkDocs hook: give callouts and phase labels a class the stylesheet can colour.

Runs on the rendered HTML (on_page_content):

  - a blockquote whose first words are bold "ระวัง" or "ห้าม" is a caution
        <blockquote>\n<p><strong>ระวัง</strong> ...   ->  <blockquote class="ws-caution">
    every other blockquote is an explanation (styled sky blue by extra.css; the record-note
    panels are made by docs/javascripts/extra.js at load time)
  - a paragraph that is one bold phrase and nothing else is an action-group label, the phase
    of a procedure ("จำลองปัญหา", "บันทึกผล"); a duration ("40 นาที") is not, and neither is
    the page's subtitle under the H1 -- only paragraphs after the first H2/H3 are labels
        <p><strong>สังเกตผล</strong></p>  ->  <p class="ws-phase"><strong>สังเกตผล</strong></p>

scripts/render-worksheets.py applies the same function to the standalone renders.
Registered in mkdocs.yml under `hooks:`. No dependencies beyond MkDocs itself.
"""
import re

CAUTION = re.compile(r"<blockquote>(\s*<p><strong>(?:ระวัง|ห้าม)\b)")
PHASE = re.compile(r"<p><strong>(?!\d+ นาที)([^<]+)</strong></p>")
FIRST_SECTION = re.compile(r"<h[23][\s>]")


def classify(html):
    html = CAUTION.sub(r'<blockquote class="ws-caution">\1', html)
    m = FIRST_SECTION.search(html)
    if not m:
        return html
    head, body = html[:m.start()], html[m.start():]
    return head + PHASE.sub(r'<p class="ws-phase"><strong>\1</strong></p>', body)


def on_page_content(html, page, config, files):
    return classify(html)
