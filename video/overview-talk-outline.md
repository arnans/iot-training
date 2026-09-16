# Overview talk — the ideas behind the three sessions, in 30 minutes (v3 outline)

**Status 16 Sep 2026: outline for recording, concept-first rewrite.** Not yet recorded. After
recording, this file is rewritten as-built from the transcripts (v3 rule: narration is the source
of truth).

**What the viewer should leave with:** (1) the concepts the workshop teaches, stated plainly, and
(2) a hint of what they will do with their hands in the room. Activities are named only as the
place where a concept gets built, never walked through step by step.

**Audience (assumed):** enrolled participants of นวัตกรเกษตรอัจฉริยะ AIoT รุ่นที่ 1, watching
before Day 1 (25 Sep 2026); organizers and TAs as a secondary audience. Spoken in Thai, technical
terms in English, as in the worksheets.

**Method:** v3 outline-driven hybrid, as book-cs1 Module 4/5 and
[PART1-RECORDING-PREP.md](../planning/PART1-RECORDING-PREP.md) §Methodology. Key points only,
no script. `[TALK]` = camera, speak from the prompter ([ov-keypoints.html](ov-keypoints.html)).
`[DEMO]` = capture the clip first, then Voice-Over Record in Premiere; every demo is its own
segment ID. One file per segment, named `ov-NN.mp4`. Flub protocol: pause a beat, re-read the whole
sentence. ASR: `asr_pass.py` defaults, then `repair_gaps.py`, no `--initial-prompt`. Validate one
`[TALK]` + one `[DEMO]` through the whole loop before recording the rest.

Sources: [SESSION-OVERVIEW.md](../planning/SESSION-OVERVIEW.md), [COURSE-DESIGN.md](../planning/COURSE-DESIGN.md),
worksheets [session-1](../docs/session-1.md) · [session-2](../docs/session-2.md) · [session-3](../docs/session-3.md),
[index](../docs/index.md).

## Learning goals: what the talk promises vs what the room delivers

The six goals in SESSION-OVERVIEW are the frame, but the talk promises only what the worksheets
actually build. Not spoken; it is the reason the segments are weighted as they are.

| Goal | In the room | Talk promises |
|---|---|---|
| 1 Input → Logic → Output | Strong: every activity, both wrap-ups | The one frame for the whole course (ov-02) |
| 2 Choose sensors/actuators from specs, form factor, price | **Thin.** The spec game was cut 15 Sep; selecting by spec survives only in post-test 1 and the Session 3 price sheet. What is strong is hands-on: value vs state, response delay, relay = switch, load needs its own supply | "Know what a sensor really gives you and what a load really needs" (ov-04); spec-and-price reasoning is named once, inside the design step (ov-11) |
| 3 Create control logic | Strong: two rules in Session 1, hysteresis / time window / trigger-vs-state / notification / Auto-Manual in Session 2 | Full segment (ov-05) |
| 4 IoT infrastructure, communication, protocols | **Partial.** One 20-min network step + a remote-access menu inside the design challenge; protocols (MQTT, HTTP, the API) are not taught, only "the board and Home Assistant talk over the zone WiFi" is opened | Local-first and choosing a link by elimination (ov-09). No protocol promise. Power sizing, which is not a named goal, is in the room and is promised |
| 5 Redundancy, fail-safe, safety, maintenance | Strong: four sabotage problems, summary table, maintenance table, control-box seed | Full segment (ov-06) + demo (ov-07) |
| 6 Dashboards | Moderate: one 35-min dashboard for one named user, plus 20 min reading their own history; phone control from Session 1 | "One dashboard for one real person, tested by a stranger" and "read your own data" (ov-08). Not "dashboards" broadly |

## Runtime plan (30:00)

