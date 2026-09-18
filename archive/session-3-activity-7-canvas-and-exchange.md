# Archived: Session 3 · Activity 7 · the design canvas, 7.7 Exchange and 7.8 Rubric check

Removed on 18 Sep 2026 (Roger: the instructor directs the peer presentation, so it need not be in the
workbook; with four design dimensions there is no need for a separate แบบร่างระบบ, students fill the
worksheet directly). Kept here so it can be restored. Nothing in `archive/` is published or rendered.

What replaced it: worksheet 7.6 became four blocks with fields inline (sensor and actuator, connectivity,
power, test plan), 7.1 gained the `d.problem` textarea, and the record sheet's canvas section became a plain
mirror of those fields. Keys that survived: `d.scenario`, `d.problem`, `d.in.1.sensor`, `d.out.1.device`,
`d.comm.*`, `d.power`, `d.power.backup`. New: `d.test.how`, `d.test.pass`. Every other `d.*` key below
no longer exists on any page.

**To restore**, paste each part back where it came from and undo the 7.6 rewrite:

1. **Worksheet** → `docs/activity-7.md`: replace the 7.6 section with the three sections below (before
   `## คืนอุปกรณ์`), restore the three task-list lines, put the `[แบบร่างระบบ](record-sheet.md#farm-design)`
   link back into the task-list intro and the 85-minute header, and drop `{{ta:d.problem}}` from 7.1.
2. **Record sheet** → `docs/record-sheet.md`: replace the `### กิจกรรมที่ 7` section with the canvas below.
3. **Run sheet** → `planning/INSTRUCTOR-RESOURCES.md`: replace `#### 7.6` and the instructor-led block
   with the three blocks below.
4. Re-run `python scripts/render-worksheets.py` and `python scripts/render-network-doc.py`.

---

## 1. Worksheet (`docs/activity-7.md`)

Task-list lines:

