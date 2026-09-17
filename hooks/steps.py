"""MkDocs hook: keep step numbers continuous across action-group breaks.

A procedure is written as one numbered list split by bold action-group headings.
Python-Markdown (sane_lists) emits each fragment as <ol start="N">, but
docs/stylesheets/extra.css draws the number badge from a CSS counter, which
ignores start= and would show 1, 2, 3 again after every break. This hook runs on
the rendered HTML (on_page_content) and seeds the counter inline:

    <ol start="6">  ->  <ol start="6" style="counter-reset: step 5">

scripts/render-worksheets.py applies the same function to the standalone renders.
Registered in mkdocs.yml under `hooks:`. No dependencies beyond MkDocs itself.
"""
import re

OL_START = re.compile(r'<ol start="(\d+)">')


def continue_steps(html):
    return OL_START.sub(lambda m: f'<ol start="{m.group(1)}" style="counter-reset: step {int(m.group(1)) - 1}">', html)


def on_page_content(html, page, config, files):
    return continue_steps(html)
