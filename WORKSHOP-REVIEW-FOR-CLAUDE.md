# Workshop worksheet review — action handoff for Claude

Reviewed: 8 September 2026.

## Purpose and scope

The user requested a review of the current `/docs/` worksheets for an IoT workshop serving **400 participants in 100 groups of four**, primarily farmers and interested individuals. They then requested this Markdown handoff so Claude can read and act on the feedback.

This review examined `docs/index.md`, the three session worksheets, `docs/record-sheet.md`, `docs/reference.md`, and the network requirements. Findings were cross-checked against `COURSE-DESIGN.md`, `WORKSHEET-TODO.md`, and relevant firmware. This was a document and implementation review, **not a classroom rehearsal or a fresh hardware test**.

Read current files before editing: existing preparation notes contain some stale statements. Preserve confirmed hardware behavior rather than changing firmware merely to match worksheet prose.

## Overall judgment

The workshop has a strong learning sequence but the current worksheet package is not yet ready for 100 groups. It provides a compelling introduction to IoT. The main weaknesses are delivery completeness, consequential technical inconsistencies, and the bridge from classroom success to practical farm use.

Preserve these strengths:

- One kit throughout: observe sensors → operate relay/pump → act as the decision-maker → automate → investigate failures → interpret data → design a system.
- Experience before terminology, particularly the manual decision-making exercise.
- The lifted-float experiment introducing trigger versus condition.
- Counting relay switching before and after hysteresis.
- Paired-team failure investigation and dashboard peer testing.
- Existing maintenance, installation cost, and recurring-cost prompts in the design canvas.

## Learning-outcome alignment

The six formal goals are in `COURSE-DESIGN.md`, under “Learning goals → where each is taught.”

| Goal | Assessment | Action |
|---|---|---|
| Explain Input / Logic / Output | Strong: reinforced throughout | Preserve the sequence and vocabulary |
| Choose sensors and actuators | Partial: supplied-kit investigation is stronger than comparison of alternatives | Protect the spec activity; add supported comparison and justification |
| Create control logic | Strong guided practice; weaker evidence of independent application | Add an independent rule/prediction task |
| Choose infrastructure and communications | Moderate: many technologies in a short lecture | Use worked decisions and scenario-based justification |
| Apply fail-safe, safety and maintenance principles | Strong concept; uneven implementation and verification | Correct claims, clarify limits, and define required tests |
| Create dashboards and controls | Strong locally; remote workflow incomplete | Finish the cloud procedure and acceptance test |

Core outcomes must not become optional when time runs short. Activity 4 is currently the timing buffer despite sensor/actuator selection being a core outcome. Session 2 promises sensor-loss and failed-operation protection while those implementations are optional, and its minimum pass criterion requires only one successful fail-safe test.

## P0 — Correct consequential technical claims before delivery

### 1. Float-switch wire failure does not become unavailable

> **Resolved in hardware (8 Sep 2026):** the float cylinder is flipped on its rod so the contact closes when wet. A cut wire or unplugged switch now reads **Dry**, the safe state. Firmware `inverted: true` + `device_class: moisture`; worksheets say Wet / Dry. The analysis below describes the pre-flip wiring.

Sources: `docs/session-2.md`, “Fail-safe 1”; `firmware/gogo-iot-workshop.yaml`, float-switch GPIO configuration and comments around lines 372–405.

The worksheet says a disconnected float-switch wire or a powered-down board becomes `unavailable`. These are different failures. The firmware documents the measured wiring: wet = open circuit, internal pull-up = HIGH, entity On = water present. A cut wire or disconnected Grove connector can therefore also read **water present**. Requiring On in the watering condition does not detect that fault.

Actions:

- Correct the worksheet and any corresponding explanations or answer keys.
- Distinguish sensor-wire disconnection, sensor-board loss, network loss, and Home Assistant loss.
- State the actual protection limits of the kit.
- If proposing a hardware remedy, verify it against the real float switch and wiring. Merely inverting the entity cannot distinguish two physically identical open-circuit states.

