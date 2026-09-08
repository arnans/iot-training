# Session 3 review and proposed revisions

Reviewed 8 September 2026 against the current `docs/session-3.md`, `docs/record-sheet.md`, `COURSE-DESIGN.md`, `SESSION-OVERVIEW.md`, `WORKSHEET-TODO.md`, and `hass/configuration.yaml`.

Audience: 400 participants in 100 teams of four; farmers and interested individuals. This is a review handoff, not an approved rewrite of the schedule. Preserve the user's current edits. Recommendations below are proposals unless explicitly identified as user preferences.

## Overall judgment

The content fits the learning outcomes, but the required work is too dense for reliable delivery at this scale. The current schedule totals exactly 150 teaching minutes: communications 20, power 20, history 10, dashboard 45, design 45, wrap-up 10. The separate 15-minute break and 15-minute post-test fill the three-hour slot. There is no allowance for getting ready, troubleshooting, transitions, saving work, or equipment return.

The strongest progression is **read evidence from the morning → build a useful dashboard → plan a small farm application**. These should be the three main participant activities. Communications and power should support those decisions through short explanations or demonstrations.

The user explicitly wants to keep the history graph. They are considering presenting Nabu Casa themselves and question the educational value of the solar test without a battery. Do not treat those questions as authorization to remove every related topic.

## 1. Reduce required work while retaining the learning outcomes

- **Keep and expand history interpretation to 25 minutes.** It connects directly to experiments participants performed and shows why recording matters to farm management.
- **Keep dashboard building**, with a functional minimum and one usability check. Make visual polishing optional. Combine the internal-member check and neighbouring-team check into one short test by a person who did not build the page.
- **Replace individual cloud setup with a prepared instructor demonstration** inside the dashboard block.
- **Condense the communications survey.** The current 20-minute block includes YAML inspection, IP lookup, opening the device website, six communication families, a 30-cell comparison table, three protocols, and a local/cloud comparison. That is more than a short introduction. Give teams a completed comparison reference; teach selection through one worked farm example. Keep distance, available power, data needs, and cost as the decision criteria. Move detailed protocol explanations and the full vocabulary survey to reference material. A reference table should include assumptions and limitations rather than present universal high/medium/low rankings.
- **Keep the farm design and paired feedback; remove the required plenary pitches.** The current two rounds serve different purposes, but only the paired exchange gives every team feedback. It also avoids nomination and microphone transitions. The instructor can mention one or two observed ideas during wrap-up if time permits.
- **Make power a 10-minute instructor-led explanation/demo**, with the narrower purpose described below. Remove participant panel wiring and battery-menu exploration from the required path.

These changes retain Goal 6 through history, dashboard construction and usability testing; Goal 4 through a justified communication choice and local/remote reasoning; and Goals 2 and 5 through the farm design.

### Proposed timetable

| Time | Work | Minutes |
|---|---|---:|
| 13:00–13:05 | Readiness: recording available, equipment in the expected state | 5 |
| 13:05–13:30 | Interpret the team's Session 2 history | 25 |
| 13:30–14:15 | Dashboard: 5 min plan, 25 min build, 5 min usability test, 10 min remote-access demo | 45 |
| 14:15–14:25 | Power: identify the supply/storage/load roles and discuss one farm example | 10 |
| 14:25–14:35 | Recovery time for unfinished work and questions | 10 |
| 14:35–14:50 | Break | 15 |
| 14:50–15:35 | Farm design: 10 min worked communications choice, 30 min team draft, 5 min paired feedback | 45 |
| 15:35–15:45 | Brief recap, save answers and return equipment | 10 |
| 15:45–16:00 | Organizer post-test | 15 |

Total: 150 instructional/operational minutes, 15-minute break, 15-minute post-test. This is a proposed budget, not a measured completion time. Validate dashboard construction and packing with a novice group using the actual VM and kit. If packing takes longer, use the recovery allowance or move the feedback survey outside the teaching slot; do not borrow from the post-test.

## 2. Preserve history, improve what participants infer from it

The current four-event search is a strong starting point. Give it enough time for interpretation rather than only filling counts and extrema.

Ask each team to identify two events, explain the likely cause from its experiment, and name one decision the graph would support on a farm. For example: repeated relay switching suggests revisiting control thresholds; missing readings mean the historical record cannot establish what happened during that interval.

