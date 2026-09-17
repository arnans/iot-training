# One worksheet page per activity

Approved by Roger, 17 Sep 2026. Two commits after this spec: images, then the restructure.

## Why

Session pages run 450–540 lines, so activities 4 and 5 blend together and a phone
loads 10 MB of inlined images per session. Participants should see one activity at a
time, with the nav grouping activities by session.

## Commit 1: renders link images instead of inlining them

- `scripts/render-worksheets.py` writes `../images/...` links by default. GitHub Pages
  serves docs/, so the committed renders work unchanged.
- `--offline` keeps inlining, for a render sent as a file. `--combined` (the Artifact
  fragment) always inlines.
- The seven renders drop from 29 MB to under 2 MB; the repository stops growing by
  ~30 MB per worksheet edit.

## Commit 2: split the session pages

Pages (source file = URL slug), in three MkDocs nav groups:

| Group | Page | Content |
|---|---|---|
| ช่วงที่ 1 | session-1-start.md | "เตรียมพร้อมก่อนเริ่ม" (team number, zone, HA IP, farm problem) |
| | activity-1/2/3.md | activity H2 promoted to H1; activity 3 ends with `## ก่อนออกจากห้อง` |
| ช่วงที่ 2 | activity-4/5.md | activity 5 ends with `## ก่อนจบช่วงที่ 2` |
| ช่วงที่ 3 | session-3-history.md | "การอ่านข้อมูลที่บันทึกไว้ย้อนหลัง" promoted to H1 |
| | activity-6/7.md | activity 7 ends with `## คืนอุปกรณ์` |

Cut: the three session summaries, the Session 2 and 3 pre-checks. "นำไปใช้ที่ฟาร์มอย่างไร"
moves to resources.md. The one assessment reference to "สรุปช่วงที่ 2" is re-pointed.

Heading ids, field keys and task-box keys are untouched. No anchor crosses a page today.

### Progress reports (the overwrite gap)

Reports stay keyed by session, so `docs/progress.html`, the Firebase rules and the data
shape do not change. `extra.js` caches a summary per page slug and, on every push, builds
each session's record by concatenating its pages' summaries in course order. Activity 2's
page therefore never replaces activity 1's counts. `page` on a report is the session key.

### Nav

- mkdocs.yml: three groups with `navigation.sections` (already on).
- Renderer switcher: a non-link group row per session on desktop; on phones the chip's
  eyebrow reads "ช่วง 1 · กิจกรรม 2". The per-page toc lists the top headings under H1
  (the sub-activities), not only H2s.

### Old URLs

`session-1.md`, `session-2.md`, `session-3.md` stay as stubs that meta-refresh to the
session's first page and show a link; same for `docs/renders/session-N.html`.
Links in index.md, index.html, resources.md, instructor-resources.html, README.md and
planning/INSTRUCTOR-RESOURCES.md move to the new pages.

### Tests

- `test_worksheet_steps.cjs` and `test_worksheet_fields.cjs` iterate the new pages.
- `test_worksheet_fields.cjs` also captures the progress PUT on an activity page and
  asserts `page` is the session key and the doc carries the cached counts of the
  session's other pages.
- `mkdocs build --strict`, renders regenerated, record-sheet key diff, a link check that
  every `href="#..."` in a render resolves on that page.