| # | seg | type | budget | concept |
|---|---|---|---|---|
| 1 | ov-01 | TALK | 1:30 | เปิด: หลักสูตรนี้ให้ความคิดอะไรกลับบ้าน |
| 2 | ov-02 | TALK | 3:30 | ความคิดที่ 1 — Input → Logic → Output และการย้าย Logic ไปเป็นโปรแกรม |
| 3 | ov-03 | DEMO | 2:00 | ระบบที่เสร็จแล้ว (ปลายทางของสามช่วง) |
| 4 | ov-04 | TALK | 3:00 | ความคิดที่ 2 — เซนเซอร์ให้อะไรเราจริง ๆ และอุปกรณ์ปลายทางต้องการอะไรจริง ๆ |
| 5 | ov-05 | TALK | 3:30 | ความคิดที่ 3 — กฎที่ทำงานได้ในโลกจริง (trigger/condition/action, hysteresis, เหตุการณ์ ≠ สถานะ) |
| 6 | ov-06 | TALK | 3:30 | ความคิดที่ 4 — ของพังได้สี่ที่ และ fail-safe ที่ป้องกันได้จริง |
| 7 | ov-07 | DEMO | 1:30 | คำสั่ง ≠ ผลลัพธ์: ความล้มเหลวที่หน้าจอมองไม่เห็น |
| 8 | ov-08 | TALK | 2:30 | ความคิดที่ 5 — ข้อมูลที่บันทึกไว้ และหน้าจอสำหรับคนจริง |
| 9 | ov-09 | TALK | 3:30 | ความคิดที่ 6 — ระบบควบคุมอยู่ที่ฟาร์ม: เลือกเครือข่ายและพลังงานด้วยเหตุผล |
| 10 | ov-10 | DEMO | 1:30 | กราฟครึ่งวันของกลุ่ม + แดชบอร์ดบนมือถือ |
| 11 | ov-11 | TALK | 2:30 | ความคิดที่ 7 — แบบร่างที่มีราคาและเหตุผล และบอกได้ว่ายังไม่รู้อะไร |
| 12 | ov-12 | TALK | 1:30 | ปิด: สิ่งที่ได้กลับบ้าน และสิ่งที่ต้องเตรียม |

TALK ≈ 25:00 · DEMO ≈ 5:00. Every TALK segment ends with one **ในห้อง:** line, the activity
hint. If the talk runs long, cut inside the hints, never the concepts.

---

## Segments

### ov-01 [TALK] 1:30 — เปิด

- หลักสูตร "IoT ในฟาร์มอัจฉริยะ" ในโปรแกรม **นวัตกรเกษตรอัจฉริยะ AIoT** · สามช่วง ช่วงละ 150 นาที · ห้องเดียว 100 กลุ่ม กลุ่มละ 4 ทุกกลุ่มลงมือเอง
- คลิปนี้ไม่ใช่ตารางกิจกรรม — เป็นเรื่อง**ความคิดเจ็ดอย่าง**ที่จะติดตัวกลับบ้าน และแต่ละความคิดจะได้จากการทำอะไรในห้อง
- เส้นเรื่องเดียว: **ชุดอุปกรณ์ชุดเดียว ระบบเดียว** ไฟสวนและรดน้ำที่ตัดสินใจเองได้ — สร้างวันแรก ทำให้ฉลาดและทนทานวันที่สอง แล้วออกแบบของตัวเอง
- เมื่อจบ: ไม่ใช่แค่ "ต่อ IoT เป็น" แต่**คิดแบบคนออกแบบระบบอัตโนมัติ**ได้ — รู้ว่าต้องถามอะไรก่อนซื้อของ
- ส่ง: "ความคิดแรกคือกรอบเดียวที่ใช้ทั้งหลักสูตร"

V2 candidates: *need* title card (ชื่อหลักสูตร + 3 ช่วง + วันที่) · *need* card "ความคิด 7 อย่าง" (รายการสั้น ใช้ซ้ำเป็น bookend ใน ov-11)

### ov-02 [TALK] 3:30 — ความคิดที่ 1: Input → Logic → Output

