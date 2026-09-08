# Session 2 and workshop review — updated handoff for Claude

## Scope and authority

This handoff incorporates the latest user corrections to the review of Session 2 and the complete workshop. It supersedes conflicting recommendations in `WORKSHOP-REVIEW-FOR-CLAUDE.md` and the preceding conversational review.

The user explicitly clarified:

1. Use Home Assistant's existing **device pages** in Session 2. Build dashboards in Session 3, where dashboard design is a main topic.
2. Treat changing the load as a **simple two-wire exchange**: disconnect the lamp's positive and negative leads, then reconnect the pump's positive and negative leads. Do not present it as rebuilding the circuit or assume each exchange requires five minutes.
3. Make automation disabling and restoration explicit. Check whether students were instructed to disable rules before working on the lights.

The user requested this file for Claude to read and act upon. The worksheets have not been changed as part of this handoff. Read the latest working files before editing and preserve the user's recent changes, including screenshot links and the time-condition explanation.

The review was based on documents, firmware, and selected screenshots. It was not a new hardware test or a rehearsal with beginners.

## Overall assessment

The workshop progression is coherent: investigate sensors, operate a pump, make decisions manually, automate, investigate failures, interpret data, and design a farm system.

Session 2's new screenshot walkthrough and time-condition experiments improve the learning experience. The remaining concern is the amount of required work, particularly four paired failure rounds plus implementation of protections. Moving dashboard construction entirely to Session 3 saves work and avoids introducing dashboard design twice.

Do not repeat earlier findings that are now resolved:

- The float cylinder is now flipped during preparation, and `inverted: true` matches wet = closed circuit. A disconnected wire now reads Dry. See the current firmware and the second-pass bench notes in `TEST-PLAN.md`.
- Failed-operation detection uses 15 seconds, before the 30-second maximum-runtime cutoff.
- Four roles now exist.
- Session 3 now includes paired presentations, the participant's own farm option, and a pilot plan.
- The Session 3 timetable now fits arithmetically; the previous 155-minute activity total is obsolete.

## Required change 1 — Use device pages throughout Session 2

Sources: `docs/session-2.md`, Activity 5 “แผงควบคุม” and Activity 6; `docs/session-1.md`, device adoption and observation.

Remove the required construction of the five-item dashboard control panel from Session 2. Do not solve the Failure Lab's missing sensor information by adding dashboard cards.

Use the existing workflow:

- **Settings → Devices & services → ESPHome → the team's GoGo-IoT device** for humidity, float status, availability, and other sensor values.
- The corresponding **relay device page** for the relay switch and its reported state.
- **Settings → Automations & scenes** to enable or disable rules and open their editors/Traces.

These are two separate devices, so do not imply that one device page contains both boards. Explain a simple arrangement, such as two browser tabs, or the sensor page on the laptop and relay page on the team's phone. Do not make successful phone access a prerequisite for the lab: two tabs are sufficient.

Update Session 2's references to “watch the dashboard” to identify the actual device page(s) participants should observe. Update the matching record-sheet column and instructions, role descriptions where relevant, and course/overview descriptions.

Preserve the distinction between the relay's commanded/reported switch state and the pump's physical operation. The pump can fail while the switch still shows On. Specify when students may inspect the physical pump to complete the “what did the pump do?” record; the current instruction forbids looking at the equipment during the observation round.

Acceptance:

- No custom dashboard or control-panel construction is required in Session 2.
- Students can find humidity, float state, and relay state using existing device pages.
- Dashboard design and card construction remain a main activity in Session 3.
- The automation-enable/disable lesson remains, using the Automations page instead of a new control panel.

## Required change 2 — Explicit automation states at every transition

### Answer to the user's question

**No: the current light-change instructions only say to set the relay to Off. They do not instruct students to disable the existing low-water automation.**

At the start of Session 2, the normal sequence has created only `น้ำหมด หยุดปั๊ม`. The two humidity-based watering rules do not exist yet. Do not tell beginners to find and disable rules they have not created.

Turning a relay Off and disabling an automation are different actions. The existing low-water rule can still switch the relay off if the float changes to Dry during the lighting experiment.

### Required transition sequence

| Point in the lesson | Required rule state | Required action |
|---|---|---|
| Before changing from pump to lamp | Disable the existing `น้ำหมด หยุดปั๊ม` rule. If repeating the lesson, also disable any other existing rules that command this relay. | Set the relay Off on its device page, then exchange the load leads. |
| While testing the lamp | Enable the applicable lighting rules; keep the pump-related rule disabled. | Observe light and relay behavior. |
| Before changing back to pump | Disable both `มืด-เปิดไฟ` and `สว่าง-ปิดไฟ`, including their added time triggers. | Set the relay Off, then exchange the lamp leads for the pump leads. |
| After the pump is connected and submerged, with the hose returning to the same container | Re-enable `น้ำหมด หยุดปั๊ม`. | Confirm the float reads Wet, then create and test the two watering rules. |
| After the exercise that temporarily disables `รดน้ำ - เปิดปั๊ม` | Re-enable that rule and confirm both watering rules are enabled. | Leave both lighting rules disabled. |
| Before each initial Failure Lab round | Confirm the intended pre-protection rules are enabled and both devices are connected. | Use the relay device page to set the pump On deliberately. |
| After upgrading the low-water rule | Use its new name, `Fail-safe - น้ำหมด`. | Avoid referring to the old and renamed rule as two separate rules. |
| At the end of Session 2 | Disable the automatic watering-start rule, then set the relay Off; keep HA recording. | Preserve the corresponding restoration instruction in Session 3. |

