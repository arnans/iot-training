# Progress dashboard — design notes

A live board for the instructor showing where each of the 100 teams stands in the worksheet,
so the session can be paced on evidence rather than a show of hands. Decided 13 Sep 2026.
Companion to [FILLABLE-WORKSHEET.md](FILLABLE-WORKSHEET.md), which owns the worksheet itself.

## Decisions

| Question | Decision | Why |
|---|---|---|
| Where do worksheet and dashboard live? | Both on GitHub Pages, as before | A server in the venue was considered and dropped: the worksheet is HTTPS, browsers block calls from an HTTPS page to a plain-HTTP LAN host, and the three WiFi zones are isolated from each other by design ([NETWORK-REQUIREMENTS.md](../network/NETWORK-REQUIREMENTS.md) guideline 2). |
| What carries the data? | Firebase Realtime Database, REST only — no SDK, no server code | Smallest possible hosted store: the worksheet does one `fetch(PUT)`, the dashboard opens one `EventSource`. Free tier is far above the load (100 teams, at most a couple of writes a second). The laptop SSIDs already have outbound 443. |
| What is sent? | **Counts only**: per activity, task boxes ticked / total and answer boxes filled / total, plus the last tick and its label | Pacing needs position, not content. Answers stay in the browser and still travel by the JSON download. |
| How is a write namespaced? | By calendar day: `progress/<YYYY-MM-DD>/<team>/<device>` | A rehearsal, the two workshop days, and someone reading the worksheet at home next month never land on the same board. No join code, no button. |
| How does a team "connect"? | Typing a valid team number is the whole act | Every extra tap is something 100 teams forget. The status line under the title shows a green dot once the board has heard from this browser. |
| Team identity | Integer 1–100 (`TEAM_MAX` in extra.js), Thai or ASCII digits, canonicalised in the browser; the database rules refuse anything else | Typos would otherwise make phantom cells. |
| Two devices per team? | Each browser has a random device id; the dashboard merges devices by taking the maximum per activity | The Recorder's phone and the Driver's laptop both report; neither overwrites the other. |
| Where is the dashboard's memory? | In the database, mirrored to the dashboard's `localStorage`, and downloadable as JSON | A dashboard opened late starts complete; one opened offline shows what it last saw. |
| Access | Reads public per day, writes only at the device leaf with a self-consistent document | Team numbers and counts are not sensitive. Nobody can wipe a day; anyone with the URL can post as any team, which is accepted for a pacing signal. |

## Moving parts

```
docs/javascripts/extra.js      summarize() counts the page · pushNow()/pushSoon() PUT the document ·
                               pushStatus() renders the dot in the #ws-bar status line
webapp/database.rules.json     the rules (paste in the console's Rules tab, or firebase deploy)
docs/progress.html             the dashboard page: tabs per worksheet page, day picker, tiles,
                               bars, the 10x10 grid, ticker, table view, export
docs/javascripts/progress.js   the dashboard's pure logic (stream events -> tree -> board)
scripts/test_progress.js       node checks for progress.js
```

### When the worksheet sends