- ระบบอัตโนมัติทุกระบบ ไม่ว่าจะเล็กแค่ไหน มีสามส่วน: **รับข้อมูล → ตัดสินใจ → สั่งงาน**
- ตู้เย็น · ไฟถนน · **ถังน้ำลูกลอย** — ลูกลอยคือ Input, แขนลูกลอยคือ Logic, วาล์วคือ Output — ครบสามกล่องโดยไม่มีคอมพิวเตอร์สักตัว
- ใจความสำคัญ: **Logic เป็นกลไก เป็นคน หรือเป็นโปรแกรมก็ได้** — ฟาร์มส่วนใหญ่วันนี้ Logic คือคน (ดูฟ้า เดินไปเปิดปั๊ม)
- หลักสูตรนี้ทั้งหมดคือ**การย้าย Logic จากคนไปเป็นโปรแกรม** โดยยังเก็บชั้นกลไกและชั้นคนไว้เป็นเบาะรองรับ (จะกลับมาเรื่องนี้ตอน fail-safe)
- แผนที่ลงของจริง: **บอร์ดเซนเซอร์ = Input** · **บอร์ดรีเลย์ = Output** · **Home Assistant บนแล็ปท็อปของกลุ่ม = Logic** และเป็นที่บันทึกข้อมูลกับหน้าจอด้วย — ทำไม Home Assistant: ของจริงที่ใช้ทั่วโลก ฟรี และทำงานในฟาร์มได้โดยไม่ต้องมีอินเทอร์เน็ต
- เมื่อคิดด้วยสามกล่องได้ จะ**อ่านระบบที่ไม่เคยเห็น**ได้ — พัดลมโรงเรือน เครื่องตีน้ำบ่อกุ้ง สปริงเกลอร์กับเซนเซอร์ฝน ล้วนสามกล่องเดียวกัน
- **ในห้อง:** ช่วงที่ 1 ประกอบสามกล่องนี้ด้วยมือตัวเอง ทีละกล่อง — อ่านเซนเซอร์จากหน้าเว็บของบอร์ดเอง ต่อวงจร 12V ให้หลอดไฟ แล้วให้ Home Assistant ตัดสินใจครั้งแรก
- ส่ง: "ดูปลายทางของสามช่วงก่อน แล้วค่อยแยกทีละความคิด"

V2 candidates: *need* card สามกล่อง + ถังน้ำลูกลอย (Input = ลูกลอย · Logic = แขน · Output = วาล์ว) · *need* card "Logic = กลไก / คน / โปรแกรม" · *have* `docs/images/gogo-iot-main-parts.png` · *have* `docs/images/relay-board.jpg` · *need* card map อุปกรณ์ → สามกล่อง

### ov-03 [DEMO] 2:00 — ระบบที่เสร็จแล้ว

Capture on the bench kit + HA screen; VO afterwards. Shots in order:

- บังบอร์ดเซนเซอร์ → ค่าแสงตก → **ไฟสวนติดเอง**, เปิดมือ → ดับ (ไม่กะพริบ)
- เป่าบอร์ด → ความชื้นขึ้น → **ปั๊มเดิน**
- ยกลูกลอยจากแก้ว → **ปั๊มหยุดเอง + แจ้งเตือน**บนจอ
- มือถือ: เกจความชื้น สถานะลูกลอย ปุ่มปั๊ม สวิตช์ Auto/Manual
- (VO ปิด) "สามกล่อง กฎสี่ห้าข้อ และแดชบอร์ดหนึ่งหน้า — ทุกกลุ่มสร้างเองครบภายในสองวัน"

No V2 (finished pair).

### ov-04 [TALK] 3:00 — ความคิดที่ 2: เซนเซอร์ให้อะไรเราจริง ๆ อุปกรณ์ปลายทางต้องการอะไรจริง ๆ

- เซนเซอร์ให้ข้อมูลสองแบบ: **ค่าปริมาณ** (ความชื้น 63%, แสง 120) กับ **สถานะ** (ลูกลอย Wet/Dry) — ค่าปริมาณต้องมี**เกณฑ์**ก่อนตัดสินใจ สถานะตัดสินใจได้เลย
- เซนเซอร์**ไม่ตอบทันที**: บังมือแล้วค่าแสงใช้เวลากี่วินาที — ความล่าช้านี้จะกลับมาเป็นปัญหาตอนเขียนกฎ
- คำถามที่ควรถามก่อนซื้อเซนเซอร์: มันวัด**สิ่งที่เราจะตัดสินใจด้วย**หรือเปล่า — ความชื้นอากาศไม่ใช่ความชื้นดิน
- ฝั่งสั่งงาน: **รีเลย์คือสวิตช์ ไม่ใช่แหล่งจ่ายไฟ** — หลอดไฟ ปั๊ม วาล์ว ต้องมีไฟของตัวเอง รีเลย์แค่ปิด-เปิดวงจรนั้น → คู่ที่ต้องดูเสมอ: โหลดกินไฟเท่าไร รีเลย์ทนเท่าไร แหล่งจ่ายให้เท่าไร
- **12V จับได้ ต่อเองได้ · 220V ต้องช่างไฟ** — ในห้องทุกอย่างเป็น 12V โดยตั้งใจ
- **ทุกอุปกรณ์ต้องมีทางสั่งด้วยมือ**: กล่องควบคุมปั๊มของจริงมีสวิตช์ Auto / Off / Manual — เมล็ดแรกของความคิดเรื่อง fail-safe
- (พูดตรง ๆ) การเลือกจากสเปกชีตและราคา ในห้องมีเวลาน้อย — จะได้ใช้ตอนทำแบบร่างของตัวเองในช่วงที่ 3 กับใบราคาจริง
- **ในห้อง:** เป่า บังมือ ยกลูกลอย ดูว่าค่าไหนขยับ · ได้ยินรีเลย์คลิกก่อนต่ออะไรเลย · ต่อสาย 12V จากกล่องจ่ายไฟผ่านรีเลย์ไปหลอดไฟด้วยมือครั้งเดียว

