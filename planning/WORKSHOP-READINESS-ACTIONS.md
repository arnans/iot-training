# Workshop blockers — recommended actions, 19 September 2026

The organizer requested recommendations for blockers and implementation of Thai-language and
coherence improvements. The latter have been applied to source worksheets, record sheet, front
page, help confirmation and instructor notes. The blockers below remain open; this is an action
plan, not a claim that the workshop is verified.

## 1. Participant preparation — choose a supported route before distributing the guide

Recommended: distribute the existing x86-64 route after a clean-machine test. For Apple Silicon,
either supply a tested ARM64 image or explicitly arrange a shared supported laptop for affected
teams. Do not leave a clickable TODO download as if it were available. Confirm platform numbers
from registration before committing to the fallback.

Replace TODO file sizes with actual sizes, capture the three installation screenshots from the
tested VM, publish the installation-confirmation form, and name a support contact. Test all links
without an organizer's signed-in account. The guide requires confirmation three days before the
workshop, so this must be completed before that deadline.

Acceptance: a participant can download, import, start the VM and reach its login page using only
the published guide; the confirmation form accepts their response.

The final answer-submission destination is a separate decision. On 19 September the organizer
said it will be decided later, most likely a form. Current wording correctly defers to the
instructor's announced channel. Once decided, add the link to the front page, Activity 8 and
record sheet; test JSON uploads and the receipt/TA verification process.

## 2. Progress tracking — implement one explicit course schema

Recommended code change:

- Define the complete required activity/task list for each session independently of data received.
  Include preparation and closing checklists deliberately; distinguish them from activities in labels.
- Represent unvisited required tasks as pending. Never infer session completion from the longest
  report received. Derive order from the schema, not whichever device or team happens to report first.
- Normalize all `hist-*` field sections to `hist` before counting, so each answer counts once and
  history has one completion denominator.
- Mark Activity 3.6 optional in task metadata. Display it separately and exclude it from required
  completion. Do not require a participant to tick something they skipped.
- Use stable task IDs. For multiple devices, combine checkbox state per task, then derive both
  activity totals and sub-step bars from that same merged state. Keep the existing any-device policy
  explicit: unchecking one device does not clear a check still present on another. One recorder is
  the participant workflow now stated in the worksheet.
- Version the progress schema or filter older reports so rehearsal data with index-based steps
  cannot distort new counts. No deletion of historical data is necessary.

Acceptance checks: Activity 1 alone never completes Session 1; disjoint activity reports remain
visible; history completes after its four tasks; skipping the optional timer does not block
completion; two devices ticking different tasks produce matching summary and detail totals;
unchecking, reload and reconnect preserve the chosen policy. Then use a designated rehearsal date
and team to verify a real write, both dashboard screens, offline recovery and help acknowledgement.

## 3. Activity 4.7 — preserve the measurement field

Recommended minimal change: keep `s1.hum.room` and change the instruction to review the room
measurement, rather than enter a threshold. Continue storing thresholds in the existing
`s2.hum.on` and `s2.hum.off` fields. No new field or migration is needed.

Suggested Thai:

> ทบทวนค่าความชื้นอากาศในห้องที่บันทึกไว้: … % จากนั้นดูค่าปัจจุบันในหน้าอุปกรณ์
> แล้วใช้ค่านี้เลือกเกณฑ์เปิดและเกณฑ์ปิดในขั้นตอนถัดไป

Acceptance: entering either watering threshold does not alter the Activity 1 measurement or its
record-sheet entry; the summary and detailed instructions use each field with the same meaning.

## 4. Power lesson — teach an estimate, then identify what must be checked

Recommended changes before teaching:

1. Keep `W = V × A` for the DC example. For the AC example, state “สมมติว่าปั๊มใช้กำลังไฟฟ้า
   ขาเข้า 1,100 W ตามสเปก” instead of deriving watts from `220 V × 5 A` without a power factor.
2. Label battery and panel calculations as preliminary, ideal estimates. State battery voltage,
   assumed usable fraction and peak-sun hours explicitly. Include conversion losses, reserve,
   temperature/aging and required autonomy when selecting real equipment. Round capacity up:
   at 80% usable capacity, the 400 Wh / 12 V example needs at least 41.7 Ah before other allowances,
   so a 40 Ah purchase recommendation does not meet even that assumption.
3. Treat three peak-sun hours as an illustrative assumption to replace with local seasonal data.
   If a pump runs directly from solar without a battery, verify instantaneous running and starting
   power as well as daily energy; a daily Wh balance alone is insufficient.
4. Remove the 390 W assertion until the instructor confirms the exact controller model and which
   rating it describes. The 12 V 10 A kit listing is not evidence for 390 W load output. Explain
   that the inverter's battery connection and ratings are separate from the controller's load output.
5. Verify battery comparisons against chosen product specifications, including BMS availability,
   usable capacity and charge settings; do not imply that the cell shape 18650 identifies NMC chemistry.

Language fixes already distinguish starting *power* from energy; the numeric sizing corrections
above remain proposed. Acceptance: the instructor can work through both examples with consistent
units/assumptions and explain why the result is not a final shopping specification.

## 5. Dry pump — verify the model before setting exercise durations

Recommended: obtain the exact pump model/manual and confirm whether dry running is allowed,
the maximum continuous duration, and cooling/repetition limits. Then bench-rehearse the full
sequence under those limits. Do not validate an unknown limit by deliberately running the pump
until it overheats or fails.

If supported, make the initial observation in 5.4 shorter than the verified limit and assign one
observer to stop it on time; include all the earlier humidity tests and the 15/30-second rules in
the same operating plan. Do not leave it running while editing or discussing.

If dry running is prohibited or undocumented, use the LED as the load for prolonged rule tests
and redesign the vibration exercise around a suitable load or instructor demonstration. If water
operation is chosen instead, restore the necessary containers, tubing and handling instructions
consistently rather than changing just one sentence. The choice requires the actual kit details.

## Final rehearsal

After the fixes, regenerate the renders and run the existing checks plus the regression cases in
item 2. Rehearse the whole participant path on representative hardware and venue WiFi. Time
Activities 4, 5 and 7 with a novice-paced group, prepare recovery states and a sample history graph,
and verify answer-file submission separately from live progress. Sign off only after recording
the results and unresolved limitations.
