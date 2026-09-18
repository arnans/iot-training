# Archived: Session 3 · Activity 7 · 7.3 remote-access menu, choice step and end question

Removed from the worksheet on 18 Sep 2026 (Roger: 7.3 has no action; students only listen to the
instructor explain the cloud concept, and the worksheet holds only acknowledgement checkboxes). Kept here
so it can be restored. Nothing in `archive/` is published or rendered.

The `d.comm.3.tech` / `d.comm.3.why` fields still exist in 7.6 and the record sheet, so restoring the choice
step needs no key changes.

**To restore**, replace the 7.3 section in `docs/activity-7.md` with the section below and the task-list
line with the one below; replace the run-sheet 7.3 block in `planning/INSTRUCTOR-RESOURCES.md` with the
blocks below; then re-run `python scripts/render-worksheets.py` and `python scripts/render-network-doc.py`.

---

## 1. Worksheet (`docs/activity-7.md`)

Task-list line:

- [ ] **[7.3 ระบบอยู่ในฟาร์ม คลาวด์ใช้เข้าถึงจากภายนอก](#a7-2c)** เข้าใจว่า Home Assistant ต้องอยู่ในฟาร์ม แล้วจดวิธีเข้าถึงจากนอกฟาร์มที่กลุ่มเลือก

Section:

### 7.3 ระบบอยู่ในฟาร์ม คลาวด์ใช้เข้าถึงจากภายนอก { #a7-2c }

**Home Assistant ต้องอยู่ในฟาร์ม**

1. Home Assistant ต้องคุยกับบอร์ดและเกตเวย์ในฟาร์มโดยตรง: บอร์ด WiFi ผ่านเครือข่ายภายใน ตัวรับ Zigbee หรือ LoRa ผ่านช่อง USB หรือสายแลน จึงต้องติดตั้งบนเครื่องที่อยู่ในฟาร์ม (แล็ปท็อปแบบในห้องนี้ มินิพีซี หรือ Raspberry Pi) ไม่ใช่บนคลาวด์ คลาวด์มีบทบาทเพียงเป็นทางเข้ามาดูและสั่งงานจากภายนอก และเป็นที่รับสำเนาข้อมูลถ้าต้องการ คุยกันว่าถ้าอินเทอร์เน็ตของฟาร์มดับ แต่ไฟฟ้าและเครือข่ายภายในยังใช้ได้ กฎยังทำงานหรือไม่ ดูแดชบอร์ดจากที่ใดได้บ้าง และข้อมูลใหม่ยังถูกบันทึกหรือไม่

> อุปกรณ์ IoT สำเร็จรูปบางยี่ห้อส่งข้อมูลให้คลาวด์ของผู้ผลิตตัดสินใจแล้วรับคำสั่งกลับมา เมื่ออินเทอร์เน็ตดับจึงสั่งงานไม่ได้ ระบบที่เราสร้างไม่เป็นแบบนั้น เพราะกฎอยู่ที่ Home Assistant ในฟาร์ม

ใช้คำตอบนี้ประกอบการเลือกวิธีเข้าถึงจากนอกฟาร์มในข้อ 3

**สำรวจทางเลือกการเข้าถึงจากภายนอก**

2. อ่านตารางแล้วเปรียบเทียบงานที่ทำได้ ค่าบริการ และผู้ดูแล ทุกวิธีเป็นทางเข้ามาหา Home Assistant ในฟาร์ม ไม่ได้ย้ายระบบไปไว้บนคลาวด์ และทุกวิธีต้องมีอินเทอร์เน็ตที่ฟาร์ม

| วิธี | ใช้ทำอะไร | ต้องเตรียมอะไร |
|---|---|---|
| **แจ้งเตือนอย่างเดียว** | รับข้อความเมื่อมีเหตุ | ช่องทางแจ้งเตือนและการตั้งค่าส่งข้อความ |
| **Home Assistant Cloud** | เปิดแดชบอร์ดและสั่งงานจากภายนอก | บัญชีและบริการสมัครสมาชิก |
| **VPN** | เชื่อมเข้าเครือข่ายส่วนตัวของฟาร์ม | ตั้งค่าการเชื่อมต่อและสิทธิ์ของผู้ใช้ |
| **ส่งสำเนาข้อมูลขึ้นคลาวด์** | ดูข้อมูลหลายฟาร์มบนเว็บของผู้ให้บริการ | บัญชีและการตั้งค่าส่งข้อมูล กฎยังทำงานที่ Home Assistant ในฟาร์มเช่นเดิม |

เปรียบเทียบค่าบริการและผู้ดูแลก่อนเลือก ไม่ต้องตั้งค่าตามทุกวิธี

**จดข้อสรุป**

3. คุยกันว่าเจ้าของต้องเข้ามาดูและสั่งงานจากนอกฟาร์ม หรือต้องการเพียงแจ้งเตือน แล้วจดวิธีที่เลือกและเหตุผลในแถว “จากฟาร์มถึงเจ้าของนอกฟาร์ม” ถ้าไม่จำเป็นต้องเข้าถึงจากภายนอก ให้ระบุว่า “ไม่ใช้”

| การเข้าถึง | วิธีที่เลือก | ทำไมจึงเลือกวิธีนี้ |
|---|---|---|
| จากฟาร์มถึงเจ้าของนอกฟาร์ม | {{f:d.comm.3.tech|16}} | {{f:d.comm.3.why|30}} |

[↑ กลับไปที่ใบงาน](#a7){ .ws-back }

**คุยท้ายเรื่อง** ถ้าอินเทอร์เน็ตดับ แต่ WiFi และ Home Assistant ในฟาร์มยังทำงาน แล้วเราจะใช้อะไรได้บ้าง หาก Home Assistant ดับไปด้วย ผลจะต่างจากเดิมอย่างไร นำข้อสรุปไปใช้ตอนออกแบบระบบใน 7.6
{: #a7-2q }

---

## 2. Run sheet (`planning/INSTRUCTOR-RESOURCES.md`)

#### 7.3 Home Assistant stays on the farm · cloud demo · choose remote access

One worksheet step since 18 Sep 2026 (Roger: the block is instructor-led, no need for three sub-activities).
The demo is scripted here only, not in the worksheet.

**Done when, where the system lives** the team can say why Home Assistant sits on a machine in the farm: it
must reach the boards on the local network, or a Zigbee or LoRa receiver on USB or LAN, so it cannot run
in the cloud. Never present a cloud-hosted Home Assistant as an option (Roger, 18 Sep 2026). The cloud is
a door in from outside and, at most, a place that receives a copy of the data. With the internet down:
automations yes, dashboard on the farm WiFi yes, new data still logged yes; live view from outside and
notifications no. The contrast, if asked, is a vendor-cloud product that sends its data to the maker's
server to decide and waits for the command back; that stops when the internet dies, and it is what
post-test item S3-POST-03 calls system B.

**Demo, instructor kit** Open **Settings → Home Assistant Cloud**, show the **Remote access** switch and the
address. Phone off WiFi, on mobile data, opens that address: the same dashboard the room saw on the
zone WiFi. Blow on the board, watch the value change on the phone, send one pump command. Ask what
the phone is connected through and where the deciding and recording still happen.

**Done when, demo** the answers are *mobile internet* and *on the farm (laptop)*. The cloud service is only a
door in; the farm's Home Assistant still decides and records.

**Done when, choice** need, method and "what is lost if the farm's internet dies" are consistent. For example,
notifications only means only messages are lost; the farm keeps running. The third
communication row in 7.3 is filled.

The worksheet's menu has four options since 15 Sep 2026: notifications only, Home Assistant Cloud,
VPN, and pushing data to a cloud platform. "Opening a door yourself" (port forwarding, DDNS, a
tunnel) was cut; mention it live if a team asks, with the warning that a bad setup exposes the farm.

#### Question after step 1

**A good answer** says that with the internet down, local automations, the dashboard on the farm WiFi and logging carry on,
while remote viewing and notifications stop. With Home Assistant down, automations, logging and the
dashboard all stop. Only protection in the board or the wiring, and the manual switch, remain.

