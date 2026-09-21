# IoT Training — Smart Farming

Materials for the four hands-on sessions "IoT Systems in Smart Farming".

First delivered inside the CMU Lifelong Education program *นวัตกรเกษตรอัจฉริยะ AIoT สำหรับเกษตรแม่นยำ*
รุ่นที่ 1, 25–26 September 2026, Chiang Mai. The worksheets in `docs/` are written to be reusable
across deliveries: no dates, venue names, or weekday references. `planning/COURSE-DESIGN.md` remains
specific to that first delivery.

## Contents

| Path | What it is |
|---|---|
| [docs/](docs/) | **Participant worksheets**, the website source (Thai), served as-is by GitHub Pages. Also holds the generated network-spec and instructor pages, the built firmware images and the standalone `renders/` |
| [planning/](planning/) | Course design and running. [COURSE-DESIGN.md](planning/COURSE-DESIGN.md) full design: session plans, goals, kit list, risks, production tasks. [SESSION-OVERVIEW.md](planning/SESSION-OVERVIEW.md) one-page summary per session. [INSTRUCTOR-RESOURCES.md](planning/INSTRUCTOR-RESOURCES.md) links page and run sheet for instructors and TAs, rendered to `docs/instructor-resources.html`. [TEST-PLAN.md](planning/TEST-PLAN.md) bench tests for firmware and kit. [WORKSHEET-TODO.md](planning/WORKSHEET-TODO.md) open items, assumptions and the dated decision log. [PART1-RECORDING-PREP.md](planning/PART1-RECORDING-PREP.md) readiness notes for the optional narrated decks |
| [network/](network/) | [NETWORK-SETUP.md](network/NETWORK-SETUP.md) the workshop network: three GL.iNet Flint routers we configure ourselves (one per zone) plus NT's internet WiFi and wired ports, with the ask for NT, the router checklist, participant rules and the acceptance test. [NETWORK-REQUIREMENTS.md](network/NETWORK-REQUIREMENTS.md) and its Thai edition [NETWORK-REQUIREMENTS-th.md](network/NETWORK-REQUIREMENTS-th.md) are the **deprecated** per-SSID VLAN spec, kept for reference. All render to standalone HTML in `docs/`, see below |
| [webapp/](webapp/) | The web app layered on the worksheet site. [FILLABLE-WORKSHEET.md](webapp/FILLABLE-WORKSHEET.md) design of the fillable fields, localStorage and JSON export. [PROGRESS-DASHBOARD.md](webapp/PROGRESS-DASHBOARD.md) the instructor's live progress board on Firebase. `database.rules.json` the Firebase rules to paste |
| [firmware/](firmware/) | The workshop ESPHome sources (sensor node, its Session 4 ESP-NOW variant, relay board, Session 4's ESP-NOW receiver), built per zone colour |
| [hass/](hass/) | Home Assistant configuration for the team VM image (plus a now-unused instructor-server config) and the OVA recipe |
| [hooks/](hooks/) | `fields.py`, the MkDocs hook that expands `{{f:key}}` markers into form fields |
| [scripts/](scripts/) | [render-worksheets.py](scripts/render-worksheets.py) renders the participant pages into self-contained HTML in `docs/renders/`. [render-network-doc.py](scripts/render-network-doc.py) renders the network specs and the instructor page into `docs/`. `power_figures.py` draws the two Activity 7.4 figures into `docs/images/`; `collect_answers.py` merges team JSON files to CSV; `video_steps.py` cuts screen recordings into step stills; `test_worksheet_fields.cjs` and `test_progress.js` are the checks |
| [reviews/](reviews/) | Dated review and handoff notes exchanged with AI assistants; what was acted on is summarised in `planning/WORKSHEET-TODO.md` |
| [archive/](archive/) | Worksheet content taken out but kept for restoring, each file with its own restore steps. Not published |

GitHub Pages serves `docs/` from `main`; re-run the two render scripts and commit after editing a
worksheet, a network spec or the instructor page.

## Participant worksheet site

Short in-room worksheets, not a full workbook. Delivered as a website participants open on
a phone or laptop during the workshop. The only printed artifact is `docs/record-sheet.md`.

Sessions refer to each other as ช่วงที่ 1/2/3/4, never as days or times, so the same pages work
whether the four sessions run over two days or some other shape. The one scheduling dependency
is the gap between sessions 1 and 2 — see `planning/WORKSHEET-TODO.md`.

```
docs/
├── index.html        the published site's front door — hand-written, links everything below
├── .nojekyll         serve docs/ as static files; without it Jekyll collides index.html with index.md
├── index.md          เริ่มต้นที่นี่ — kit, roles, safety, vocabulary (MkDocs preview only)
├── session-1-start.md   team number, zone, Home Assistant address
├── activity-1..11.md one worksheet page per activity, grouped by session in the nav (9–11 are Session 4, ESP-NOW)
├── session-1/2/3.md, session-3-history.md  stubs that forward the old URLs to the pages above
├── record-sheet.md   Printed team record sheet
├── reference.md      Home Assistant menu paths and troubleshooting
├── resources.md      every download and link participants need, in one place
├── network-requirements.html      generated — Thai network spec
├── network-requirements-en.html   generated — English network spec
├── instructor-resources.html      generated — planning/INSTRUCTOR-RESOURCES.md as a standalone page
├── firmware/                      the twelve built ESP32 images, served for flashing (Session 4 teams flash two of them themselves)
├── renders/                       generated — every participant page as standalone HTML
└── images/
    ├── network-*.svg              generated — the two spec diagrams, per language
    └── power-*.svg                generated — the two Activity 7.4 figures (scripts/power_figures.py)
```

### Build and preview

```bash
pip install -r requirements.txt
python scripts/render-network-doc.py   # regenerate the two network-spec pages
python scripts/render-worksheets.py    # regenerate docs/renders/ (standalone worksheets)
mkdocs serve                           # preview at http://127.0.0.1:8000
mkdocs build                           # static site into site/
```

Published by **GitHub Pages** from `docs/` on `main`, at https://arnans.github.io/iot-training/.
Pages serves the committed files as they are and does not run MkDocs: the generated HTML
(network spec, `renders/`) must be regenerated and committed after editing its Markdown, and
the `.md` pages at that address are GitHub's plain rendering, without the worksheet theme or
fields. `site/` is generated and not tracked.

### The network spec pages

The two `network-requirements*.html` files in `docs/` are **generated, not edited**. The
Markdown in `network/` is the source; `scripts/render-network-doc.py` wraps it in a
standalone print-ready page and writes it into `docs/`. It also draws the two diagrams
(`scripts/network_figures.py`) as SVG, one pair per language, and inlines them so the page
stays self-contained; the Markdown keeps a plain image link so the diagrams also show on
GitHub. MkDocs copies non-Markdown files
through untouched, so these publish at `/network-requirements.html` and
`/network-requirements-en.html` without the worksheet theme — a plain document to send to the
network provider, and a clean A4 print. Edit the Markdown, re-run the script, commit both.

### Conventions

Web-rendered Markdown (see KSM `knowledge/md-for-web-rendering.md`): Markdown image syntax
with an `attr_list` width — `![alt](images/x.png){ width="60%" }` — because MkDocs serves each
page at a directory URL and rewrites only Markdown image paths, so a raw `<img src>` 404s on
every page but the root. Blockquote callouts, relative cross-links, no page-break markers.
`record-sheet.md` is the one exception — it is print-bound and uses dotted fill-in lines.
A YouTube link alone on its own line becomes an embedded player in `docs/renders/` (the Markdown keeps
the plain link).
