# Session 3 — handoff for Codex

Written by Claude, 8–9 September 2026, after acting on `SESSION-3-REVIEW-FOR-CLAUDE.md` and then on
Roger's own three-point review of 9 September. Roger's steers, in order:

1. **Session 3 is too dense; give teams real time to think of a project, work on it, and exchange.**
2. **Network and power had too little participation for an after-lunch slot.** Reframe both as
   *parameters of the design* inside the design challenge, and open the afternoon with the two
   hands-on blocks (history, dashboard).
3. **Power needs a participation exercise** (how many panels for which load; a pump is daytime DC
   solar with no battery), and **network needs one too**: framed as local network vs access from
   outside, keep WiFi/Zigbee/etc. as the local menu, drop MQTT/HTTP, and show that Nabu Casa is one
   of several ways to reach a farm from outside.

Read first: `docs/session-3.md` (the worksheet, Thai), then the Session 3 rows in `COURSE-DESIGN.md`
and `SESSION-OVERVIEW.md`, and the two Session 3 sections at the end of `WORKSHEET-TODO.md`.
House rules for the worksheet voice are in Roger's KSM (`roger-ksm/skills/hands-on-workshop-at-scale.md`,
`roger-ksm/mindset/writing-voice-universal.md`): เรา/ของเรา, never คุณ; UI terms in English; no
exclamation marks; say *why* after each constraint; session-neutral wording (ช่วงที่ 1/2/3, never
"yesterday", "this morning", "tonight").

## Current shape (150 min)

| Block | Min | What |
|---|---:|---|
| History | 20 | four things on the graph; relay **commands** after `s2.pump_back_t`; two-event interpretation table; overnight-gap question |
| Dashboard (Activity 7) | 35 | plan 5, build 25 with a stated minimum, one usability test by someone who did not build it |
| Break | 15 | |
| Design (Activity 8) | 85 | scenario 5 · **step 1 network 20** (กำพล) · **step 2 power 15** · fill canvas 30 · paired exchange 10 · revise 5 |
| Wrap-up | 10 | recap, save answers, kit return in the safe order |

Network step = local network chosen by **elimination** (distance, then power at the far end) for the
team's own two links (`s3.net.{1,2}.*`, instructor works card B on screen), then access from outside
as a **five-way menu** (notifications only / Home Assistant Cloud / private VPN / open a door yourself /
IoT cloud platform) with the instructor demoing Home Assistant Cloud as one of them, and a decision
for the team's scenario (`s3.remote.need/method/lost`).

Power step = read the charge controller at the team's own box, then a **panel-sizing table** for four
loads on two rules (15 W ≈ 60 Wh/day; Wh/day = W × h) with one-night storage and a self-check answer
(`s3.pwr.size.*`). Landing: pumps run on direct daylight solar and you store water, not electricity.

Field keys removed since the original: `s3.comm.*` (all), `s3.pwr.btype/amp_*/unplug.*/order*`,
`s3.cloud.tool/url/what/every/where`, `s3.remote.age/control`, `s3.hist.pump_runs`.
Field keys added: `s2.pump_back_t` (Session 2 too), `s3.hist.relay_on`, `s3.hist.ev{1,2}.*`,
`s3.net.{1,2}.{dist,power,out_dist,out_power,left}`, `s3.remote.{conn,where,need,method,lost}`,
`s3.q.cloud`, `s3.pwr.size.{node,ha,kitpump,farmpump}.{wh,panels,bat}`, `s3.pwr.size.night_{node,pump}`,
`d.unknown`, `d.revise`. The worksheet and `docs/record-sheet.md` share keys — change both or neither.

## Suggestions, in priority order

1. **Read the Thai as a participant would.** Most worth a native-ear pass: the elimination table's
   column headers, the five-way remote-access table, the panel-sizing rules and the เฉลย paragraph,
   and "เก็บน้ำแทนเก็บไฟ". Keep them short; the whole point was less density.

2. **Check the arithmetic and the assumptions in the sizing exercise** with Roger: 4 full-rated
   sun-hours/day, 0.5 W for the sensor node, 10 W for router + HA host, 18 W for the kit pump, 750 W
   for a 1 hp pump, 50 % usable depth for lead-acid; 400 W panel → 1,600 Wh/day by the same rule (the เฉลย says 2 panels by arithmetic, ~3 in practice for a direct-drive pump; an earlier draft wrongly said 6). The numbers were chosen to be round; if a kit
   measurement disagrees (the aquarium pump may draw less than 18 W), change the table and the เฉลย
   together.

3. **The comms reference ranges are general estimates** (WiFi 30–50 m, ESP-NOW 100–200 m, Zigbee
   10–30 m per hop, LoRa 1–10 km, RS-485 ~1 km). กำพล should confirm against what they teach. The
   Zigbee row names the showroom demo set on purpose.

4. **Timing.** 20 min for the network step is the tightest block: opener 4, elimination 6, remote
   menu + demo 6, decisions 4. If a rehearsal overruns, cut the YAML opener to the one sentence
   "no IP in the file" and keep the two team decisions. Do not take time from the 30-min canvas fill.

5. **Dashboard build (25 min) still needs a novice timing.** If it does not fit, make step 4
   (History graph) optional; the graph was already read in the previous block.

6. **Screenshots.** Every `images/placeholder.png` still needs a real image: the History page with
   the relay bar showing the lamp period vs the pump period; the Home Assistant Cloud settings page;
   the remote dashboard on a phone; the charge controller front. Pipeline: `scripts/video_steps.py`
   (see `roger-ksm/skills/video-to-step-screenshots.md`).

7. **Record sheet print layout.** The Session 3 block was reordered and grew two tables; check the
   print-to-PDF page breaks, and that the design canvas still starts on its own page.

8. **Do not touch** Session 1 and 2 beyond the one `s2.pump_back_t` line, and do not change the
   150-min totals without updating COURSE-DESIGN and SESSION-OVERVIEW in the same commit; the
   risk-register row "Session 3 timed blocks overrun the slot" lists the numbers.

## Open decisions that are Roger's, not yours

- Home Assistant Cloud stays the *demonstrated* option; กำพล has to agree because the network step
  is in their block.
- Whether the instructor kit gets a real 12 V battery for a lit-vs-shaded charging demo, and if not
  whether the 15 W panel stays in 100 kits as a prop for the sizing exercise (it is handled, not wired).
- The equipment price sheet and the take-home worked farm example are still owed (WORKSHEET-TODO).
