# Archived: Session 3 · Activity 7 · 7.4 Cloud demo and 7.5 Choose remote access

Removed from the worksheets on 18 Sep 2026 (Roger: the block is instructor-led and 7.3 covers it;
no need for separate sub-activities). Kept here so it can be restored. Nothing in `archive/` is
published or rendered.

What survived the cut: the canvas row `d.comm.3.tech` / `d.comm.3.why` moved into 7.3 as step 3, and the
demo script moved into the run sheet under 7.3.

**To restore**, paste each part back where it came from, delete step 3 from 7.3, restore the run-sheet
7.3 block below, then renumber 7.4–7.8 back to 7.6–7.10 in the worksheet, the run sheet,
`assessments/*.md` (`หัวข้อ 7.x`), `planning/WORKSHEET-TODO.md` and `planning/COURSE-DESIGN.md`:

1. **Worksheet** → `docs/activity-7.md`: the two task-list lines go after the 7.3 line inside the
   `ws-tasks` block; the sections go after 7.3's `[↑ กลับไปที่ใบงาน]` line, before `**คุยท้ายเรื่อง**`.
2. **Run sheet** → `planning/INSTRUCTOR-RESOURCES.md`: replace the merged `#### 7.3` block with the
   three blocks below, before `#### Question after step 1`.
3. Re-run `python scripts/render-worksheets.py` and `python scripts/render-network-doc.py`.

---

## 1. Worksheet (`docs/activity-7.md`)

Task-list lines:

- [ ] **[7.4 ดูสาธิตการเข้าถึงจากนอกฟาร์ม](#a7-2d)** สังเกตช่องทางเชื่อมต่อและตำแหน่งที่ระบบตัดสินใจ
- [ ] **[7.5 เลือกวิธีเข้าถึงจากนอกฟาร์ม](#a7-2e)** จดวิธีที่กลุ่มต้องใช้และเหตุผล หรือระบุว่าไม่จำเป็น

Sections:

### 7.4 ดูสาธิตการเข้าถึงจากนอกฟาร์ม { #a7-2d }

ใช้ชุดของผู้สอน กลุ่มดูและตอบคำถามร่วมกัน

**ดูช่องทางเข้าถึงจากภายนอก**

1. ผู้สอนเปิด **Settings → Home Assistant Cloud** ให้ดูสวิตช์ **Remote access** และที่อยู่สำหรับเข้าถึงระบบจากภายนอก

**ทดสอบผ่านอินเทอร์เน็ตมือถือ**

2. ปิด WiFi บนโทรศัพท์ แล้วใช้อินเทอร์เน็ตมือถือเปิดที่อยู่นั้น สังเกตว่าเป็นแดชบอร์ดเดียวกับที่เปิดดูในเครือข่ายของห้องอบรม
3. เป่าลมใส่บอร์ด สังเกตค่าที่เปลี่ยนบนโทรศัพท์ แล้วทดลองสั่งปั๊มหนึ่งครั้ง

ในการสาธิตนี้ Home Assistant ที่ฟาร์มยังตัดสินใจและบันทึกข้อมูล บริการคลาวด์ช่วยให้เข้าถึงเครื่องเดิมจากภายนอก

**ทบทวนจากสิ่งที่เห็น**

4. คุยกันว่าโทรศัพท์เชื่อมต่อผ่านอะไร และส่วนที่ตัดสินใจกับบันทึกข้อมูลยังอยู่ที่ใด

[↑ กลับไปที่ใบงาน](#a7){ .ws-back }

### 7.5 เลือกวิธีเข้าถึงจากนอกฟาร์ม { #a7-2e }

**เลือกวิธีตามความต้องการ**

1. คุยกันว่าเจ้าของต้องเข้ามาดูและสั่งงานจากนอกฟาร์ม หรือต้องการเพียงแจ้งเตือน แล้วเลือกวิธีที่เหมาะ ถ้าไม่จำเป็นต้องเข้าถึงจากภายนอก ให้ระบุว่า “ไม่ใช้”

**จดข้อสรุปลงแบบร่าง**

2. จดวิธีที่เลือกและเหตุผลในแถว “จากฟาร์มถึงเจ้าของนอกฟาร์ม” พร้อมระบุว่าระบบประมวลผลและสั่งงานอยู่ที่ใด

| การเข้าถึง | วิธีที่เลือก | ทำไมจึงเลือกวิธีนี้ |
|---|---|---|
| จากฟาร์มถึงเจ้าของนอกฟาร์ม | {{f:d.comm.3.tech|16}} | {{f:d.comm.3.why|30}} |

[↑ กลับไปที่ใบงาน](#a7){ .ws-back }

---

## 2. Run sheet (`planning/INSTRUCTOR-RESOURCES.md`), the 7.3–7.5 blocks before the merge

#### 7.3 If the internet goes down

**Done when**

- *Our system:* automations yes, dashboard on the farm WiFi yes, live data from outside no, new data still logged yes.
- *Cloud-run system:* automations no, farm dashboard no, live data from outside no, nothing new logged.

#### 7.4 Home Assistant Cloud demo

**Done when** the answers are *mobile internet* and *on the farm (laptop)*. The cloud service is only a
door in; the farm's Home Assistant still decides and records.

#### 7.5 Choose remote access for the team's farm

**Done when** need, method and "what is lost if the farm's internet dies" are consistent. For example,
notifications only means only messages are lost; the farm keeps running. The canvas's third
communication row and "where the logic runs" are filled.

The worksheet's menu has four options since 15 Sep 2026: notifications only, Home Assistant Cloud,
VPN, and pushing data to a cloud platform. "Opening a door yourself" (port forwarding, DDNS, a
tunnel) was cut; mention it live if a team asks, with the warning that a bad setup exposes the farm.