Important sequencing detail: the initial Failure Lab deliberately demonstrates the limitations of the original low-water rule. Do not install the improved manual-start protection before the fault that is meant to expose that limitation.

Suggested concise Thai instruction before the lighting exercise:

> ไปที่ **Settings → Automations & scenes** แล้วปิดการใช้งานกฎ `น้ำหมด หยุดปั๊ม` ชั่วคราว จากนั้นเปิดหน้าอุปกรณ์บอร์ดรีเลย์และสั่งรีเลย์เป็น **Off** ก่อนเปลี่ยนจากปั๊มเป็นหลอดไฟ การปิดกฎกับการสั่งรีเลย์ Off เป็นคนละขั้นตอน ต้องทำทั้งสองอย่าง

Suggested restoration instruction after reconnecting the pump:

> ตรวจว่าปั๊มจมน้ำ ปลายสายยางกลับลงถังเดิม และลูกลอยแสดง **Wet** แล้วเปิดใช้งานกฎ `น้ำหมด หยุดปั๊ม` อีกครั้ง โดยยังปิดกฎไฟสวนทั้งสองข้อไว้

Acceptance: at each transition, participants know which rules exist, which should be enabled, and what the relay's starting state must be.

## Required change 3 — Describe the load exchange simply and consistently

The current worksheet leaves the pump's negative lead connected when changing to the lamp, then reconnects only the pump's positive lead on the return. The user now specifies exchanging both load leads. Update both directions so the text matches that choice.

- Pump to lamp: remove pump positive from NO and pump negative from the negative row; connect lamp positive to NO and lamp negative to the negative row.
- Lamp to pump: remove both lamp leads and reconnect both pump leads to the corresponding terminals.
- Keep the established controller, terminal-block, relay COM, and board-power wiring in place.
- Keep the automation-disable and relay-Off steps distinct from the physical exchange.

Remove the fixed “two swaps of roughly five minutes each” assumption from the worksheet and supporting timing descriptions. Measure the exchange during rehearsal rather than treating ten minutes as a known requirement. The principal time pressure is software construction, testing, discussion, and recovery.

## Remaining Session 2 fixes

### 4. Make the time-condition experiments repeatable

Source: `docs/session-2.md`, Activity 5(c).

Preserve the new conceptual explanation and the use of Traces. Add explicit experiment resets:

- Before each new light-threshold test, uncover the sensor, wait for a reading above the relevant threshold, and confirm the lamp is Off before covering it again.
- When repeating Test 3 after adding the time trigger, choose a new future start time and update **both After and At**. A previously elapsed trigger time will not repeat just because the condition was edited.
- Give enough lead time to save the configuration before the selected time arrives.
- Test the **Before** cutoff as well as the scheduled turn-on.
- Verify the route to Traces against the workshop VM. The supplied completed-editor screenshot shows a direct Traces button near the top; do not force an unverified menu route.

The current Home Assistant illuminance trigger really is a crossing trigger. The menu change itself is not an error. General State/Numeric state triggers still exist, but the worksheet should explain how to reach them when moving from the new target-based walkthrough to later instructions.

Reference: https://www.home-assistant.io/triggers/illuminance.crossed_threshold/

### 5. Align the hysteresis test with the record sheet

The worksheet now uses a subjective “no repeated flickering” pass criterion, while the record sheet still asks for transition counts over one minute.

Keep a simple measured before/after comparison and also verify:

- Sufficiently dark → lamp turns on.
- Sufficiently bright → lamp turns off.

A lamp that never switches must not pass merely because it does not flicker. Ensure the chosen thresholds are reachable using the measured light/dark readings.

### 6. Clarify the remaining fail-safe limits

Source: `docs/session-2.md`, Fail-safe 1 and the failure-summary table.

- Separate a **disconnected wire** from a **mechanically stuck float**. The revised wiring makes an open wire read Dry, but a float stuck in its raised position can remain Wet.
- Describe the Wet condition as preventing a new automatic start. Do not imply that it alone stops a running pump when the sensor becomes unavailable.
- Describe vibration as evidence of movement, not proof that water is reaching the crop.
- For the optional sensor-loss experiment, verify the cause of shutdown using Traces or the specific notification. The 30-second runtime cutoff could otherwise stop the pump and make the sensor-loss rule appear successful.
- Keep HA-dependent protection distinct from protection that works when HA or the network is unavailable.

### 7. Use a deterministic Failure Lab starting state

Do not tell teams to raise the humidity threshold as the primary way to make the pump run. Use the relay device page to start it deliberately, while preserving the intended rules for that stage of the lesson.