Correct these details:

1. **Relay On is not proof the pump ran.** The same relay controlled the light earlier that morning. Restrict any pump-command count to the period after reconnecting the pump, using a recorded changeover time. Label it as a command count; physical operation needs separate evidence. This reinforces the Session 2 disconnected-pump fault.
2. **Do not promise every team's trace contains every illustrated pattern.** Chattering may not have happened; short failures may not produce a clearly visible gap. Allow “not observed” and provide an instructor example for missing patterns. Ask what evidence is available rather than require an invented count.
3. **Explain the displayed time window versus available data.** A 24-hour graph contains only the data actually recorded. Start with “since this morning” where useful, then explain why a farm would use a longer window.
4. **Protect the dependency on Session 2 data.** Keep the VM recording through lunch where practical, and provide a sample graph if a laptop slept, restarted, or lost its history. Do not make a failed recorder block dashboard learning.
5. Keep the missing-overnight-history question. It gives a concrete reason for an always-on Home Assistant host at the farm.

Suggested Thai framing:

> เลือกเหตุการณ์บนกราฟสองช่วง แล้วอธิบายว่าแต่ละช่วงตรงกับการทดลองใดของทีม ถ้าเห็นลักษณะนี้ในฟาร์มจริง เราควรตรวจสอบหรือปรับอะไรต่อ?

## 3. Replace the vague cloud exercise with Nabu Casa remote access

The present section promises an unspecified cloud service, each team's URL, chosen values and transmission interval. That is not a complete activity and should not remain a required deliverable.

Nabu Casa's remote-access feature lets users reach their existing Home Assistant instance. In this activity, the local instance still runs the dashboard, automation and recording; participants are not building a second cloud dashboard or configuring a telemetry publishing interval. [Official remote-access instructions](https://support.nabucasa.com/hc/en-us/articles/26474279202973-Enabling-remote-access-to-Home-Assistant).

### Recommended instructor demonstration, 10 minutes

Prepare the instructor account and connection before the session. Do not spend class time creating 100 accounts or waiting for initial provisioning.

1. Show **Settings → Home Assistant Cloud**, the signed-in account, enabled **Remote access**, and the generated remote URL.
2. On the instructor's phone, turn WiFi off and use mobile data.
3. Open that URL, sign into Home Assistant if prompted, and show the same dashboard.
4. Change a sensor input so participants see a new reading arriving. Demonstrate one controlled pump command on the prepared kit if appropriate.
5. Ask what still works if the farm loses internet while its local WiFi and Home Assistant remain running. Also ask what changes if the Home Assistant host itself stops. Do not equate those failures.

The official instructions describe the remote-access toggle and URL, and note that initial setup can require waiting. Prepare a short recording as a fallback. A talk using screenshots is acceptable if live demonstration is impractical, but the stated outcome must then be “explain how remote access works,” not “each team tested access from outside the farm.”

