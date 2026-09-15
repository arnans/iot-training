# Archived: Session 1 · Activity 4 — Spec (15 min)

Removed from the worksheets on 15 Sep 2026 (Roger: no time for it in Session 1). Kept here so it can
be restored. Nothing in `archive/` is published or rendered.

**To restore**, paste each part back where it came from:

1. **Worksheet** → `docs/session-1.md`, after Activity 3's end question and its `---`, before
   `## ก่อนออกจากห้อง`. Follow it with a `---` line. Also restore summary point 6:
   `6. **เลือกอุปกรณ์ให้ตรงกับงาน** หากความต้องการเกินสเปก ต้องเปลี่ยนอุปกรณ์ให้เหมาะสม`
2. **Record sheet** → `docs/record-sheet.md`, after the Activity 3 question (`{{ta:s1.q3}}`),
   before the `---` that opens `## ช่วงที่ 2`.
3. **Run sheet** → `planning/INSTRUCTOR-RESOURCES.md`, after Session 1 Activity 3, before
   `### Session 2 · Activity 5`.
4. Re-run `python scripts/render-worksheets.py` and `python scripts/render-network-doc.py`.

The fields keep their original keys (`s1.spec.*`, `s1.card`, `s1.q4`), so answers exported
before removal still import. Scenario cards and spec handouts are listed in `planning/WORKSHEET-TODO.md`.

---

## 1. Worksheet (`docs/session-1.md`)

## กิจกรรมที่ 4 — อ่านสเปกและเลือกอุปกรณ์ (Spec)

**15 นาที**

**อุปกรณ์ที่ใช้** บัตรสถานการณ์จากผู้สอน, สเปกที่แจก (เซนเซอร์ความชื้นและอุณหภูมิ สวิตช์ลูกลอย ปั๊มที่จะใช้ในช่วงที่ 2), บอร์ดรีเลย์ ไม่ต้องแตะอุปกรณ์ที่ต่ออยู่

> กิจกรรมนี้ไม่ข้าม ถ้าเวลาเหลือน้อยกว่า 15 นาที ให้ทำแบบย่อ: อ่านสเปกเฉพาะรีเลย์กับปั๊ม บัตรใบเดียว ตอบผ่านหรือไม่ผ่านข้อเดียว

เราทดลองจนรู้แล้วว่าชุดอุปกรณ์นี้ทำงานได้ ต่อไปต้องพิจารณาว่าเหมาะกับงานที่ต้องการหรือไม่ ให้กลุ่มรับบัตรสถานการณ์หนึ่งใบ แล้วเปรียบเทียบความต้องการในบัตรกับสเปกของอุปกรณ์

### ใบงาน { #a4 }

<div class="ws-tasks" markdown>
ข้อใดเสร็จแล้วให้กรอกในใบงานนี้ด้วย

