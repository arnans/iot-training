# Workshop readiness review — 19 September 2026

**Follow-up implementation:** Thai wording and coherence changes were applied after this review,
including Manual-mode boundaries, history fallback/hypothetical framing, cloud-access wording,
two design prompts mirrored on the record sheet, a single-recorder workflow, answer-file receipt
instructions, and accurate help-request confirmation. Participant and instructor HTML was regenerated.
The organizer deferred the submission destination (likely a form). The blockers remain proposals;
see [recommended actions and acceptance checks](../planning/WORKSHOP-READINESS-ACTIONS.md).
Existing form, step/anchor and progress tests pass after the changes; the known completion bugs
remain reproducible and are not covered by those existing tests.

**Verdict: close, but not ready for an unqualified workshop sign-off.** The teaching sequence is coherent, and the fillable worksheets mostly work. Preparation links, progress calculations, one answer-field collision, and parts of the power lesson need correction. A timed rehearsal on the actual kit and venue network remains necessary.

This is a review, not an implementation pass. Participant content and application code were not changed. Activity 1 and its walkthrough assets changed in the working tree during the review; those concurrent edits were left alone.

## What was verified

- Read the seven activities, preparation page, history page, installation/resources/reference material, and supporting implementation/planning files.
- `scripts/test_progress.js`: passed.
- `scripts/test_worksheet_fields.cjs`: passed for all ten tested pages, including duplicate-field/radio synchronization, persistence, record-sheet transfer, completion-box mirrors, and activity-to-session report merging. These use a simulated DOM and mocked network.
- `scripts/test_worksheet_steps.cjs`: passed for all eight tested activity/history pages: 44 procedures, numbering, and in-page anchors.
- A local rendered-file scan found 318 existing relative file references and no missing targets at the time of the scan. This is not an exhaustive external-link or visual audit.
- Published Activity 4, installation page, and progress JavaScript returned HTTP 200 and matched local files. The placeholder installation links therefore affect the published material too.
- Firebase accepted a read-only day request (HTTP 200). No live progress writes or help messages were sent. Live write permissions, SSE delivery, help acknowledgement, offline recovery, export/import in a real browser, physical automations, and venue-scale operation were not independently verified in this pass.

## Fix before delivery

### 1. Preparation still contains unusable links

`docs/install.md:17,57,81` and `docs/resources.md:17,24,25` retain the Apple Silicon OVA URL `https://TODO/...`, installation-confirmation form, and support-contact placeholders. Both tables still say `TODO GB`; the installation screenshots are placeholders.

Publish the actual supported download and confirmation/contact details, or explicitly route affected participants to a tested shared laptop. This matters before the workshop: the instructions require installation confirmation three days beforehand.

### 2. Dashboard completion is not reliable after the page split

`docs/javascripts/progress.js:118–128` derives the activity list from whichever team reports the longest list. `extra.js` reports only pages a browser has visited.

Reproduced with the rendered Activity 1 and current reporting code: check all six Activity 1 boxes in a fresh browser, and the Session 1 board receives only `a1` and reports `standing.done = true`. Preparation, Activities 2 and 3 have never been visited. If another team later visits those pages, the definition of complete changes. Also reproduced: one team reporting only `a4` and another only `a5` produces an order containing only `a4`; selecting the longest list does not form a union.

Use a fixed session/activity schema so unvisited required work stays pending. Define optional-task handling explicitly: Activity 3.6 is labelled optional but currently counts toward the completion denominator.

### 3. History produces items that can never be complete

`docs/javascripts/extra.js:333` folds `aN-*` subheadings into their activity but does not fold `hist-*`. Its checkbox summary belongs to `hist`; duplicate answer fields below belong to `hist-2`, `hist-3`, and `hist-4`.

Reproduced report order: `hist, hist-2, hist-3, hist-4`. The latter three have `total: 0`, while `isComplete` requires `total > 0`. Checking every history task therefore cannot complete all the generated items. The same answers also count in multiple groups. Normalize the history headings to one activity before counting.

### 4. Activity 4.7 overwrites an earlier measurement

`docs/activity-4.md:202` asks for a chosen threshold but binds it to `s1.hum.room`, the measured room humidity from Activity 1. The top summary still labels that key as room humidity. Synchronization works, but synchronizes two different meanings.