V2 candidates: *need* card ค่าปริมาณ vs สถานะ (ตัวอย่างจากชุด) · *have* `docs/images/gogo-iot-float-switch.jpg` · *need* card "รีเลย์ = สวิตช์" (โหลด / รีเลย์ / แหล่งจ่าย) · *have* `docs/images/activity2-2-relay-wiring-diagram.png` · *need* photo กล่องควบคุมปั๊ม Auto/Off/Manual

### ov-05 [TALK] 3:30 — ความคิดที่ 3: กฎที่ทำงานได้ในโลกจริง

- เริ่มจากภาษาคน: **"ถ้า…ให้…"** สองประโยค — ถ้ามืดให้เปิดไฟ ถ้าสว่างให้ปิดไฟ — เขียนให้ชัดก่อนแตะโปรแกรม
- แปลเป็นภาษาโปรแกรม: **automation = trigger + condition + action** — trigger คือเหตุการณ์ที่ปลุกกฎ condition คือด่านตรวจ action คือคำสั่ง
- ปัญหาแรกที่ทุกกลุ่มจะเจอกับตา: เกณฑ์เดียว ค่าแกว่งอยู่ตรงเกณฑ์ → **ไฟกะพริบ** (chatter) — นับได้เป็นครั้งต่อนาที
- ทางแก้ชื่อ **hysteresis**: เกณฑ์เปิดกับเกณฑ์ปิดคนละค่า เว้นช่องตรงกลาง — หลักเดียวใช้กับไฟ ปั๊ม พัดลม แอร์ ทุกอย่างที่เปิด-ปิด
- ความคิดที่คนพลาดบ่อยที่สุด: **trigger คือเหตุการณ์ ไม่ใช่สถานะ** — "เปิดไฟเฉพาะหลังหกโมง" ถ้ามืดอยู่แล้วตอนหกโมง ไฟจะไม่ติด เพราะไม่มีอะไร"ข้าม"เกณฑ์ — ต้องเพิ่ม trigger ตามเวลาอีกตัว · ทดสอบกฎต้องทำให้ค่า**ข้าม**เกณฑ์จริง
- ระบบควร**บอก**ได้ ไม่ใช่แค่ทำ: การแจ้งเตือนเป็น action หนึ่งแบบ
- กฎอัตโนมัติต้อง**ปิดได้จากหน้าจอ**: สวิตช์ Auto / Manual ในซอฟต์แวร์เป็น condition ของกฎ — คนสั่งเองได้เสมอ กฎไม่ทับ
- **ในห้อง:** ท้ายช่วงที่ 1 สร้างกฎไฟสองข้อแล้วผ่านสามรอบ · ช่วงที่ 2 นับไฟกะพริบด้วยตัวเอง แก้ด้วย hysteresis เพิ่มเงื่อนไขเวลา ดูหน้า Traces ว่ากฎถูกบล็อกเพราะอะไร แล้วเปลี่ยนหลอดไฟเป็นปั๊มพร้อมกฎรดน้ำและสวิตช์ Auto/Manual

V2 candidates: *need* card "ถ้า…ให้…" → trigger + condition + action · *need* card chatter → hysteresis (กราฟค่าแกว่ง เกณฑ์เดียว vs สองเกณฑ์) · *need* card "trigger = เหตุการณ์ ไม่ใช่สถานะ" (เส้นเวลา มืดก่อนหกโมง) · *have* `docs/images/steps/s2-a5-06-pick-crossed-threshold.png` · *need* screenshot Traces page · *need* screenshot สวิตช์ Pump Auto Mode

### ov-06 [TALK] 3:30 — ความคิดที่ 4: ของพังได้สี่ที่ และ fail-safe ที่ป้องกันได้จริง