Acceptance: no material claims that this float-wire failure is detected as unavailable or prevented by the On condition. The lesson explicitly identifies the limitation and includes a verified demonstration or instructor explanation.

### 2. Separate competing fail-safe timers

Source: `docs/session-2.md`, Fail-safe 2 and Fail-safe 4.

Both maximum runtime and commanded-on-without-vibration use 30 seconds. Their actions can interfere, making the failed-operation notification test ambiguous.

Actions:

- Choose distinct, rehearsed timing for operation confirmation and maximum runtime.
- Specify which rules are enabled, the starting conditions, expected result, and reset procedure for each test.
- Keep record-sheet prompts and screenshots synchronized.

Acceptance: each protection can be demonstrated independently with an unambiguous cause and observed result.

### 3. Distinguish automatic-start conditions from universal interlocks

Source: `docs/session-2.md`, recap, Fail-safe 1, and manual controls.

Adding a float condition to `รดน้ำ - เปิดปั๊ม` restricts that automation's start action. It does not prevent starting through the dashboard or onboard button while the float is already low. The low-water state-change rule need not fire again.

Actions:

- Narrow claims that the pump cannot start when water is low.
- Explain the distinction between a software command, an automation condition, and an independent protective interlock.
- State expected manual-control behavior and what remains unprotected in the teaching kit.

Acceptance: participants can explain which start paths are protected and which are not.

### 4. Explain cutoff recovery and controller dependence

Source: `docs/session-2.md` and `docs/reference.md`.

A numeric-state trigger responds to a threshold crossing; a value remaining dry does not itself repeatedly start watering after a cutoff. Home Assistant `for` timers also do not survive automation reloads or restarts.

Actions:

- Specify recovery after maximum-runtime cutoff, low-water stop, sensor recovery, and controller restart at the level appropriate to this introductory workshop.
- Clearly distinguish deliberate teaching limitations from production-ready protection.
- Preserve the discussion of protection outside Home Assistant; do not imply that HA rules work when HA or its command path is unavailable.

