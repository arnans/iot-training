# Fillable worksheet — design notes

The three session pages and the record sheet are forms. Teams type observations and answers
straight into the worksheet; the browser remembers them; a JSON download is the team's copy
and the instructor's submission. No server, nothing beyond GitHub Pages. Decided 8 Sep 2026,
replacing the one-per-team printed record sheet (which survives as the blank fallback).

## Decisions

| Question | Decision | Why |
|---|---|---|
| Where do answers live during the workshop? | `localStorage`, one JSON blob per browser origin | Zero infrastructure; survives reloads, tab closes, and both days as long as the same browser on the same device is used. Strictly *site data*, not cache: "clear cache" leaves it alone, "clear site data" and incognito do not. |
| Durable copy | **ดาวน์โหลดคำตอบ** → `farm-team-<n>-<zone>.json`, and **พิมพ์ / บันทึก PDF** of the record sheet | localStorage cannot be promised past the workshop (Safari evicts after 7 idle days, shared laptops get wiped). The file is also what teams send the instructor, so there is no submission endpoint to run. |
| Moving between devices | **นำเข้าจากไฟล์** merges a downloaded file into the current browser | The Recorder may type on a phone while the Driver holds the laptop; export on one, import on the other. Merge fills blanks and asks once before overwriting values that differ. |
| Save timing | Every `input` event, debounced 300 ms; radios and checkboxes on `change` | Saving on blur loses the field being typed when the phone locks or the tab closes. |
| Identity | Team number and zone only, no member names | Roger, 8 Sep 2026. Team number also names the export file. |
| Where fields appear | Inline in the session pages at the moment of measurement, **again** in the activity's task list at the top, **and** collected on the record sheet, all sharing the same keys | Inline is where the team is when the number appears; the task list is what the team works from; the record sheet is the compact printable summary and the paper fallback. One key, three places, one value. |
| Activity task list | `### สิ่งที่กลุ่มต้องทำและตอบ { #a5 }` then `<div class="ws-tasks" markdown>` holding one `- [ ]` item per sub-section: a bold link to the sub-section (`#a5-3`), the question with its fields, and for step-only items the tick criterion. Each sub-section ends with `[↑ กลับไปที่รายการ](#a5){ .ws-back }` | Roger, 13 Sep 2026, after the TA workshop: teams listened to the instructor instead of reading the prose. A list of what to do and answer, with the steps one tap away, works alongside the talk. Step-only sub-sections are listed too, so jumping between questions cannot skip a rule-state change. Piloted on Session 2 Activity 5, then applied to Activities 1–4, 6–8 and Session 3's graph-reading block. Wide tables become one sub-bullet per row inside the item. Ids: `a<n>` for the list, `a<n>-<sub>` for headings, `a<n>-q` for the end question (a paragraph id via `{: #… }`); the graph-reading block uses `hist`. |
| Authoring | Short `{{f:key}}` markers in Markdown, expanded by a build hook | Raw `<input>` HTML in Thai prose is unreadable and fragile in table cells. The marker survives the Pandoc path as visible text and never contains a `|` after expansion, so Markdown tables stay intact. |
| Checklists | The `- [ ]` task lists are clickable and remembered per page | Free progress tracking; `pymdownx.tasklist: clickable_checkbox: true`. |

## Moving parts

```
docs/*.md          {{f:key}} markers in prose, tables, blockquotes, list items
hooks/fields.py    MkDocs hook (on_page_markdown) → <input class="fld" data-k="key">,
                   <textarea class="fld fld-ta">, <span class="fld-radio"><label><input type=radio>…
docs/javascripts/extra.js
                   restore on load · save on input · sync same-key boxes on one page ·
                   grow boxes to content · toolbar (#ws-bar) · export / import / print / clear ·
                   task-list checkbox memory · cross-tab refresh via the `storage` event ·
                   team-number validation · progress counts sent to the instructor's board
                   (PROGRESS-DASHBOARD.md)
docs/stylesheets/extra.css
                   field look (marigold underline on the record-panel tint), toolbar, @media print
scripts/collect_answers.py
                   instructor side: folder of team JSON files → one CSV row per team
```

### Marker syntax

| Marker | Renders | Notes |
|---|---|---|
| `{{f:key}}` `{{f:key|16}}` | one-line text box | number = width in characters (default 10); grows if the answer is longer |
| `{{n:key}}` `{{n:key|4}}` | one-line box with `inputmode="decimal"` | phones open the number keypad; still accepts any text (units, "Wet") |
| `{{ta:key}}` `{{ta:key|3}}` | multi-line box, full width | number = starting rows (default 2); grows while typing, no scrollbar |
| `{{r:key|A|B|C}}` | radio buttons | labels as written; the stored value is the label text |

Markers are replaced before Python-Markdown runs, so the pipes in `{{r:…|A|B}}` do not break a
table row. Anything that is not a recognised marker is left alone.

### Key naming

`<scope>.<topic>.<detail>`, ASCII, dots as separators, stable forever. Renaming a key orphans
every team's saved answer for it, so add new keys rather than rename.