Keep this field as a measured baseline and rewrite the instruction accordingly; use `s2.hum.on` and `s2.hum.off` for thresholds. Example: “ตรวจค่าความชื้นอากาศในห้องก่อนเลือกเกณฑ์ แล้วบันทึกค่าที่อ่านได้ … จากนั้นเลือกเกณฑ์เปิดให้สูงกว่าค่านี้เล็กน้อย และเลือกเกณฑ์ปิดให้สูงกว่าเกณฑ์เปิดอีก 5–10 จุดเปอร์เซ็นต์”

### 5. Correct the power lesson before treating its results as equipment sizes

`docs/activity-7.md:149–185`:

- The AC pump example equates `220 V × 5 A` with 1,100 W without a power-factor assumption. Simplest teaching fix: state that the pump's electrical input power is 1,100 W from its specification, and retain `V × A` for the DC example.
- “ตัวเลขที่ได้คือความจุที่ต้องซื้อ” is too definite. Battery/inverter losses, reserve, actual battery voltage and usable capacity affect selection. Label these as preliminary ideal calculations and add the factors that must be checked before purchase.
- Three peak-sun hours is an example assumption, not a guaranteed worst cloudy day. The no-battery pump example also needs enough instantaneous panel/controller power to start and run the pump; daily Wh alone does not establish that.
- The controller is described as 12 V 10 A in `docs/index.md`, but this lesson asserts 390 W. Verify the actual model and distinguish PV-input rating, load-output rating, and inverter rating. The preceding diagram correctly bypasses the controller load output for the inverter; keep the explanation consistent with that diagram.
- “พลังงานสูงถึง 3,000 W” should be “กำลังไฟขณะเริ่มทำงาน”; W is power. Any surge figure should be an example that must be checked against the pump/inverter specifications.

