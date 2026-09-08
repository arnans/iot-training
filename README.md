# IoT Training — Smart Farming

Materials for the three hands-on sessions "IoT Systems in Smart Farming".

First delivered inside the CMU Lifelong Education program *นวัตกรเกษตรอัจฉริยะ AIoT สำหรับเกษตรแม่นยำ*
รุ่นที่ 1, 25–26 September 2026, Chiang Mai. The worksheets in `docs/` are written to be reusable
across deliveries: no dates, venue names, or weekday references. `COURSE-DESIGN.md` remains
specific to that first delivery.

## Contents

| Path | What it is |
|---|---|
| [SESSION-OVERVIEW.md](SESSION-OVERVIEW.md) | One-page summary of the three sessions: what teams do, objective, learning-goal alignment |
| [COURSE-DESIGN.md](COURSE-DESIGN.md) | Full course design: session plans, goals, kit list, risks, production tasks |
| [PART1-RECORDING-PREP.md](PART1-RECORDING-PREP.md) | Readiness notes for the optional narrated online decks |
| [WORKSHEET-TODO.md](WORKSHEET-TODO.md) | Open items and assumptions in the worksheets |
| [NETWORK-REQUIREMENTS.md](NETWORK-REQUIREMENTS.md) | Wireless network spec for the venue's network provider. Thai edition: [NETWORK-REQUIREMENTS-th.md](NETWORK-REQUIREMENTS-th.md). Both render to standalone HTML in `docs/` — see below |
| `scripts/` | [render-network-doc.py](scripts/render-network-doc.py) turns the two network Markdown files into print-ready HTML |
| [TEST-PLAN.md](TEST-PLAN.md) | Bench test for the ESPHome provisioning flow, before committing the firmware image |
| `firmware/` | The two workshop ESPHome images (sensor node, relay board) |
| `hass/` | Home Assistant configuration for the team VM image (plus a now-unused instructor-server config) |
| `docs/` | **Participant worksheets** — the website source (Thai), plus the two generated network-spec pages |

## Participant worksheet site

Short in-room worksheets, not a full workbook. Delivered as a website participants open on
a phone or laptop during the workshop. The only printed artifact is `docs/record-sheet.md`.

Sessions refer to each other as ช่วงที่ 1/2/3, never as days or times, so the same pages work
whether the three sessions run over two days or some other shape. The one scheduling dependency
is the gap between sessions 1 and 2 — see `WORKSHEET-TODO.md`.

```
docs/
├── index.md          เริ่มต้นที่นี่ — kit, roles, safety, vocabulary
├── session-1.md      Input → Logic → Output: sensors to pump
├── session-2.md      Automation logic and fail-safe design
├── session-3.md      Networking, dashboards, and the design challenge
├── record-sheet.md   Printed team record sheet + design canvas
├── reference.md      Home Assistant menu paths and troubleshooting
├── network-requirements.html      generated — Thai network spec
├── network-requirements-en.html   generated — English network spec
└── images/
    └── network-*.svg              generated — the two spec diagrams, per language
```

### Build and preview

```bash
pip install -r requirements.txt
python scripts/render-network-doc.py   # regenerate the two network-spec pages
mkdocs serve                           # preview at http://127.0.0.1:8000
mkdocs build                           # static site into site/
```

Deployment config for Netlify is in `netlify.toml`, which runs the render step before the
build so the published spec always matches its Markdown. `site/` is generated and not tracked.

### The network spec pages

The two `network-requirements*.html` files in `docs/` are **generated, not edited**. The
Markdown at the repo root is the source; `scripts/render-network-doc.py` wraps it in a
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