| Prefix | Scope |
|---|---|
| `team.no` `team.zone` `team.wifi` | team identity (`team.zone` is the Thai label: แดง / เขียว / น้ำเงิน) |
| `ha.ip1` `ha.ip2` `board.iot.*` `board.relay.*` `farm.problem` | addresses and the one-sentence farm problem, filled at the start of Session 1 |
| `s1.*` `s2.*` `s3.*` | session observations and end-of-activity answers (`s1.q1` … `s3.q7` are the textareas) |
| `s2.sab.<round>.*` `s2.maint.<item>.*` `s3.comm.<tech>.*` `s3.dash.<row>.*` | table cells, row then column |
| `d.*` | the design canvas at the end of the record sheet |

The record sheet is the canonical list: `grep -o '{{[^}]*}}' docs/record-sheet.md`. Every key
used in a session page must also appear on the record sheet with the same kind and options;
the only record-sheet-only keys are `team.wifi` and the design canvas (`d.*`). After editing,
a quick check is to extract the markers from all four files and diff the key sets.

### Storage format (`localStorage["farm-worksheet.v1"]`)

```json
{
  "v": 1,
  "updated": "2026-09-08T07:12:40.000Z",
  "fields": { "team.no": "17", "team.zone": "แดง", "s1.hum.room": "61", "s1.q1": "…" },
  "checks": { "/session-1/#3": true }
}
```

- `fields` — key → string. Radios store the chosen label. Empty strings are written as typed.
- `checks` — `"<pathname>#<index>": true` for ticked task-list boxes, index in page order. Editing a checklist shifts indexes; that is accepted for progress ticks.
- `dev`, `prog`, `last` — the progress tracker's device id, per-page activity counts, and last tick (PROGRESS-DASHBOARD.md). Not part of the export file.
- Bump the storage suffix (`v1` → `v2` in `extra.js`) only if the shape changes incompatibly; old data is then ignored, not migrated.

### Export file

Same as the storage blob plus `kind: "iot-farm-worksheet"`, `team`, `zone`, `exported`. Filename
`farm-team-<team.no>-<red|green|blue>.json`; the zone suffix is dropped if no zone is chosen. If
`team.no` is empty the export button prompts for it and saves it before downloading.

### Import merge rule

1. A file without a `fields` object is rejected with a message.
2. For each non-empty value in the file: if the local box is empty, take it; if the local
   value differs, count it as a conflict.
3. One `confirm()` for all conflicts: OK = file wins, Cancel = local wins.
4. `checks` are OR-merged (a tick anywhere stays a tick).
5. Save, refill the page, report counts.

### Same key in two places

Two boxes with the same `data-k` on one page (record sheet header and canvas both show
`team.no`) are kept in sync on every keystroke. Across tabs, a `storage` event refreshes the
other tab. Across devices, only export/import.

### Print

`@media print` hides the toolbar, screenshot chips, and hover panel; boxes print as
underlines with their content; textareas keep their grown height so nothing is clipped;
blockquotes, tables and textareas avoid page breaks inside. Material's own print styles hide
navigation. Printing a session page prints the whole worksheet with screenshots; the record
sheet is the compact form and is what teams should print. A blank record sheet printed before
the workshop is the paper fallback.

## Instructor pipeline

1. Teams send `farm-team-*.json` (LINE, email, USB) into one folder.
2. `python scripts/collect_answers.py answers/ -o answers.csv` → one row per team, one column
   per key, sorted so `s1.*`, `s2.*`, `s3.*`, `d.*` group together. UTF-8 with BOM for Excel.
3. Duplicate team numbers are reported on stderr; the last file wins nothing, both rows stay.

## Device workflow to tell teams

- The laptop is busy with Home Assistant; the Recorder can type on a phone, the answers then
  live in that phone's browser. Before the end of each day: download on the phone, import on the
  laptop (or the other way round), so one device holds everything.
- Do not use a private/incognito window for the worksheet.
- The bar under the page title holds the team number, a dot that turns green once the
  instructor's board has heard from this browser, the **⋯ เครื่องมือ** menu (download, import,
  print, clear), and the message composer (PROGRESS-DASHBOARD.md). Saving is silent; the JSON
  download is the proof.

## Known limits

- One team per browser profile. A second team on the same laptop must **ล้างคำตอบทั้งหมด** first
  (the button asks for confirmation and suggests downloading first).
- No history or undo beyond the browser's own field undo. The export file is the backup.
- Team number is validated in the browser only: an integer 1–100 (`TEAM_MAX` in extra.js), typed
  in Thai or ASCII digits, stored as plain digits without leading zeros. A box holding anything
  else gets a red underline and the toolbar says why; export and the progress tracker refuse it.
  The toolbar carries a `team.no` box so the number can be typed on any page.
- The table cells with many boxes (comparison, maintenance, design canvas) scroll horizontally
  on phones like any wide table in Material.
- `size` is in characters; Thai glyphs are narrower than the browser's estimate, so boxes look
  roomy. They grow to fit anyway.

## Adding or changing a field

1. Put the marker in the session page where the team is when the value appears, inside the
   `> **บันทึกผล** …` callout if there is one (extra.js gives those the marigold record panel).
2. Put the same marker with the same key and options on `docs/record-sheet.md`.
3. `mkdocs build --strict`; open the page, type, reload, check it comes back; check the record
   sheet shows it.
4. Never reuse or rename an existing key.