- ระบบอัตโนมัติพังได้**สี่ที่**: เซนเซอร์ · เครือข่าย · อุปกรณ์ปลายทาง · ตัวควบคุมเอง — และแต่ละที่พังคนละแบบ
- ตัวอย่างที่ทุกกลุ่มจะเห็น: น้ำหมดแต่ปั๊มเดิน (ไม่มีกฎไหนดูลูกลอย) · เซนเซอร์หายไปเฉย ๆ (ค่าเป็น unavailable กฎเงียบ) · ปั๊มที่สั่งด้วยมือแล้วลืม · และตัวร้ายที่สุด →
- **คำสั่ง ≠ ผลลัพธ์**: รีเลย์คลิก จอบอก On แต่ปั๊มไม่เดิน — หน้าจอมองไม่เห็น เพราะหน้าจอแสดง**สิ่งที่สั่ง** ไม่ใช่**สิ่งที่เกิด** — ต้องมีเซนเซอร์อีกตัวดูผลลัพธ์ (ในชุดคือแรงสั่นบนปั๊ม)
- **fail-safe ที่ดีไม่ใช่แค่แจ้งเตือน** — ต้องพาระบบไปสู่สถานะที่ปลอดภัย (ปั๊ม Off) ด้วยตัวเอง
- ขีดจำกัดที่ต้องรู้: fail-safe ทุกข้อใน Home Assistant **เงียบพร้อมกัน**เมื่อ Home Assistant ติดต่อบอร์ดไม่ได้ — ปั๊มค้างสถานะล่าสุด → ต้องมี**ชั้นป้องกันที่ไม่พึ่ง Logic หลัก** (กล่อง Auto/Off/Manual, ลูกลอยกลไก, ตัวตั้งเวลาบนบอร์ด) — กลับไปที่ความคิดแรก: เก็บชั้นกลไกและชั้นคนไว้
- **การบำรุงรักษาเป็นส่วนหนึ่งของการออกแบบ**: ใครตรวจอะไร บ่อยแค่ไหน — ตัดสินใจตั้งแต่วันแรก ไม่ใช่วันที่พัง
- **ในห้อง:** กิจกรรมที่กลุ่มจำได้นานที่สุด — กลุ่มคู่มา**ก่อกวน**ระบบของเรา (ยกลูกลอย คลายสาย ปิดบอร์ด) เราดูได้แค่หน้าจอ แล้วสร้างกฎป้องกัน แล้วให้เขาก่อกวนซ้ำเพื่อพิสูจน์ · ปิดท้ายด้วยตารางบำรุงรักษาของกลุ่ม

V2 candidates: *need* card ห่วงโซ่ 4 จุด (เซนเซอร์ · เครือข่าย · อุปกรณ์ · ตัวควบคุม) · *need* card "คำสั่ง ≠ ผลลัพธ์" · *need* card fail-safe = แจ้งเตือน + สถานะปลอดภัย + ชั้นอิสระ · *need* card sabotage → fix → sabotage again

### ov-07 [DEMO] 1:30 — คำสั่ง ≠ ผลลัพธ์

Capture on the bench kit, phone on the pump + screen recording; VO afterwards.

- กฎรดน้ำเปิด ปั๊มเดินปกติ → คลายสายปั๊มที่ขั้ว NO ของรีเลย์
- สั่ง On: **รีเลย์คลิก LED ติด จอบอก On** — ปั๊มนิ่ง
- นับ 15 วินาที → fail-safe ทำงาน: รีเลย์ Off + แจ้งเตือน "สั่ง On แต่ไม่มีแรงสั่น"
- (VO ปิด) "หน้าจอบอกสิ่งที่สั่ง เซนเซอร์อีกตัวถึงจะบอกสิ่งที่เกิด"

No V2 (finished pair).

### ov-08 [TALK] 2:30 — ความคิดที่ 5: ข้อมูลที่บันทึกไว้ และหน้าจอสำหรับคนจริง

