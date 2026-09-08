# Session 3 — handoff for Codex

Written by Claude on 8 September 2026 (evening), after acting on `SESSION-3-REVIEW-FOR-CLAUDE.md`.
Roger's steer that evening: **Session 3 is too dense; give teams real time to think of a project,
work on it, and exchange with each other.** Everything below follows from that.

Read first: `docs/session-3.md` (the worksheet, Thai), then the Session 3 rows in `COURSE-DESIGN.md`
and `SESSION-OVERVIEW.md`, and the "Session 3 review, 8 Sep 2026" section of `WORKSHEET-TODO.md`.
House rules for the worksheet voice are in Roger's KSM (`roger-ksm/skills/hands-on-workshop-at-scale.md`,
`roger-ksm/mindset/writing-voice-universal.md`): เรา/ของเรา, never คุณ; UI terms in English; no
exclamation marks; say *why* after each constraint; session-neutral wording (ช่วงที่ 1/2/3, never
"yesterday", "this morning", "tonight").

## What changed tonight (so you do not undo it)

| Block | Was | Now |
|---|---|---|
| Network (กำพล, live) | 20 min: YAML + IP + blank 30-cell มาก/กลาง/น้อย table + 3 protocols + local/cloud | 20 min: same opener; **completed reference table** with a limitation column; one worked choice (card A) then one team choice (card B) as the only record; protocols read-only; local/cloud table; ends with the **Home Assistant Cloud remote-access demo** on the instructor kit |
| Power | 20 min hands-on: terminals, battery menu, wire panel, window walk, adapter-pull demo | 10 min instructor-led at the team's own box: terminals, LCD, produce/store/supply, "who needs power all night". No panel wiring, no menu, no adapter pull |
| History | 10 min: find four things, counts | 20 min: four things (with "not observed" allowed), relay **command** count only after `s2.pump_back_t`, two-event interpretation table, overnight-gap question kept |
| Dashboard | 45 min incl. cloud push | 35 min: plan 5, build 25 (minimum vs optional stated), one usability test by someone who did not build it |
| Design | 45 min: 30 design, 5 pair, 10 plenary | **55 min: 40 design, 10 paired exchange, 5 revise.** No plenary. First-pilot framing, C/D marked advanced, new canvas box "สิ่งที่ยังไม่แน่ใจ", `d.revise` field |
| Kit return | drain first, automations still live | automations off → relay Off → isolate power → drain |

Field keys removed: `s3.comm.<tech>.*` (all six rows), `s3.pwr.btype/amp_room/amp_light/unplug.*/order*`,
`s3.cloud.tool/url/what/every/where`, `s3.remote.age/control`, `s3.hist.pump_runs`.
Field keys added: `s3.comm.choice.tech/why`, `s3.remote.conn/where`, `s3.q.cloud`, `s3.pwr.night`,
`s3.hist.relay_on`, `s3.hist.ev{1,2}.{what,t,cause,action}`, `s2.pump_back_t` (also in Session 2),
`d.unknown`, `d.revise`. `s3.q7` kept but now asks about the usability test.
The worksheet and `docs/record-sheet.md` share keys — change both or neither.

## Suggestions for what to do next, in priority order

1. **Read the Thai as a participant would.** I wrote it in one pass. The new passages most worth a
   native-ear check: the comms reference table's limitation column, the Home Assistant Cloud demo
   section, "ใครต้องมีไฟตอนกลางคืน", the two-event history table's header row, and the design
   challenge's first-pilot framing. Keep them short; the session is being made *less* dense.

2. **Timing sanity on the design block.** 40 min design + 10 min exchange + 5 min revise. If a
   rehearsal shows teams stall in the first ten minutes, the fix is a worked example on the canvas
   (WORKSHEET-TODO already owes a "take-home worked farm example"), not more minutes taken from the
   first half. Do not reintroduce the plenary.

3. **Dashboard build is the one unmeasured number.** 25 min for seven steps on a VM the team has used
   for two sessions. If a novice timing says it does not fit, cut steps 3's Severity and 5's icon to
   "optional" text only (already marked) and consider dropping step 4 (History graph) to optional as
   well; the graph was already read in the previous block.

4. **The comms reference table's numbers are my general estimates.** Roger or กำพล should confirm
   the ranges (WiFi 30–50 m, ESP-NOW 100–200 m, Zigbee 10–30 m per hop, LoRa 1–10 km, RS-485 ~1 km)
   against what they teach. The Zigbee row mentions the showroom demo set on purpose (Roger asked for
   Zigbee to be listed because that set uses it).

5. **Screenshots.** Every `images/placeholder.png` in session-3.md still needs a real image. New or
   changed ones: the History page with the relay bar (now must show the lamp period vs pump period),
   the Home Assistant Cloud settings page, the remote dashboard on a phone. The step-screenshot
   pipeline is `scripts/video_steps.py` (see `roger-ksm/skills/video-to-step-screenshots.md`).

6. **Record sheet print layout.** The Session 3 block on `docs/record-sheet.md` shrank; check the
   print-to-PDF page breaks still fall sensibly (the design canvas should still start on its own page).

7. **Do not touch** the Session 1 and 2 pages beyond the one `s2.pump_back_t` line already added, and
   do not change the timetable totals (150) without updating COURSE-DESIGN and SESSION-OVERVIEW in the
   same commit; the risk-register row "Session 3 timed blocks overrun the slot" lists the numbers.

## Open decisions that are Roger's, not yours

- Home Assistant Cloud as the remote-access tool is Roger's working choice; กำพล has to agree
  because it lands in their block. The worksheet already says "instructor demo, teams do not follow".
- Whether the instructor kit gets a real 12 V battery for a lit-vs-shaded charging demo, and if not
  whether the 15 W panel stays in 100 kits as a prop.
- The network block stays at 20 min because it is กำพล's; the review implied cutting it further.