For each fault, state the starting condition, observation interval, expected evidence, and restoration procedure. Identify which paired team acts first, so both teams do not simultaneously wait for the other to intervene.

## Timing: reassess after removing dashboard work

The documented slots are 180 minutes each: **150 teaching minutes + 15-minute break + 15-minute post-test**.

| Session | Current planned teaching time | Assessment |
|---|---|---|
| 1 | 20-minute opening + 130 minutes of activities | Fits exactly; setup and troubleshooting need to be included within those blocks. |
| 2 | 15 + 75 + 45 + 15 = 150 minutes | Fits on paper. Removing dashboard construction saves time. The expanded time-condition lesson and four paired failure rounds still need rehearsal. |
| 3 | 140 minutes of activities + 10-minute wrap-up | Fits on paper. Cloud setup, equipment return, and group movement remain uncertain. |

Four faults performed in both directions create eight intervention/observation turns, plus restoration, diagnosis, and construction of protections. That is the main uncertainty in the 45-minute Failure Lab.

**Do not automatically cut the user's new time experiments or reduce the number of fault rounds.** The previous recommendation to move the time lesson to an instructor demonstration and assign only two faults per team was a possible way to fit the schedule, not a decision accepted by the user.

First remove Session 2 dashboard work and the inflated load-swap assumption, then produce a revised internal time breakdown. If rehearsal still overruns, identify options explicitly:

- Full participant time-condition experiments versus a shared demonstration.
- Four faults per team versus assigned faults followed by shared findings.
- Required low-water and maximum-runtime protections versus optional sensor-loss/vibration extensions.

Do not claim these timings have been verified without an actual timed run.

## Whole-workshop consistency and remaining gaps

### 8. Synchronize the plans with the worksheets

Update `COURSE-DESIGN.md`, `SESSION-OVERVIEW.md`, `WORKSHEET-TODO.md`, and participant documents together where applicable:

- Remove Session 2 custom control-panel construction and its learning-goal claims. Goal 6 still has preliminary exposure through device values/history and phone control; dashboard construction is in Session 3.
- Resolve whether the expanded time-condition experiments are core or optional. The course plan currently describes time conditions as stretch work, unlike the current worksheet.
- Resolve the spec-activity mismatch: Session 1 says it must not be skipped, while the course plan still allows it to become homework.
- Keep the new lighting rule names consistent: `มืด-เปิดไฟ` and `สว่าง-ปิดไฟ`. If arbitrary names are permitted, make later references understandable.
- Preserve the latest board-power arrangement: the relay board uses the controller's USB port, not its 7–60 V input. Do not reintroduce older wiring from stale notes.

### 9. Finish the cloud procedure before promising the outcome

Session 3 promises remote access, while the backlog says the service/procedure is still awaiting the responsible instructor's choice. Define the service, prerequisites, per-team identity, published data, update interval, whether access includes control, and the fallback.

Do not silently choose or commit to an external service on the instructor's behalf. Without the workflow, the 45-minute dashboard/cloud block cannot be timed reliably.

### 10. Resolve the solar demonstration against the actual kit

Session 3 explicitly proposes an instructor demonstration using a disconnection order that the worksheet says the controller manual prohibits. Instructor-only delivery does not establish electrical compatibility.

Verify the exact controller and adapter arrangement, and revise or replace the demonstration if necessary. Preserve the learning objective about energy storage and independent battery power. Do not invent successful bench verification.

### 11. Complete the delivery materials

The backlog still lists specification/scenario cards, price sheets, individual post-tests, facilitator instructions, and other assets as unfinished. Many images and take-home QR destinations remain placeholders, though the first lighting-automation screenshots are now real and should be retained.

At 100 groups, materials and recovery instructions affect timing directly. Confirm facilitator assignments, help requests, spare kits, checkpoint recovery, and water/equipment restoration procedures.

### 12. Complete the bridge to farm use

The own-farm scenario and pilot plan already exist: preserve them. The remaining gap is a worked example connecting a farm problem to sensor placement, interpretation, a justified control rule, equipment choice, and maintenance.

Keep the air-humidity stand-in clearly identified. Classroom thresholds should not become recommendations for actual irrigation. The worked example can be take-home material rather than another required technical build.

## Copy edits

In Session 2, correct `กฏ` to `กฎ`, `โดอย` to `โดย`, `ชีวิติจริง` to `ชีวิตจริง`, `หลาดไฟ` to `หลอดไฟ`, and standardize `เซนเซอร์`.

Preserve the user's clearer explanations and screenshots. This is not a request to rewrite the entire course again.

## Implementation priorities and evidence

1. Remove Session 2 dashboard construction; establish device-page observation.
2. Fix rule-disable/restore sequencing and describe the two-wire load exchange consistently.
3. Make time experiments and Failure Lab resets reproducible.
4. Align the hysteresis records and narrow the remaining fail-safe claims.
5. Reconcile schedules and supporting documents; list unresolved instructor/hardware decisions separately.

Report files changed, checks performed, and decisions still pending. Verify names, links, screenshots, activity/record-sheet correspondence, and the intended rule states at each transition. Distinguish document review from real hardware or classroom rehearsal.