- ระบบที่ตัดสินใจเองได้ **จำสิ่งที่เกิดขึ้น**ได้ด้วย — กราฟความชื้น แสง และทุกครั้งที่สั่งรีเลย์ ย้อนดูได้ทั้งวัน
- อ่านกราฟให้เป็น: จุดนี้เกิดตอนเราทำอะไร · ถ้าเกิดในฟาร์มตอนไม่มีคนอยู่ จะตรวจอะไร · กับดัก: **จำนวนครั้งที่สั่ง Relay On ไม่ใช่เวลาที่ปั๊มเดินจริง** (ความคิดที่ 4 อีกครั้ง)
- บทเรียนที่มาจากข้อผิดพลาดโดยตั้งใจ: กราฟไม่มีคืนแรก เพราะ**เครื่องบันทึกกลับบ้านในกระเป๋าแล็ปท็อป** → ฟาร์มต้องมีเครื่องเล็ก ๆ ที่ไม่ปิดฝา มีไฟและเครือข่ายตลอด
- แดชบอร์ด: ออกแบบให้**คนหนึ่งคนที่มีชื่อ** (คนเฝ้าสวน เจ้าของ คนงาน) — สิ่งสำคัญที่สุดอยู่บนสุด อ่านได้โดยไม่ต้องรู้ตัวเลข มีปุ่มควบคุมและบอกว่ากฎไหนเปิดอยู่
- วัดว่าดีหรือไม่ด้วยวิธีเดียว: **ให้คนที่ไม่ได้สร้างลองใช้** แล้วถามสามคำถาม
- **ในห้อง:** ช่วงที่ 3 เปิดกราฟครึ่งวันของกลุ่มเอง หาสามจุดที่โยงกับสิ่งที่ทำเมื่อเช้า · สร้างแดชบอร์ดหนึ่งหน้าสำหรับผู้ใช้ที่เลือก แล้วส่งมือถือให้คนจากกลุ่มคู่ทดสอบ

V2 candidates: *have* `docs/images/sensor-log-view.png` · *need* card "สั่ง ≠ เดิน" บนกราฟ · *need* card แดชบอร์ดสำหรับหนึ่งคน (บนสุด / อ่านออก / ควบคุมได้ / กฎไหนเปิด) · *need* screenshot แดชบอร์ดตัวอย่างบนมือถือ

### ov-09 [TALK] 3:30 — ความคิดที่ 6: ระบบควบคุมอยู่ที่ฟาร์ม

- สองวันแรกเราซ่อนสองกล่องไว้: **เครือข่าย**กับ**พลังงาน** — ในห้องมันทำงานเองเพราะจัดไว้ให้ ที่ฟาร์มต้องเลือกเอง
- ความคิดหลัก: **Logic อยู่ที่ฟาร์ม ไม่ใช่บนคลาวด์** — บอร์ดกับ Home Assistant คุยกันผ่านเครือข่ายในพื้นที่ อินเทอร์เน็ตล่มก็ยังรดน้ำ · การเข้าดูจากนอกฟาร์มเป็นแค่**ทางเข้า**ไปยังเครื่องเดิมที่ฟาร์ม
- เลือกเครือข่ายในฟาร์ม**ด้วยการตัดออก** ไม่ใช่ตามกระแส: ถามระยะทางก่อน แล้วถามว่าปลายทางมีไฟไหม — WiFi · ESP-NOW · Zigbee · LoRa · เซลลูลาร์ · RS-485 แต่ละแบบเหมาะกับคู่คำตอบต่างกัน (ไม่ลงลึกโปรโตคอล — เปิดกล่องเท่าที่การตัดสินใจต้องใช้)
- เข้าจากนอกฟาร์ม**จำเป็นจริงไหม**ก่อน แล้วค่อยเลือกจากสี่ทาง: แจ้งเตือนอย่างเดียว · Home Assistant Cloud · VPN · ส่งข้อมูลขึ้น IoT cloud — แต่ละทางแลกอะไร
- พลังงาน: แยก**พลังงานต่อวัน**ออกจาก**กำลังขณะทำงาน** — ปั๊มกินกำลังมากช่วงสั้น เซนเซอร์กินน้อยแต่ตลอดวัน → ข้อสรุปที่จะค้นพบเองจากเลขคณิตง่าย ๆ: **ปั๊มสูบตอนมีแดดแล้วเก็บน้ำ ไม่ใช่เก็บไฟ** · เซนเซอร์ใช้แผงเล็กแบตเล็ก
- charge controller ที่โต๊ะก็เป็น Input → Logic → Output: วัดแรงดัน ตัดสินใจ จ่ายหรือตัด — ความคิดแรกอยู่ในทุกกล่อง
- **ในห้อง:** ช่วงที่ 3 เปิดดูว่าบอร์ดคุยกับ Home Assistant อย่างไร · เลือกเครือข่ายสองเส้นของโจทย์ตัวเองจากตารางสั้น ๆ · ดูสาธิต Home Assistant Cloud · อ่าน charge controller ของจริง แล้วคิดแผงและแบตสำหรับสี่โหลด