- [ ] **[7.6 สรุปแบบร่าง](#a7-4)** เลือกอุปกรณ์ กฎเปิด–ปิด วิธีป้องกัน และแผนทดลองครั้งแรก
- [ ] **[7.7 แลกเปลี่ยนและปรับแบบร่าง](#a7-5)** รับข้อเสนอแนะ แล้วแก้ข้อสรุปในแบบร่างได้เลย
- [ ] **[7.8 ตรวจแบบร่าง](#a7-6)** ตรวจว่าแผนนี้บอกได้ว่าจะทำอะไร ใครดูแล และต้องตรวจอะไรเพิ่ม

Sections:

### 7.6 สรุปแบบร่างสำหรับทดลองหนึ่งจุด { #a7-4 }

เปิด[แบบร่างระบบ](record-sheet.md#farm-design) คำตอบเรื่องการสื่อสารและพลังงานที่จดไว้จะปรากฏให้แล้ว เติมข้อสรุปที่เหลือเป็นข้อความสั้น ๆ

1. ระบุเซนเซอร์หลักและอุปกรณ์ที่จะสั่งงาน พร้อมสเปกที่มีผลต่อการต่อใช้งานและวิธีตรวจว่าทำงานจริง หากยังไม่รู้ ให้จดสิ่งที่ต้องตรวจเพิ่ม
2. เขียนกฎหลักสองข้อ เช่น กฎเปิดและกฎปิด แล้วเลือกว่าระบบจะตัดสินใจที่ใด
3. เลือกการป้องกันที่สำคัญอย่างน้อยหนึ่งข้อ ระบุว่าทำงานที่ใด และจะสั่งงานด้วยมืออย่างไร
4. จดผู้ดูแล งานตรวจที่สำคัญ และงบประมาณคร่าว ๆ เฉพาะที่มีข้อมูลแล้ว ไม่ต้องแจกแจงราคาทุกชิ้น
5. เลือกจุดทดลอง วิธีวัดผล และเกณฑ์ที่จะใช้ตัดสินใจว่าจะปรับหรือขยายระบบ พร้อมจดสิ่งแรกที่จะทำหลังอบรม

[↑ กลับไปที่ใบงาน](#a7){ .ws-back }

### 7.7 แลกเปลี่ยนและปรับแบบร่าง { #a7-5 }

จับคู่กับกลุ่มเดิม ใช้เวลาแลกเปลี่ยน 10 นาที และปรับแก้ 5 นาที

1. เล่าแบบร่างจากข้อสรุปที่มีในหนึ่งนาที: ปัญหาที่แก้ วิธีที่เลือก และการป้องกันที่สำคัญ ไม่ต้องเขียนบทพูดเพิ่ม
2. ให้อีกกลุ่มเสนอแนะว่าเหตุผลใดชัดเจน และถ้าอุปกรณ์เสียแล้วมีจุดไหนที่ยังไม่รู้ผลกระทบ จากนั้นสลับบทบาท
3. แก้ข้อสรุปในแบบร่างตามข้อเสนอแนะได้เลย ไม่ต้องเขียนบันทึกการแก้ไขแยกอีกช่อง

[↑ กลับไปที่ใบงาน](#a7){ .ws-back }

### 7.8 ตรวจข้อสรุปก่อนนำไปทดลอง { #a7-6 }

ช่วยกันอ่านแบบร่างครั้งสุดท้าย ให้เพื่อนในกลุ่มอธิบายได้ว่า:

1. จะเริ่มที่จุดใด ใช้เซนเซอร์และอุปกรณ์อะไร เชื่อมต่อและจ่ายไฟอย่างไร
2. ระบบเปิด–ปิดเมื่อไร ถ้าระบบขัดข้องแล้วจะป้องกันอย่างไร และใครเป็นผู้ดูแล
3. จะวัดผลจากอะไร และมีข้อมูลใดที่ต้องตรวจเพิ่มก่อนซื้อหรือติดตั้งจริง

หากยังตอบไม่ได้ ให้เติมเฉพาะข้อสรุปหรือสิ่งที่ต้องตรวจเพิ่มใน[แบบร่างระบบ](record-sheet.md#farm-design)

[↑ กลับไปที่ใบงาน](#a7){ .ws-back }

---

## 2. Record sheet (`docs/record-sheet.md`), from `### กิจกรรมที่ 7` to the end

### กิจกรรมที่ 7

อภิปราย เปรียบเทียบ และลองคำนวณร่วมกันใน[กิจกรรมที่ 7](activity-7.md) แล้วจดข้อสรุปในแบบร่างด้านล่างเพียงชุดเดียว

---

# แบบร่างระบบ IoT สำหรับทดลองหนึ่งจุด { #farm-design }

**กลุ่มที่** {{f:team.no|4}} · **สถานการณ์** {{f:d.scenario|14}}

**ปัญหาที่ต้องการแก้ (หนึ่งประโยค)**

{{ta:d.problem}}

จดเฉพาะสิ่งที่กลุ่มเลือกแล้ว หากข้อมูลยังไม่พอ ให้ใช้ช่อง “สิ่งที่ต้องตรวจเพิ่ม” ไม่ต้องเดาค่าหรือกรอกให้เต็มทุกช่อง อุปกรณ์เพิ่มเติมที่จำเป็นต่อโจทย์ให้จดรวมในช่องอุปกรณ์หลักได้

### อุปกรณ์หลัก

| สิ่งที่ต้องเลือก | ข้อสรุปของกลุ่ม | ข้อมูลสำคัญก่อนต่อใช้งาน |
|---|---|---|
| เซนเซอร์ | {{f:d.in.1.sensor|18}} จำนวน {{n:d.in.1.qty|2}} | ชนิดสัญญาณและสเปกที่ต้องใช้ {{f:d.in.1.spec|28}} |
| อุปกรณ์ที่สั่งงาน | {{f:d.out.1.device|18}} | แรงดัน / กระแส {{f:d.out.1.va|12}} วงจรขับ {{f:d.out.1.driver|16}} |

รู้ได้อย่างไรว่าอุปกรณ์ทำงานจริง {{f:d.out.1.verify|30}}

### วิธีสื่อสารที่เลือกและเหตุผล

| จุดเชื่อมต่อ | วิธีที่เลือก | ทำไมจึงเลือกวิธีนี้ |
|---|---|---|
| จากเซนเซอร์ถึงระบบควบคุม | {{f:d.comm.1.tech|12}} | {{f:d.comm.1.why|30}} |
| จากระบบควบคุมถึงอุปกรณ์ปลายทาง | {{f:d.comm.2.tech|12}} | {{f:d.comm.2.why|30}} |
| จากฟาร์มถึงเจ้าของนอกฟาร์ม (ถ้าไม่ใช้ ให้ระบุว่าไม่ใช้) | {{f:d.comm.3.tech|16}} | {{f:d.comm.3.why|30}} |

### แผนพลังงาน

แหล่งจ่ายไฟของเซนเซอร์ ระบบควบคุม และอุปกรณ์ปลายทาง {{f:d.power|50}}

อุปกรณ์ที่ต้องมีไฟสำรองและระยะเวลาที่ต้องการ (ถ้าไม่มี ให้ระบุว่าไม่มี) {{f:d.power.backup|40}}

### กฎหลักและตำแหน่งระบบควบคุม

เขียนกฎหลักสองข้อ เช่น กฎเปิดและกฎปิด ถ้าไม่มีเงื่อนไขร่วม ให้เว้นช่อง “และ” ไว้ได้

> 1. ถ้า {{f:d.rule.1.if|18}} และ {{f:d.rule.1.and|12}} แล้วให้ {{f:d.rule.1.then|18}}
>
> 2. ถ้า {{f:d.rule.2.if|18}} และ {{f:d.rule.2.and|12}} แล้วให้ {{f:d.rule.2.then|18}}

ระบบประมวลผลและสั่งงานอยู่ที่ {{r:d.logic.where|ในฟาร์ม|บนคลาวด์|ในบอร์ด}} เพราะ {{f:d.logic.why|24}}

### การป้องกันที่สำคัญและการสั่งงานด้วยมือ

ถ้า {{f:d.fs1.when|18}} แล้วระบบจะ {{f:d.fs1.do|18}} การป้องกันนี้ทำงานที่ {{r:d.fs1.where|HA|บอร์ด|สายไฟตรง}}

วิธีสั่งงานด้วยมือ {{f:d.manual|40}}

### ผู้ดูแลและงบประมาณคร่าว ๆ

ใครดูแล {{f:d.care.who|12}} งานตรวจประจำที่สำคัญ {{f:d.care.weekly|24}}

ถ้ามีข้อมูลราคาแล้ว ให้ประมาณเฉพาะยอดรวม ไม่ต้องแจกแจงราคาทุกชิ้น หากยังไม่รู้ ให้จดแหล่งที่จะสอบถามในช่องถัดไป

อุปกรณ์รวม {{n:d.budget.parts|7}} บาท · ค่าติดตั้ง {{n:d.budget.install|7}} บาท · ค่าใช้จ่ายรายเดือน {{n:d.budget.monthly|6}} บาท

### สิ่งที่ต้องตรวจเพิ่มก่อนซื้อหรือติดตั้ง

ระบุข้อมูลที่ยังไม่รู้ เช่น ระยะจริง สัญญาณ กำลังไฟ หรือราคา พร้อมบอกว่าจะถามใครหรือวัดอย่างไร

{{ta:d.unknown}}

### แผนทดลองครั้งแรก

เริ่มทดลองที่จุดใดและใช้อุปกรณ์อะไร {{f:d.pilot.start|36}}

วัดผลจากอะไร {{f:d.pilot.measure|24}} เกณฑ์ที่จะใช้ตัดสินใจว่าจะปรับหรือขยายระบบ {{f:d.pilot.criteria|30}}

สิ่งแรกที่จะทำหลังอบรม {{f:d.pilot.first|30}}

หลังแลกเปลี่ยนกับอีกกลุ่ม ให้แก้ข้อสรุปในแบบร่างนี้ได้เลย แล้วใช้แบบร่างเล่าแผนหนึ่งนาที ไม่ต้องเขียนสรุปหรือบทพูดซ้ำ

---

## 3. Run sheet (`planning/INSTRUCTOR-RESOURCES.md`)

#### 7.6 Fill the canvas

**Done when** every canvas section has something: Input, Output (with how the team knows it actually runs),
Logic, at least one fail-safe plus a manual override, care and budget, the first pilot, and what the team is not
sure of yet.

#### 7.7 Paired exchange and revise

**Done when** both teams have pitched in one minute and given three minutes of feedback on two points:
the best-reasoned decision, and the part with no answer to "what happens if it fails". One change is
recorded in `d.revise`. There is no plenary.

#### 7.8 Check against the rubric

**Done when** the team has walked its canvas down the rubric: parts chosen from specs, with real prices;
network chosen on all four factors; power source per location; at least one fail-safe and a manual override; a named
carer and schedule; a budget that fits the farm; open questions and how they will be checked.

