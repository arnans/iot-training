# IoT Training — Smart Farming

Materials for the three hands-on sessions "IoT Systems in Smart Farming".

First delivered inside the CMU Lifelong Education program *นวัตกรเกษตรอัจฉริยะ AIoT สำหรับเกษตรแม่นยำ*
รุ่นที่ 1, 25–26 September 2026, Chiang Mai. The worksheets in `docs/` are written to be reusable
across deliveries: no dates, venue names, or weekday references. `COURSE-DESIGN.md` remains
specific to that first delivery.

## Contents

| Path | What it is |
|---|---|
| [COURSE-DESIGN.md](COURSE-DESIGN.md) | Full course design: session plans, goals, kit list, risks, production tasks |
| [PART1-RECORDING-PREP.md](PART1-RECORDING-PREP.md) | Readiness notes for the optional narrated online decks |
| [WORKSHEET-TODO.md](WORKSHEET-TODO.md) | Open items and assumptions in the worksheets |
| [NETWORK-REQUIREMENTS.md](NETWORK-REQUIREMENTS.md) | Wireless network spec to hand to the venue's network provider |
| `docs/` | **Participant worksheets** — the website source (Thai) |

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
└── images/
```

### Build and preview

```bash
pip install -r requirements.txt
mkdocs serve      # preview at http://127.0.0.1:8000
mkdocs build      # static site into site/
```

Deployment config for Netlify is in `netlify.toml`. `site/` is generated and not tracked.

### Conventions

Web-rendered Markdown (see KSM `knowledge/md-for-web-rendering.md`): `<img>` tags with
percentage widths, blockquote callouts, relative cross-links, no page-break markers.
`record-sheet.md` is the one exception — it is print-bound and uses dotted fill-in lines.