- Any task checkbox `change` — immediately, with the tick as `last`. The **ทำข้อนี้เสร็จแล้ว**
  box at the foot of a sub-section forwards to its row in the task list, so it counts once.
  Boxes inside `<div class="ws-untracked" markdown>` (Activity 7.3's acknowledgements) are
  remembered in the browser but never counted or sent
- Any field `input` or radio `change`, and an import — 1.5 s after the last one
- Page load, tab becoming visible again, browser coming back online — 1.5 s later
- Never while the team number is empty or invalid

### Guarding the team number

A wrong number paints another team's cell, so nothing is sent until the number is checked
(`store.sentAs` = the number this browser has reported as). The worksheet first looks the new
number up (a shallow GET of `progress/<day>/<team>`), then asks **at most one** `confirm`,
worded for whichever of these apply:

1. **Changing a number that has already reported** ("เปลี่ยนหมายเลขกลุ่มจาก กลุ่ม 17 เป็น กลุ่ม 23
   ใช่ไหม?"). Cancel puts the old number back; OK moves this device's row (the entry under the
   old number is deleted, so no ghost stays on the board).
2. **A number another device already reports under today** ("กลุ่ม 23 มีอุปกรณ์อีกเครื่องส่ง
   ความคืบหน้าอยู่แล้ว ถ้าเป็นโทรศัพท์หรือแล็ปท็อปอีกเครื่องของกลุ่มเรา กด OK"). The phone-and-laptop
   team answers once; a wrong number is cancelled and the box clears.
3. **Both at once**: one combined question; Cancel goes back to the old number.

Offline, the lookup fails quietly and only case 1 can be asked. (Until 14 Sep 2026 cases 1 and 2
were two dialogs in a row, which felt redundant.)

Typing in the box does not trigger a report; leaving it does, so a half-typed "2" on the way
to "23" is never checked. The status shows "● กำลังตรวจสอบหมายเลขกลุ่ม…" until the check passes.

### Document (`progress/<day>/<team>/<dev>`)

```json
{
  "team": "17", "dev": "k3f9a2", "zone": "red", "ts": 1758340000000, "srv": 1758340000123,
  "page": "session-2",
  "pages": {
    "session-1": { "ts": 1758330000000, "acts": { "ก่อนเริ่ม": { "done": 4, "total": 4, "filled": 2, "nf": 2 },
                                                  "a1": { "done": 3, "total": 3, "filled": 2, "nf": 2 } } },
    "session-2": { "ts": 1758340000000, "acts": { "a5": { "done": 3, "total": 7, "filled": 4, "nf": 6 } } }
  },
  "last": { "page": "session-2", "act": "a5", "label": "5.3 ตั้งค่ากฎ", "on": true, "ts": 1758340000000 }
}
```

- An **optional** task item carries `(ไม่บังคับทำ)` inside its **bold** link text, so the marker
  travels into `label` and into the step list and is visible on the dashboard. Put the marker
  outside the bold only when just one step inside a required item is optional.
- `acts` keys are the id of the nearest heading above the item (`### … { #a5 }` gives `a5`);
  sub-section ids `a5-3`, `a2-1b` fold into their activity; anything before the first activity
  lands under the heading it sits below. Slugs drop Thai vowels (`ก่อนเริ่ม` → `กอนเรม`), so each
  page also carries `names`, id → heading text, for the headings that are not numbered
  activities; the dashboard labels by name when it has one. Each page also carries `order`, the same ids in page
  order, because **the database returns object keys sorted** (`a1, a2, ก่อนเริ่ม`), which would put
  the prep list last. The dashboard takes the order from whichever team reported the most
  activities; a document without `order` falls back to prep lists first, then `a1…aN` numerically.
- Two more database habits the dashboard normalises: a node whose keys are mostly small
  integers (a day of teams) arrives as an **array with `null` gaps**; and deleting a team's
  last device leaves an **empty parent** that must not count as a team.
- `filled` / `nf` count distinct field keys inside the activity, `team.no` and `team.zone` excluded.
- `steps` — per activity, one `{ l, on }` per task box in page order: its label (`1.1 ต่อสวิตช์…`,
  from the bold link in a task list; the first words of the item otherwise) and whether it is
  ticked. This is what the dashboard's chevron opens: how many teams have ticked each box.
  Devices merge by OR per box.
- `pages` holds every page this browser has visited (cached in the store as `prog`), so one
  document describes the team's whole worksheet.
- `srv` is the database's own clock (`{".sv":"timestamp"}`); the dashboard uses it for the
  "quiet for 10 minutes" fade, so a phone with a wrong clock does not look stale or fresh.

### Messages (`messages/<day>/<pushId>`)

The toolbar on every worksheet has a second row shaped like a chat composer: the button
**🙋 ขอความช่วยเหลือ** (sends at once), then a pill with **😊** (opens a strip of eight emoji that
drop into the box: 👍 🎉 🤔 😅 🙏 🔥 🌱 💧), the text box (120 characters), and a round green **➤**.
"ส่งแล้ว ✓" appears inside the pill for a moment. Each message is one document sent by `POST`, so the database
assigns a time-ordered id; the rules make messages create-only. (A "เสร็จแล้ว" chip was tried and
dropped, 14 Sep 2026 — unclear whether it meant the step, the activity or the day; `kind: done`
stays valid in the rules for compatibility.)

```json
{ "team": "17", "dev": "k3f9a2", "kind": "help", "text": "ขอความช่วยเหลือ", "page": "session-2",
  "zone": "red", "ts": 1758340000000, "srv": 1758340000123 }
```

`kind` is `help`, `done` or `note`; the dashboard paints help red and rings the team's cell
until a TA marks it done: **click the cell → ✓ ช่วยเหลือแล้ว** (clears every open call from that
team), or × on one message in the feed. That writes `handled: <timestamp>` onto the message, so
**every dashboard screen agrees**, TAs on phones included; ↺ on a hidden message clears it
again. "แสดงที่ซ่อนไว้" lists the handled ones. One message per five seconds per browser; the team
number must be valid, otherwise the usual prompt appears first.

**Withdrawing a call (20 Sep 2026).** Teams often sort the problem out while they wait, so the
🙋 button turns into **✖ ยกเลิกคำขอ** (amber, so it never reads as a second way to ask) as soon as
their own call is sent. Pressing it writes `cancelled: <timestamp>` onto that message. The
worksheet learns the message's id from the `POST` reply, which is why message POSTs no longer
use `?print=silent`, and keeps it in the store (`store.help = {id, day, ts}`), so the offer
survives moving to the next page. It goes back to 🙋 once a TA marks the call handled (the
worksheet polls that one field every 20 s while a call is open), on a new day, or after 20
minutes — a team is never left unable to call again.

`handled` and `cancelled` are the only fields of a message that may change after it is written.
A withdrawn call stops counting in **กลุ่มที่ขอความช่วยเหลือ** and its cell loses the ring at once, but the
message **stays in the feed for three minutes**, struck through and tagged กลุ่มยกเลิกแล้ว, so a TA
already walking over sees what happened instead of finding the row gone; × dismisses it sooner.
After that it joins the hidden pile. ↺ on a hidden one clears `handled` and `cancelled` both,
which brings the call back for everyone.

### Dashboard reading

`docs/progress.html?page=session-2&day=2026-09-20` (both default: session 1, today).
`&plus=1` also streams the previous day and merges it, for the second workshop day.
**จำนวนกลุ่ม** sets how many cells the grid shows (1–400; remembered in the browser and in the
URL as `&max=`); teams above it are counted and listed rather than drawn. It only changes the display: the worksheet's own limit is `TEAM_MAX` in
extra.js (100 for this workshop — change it per event), and the database rules accept 1–400 so
that constant can move without another rules paste. Numbers above the dashboard's setting are
listed under "หมายเลขกลุ่มที่ไม่อยู่ในช่วง".

Layout (revised 14 Sep 2026, Roger's priorities): the **กลุ่มใดอยู่กิจกรรมใด** bars are the largest
element and come first in the main column; the team grid sits under them, its first job being
to show **who is asking for help** (heavy red ring and 🙋, pulsing when new) and only second the
colour overview; messages run as a **sticky live feed down the right side**, newest on top,
new ones sliding in; the tick ticker is an admin view behind the **ติ๊กล่าสุด** toggle, off by default.

- **Cell colour** = the furthest activity the team has touched, on an 8-step green ramp
  (light and dark variants validated as ordinal ramps against the site surfaces).
  Marigold = every activity on the page complete. Dashed and faded = nothing heard for 10 minutes.
  Outline only = never reported on this page.
- **Bars** = how many teams currently stand at each activity — the pacing number. The chevron
  on an activity opens one bar per task box (1.1, 1.2, …): how many teams have ticked it.
  Open/closed state is remembered in the browser.
- **ข้อความจากกลุ่ม** = every message of the day, newest first, across all pages; a fifth tile
  counts teams with an unhidden call for help.
- **Ticker** = the 20 most recent ticks for the page.
- **ตาราง** toggles a table of the same numbers (the accessible view; also fine to screenshot).
- **ดาวน์โหลด JSON** saves everything the page holds: per-team merged views and the raw trees.
- The raw day is also one URL: `<DB>/progress/<day>.json`.

## Setting up the database (once)

1. Firebase console → project `iot-farm-workshop` → Realtime Database (Singapore). Done 13 Sep 2026:
   `https://iot-farm-workshop-default-rtdb.asia-southeast1.firebasedatabase.app`
2. **Rules** tab → replace the contents with [database.rules.json](database.rules.json) → Publish.
   The file is plain JSON with `rules` as its only top-level key — the console rejects anything
   else there, so the explanation of what the rules do lives here, not in the file:
   `progress/` reads public per day, writes only at the per-device leaf for team 1–400 with a
   document that names its own team and device; `messages/` create-only, read public per day,
   with only the `handled` and `cancelled` timestamps settable or clearable afterwards.
   (Or `npm i -g firebase-tools`, `firebase login`, `firebase init database` pointing at that file,
   `firebase deploy --only database`.)
3. Smoke test. In PowerShell (`curl` there is an alias of `Invoke-WebRequest`, so use the cmdlet):
   ```powershell
   $u = "https://iot-farm-workshop-default-rtdb.asia-southeast1.firebasedatabase.app/progress/2026-01-01/1/test01.json"
   $doc = '{"team":"1","dev":"test01","ts":1,"pages":{"session-1":{"ts":1,"acts":{"a1":{"done":1,"total":3,"filled":0,"nf":2}}}}}'
   Invoke-RestMethod -Method Put -Uri $u -Body $doc -ContentType "application/json"   # echoes the document
   Invoke-RestMethod -Method Delete -Uri $u                                            # cleans up
   ```
   In bash: `curl -s -X PUT -d '<same JSON>' "$u"` and `curl -s -X DELETE "$u"`.
   `pages` must not be empty — Firebase stores an empty object as nothing, and the rules
   require the child to exist (the worksheet always sends at least the current page).
   Refusals to expect, each `401 Permission denied`: a PUT to `progress/2026-01-01/999/x1.json`;
   a PUT whose `team` does not match the path; a GET of `progress.json` (the root).
   Verified against the live database 14 Sep 2026.
4. Open `progress.html`, tick a box on a worksheet with a team number set, watch the cell change.
   `progress.html?demo=1` shows the board with made-up teams and no connection, for a look at
   the layout before any real data exists.

### Free-tier arithmetic (Spark plan, checked 14 Sep 2026)

Limits that matter: **100 simultaneous connections**, **10 GB/month downloaded**, 1 GB stored.
Uploads are not metered.

- Connections: only streaming (SSE/WebSocket) connections count — the dashboard screens, two
  per screen (progress + messages; four with "รวมวันก่อนหน้า"). The worksheets' PUTs and POSTs
  are one-shot HTTP requests. So **up to ~45 dashboard screens** at once; a projector plus 10–15
  TAs on phones is ~30 connections. A burst of 100 teams ticking in the same second is
  ~100 writes/s against a ~1000/s ceiling.
- Download: a team document is ~3–8 KB (the `steps` labels are most of it), and **every open
  dashboard receives every write**, so screens multiply it. Generous estimate: 100 teams ×
  200 writes/day × 2 days = 40k writes × 8 KB ≈ 320 MB per screen over the workshop — about
  4 GB with 12 screens open all day. Writes use `?print=silent` so the database does not echo
  the document back. Messages are negligible. The margin matters: **a Spark database that
  exceeds its download quota stops serving until the month rolls over**, so ask TAs to close
  the dashboard between sessions. With 25+ screens, or a longer event, switch the project to
  Blaze (pay-as-you-go): at this volume it costs cents and removes the cliff.

### Removing a team's progress data

Click a team's cell (or its number in "หมายเลขกลุ่มที่ไม่อยู่ในช่วง") and the pinned popover lists
**the devices reporting for that team**: a short device id, last seen, where that device is on
the current page, faded with "(เงียบ)" after 10 minutes of silence. Each has **ลบ**, and
**ล้างข้อมูลกลุ่มนี้ทั้งหมด** removes them all. Both confirm first. Each removal is a DELETE of
`progress/<day>/<team>/<dev>` (the rules already allow it; deleting a whole team in one request
is refused), and the cell updates on every screen through the stream. Messages and help
calls are not touched.

What it is for, given that the dashboard never writes back to worksheets and every worksheet
re-sends its full state on its next tick:

| Case | Does removal stick? |
|---|---|
| Leftover slot after **ล้างคำตอบทั้งหมด** (same team restarted, or the laptop passed on) — the browser now has a new device id | Yes |
| A device that changed its number, or went home | Yes |
| A **live** device reporting under the wrong team | No: it re-sends on its next tick. Fix the number on that worksheet; the popover shows which device to look for |
| "Start this team from zero" while its devices still hold ticks | No, and correctly: the board mirrors the worksheets |

The typical sign of a leftover: the cell shows a team further along than it is (devices merge
by maximum), and the popover shows one faded device ahead of the live one.

### Several TAs at once

Any number of TAs may open the same URL, each on their own device. A help call rings on
every screen; whoever presses **✓ ช่วยเหลือแล้ว** writes `handled` to the database and the ring
clears on every screen within a second or two; ↺ on any screen brings it back everywhere. Two
TAs pressing at the same moment is harmless (both write a timestamp; the last one stays).
Each screen shows its own press immediately and waits for the database to agree; if the write
fails, that screen reverts and says so. Verified 14 Sep 2026 with two screens: clear on A,
undo on B, simultaneous clear on both — the screens stayed in step each time. A team
withdrawing its own call (✖ ยกเลิกคำขอ on the worksheet) clears the ring on every screen the same
way, and leaves the struck-through message behind for three minutes.
- Storage: kilobytes.

## Testing checklist (browser)

Verified 14 Sep 2026 with headless Chrome driven over the DevTools protocol (scripts kept out of
the repo): the dashboard connects, shows two written teams within 5 s, reflects a patch in
under 3 s, drops a deleted team; the rendered Session 1 worksheet normalises `๙๙` to `99`,
shows the green dot, and one tick lands in the database with `order`, `names`, counts and
`last` about 2.5 s after the click. Still to do by hand on the day's hardware:

- [ ] Worksheet with no team number: status line asks for it; nothing is sent
- [ ] Type `17`: dot turns green within two seconds; cell 17 appears on the board
- [ ] Tick a box: ticker shows it at once; cell sub-label updates
- [ ] Untick: ticker shows ✗; count drops
- [ ] Second browser, same team number: board shows "2 เครื่อง" in the tooltip; counts are the max
- [ ] Airplane mode, tick, reconnect: dot grey then green again; board catches up
- [ ] Dashboard reload: starts full (replay from the database); offline reload: shows cached state
- [ ] Change the date to yesterday: empty board; "รวมวันก่อนหน้า" on today's date shows both
- [ ] Rendered worksheets (`docs/renders/session-1.html`) report too — same code, re-rendered

## Known limits

- One shared write path with no auth: anyone with the site can post as any team. Accepted.
- Internet on the laptop SSIDs is required for reporting; the worksheet itself works without it.
- Activity granularity depends on the `ws-tasks` rollout; pages without task lists report only
  their loose checkboxes and fields, grouped under the nearest heading.
- Ticks made while offline arrive as the *current* counts, not as a history; the ticker shows
  only the last tick per device.

## Follow-on

Once every team writes to the database, adding the full `fields` blob to the same document is
one line, and the instructor's collection pipeline (100 JSON files over LINE →
`collect_answers.py`) becomes one download of `progress/<day>.json`. Not done yet: decide
first whether answers should leave the browser at all.