V2 candidates: *need* card "Logic อยู่ที่ฟาร์ม" (ฟาร์ม ↔ ทางเข้าจากนอก) · *have* `docs/images/network-zones-th.svg` (บอร์ด ↔ HA ผ่านโซน) · *need* card ตารางเครือข่าย 6 แบบ (ระยะ / ไฟปลายทาง) · *need* card 4 ทางเข้าจากนอกฟาร์ม · *need* card พลังงานต่อวัน vs กำลัง (ปั๊ม = แดด + ถังน้ำ, เซนเซอร์ = แผงเล็ก + แบตเล็ก)

### ov-10 [DEMO] 1:30 — กราฟครึ่งวัน + แดชบอร์ดบนมือถือ

Screen recording of the bench HA with a real half-day of history + phone capture; VO afterwards.

- History: แสงตกทุกครั้งที่บัง · ความชื้นพุ่งตอนเป่า · Relay On เป็นแท่งสั้น · ช่องว่างตอนปิดเครื่อง
- แดชบอร์ดบนมือถือ: เกจ · Wet/Dry · ปุ่มปั๊ม · Auto/Manual · กฎที่เปิดอยู่
- (ถ้าพร้อม) เปิดจากนอกเครือข่ายผ่าน Home Assistant Cloud — หน้าเดิม เครื่องเดิมที่ฟาร์ม
- (VO ปิด) "ข้อมูล หน้าจอ และ Logic ทั้งหมดอยู่บนเครื่องเดียวที่ฟาร์ม"

No V2 (finished pair).

### ov-11 [TALK] 2:30 — ความคิดที่ 7: แบบร่างที่มีราคาและเหตุผล

- ปลายทางของหลักสูตรไม่ใช่ชุดทดลอง แต่คือ**แบบร่างระบบสำหรับปัญหาจริงของฟาร์มเรา** — ประโยคเดียวที่เขียนไว้ตั้งแต่นาทีแรกของวันแรก
- แบบร่างที่ดีตอบได้ว่า: เซนเซอร์และอุปกรณ์**เลือกเพราะอะไร** (ตรงนี้คือที่ใช้สเปกและใบราคาจริง) · ราคารวมเท่าไร · เครือข่ายเลือกด้วยการตัดออก · พลังงานต่อจุดสมเหตุผล · **มี fail-safe** · และ**บอกได้ว่ายังไม่รู้อะไร**ก่อนลงมือ
- คิดเป็น**แผนทดลองจุดแรก** ไม่ใช่ทั้งฟาร์ม — ทดลองหนึ่งจุด เรียนรู้ แล้วขยาย
- ความคิดจะดีขึ้นเมื่อ**คนอื่นถาม**: แลกแบบร่างกับอีกกลุ่ม สองคำถาม แล้วแก้หนึ่งอย่าง — ไม่มีนำเสนอหน้าห้อง
- ย้อนดูเจ็ดความคิดในหนึ่งลมหายใจ: สามกล่อง · เซนเซอร์กับโหลด · กฎที่ทำงานจริง · ของพังสี่ที่ · ข้อมูลกับหน้าจอ · ควบคุมที่ฟาร์ม · แบบร่างที่มีเหตุผล
- (หนึ่งประโยค) ท้ายทุกช่วงมี post-test 15 นาทีของผู้จัด ถามความคิดเหล่านี้ ไม่ใช่ขั้นตอนกดปุ่ม · แบบร่างตรวจตามเกณฑ์หกข้อข้างต้น
- **ในห้อง:** 85 นาทีสุดท้ายของช่วงที่ 3 — เลือกโจทย์ เปิดสองกล่อง เติมแบบร่างพร้อมใบราคา แลกกับกลุ่มคู่ แก้หนึ่งอย่าง กลับบ้านพร้อมกระดาษแผ่นนี้

V2 candidates: *need* card เกณฑ์แบบร่าง 6 ข้อ · *need* card "ความคิด 7 อย่าง" (ใบเดียวกับ ov-01, bookend) · *need* photo/scan แบบร่าง (canvas) ที่กรอกแล้ว