Technical reference: [Home Assistant automation triggers](https://www.home-assistant.io/docs/automation/trigger/).

## P1 — Make the workshop deliverable at 100-group scale

### 5. Reconcile the schedule

Sources: `docs/session-3.md`; `COURSE-DESIGN.md` session schedules.

Session 3's timed blocks total **155 minutes**: network 30 + energy 20 + history 10 + dashboard/cloud 50 + design 45. This excludes wrap-up, cleanup, and transitions. The course design allocates 150 teaching minutes per session. The energy block appears to have been added without a corresponding schedule reduction.

Actions:

- Produce one consistent schedule covering instruction, transitions, breaks, assessment, and equipment return.
- Protect core learning activities; move optional depth to demonstrations or take-home material as needed.
- Rehearse the 45-minute Failure Lab with beginners: it currently contains six intervention/observation half-rounds, recovery, diagnosis, rule editing, testing, and recording.
- Define a minimum required route and meaningful extensions for fast teams.

Acceptance: timed blocks fit the actual organizer slots, including required non-teaching time, and all documents agree.

### 6. Specify a parallel presentation format

Source: `docs/session-3.md`, Activity 8.

One minute per team means at least 100 minutes if all teams present to the room. The worksheet does not specify how this fits the 45-minute design activity.

Action: use simultaneous paired-team pitches or small clusters, then a few selected plenary examples. Include peer-feedback criteria and timing.

Acceptance: all 100 teams can present and receive feedback within the scheduled block.

### 7. Complete the participant-facing materials

Sources: all `docs/*.md`; `WORKSHEET-TODO.md`, “Not yet written” and “Images.”

At review time there were **21 references to `images/placeholder.png`**, including the full wiring diagram, interface screenshots, and take-home QR codes. The backlog also identifies missing specification excerpts, scenario cards, price sheets, role/team cards, installation guidance, and post-tests.

Actions:

- Replace essential placeholders with accurate visuals matched to the actual kit and workshop software.
- Finish the referenced handouts and concise answer keys.
- Complete the pre-event laptop readiness procedure and participant recovery instructions.
- Publish working take-home destinations before producing their QR codes.
- Verify the printed record sheet for readable tables, writing space, and intentional page breaks.

Acceptance: a participant or facilitator can follow every required step without an unpublished handout, missing illustration, or unspecified destination.

### 8. Finish the cloud activity

Source: `docs/session-3.md`, Activity 7, “ส่งข้อมูลขึ้นคลาวด์.”

The worksheet promises remote access but currently delegates the procedure to unspecified instructor-led steps.

Actions:

- Resolve the actual service and workflow with the responsible instructor; do not silently invent a service commitment.
- Document prerequisites, per-team identification, setup, published values, update interval, access, and verification.
- State whether the remote interface supports observation only or control as well.
- Provide a fallback when venue internet, mobile access, or account setup is unavailable.

Acceptance: the mobile-data test has a specific destination and expected result; core versus optional remote outcomes are stated accurately.

### 9. Give all four participants accountable roles

Sources: `docs/index.md`; `docs/record-sheet.md`; `COURSE-DESIGN.md`.

There are four participants per group but three defined roles. The fourth person merely follows on a phone.

Action: add a rotating **Tester** role: predict behavior, execute the test, time the response, and verify the pass criterion. Update the rotation table and activity instructions.

Acceptance: every participant has a meaningful role and rotates through practical responsibility. Retain individual post-tests: team completion alone does not establish individual learning.

Suggested individual transfer question: “Your pump is on, but the dashboard stops updating. What can you conclude, and what should you check?”

### 10. Complete the facilitation and recovery plan

Sources: `WORKSHEET-TODO.md`, scale section; `COURSE-DESIGN.md`, risks; network requirements.

Network planning is already substantial: zoning, identification, bridged-VM connectivity, and acceptance tests exist. Do not describe those as absent. The network document also explicitly acknowledges that its 20–30-board test does not establish full-load capacity.

Actions:

- Confirm facilitator assignments; the repository proposes approximately ten roving facilitators, but this remains a planning assumption to validate.
- Define a visible help-request process, escalation ownership, spare-kit policy, and recovery checkpoints.
- Specify water handling, equipment resets, and restoration between failure rounds.
- Preserve same-zone device identification checks to prevent adopting another team's equipment.

Acceptance: facilitators have a concrete run sheet and recovery route, and progress does not depend on one instructor visiting all teams.

## P2 — Improve the farmer's path from learning to use

### 11. Anchor the experience in participants' own problems

The current workshop likely fulfills “help me understand IoT and build an automated example.” It only partially fulfills “help me decide what to introduce on my farm and how to begin.”

Actions:

- At the start, have participants name a farm problem, current practice, consequence of failure, and desired improvement.
- Offer “my own farm” as a final-design option alongside scenarios A–D.
- Keep supplied scenarios for participants without a farm or a sufficiently defined problem.

Acceptance: participants can connect the final design to a meaningful use case rather than only reproduce the tabletop system.

### 12. Close the gap between simulated humidity and an irrigation decision

Sources: `docs/session-1.md`, manual Logic exercise; `docs/session-3.md`, design challenge.

The worksheets correctly disclose air humidity as a classroom stand-in for soil moisture. Preserve that disclosure. The missing bridge is how to obtain and validate an appropriate input and threshold for a real application.

Action: add one concise worked farm example connecting the problem to sensor choice, placement, interpretation, justified control rules, equipment, and maintenance. Avoid presenting classroom thresholds as agronomic recommendations.

Acceptance: learners can explain what must be re-evaluated before applying the demonstration to their farm.

### 13. Add a small pilot plan to the existing design canvas

Source: `docs/record-sheet.md`, final design canvas.

Maintenance, equipment cost, installation cost, and monthly costs already exist. Extend them rather than duplicating them.

Add:

- Expected practical benefit.
- Measurable success criterion and baseline.
- First small trial and first action.
- Responsible person.
- Review date and decision about expanding the trial.

Acceptance: each team leaves with an actionable first experiment and a way to decide whether it worked.

### 14. Make the take-home path usable

Source: `docs/session-3.md`, equipment return and “ไปต่ออย่างไร.”

Participants return the hardware. Home Assistant remaining on their laptop is not enough to reproduce the workshop.

Action: provide accessible configuration files, actual setup instructions, a clear equipment reference, and a defined support route or named next learning step.

Acceptance: all links work and the participant knows what to do first after returning home.

## Smaller consistency fixes

- `docs/record-sheet.md`: the cloud Recorder question is labeled Activity 5; it belongs to Activity 7.
- `COURSE-DESIGN.md`: the final design challenge is still called Activity 7 in the Session 3 timetable; current worksheets call it Activity 8.
- `docs/session-3.md`: the retrospective refers to the instructor shutting down a router, whereas the current paired sabotage design uses laptop WiFi being turned off. Align the narrative with the actual experiment.
- The record sheet asks for history before communications/energy, while the worksheet presents communications/energy first. Match the order to reduce page searching.
- Dashboard planning provides four rows while asking for at least five elements. Give sufficient space or clarify that rows may combine elements.
- Reconcile the course-design claim that Sessions 1–2 run fully offline with their use of `web.esphome.io` and online worksheets; document actual preloading/offline arrangements if intended.
- Review power-loss demonstrations against the actual 18650 installation state. The kit lists a cell, while some demonstrations expect removal of USB power to make the sensor board unavailable. Specify and verify the workshop configuration before promising that result.
- The solar activity should receive a kit-specific technical check: it connects a panel while an adapter substitutes for a battery, then temporarily removes adapter power despite warning against panel operation without a battery. Resolve the procedure using the actual controller/adapter documentation and verified setup; this review has not established electrical compatibility.

## Recommended implementation order

1. Correct the float-failure claim and scope of protection; resolve test interference and recovery instructions.
2. Reconcile the actual schedule, required outcomes, and parallel presentation format.
3. Complete the participant assets, cloud workflow, facilitator run sheet, and readiness checks.
4. Add the fourth role and individual learning evidence.
5. Strengthen the farm example, personal design option, pilot plan, and take-home route.
6. Synchronize the worksheets, record sheet, reference, course design, and preparation backlog.

Do not redesign the entire course or add another large technical build. Its experiential structure is the strength. The goal is a reliable delivery package with accurate claims and a clearer route from classroom learning to farm application.

## Completion evidence to report

- Files changed and which review items they address.
- A reconciled schedule with explicit required and optional activities.
- Remaining decisions that require the responsible instructor or kit-specific verification.
- Checks actually performed: document consistency, links/assets, print layout where applicable, and any real hardware/classroom rehearsal results.
- Clearly distinguish completed verification from proposed tests. Do not claim the workshop has been rehearsed or hardware behavior verified unless that work was actually performed.

---

## Response (8 September 2026)

Reviewed against the repository at `c05bccb` and acted on the same day. Verified by document
consistency checks and a MkDocs build. **No classroom rehearsal and no new hardware test was
performed for this response**; items that need the bench are listed as open below.

### Accepted and done

| Item | Where |
|---|---|
| P0-2 timers | Fail-safe 4 now 15 s, Fail-safe 2 stays 30 s; the test names which notification must appear first (`docs/session-2.md`, COURSE-DESIGN) |
| P0-3 manual start paths | Fail-safe 1 gains a second trigger (pump switch → On, condition float Dry) so dashboard and onboard-button starts with no water are switched back off; a callout names what stays unprotected when HA is down; a "who catches what" table lists wire fault / board loss / no-vibration / overrun / HA loss (`docs/session-2.md`) |
| P0-4 recovery | One callout after Fail-safe 2: after a cutoff the pump does not restart until the value crosses the threshold again, which is why every cutoff carries a notification. Reload/restart timer behaviour deliberately left out for this audience |
| P1-5 schedule | Session 3 now 20 + 20 + 10 + 45 + 45 + 10 = 150 in both `docs/session-3.md` and COURSE-DESIGN, with the energy block added to the timetable |
| P1-6 presentations | 30 min design, 5 min paired pitches with two feedback questions, 10 min plenary of three or four nominated teams |
| P1-9 fourth role | **Tester**: predicts, times, calls pass/fail, holds the phone dashboard, walks over for the sabotage. `docs/index.md`, record-sheet rotation table, COURSE-DESIGN, and every "จับเวลา" step in Session 2 |
| Pass criterion | Failure-lab self-check now requires Fail-safes 1 and 2 both demonstrated |
| P2-11 own farm | One-sentence farm problem written at the start of Session 1 on the record sheet; scenario card E "ฟาร์มของเราเอง" in Activity 8 |
| P2-13 pilot plan | Five lines added to the design canvas after the budget block |
| Smaller fixes | Record-sheet cloud question relabelled Activity 7; COURSE-DESIGN design challenge renumbered Activity 8 and the dashboard block labelled Activity 7; Session 3 retrospective now says the paired team switched the laptop's WiFi off; record-sheet history block moved after energy to match the worksheet; dashboard plan has five rows |
| Offline claim | COURSE-DESIGN corrected: laptop SSIDs need internet all three sessions (web.esphome.io, worksheet site); only the cloud push *activity* depends on it. Matches NETWORK-REQUIREMENTS acceptance test 7 |
| Activity 4 | Kept as the timing buffer but given a short form that is never cut (one card, relay and pump spec only) |
| Solar step 4 | Now an instructor-only demo on the projected kit; teams do not pull the adapter with the panel connected |

### Accepted with a correction to the review

**P0-1 float switch.** The review read the committed firmware. The float cylinder was flipped on
8 Sep 2026 (`ea4f7e2`, `4a3a511`, `c05bccb`): firmware is `inverted: true` with
`device_class: moisture`, HA shows Wet/Dry, and an unplugged switch reads Dry on the bench. The
worksheet's claim is now accurate: a cut wire reads Dry, a dead board reads unavailable, neither
is Wet. Remaining: the re-flash checks in TEST-PLAN test G second pass, and "flip every float" on
the kit-prep list (COURSE-DESIGN open decisions).

**18650 cell** was a "smaller fix" in the review; it is bigger. The GoGo-IoT has a battery
path with source selection, so a charged cell keeps the board running when USB is pulled, and
sabotage card 1, the Fail-safe 3 test and the Session 3 adapter note all expected a pulled cable
to make the board `unavailable`. Decided (Roger, 8 Sep 2026): the cell stays in the kit, and every
power-loss step now says **switch the board off**. The adapter demo now shows the sensor board
surviving on its cell, which is scenario D's night-time node.

### Declined or deferred

- Home Assistant `for:` timers across reloads and restarts: out of scope for this audience.
- In-session worked farm example (P2-12): no session time; added to the backlog as a take-home page.
- Placeholder images (P1-7): known and deliberately parked until the text settles; not reordered.
- Cloud procedure (P1-8): blocked on กำพล's tool choice; recorded as an open decision, not invented.
- Facilitator run sheet (P1-10): already on the production list; backlog entry expanded.

### Still open, needs the bench or a decision

- TEST-PLAN test G second-pass re-flash checks.
- Bench check that switching the GoGo-IoT off makes its entities `unavailable` within seconds and that switching it back on needs no re-adoption.
- Adapter-out demo with the panel connected: one bench check of the LOAD pair and USB when the
  controller is to hand (not available on 8 Sep), before it is shown on the projector.
- Cloud push tool and procedure.
- Post-tests, scenario cards, role cards (Tester text), price sheet, install guide, take-home page.