Manufacturer context: [Victron inverter sizing](https://www.victronenergy.com/inverters-chargers/help-me-choose) distinguishes VA and W, continuous and starting demand, and system-voltage considerations.

### 6. Resolve the dry-pump operating assumptions

Activity 4.6 says not to leave the dry pump running longer than one minute. Activity 5.4 starts with a full one-minute run before observation and manual shutdown, leaving no margin. Earlier humidity tests can also leave the pump running while teams discuss or edit rules.

Confirm the exact pump's permitted dry-run duration and a cooling/repetition policy on the actual kit. This review does not establish that dry operation is safe or unsafe for this model. Give the observer a clear shutdown deadline and make every exercise fit the verified limit. `docs/reference.md` still says to check whether the pump is submerged; that conflicts with the current dry demonstration.

## Coherence and remaining gaps

- **Overall sequence works.** Physical observations lead naturally to rules, hysteresis, time conditions, fault handling, history, dashboard use, and farm design. The distinction between a relay command and evidence of real pump operation is particularly useful.
- **Manual-mode meaning needs one sentence.** Activity 4.8 gates only automatic starting. The humidity-based stop rule and later protection rules remain active. Explain that Manual does not disable those rules, and turning Auto on does not itself trigger a start while humidity is already below its threshold. Do not equate the toggle with a complete physical Auto/Off/Manual selector.
- **Remote access is overstated.** Activity 7.3 says outside access requires a cloud service. Keep Nabu Casa as the taught example, but say it is one route. [Home Assistant's official remote-access guide](https://www.home-assistant.io/docs/configuration/remote/) also describes VPN access. No extra activity is necessary.
- **History prompt and selected time window differ.** The chart starts at Session 2, but the final question asks about the break after Session 1. Mark it as a hypothetical question, or extend the selected time range. Add a participant-facing fallback for teams with too little history; the instructor notes already propose a projected or neighbouring graph.
- **Activity 7.6 lacks an explicit control decision and failure response.** It collects sensors, outputs, communication, power, and tests, but never requires the group to apply its main automation/fail-safe learning to the chosen farm. Add two short prompts inside the existing four-part design: “เมื่อเกิดอะไร ระบบจะสั่งให้อุปกรณ์ทำอะไร” and “ถ้าเซนเซอร์หรือการสื่อสารขัดข้อง ระบบควรทำอย่างไร”. No need to restore the old large canvas.
- **One recorder remains the safest workflow.** Cross-device answers do not synchronize automatically. The dashboard receives progress counts, not answers, and cannot recover a lost answer file. Specify the actual hand-in destination and when the instructor verifies receipt. Current end text only says to send the file to the instructor.
- **Help confirmation promises too much.** `extra.js:494` says “แจ้งผู้สอนแล้ว กำลังไปหา” immediately after database acceptance. No TA has accepted the request at that point. Use “ส่งคำขอความช่วยเหลือแล้ว กรุณารอผู้สอน”.
- **Multi-device counts can disagree.** Progress merges activity counts using maximum, but sub-step ticks using OR. If two devices tick different boxes, sub-step bars can show more completion than the activity count. With the single-recorder instruction this is less urgent, but the dashboard should make its policy consistent.
- **Timing is estimated, not rehearsed.** Activity 4's eight subactivities, Activity 5's four problem/fix/retest loops plus maintenance table, and Activity 7's expanded battery lesson are the likely bottlenecks. Run one novice-paced rehearsal and define where TAs provide prepared recovery states. Test actual VLAN discovery, VM/phone access, kit calibration, and network reporting with representative devices.

## Thai language assessment

The main procedural prose is generally natural and usable. It does not need wholesale shortening or a rewrite into telegraphic commands. Activities 1–3 are especially consistent; later edits contain more awkward noun phrases, mixed terminology, and unfinished sentences. Keep connectors such as “จากนั้น”, “เมื่อ…แล้ว”, “หาก…ให้…”, and “เพื่อให้…” where they express sequence, condition, or purpose. Tables and checklists can be brief; explanations should remain full Thai sentences.

| Current text | Suggested revision |
|---|---|
| “เลือกสถานการณ์จากสถานการสมมุติที่กำหนด” (7.1) | “เลือกหนึ่งสถานการณ์จากตารางด้านล่าง หรือใช้ปัญหาจริงของสมาชิกในกลุ่มก็ได้” |
| “เพิ่ม Trigger ให้รองรับทุกกรณี ให้ไฟเปิดได้เมื่อถึงเวลา” (4.4) | “เพิ่มเหตุการณ์เวลา เพื่อให้ไฟเปิดได้แม้ฟ้ามืดก่อนเวลาที่กำหนด” |
| “การทำให้ระบบทำงานได้สมบูรณ์นั้น จำเป็นต้องเพิ่ม Trigger เมื่อถึงเวลา 18.30 น. เพิ่มเติม” (4.4) | “เพื่อให้ไฟเปิดได้ในกรณีที่ฟ้ามืดก่อนเวลา เราจึงต้องเพิ่ม trigger อีกข้อให้เริ่มกฎเมื่อถึงเวลา 18.30 น.” |
| “สร้างแดชบอร์ดที่ช่วยให้การสังเกตการณ์และควบคุมการทำงานอุปกรณ์ในฟาร์มทำได้คล่องตัวขึ้น” (6 intro) | “เราจะสร้างแดชบอร์ดเพื่อให้ผู้ใช้ดูข้อมูลและสั่งงานอุปกรณ์ในฟาร์มได้สะดวกขึ้น” |
| “ลองดูกราฟแล้วทบทวนว่าสามารถเชื่อมโยงการเปลี่ยนแปลงใดในกราฟที่เกิดจากกิจกรรมก่อนหน้านี้บ้าง” (history summary) | “ลองดูกราฟแล้วทบทวนว่า การเปลี่ยนแปลงแต่ละช่วงตรงกับการทดลองใดที่เราทำไปแล้ว จากนั้นเลือกมาอธิบาย 3 จุด” |
| “นอกจากปัจจับข้อต้นแล้ว” (7.5) | “นอกจากการคำนวณข้างต้นแล้ว” |
| “อุปกรณ์ที่เผื่อความต้องการนี้ด้วย” (7.5) | “จึงต้องเลือกอุปกรณ์ที่รองรับกระแสขณะเริ่มทำงานได้ด้วย” |
| “ส่วนที่จดไว้แล้วใน 7.2 7.3 และ 7.5 จะแสดงให้เอง” (7.6) | “คำตอบที่กรอกไว้ในข้อ 7.2, 7.4 และ 7.5 จะปรากฏในส่วนนี้โดยอัตโนมัติ” — 7.3 has acknowledgements, not these answer fields. |

Use “แดชบอร์ด”, “กฎอัตโนมัติ”, “แอป”, and “การอบรม” consistently in prose; preserve exact English labels for buttons and menus. Standardize “โซลาร์” rather than alternating with “โซล่าร์”. Avoid claiming “ทุกกรณี” or “สมบูรณ์” for a demonstration that handles only the cases taught.

## Release recommendation

Correct items 1–6, polish the listed Thai passages and contradictory instructions, regenerate the published renders, then run one timed end-to-end rehearsal. Add regression checks for the actual failures above; the existing passing tests do not cover semantic field meaning or complete-session expectations. Verify live reporting from a designated rehearsal browser, including reconnect and a second dashboard screen, before relying on the board to pace the room.
