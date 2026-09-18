# Archived: Session 3 · Activity 7 · 7.2 Survey the room network

Removed from the worksheets on 18 Sep 2026 (Roger: no clear point). Kept here so it can be
restored. Nothing in `archive/` is published or rendered.

**To restore**, paste each part back where it came from, then renumber 7.2–7.10 back to 7.3–7.11
in the worksheet, the run sheet, `assessments/*.md` (`หัวข้อ 7.x`), `planning/WORKSHEET-TODO.md` and
`planning/COURSE-DESIGN.md`:

1. **Worksheet** → `docs/activity-7.md`: the task-list line goes after the 7.1 line inside the
   `ws-tasks` block; the section goes after 7.1's `[↑ กลับไปที่ใบงาน]` line, before `### 7.3`.
2. **Run sheet** → `planning/INSTRUCTOR-RESOURCES.md`, after `#### 7.1 Pick the scenario`, before
   `#### 7.3 Choose the farm network`.
3. Re-run `python scripts/render-worksheets.py` and `python scripts/render-network-doc.py`.

The section had no form fields, so nothing in the record sheet or the exported answers changes.

---

## 1. Worksheet (`docs/activity-7.md`)

Task-list line:

- [ ] **[7.2 สำรวจเครือข่ายในห้อง](#a7-2)** ดูการตั้งค่าและลองเปิดหน้าเว็บของบอร์ดร่วมกัน

Section:

### 7.2 สำรวจเครือข่ายในห้อง { #a7-2 }


**อ่านการตั้งค่าเครือข่าย**

1. เปิดไฟล์ ESPHome ที่แจก หา **ssid** (ชื่อ WiFi), **name_add_mac_suffix** (เติมรหัสท้ายชื่อบอร์ด) และ **api** (เชื่อมกับ Home Assistant)

**เปิดหน้าเว็บผ่านเครือข่ายภายใน**

2. ใน **Settings → Devices & services → ESPHome** เปิดอุปกรณ์และอ่านค่า **หมายเลข IP**
3. เปิดแท็บใหม่ พิมพ์ `http://` ตามด้วย IP เพื่อเปิดหน้าเว็บของบอร์ด

> บอร์ดกับ Home Assistant สื่อสารผ่านเครือข่ายภายใน ไม่จำเป็นต้องผ่านอินเทอร์เน็ต ส่วนการดูจากนอกฟาร์มต้องมีช่องทางเพิ่ม

[↑ กลับไปที่ใบงาน](#a7){ .ws-back }

---

## 2. Run sheet (`planning/INSTRUCTOR-RESOURCES.md`)

#### 7.2 The network we already use

**Done when** the team has found `ssid`, `name_add_mac_suffix` and `api` in the ESPHome file, and has opened the board's page
from the IP entity Home Assistant shows. There is no fixed IP in the file: the router hands it out.