- [ ] **[4.1 อ่านสเปกเซนเซอร์และสวิตช์ลูกลอย](#a4-1)** ความแม่นยำความชื้นอากาศ ± {{n:s1.spec.hum_acc|4}} %RH อุณหภูมิ ± {{n:s1.spec.temp_acc|4}} °C · สวิตช์ลูกลอยทนได้ {{n:s1.spec.float_a|4}} A {{n:s1.spec.float_v|4}} V
- [ ] **[4.1 อ่านสเปกรีเลย์และปั๊ม](#a4-1)** รีเลย์ DC {{n:s1.spec.relay_dc_a|3}} A {{n:s1.spec.relay_dc_v|3}} V · AC {{n:s1.spec.relay_ac_a|3}} A {{n:s1.spec.relay_ac_v|3}} V · ปั๊มใช้กระแส {{n:s1.spec.pump_a|4}} A (ถ้าเวลาเหลือน้อยกว่า 15 นาที ข้ามข้อบนมาทำข้อนี้ แล้วเทียบกับงานในบัตรข้อเดียว)
- [ ] **[4.2 เปรียบเทียบกับงานในบัตร](#a4-2)** บัตรสถานการณ์หมายเลข {{f:s1.card|3}}
    - งานต้องการ {{f:s1.spec.need1|16}} ชุดเราให้ได้ {{f:s1.spec.have1|16}} {{r:s1.spec.pass1|ผ่าน|ไม่ผ่าน}}
    - งานต้องการ {{f:s1.spec.need2|16}} ชุดเราให้ได้ {{f:s1.spec.have2|16}} {{r:s1.spec.pass2|ผ่าน|ไม่ผ่าน}}
    - ถ้าไม่ผ่าน ชิ้นที่ต้องเปลี่ยน {{f:s1.spec.change|16}}
- [ ] **[คำถามท้ายกิจกรรม](#a4-q)** ชุดเรารับงานในบัตรได้หรือไม่ เพราะสเปกข้อใด {{ta:s1.q4}}

</div>

### 4.1 อ่านสเปกของชุดเรา { #a4-1 }

- **เซนเซอร์ความชื้นอากาศและอุณหภูมิ** ช่วงการวัด · ความแม่นยำ (± กี่ %RH และ ± กี่ °C) · ค่าที่เราเห็นแกว่งอยู่ในช่วงความแม่นยำนั้นหรือไม่ บันทึก ± {{n:s1.spec.hum_acc|4}} %RH ± {{n:s1.spec.temp_acc|4}} °C
- **สวิตช์ลูกลอย** ทนกระแสและแรงดันได้เท่าไร · วัสดุ · ปิดวงจรเมื่อลอยขึ้นหรือลง บันทึก {{n:s1.spec.float_a|4}} A {{n:s1.spec.float_v|4}} V
- **รีเลย์** อ่านตัวเลขที่พิมพ์บนตัวรีเลย์สีน้ำเงินบนบอร์ด จะเห็นสี่บรรทัด เช่น `10A 250VAC` และ `10A 30VDC` จดค่าฝั่ง DC ไว้ บันทึก DC {{n:s1.spec.relay_dc_a|3}} A {{n:s1.spec.relay_dc_v|3}} V · AC {{n:s1.spec.relay_ac_a|3}} A {{n:s1.spec.relay_ac_v|3}} V
- **ปั๊มของเรา** (จะต่อในช่วงที่ 2) กระแสที่ใช้ตามสเปก เทียบกับพิกัดรีเลย์ บันทึก {{n:s1.spec.pump_a|4}} A

[↑ กลับไปที่ใบงาน](#a4){ .ws-back }

### 4.2 เปรียบเทียบกับงานที่ต้องการ { #a4-2 }

ในบัตรสถานการณ์จะระบุงานและค่าที่ต้องการ เช่น ความแม่นยำในการวัดอุณหภูมิ หรือกระแสไฟฟ้าที่ปั๊มใช้ ให้เทียบกับสเปกทีละข้อ แล้วกรอกผลลงในตาราง **บัตรสถานการณ์หมายเลข** {{f:s1.card|3}}

| งานต้องการ (จากบัตร) | ชุดเราให้ได้ (จากสเปก) | ผ่าน / ไม่ผ่าน |
|-----------|-------------|---------------|
| {{f:s1.spec.need1|16}} | {{f:s1.spec.have1|16}} | {{r:s1.spec.pass1|ผ่าน|ไม่ผ่าน}} |
| {{f:s1.spec.need2|16}} | {{f:s1.spec.have2|16}} | {{r:s1.spec.pass2|ผ่าน|ไม่ผ่าน}} |

ถ้าอุปกรณ์ไม่ผ่านเกณฑ์ ให้ระบุว่าควรเปลี่ยนอุปกรณ์ชิ้นใดเพื่อให้ใช้งานได้ โดยยังใช้ส่วนอื่นของชุดเดิม ชิ้นที่ต้องเปลี่ยน {{f:s1.spec.change|16}}

> สเปกบอกขอบเขตการใช้งานของอุปกรณ์ หากงานต้องการเกินกว่าที่ระบุไว้ ต้องเลือกอุปกรณ์ใหม่ให้เหมาะสม การแก้กฎควบคุมอย่างเดียวไม่สามารถชดเชยข้อจำกัดของอุปกรณ์ได้

[↑ กลับไปที่ใบงาน](#a4){ .ws-back }

**คำถามท้ายกิจกรรม** ชุดเรารับงานในบัตรได้หรือไม่ เพราะสเปกข้อใด
{: #a4-q }

{{ta:s1.q4}}

ผู้สอนสรุปห้าอย่างที่ต้องอ่านบนสเปกทุกครั้ง: ช่วงการวัด · ความแม่นยำ · อินเทอร์เฟซ · แรงดันและกระแส · IP rating

---

## 2. Record sheet (`docs/record-sheet.md`)

**สเปก** (กิจกรรมที่ 4) ความแม่นยำเซนเซอร์ความชื้น ± {{n:s1.spec.hum_acc|4}} %RH อุณหภูมิ ± {{n:s1.spec.temp_acc|4}} °C · สวิตช์ลูกลอยทนได้ {{n:s1.spec.float_a|4}} A {{n:s1.spec.float_v|4}} V

**รีเลย์** ทนได้ {{n:s1.spec.relay_dc_a|3}} A ที่ DC {{n:s1.spec.relay_dc_v|3}} V และ {{n:s1.spec.relay_ac_a|3}} A ที่ AC {{n:s1.spec.relay_ac_v|3}} V · ปั๊มใช้กระแส {{n:s1.spec.pump_a|4}} A

**บัตรสถานการณ์หมายเลข** {{f:s1.card|3}}

| งานต้องการ (จากบัตร) | ชุดเราให้ได้ (จากสเปก) | ผ่าน / ไม่ผ่าน |
|-----------|-------------|---------------|
| {{f:s1.spec.need1|16}} | {{f:s1.spec.have1|16}} | {{r:s1.spec.pass1|ผ่าน|ไม่ผ่าน}} |
| {{f:s1.spec.need2|16}} | {{f:s1.spec.have2|16}} | {{r:s1.spec.pass2|ผ่าน|ไม่ผ่าน}} |

ถ้าไม่ผ่าน ชิ้นที่ต้องเปลี่ยน {{f:s1.spec.change|16}}

**คำถามท้ายกิจกรรมที่ 4** ชุดเรารับงานในบัตรได้หรือไม่ เพราะสเปกข้อใด ถ้าไม่ผ่าน ต้องเปลี่ยนชิ้นใด

{{ta:s1.q4}}

---

## 3. Instructor run sheet (`planning/INSTRUCTOR-RESOURCES.md`)

### Session 1 · Activity 4 — Spec (15 min)

Paper only. Never skipped: under 15 minutes left, run the short form (relay and pump only, one
card, one pass/fail).

#### 4.1 Sensor and float specs

**Done when** the humidity and temperature accuracy and the float's current and voltage rating are copied
from the handout. The humidity sensor on the board is a GXHT30C (SHT3x-compatible).

#### 4.1 Relay and pump specs

**Done when** the relay's printed ratings are read off the blue relay itself: `10A 30VDC` and `10A 250VAC`.
The pump current comes from its spec, 18 W at 12 V, which is 1.5 A.

**If stuck** Check the comparison uses the DC rating: our pump circuit is 12 V DC.

#### 4.2 Compare with the card

**Done when** each of the card's demands sits next to what the kit offers, with a pass or fail, and a failed card names the one
part to change. The card set is built so one card exceeds the sensor accuracy (change the sensor),
one exceeds the relay rating (change the relay or add a contactor), and one passes.

#### End-of-activity question

**A good answer** names the spec line that decided it, not "it worked on the table". Close with
the five things to read on every spec: range, accuracy, interface, voltage and current, IP rating.