**Concrete configuration gap:** `hass/configuration.yaml` intentionally omits both `default_config:` and `cloud:` and labels Nabu Casa unused. Enable `cloud:` on the instructor demonstration instance and reconcile its setup instructions. There is no need to restore the full `default_config:` or enable cloud on every team VM for this demonstration. [Official cloud configuration](https://www.home-assistant.io/integrations/cloud/).

Rename the section to **ดูข้อมูลฟาร์มจากนอกพื้นที่ด้วย Home Assistant Cloud**. Replace the publishing-interval/sender fields with two observations: what connection the phone used, and what remains available when the farm's internet fails. Mention that ongoing cloud access is a subscription service; do not imply it is a free permanent part of the open-source installation. [Nabu Casa](https://www.nabucasa.com/).

## 4. Keep the useful charger lesson; replace the batteryless experiment

There is educational value in the charger already used by the kit:

- Recognize the panel, battery and load connections, and the 5 V USB outputs.
- Distinguish producing energy, storing energy and supplying a load.
- Explain that a controller acts on measured values; a battery icon is an estimate, not direct knowledge of stored energy.
- Explain why different devices need backup power. A sensor board surviving on its internal cell does not keep the relay, router or Home Assistant host running.
- Connect power planning to the farm design: what must remain available overnight or through poor weather?

These points justify a short demonstration. They do not require every team to move a panel toward a window or navigate battery menus.

### Problems with the current test

- Unplugging the adapter removes the kit's supply. It does not reproduce sunset in a correctly configured battery-backed solar system, nor measure autonomy.
- The worksheet explicitly says that the demonstration violates the controller's disconnect sequence. Instructor-only delivery does not resolve that contradiction. Remove this step.
- Indoor/window current may be indistinguishable from zero, making the comparison inconclusive. Do not depend on it for the learning outcome.
- The exact controller model/manual and the adapter's suitability with PV connected need confirmation. An adapter supplying the BATT terminals is not automatically an approved substitute for a battery during charging. Treat this as an unresolved equipment-specific prerequisite, not a proven safe or unsafe configuration.
- Do not teach “18650 means select b02” as a sufficient battery-selection rule. Compatibility needs the actual cell chemistry, pack voltage/series count, protection, charging settings and controller specification. Remove that shortcut from beginner instructions.

### Practical replacement

With the existing kit, keep the panel disconnected and use the controller to identify terminals, trace loads and read the supply voltage. Explain storage with a diagram and a concrete question: “Which parts of this system need power if we want to keep recording all night?”

If a live solar comparison is desired, prepare a separate manufacturer-compatible controller/battery/panel demonstration. Compare illuminated and shaded panel conditions with the battery connected throughout, using the documented procedure. Demonstrate only observations that can be reproduced at the venue. Otherwise use a recorded demonstration. Battery and panel sizing can remain further study.

For scenario D, distinguish powering sensors/communications from sizing a solar irrigation pump. The 15 W workshop panel is not evidence that a farm pump's energy needs have been addressed.

## 5. Make the farm design achievable and useful

The existing canvas already includes costs, failure handling, maintenance and a pilot plan. Preserve those strengths. The risk is asking novices to research unfamiliar equipment and finish a defensible specification in 30 minutes.

- Supply the promised short equipment/specification/price sheet. Mark prices as dated examples. Make live shopping optional.
- Define success as a **first pilot**, with one clear farm problem and a manageable control or monitoring task. Do not require a complete commercial installation design.
- Prefer the team's own farm or a supported basic scenario. Hydroponic EC/pH and a remote solar pump introduce specialist dependencies; mark those cards as advanced or give them extra reference information.
- Allow teams to record an assumption or an item needing expert verification. Reward recognizing missing information.
- Keep the paired pitch at five minutes: one minute each, then three minutes for feedback and a noted revision. A useful second question is “If this component or connection fails, what happens next?”
- Ensure the transfer to farming is explicit: the workshop's air-humidity thresholds demonstrate control logic; they are not a ready-made irrigation prescription for soil and crops. The farm design should select an appropriate measurement for its actual decision.

## 6. Synchronize implementation and acceptance checks

If these proposals are adopted, update `docs/session-3.md`, matching fields in `docs/record-sheet.md`, `COURSE-DESIGN.md`, `SESSION-OVERVIEW.md`, and `WORKSHEET-TODO.md` together. Preserve the form-field conventions; remove obsolete cloud/solar questions consistently. Revise learning-outcome wording and post-test expectations if remote access becomes demonstration-only.

Also fix the equipment-return sequence: disable the pump-start automation and any other rule that could energize the relay, command the pump Off, then isolate power before draining and dismantling. The present checklist starts with Off and draining while automation is still enabled.

Before delivery, confirm:

- One novice team can finish the minimum dashboard and usability check in the allocated build time.
- The instructor remote demonstration works from mobile data on the actual workshop network and VM; a backup recording is available.
- History examples exist, and the relay history is not mislabeled as measured pump operation.
- The chosen power demonstration follows the actual equipment documentation and has a reproducible observation.
- The equipment price sheet, example farm plan, screenshots and take-home links replace placeholders.
- The revised schedule includes transitions, saving and packing as well as teaching.

The likely farmer takeaway should be: “I can see what happened, operate a readable dashboard, explain how I would check the farm remotely, and plan a small trial with costs and failure handling.” That is a credible outcome for this session. Independent remote-access deployment and solar-system engineering should not also be promised within the same time.