### ov-12 [TALK] 1:30 — ปิด

- กลับบ้านพร้อม: **Home Assistant ที่ใช้งานได้บนแล็ปท็อป** · ใบบันทึกของกลุ่ม · แบบร่างที่มีราคา · คู่มือติดตั้งและแหล่งเรียนรู้ต่อ — และคำถามที่จะถามก่อนซื้อของทุกชิ้น
- เริ่มที่ฟาร์ม: หนึ่งจุด ตรวจสเปกและราคาก่อนซื้อ ให้เครื่องบันทึกมีไฟและเครือข่ายตลอด
- **เตรียมก่อนวันแรก**: (1) แล็ปท็อปหนึ่งเครื่องต่อกลุ่ม ติดตั้ง VirtualBox + นำเข้าไฟล์ Home Assistant ตามคู่มือ ส่งภาพหน้าจอยืนยัน**ก่อนวันงานอย่างน้อย 3 วัน** (2) มือถือที่ต่อ WiFi ได้ (3) **ปัญหาในฟาร์มหนึ่งประโยค** ยังไม่ต้องคิดวิธีแก้
- ปิด: "เจอกันวันที่ 25 กันยายน — มาพร้อมแล็ปท็อปที่พร้อมและปัญหาหนึ่งข้อ ที่เหลือทำด้วยกันในห้อง"

V2 candidates: *need* card เตรียม 3 ข้อ · *have* `docs/images/ha-login.png` (ภาพยืนยันที่ต้องส่ง) · *need* closing card (ชื่อหลักสูตร + ลิงก์ใบงาน + วันที่)

---

## Media inventory (after recording, becomes the placement table)

**Have (in repo):** 7 activity banners `docs/images/activity-banners/` (use sparingly; the talk is
about concepts, banners are hint-line decoration at most) · `gogo-iot-main-parts.png` ·
`relay-board.jpg` · `relay-board-terminals.png` · `activity2-2-relay-wiring-diagram.png` ·
`session2-relay-led-wiring.jpg` · `led-module-12v.jpg` · `gogo-iot-float-switch.jpg` ·
`network-zones-th.svg` · `network-multicast-th.svg` · `sensor-log-view.png` · `ha-login.png` ·
15 HA automation-editor stills `docs/images/steps/` · 2 GIFs `docs/images/activity1/`.
Every still is composited to 1920×1080 with white pad before it goes on V2 (v3 full-frame rule).

**Need from Roger (photos/screens):** pump control box with Auto/Off/Manual selector · Traces
page · Pump Auto Mode toggle on a dashboard · example dashboard on a phone · a filled design
canvas · (optional) Home Assistant Cloud remote view.

**Cards (generated after recording from the transcripts, then manual beautify):** title · ความคิด 7
อย่าง (bookend, ov-01 + ov-11) · สามกล่อง + ถังน้ำ · Logic = กลไก/คน/โปรแกรม · map อุปกรณ์ → กล่อง ·
ค่าปริมาณ vs สถานะ · รีเลย์ = สวิตช์ · ถ้า…ให้… → trigger/condition/action · chatter → hysteresis ·
trigger = เหตุการณ์ · ห่วงโซ่ 4 จุด · คำสั่ง ≠ ผลลัพธ์ · fail-safe 3 ชั้น · sabotage → fix → again ·
สั่ง ≠ เดิน · แดชบอร์ดสำหรับหนึ่งคน · Logic อยู่ที่ฟาร์ม · ตารางเครือข่าย · 4 ทางเข้า · พลังงาน vs กำลัง ·
เกณฑ์แบบร่าง 6 ข้อ · เตรียม 3 ข้อ · closing. About 23 cards; concept-heavy talk, so more cards and
fewer kit photos than the first draft.

## Recording checklist (day one)

1. Bench kit live with all Session 2 automations and the four fail-safes, plus a real half-day of
   history before capturing ov-10.
2. Capture the three `[DEMO]` clips first (ov-03, ov-07, ov-10).
3. Open [ov-keypoints.html](ov-keypoints.html), record the nine `[TALK]` segments in one sitting.
4. Validate ov-01 + ov-03 through ASR → transcript → XML → Premiere before the rest.
5. Then per batch: `asr_pass.py` → `repair_gaps.py` → transcripts to Claude → as-built rewrite of
   this file → placement table → cards → `build_narration_xml.py` → import.
