"""MkDocs hook: expand worksheet field markers into form controls.

Runs on the raw Markdown of every page (on_page_markdown), before Python-Markdown
parses it, so a marker works anywhere: in a table cell, a blockquote, a list item.

    {{f:key}}   {{f:key|size}}     one-line text box; size = width in characters (default 10)
    {{n:key}}   {{n:key|size}}     same, but phones show the number keypad (default 6)
    {{ta:key}}  {{ta:key|rows}}    multi-line box (default 2 rows; grows while typing)
    {{r:key|A|B|C}}                radio buttons, one per option, labels as written

`key` is the answer's permanent id ("s2.hum.on"). The same key on two pages is one
answer shown twice; docs/javascripts/extra.js keeps them in sync and stores every
answer in localStorage. Design notes and the key conventions: webapp/FILLABLE-WORKSHEET.md.

Registered in mkdocs.yml under `hooks:`. No dependencies beyond MkDocs itself.
"""
import html
import re

MARKER = re.compile(r"\{\{(f|n|ta|r):([A-Za-z0-9_.\-]+)((?:\|[^|}]*)*)\}\}")


def _render(m):
    kind, key, tail = m.group(1), m.group(2), m.group(3)
    args = tail.split("|")[1:] if tail else []
    if kind in ("f", "n"):
        size = args[0] if args and args[0].isdigit() else ("6" if kind == "n" else "10")
        mode = ' inputmode="decimal"' if kind == "n" else ""
        return (
            f'<input class="fld" type="text" data-k="{key}" data-size="{size}" '
            f'size="{size}"{mode} autocomplete="off" spellcheck="false">'
        )
    if kind == "ta":
        rows = args[0] if args and args[0].isdigit() else "2"
        return f'<textarea class="fld fld-ta" data-k="{key}" rows="{rows}"></textarea>'
    if kind == "r":
        opts = "".join(
            f'<label><input class="fld" type="radio" name="{key}" data-k="{key}" '
            f'value="{html.escape(o, quote=True)}"> {html.escape(o)}</label>'
            for o in args
            if o.strip()
        )
        return f'<span class="fld-radio" data-k="{key}">{opts}</span>'
    return m.group(0)


def on_page_markdown(markdown, page, config, files):
    return MARKER.sub(_render, markdown)
