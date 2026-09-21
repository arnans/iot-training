# รวมไฟล์และลิงก์

หน้านี้รวมทุกไฟล์และทุกลิงก์ที่ผู้เข้าอบรมต้องใช้ไว้ที่เดียว เปิดหน้านี้เมื่อจำไม่ได้ว่าของที่ต้องการอยู่หน้าไหน ขั้นตอนการทำงานจริงอยู่ในใบงานแต่ละช่วง

---

## 1. ก่อนวันอบรม — ติดตั้งลงแล็ปท็อป

ทำให้เสร็จ **ที่บ้านก่อนวันอบรม** ขั้นตอนละเอียดอยู่ใน[คู่มือเตรียมแล็ปท็อป](install.md)

ดูว่าแล็ปท็อปของเราเป็นแบบไหน แล้วดาวน์โหลด **ทั้งสองไฟล์ในแถวนั้น** (Mac: เมนู Apple → About This Mac ดูบรรทัด Chip หรือ Processor)

| แล็ปท็อป | VirtualBox | ไฟล์ Farm Workshop |
|---------|-----------|------------------------------|
| Windows | [Windows hosts](https://www.virtualbox.org/wiki/Downloads) | [Farm-Workshop-win-1.2.ova](https://drive.google.com/file/d/1DrX4O-jywvnCA0b4aqdQ3z9r7F2EkEf8/view?usp=sharing) (~2.6 GB) |
| Mac ชิป Intel | [macOS / Intel hosts](https://www.virtualbox.org/wiki/Downloads) | [Farm-Workshop-win-1.2.ova](https://drive.google.com/file/d/1DrX4O-jywvnCA0b4aqdQ3z9r7F2EkEf8/view?usp=sharing) (~2.6 GB) |
| Mac ชิป Apple (M1 ขึ้นไป) | [macOS / Apple Silicon hosts](https://www.virtualbox.org/wiki/Downloads) — ต้อง **รุ่น 7.2 ขึ้นไป** | [Farm-Workshop-arm64-1.2.ova](https://drive.google.com/drive/folders/1XiTigV52XVenZ8DhMZ6351dHOZvRHgMD) (~1.9 GB) — ลิงก์เปิดเป็นโฟลเดอร์ ให้ดาวน์โหลดไฟล์ `.ova` ที่อยู่ข้างใน |

> ไฟล์ `.ova` มีขนาดใหญ่ **ดาวน์โหลดที่บ้านหรือที่ทำงานล่วงหน้า** ดาวน์โหลดที่สถานที่อบรมไม่ทัน · ต้องมี RAM 8 GB และพื้นที่ว่าง 20 GB ขึ้นไป · Chromebook, iPad และ Windows ชิป ARM ใช้ไม่ได้ · **Mac ชิป Apple ใช้ไฟล์ของ Windows ไม่ได้** ต้องใช้ไฟล์ `arm64` และ VirtualBox รุ่น 7.2 ขึ้นไป

| สิ่งที่ต้องทำ | ลิงก์ |
|--------------|-------|
| คู่มือติดตั้งทีละขั้น | [เตรียมแล็ปท็อปก่อนวันอบรม](install.md) |
| ไฟล์ที่ต้องมีหากติดตั้ง VirtualBox บน Windows แล้วไม่ผ่าน | [vc_redist.x64.exe](https://aka.ms/vs/17/release/vc_redist.x64.exe) |

---

## 2. ใบงานที่ใช้ระหว่างอบรม

เปิดจากโทรศัพท์หรือแล็ปท็อปก็ได้ คำตอบที่กรอกจะถูกจำไว้ในเบราว์เซอร์ของเครื่องที่กรอก

| หน้า | ใช้เมื่อ |
|------|---------|
| [เริ่มต้นที่นี่](index.md) | ดูภาพรวม อุปกรณ์ในชุด ข้อควรระวัง และคำศัพท์ |
| [ช่วงที่ 1 — รับรู้ ตัดสินใจ สั่งการ](session-1-start.md) | อ่านค่าเซนเซอร์ ต่อวงจร 12V และสั่งปั๊มจากแดชบอร์ด |
| [ช่วงที่ 2 — ควบคุมอัตโนมัติและ Fail-safe](activity-4.md) | เขียนกฎอัตโนมัติ hysteresis และกฎกันพลาด |
| [ช่วงที่ 3 — แดชบอร์ดและออกแบบระบบ](activity-6.md) | อ่านกราฟ สร้างแดชบอร์ด และออกแบบระบบของกลุ่ม |
| [ช่วงที่ 4 — ขยายระบบไปแปลงที่ WiFi ไม่ถึง](activity-9.md) | อัปเดตเฟิร์มแวร์ให้ส่ง ESP-NOW เพิ่มบอร์ดตัวรับ และแดชบอร์ดแปลงไกล |
| [ใบบันทึกของกลุ่ม](record-sheet.md) | รวมคำตอบทุกช่อง รวมทั้งแบบระบบจากกิจกรรมที่ 8 กด **ดาวน์โหลดคำตอบ** ก่อนจบการอบรม และ **พิมพ์ / บันทึก PDF** ไว้อ้างอิง |
| [เมนูและวิธีแก้ปัญหา](reference.md) | ค้นเมนู Home Assistant และแก้อาการที่เจอบ่อย |

> กลุ่มที่สะดวกเขียนกระดาษ ให้พิมพ์[ใบบันทึกของกลุ่ม](record-sheet.md)ตอนที่ยังว่างไว้ล่วงหน้า

---

## 3. เว็บและที่อยู่ที่ใช้ระหว่างอบรม

| ต้องการ | เปิดที่ |
|---------|--------|
| อ่านชื่อบอร์ดจากสาย USB และติดตั้งเฟิร์มแวร์ (ช่วงที่ 4) | <https://web.esphome.io> (ใช้ Chrome หรือ Edge เท่านั้น) |
| เปิด Home Assistant ของกลุ่ม | `http://` ตามด้วยเลข IP ที่อ่านจากหน้าต่างเครื่อง Farm Workshop — **ไม่ใช้ `homeassistant.local`** และไม่ต้องใส่ `:8123` |
| ดูค่าจากบอร์ดโดยตรง ไม่ผ่าน Home Assistant | `http://` ตามด้วย IP ของบอร์ด หรือ `http://<ชื่อบอร์ด>/` (ต้องมี `/` ปิดท้าย) |
| ใบงานหน้านี้ทั้งชุด | <https://arnans.github.io/iot-training/> |

**ไฟล์เฟิร์มแวร์สำหรับช่วงที่ 4** เลือกไฟล์ตามสีโซนของกลุ่ม ติดตั้งผ่าน web.esphome.io ตามขั้นตอนในกิจกรรมที่ 9 และ 10

| บอร์ด | แดง | เขียว | น้ำเงิน |
|---|---|---|---|
| GoGo-IoT รุ่น ESP-NOW (ติดตั้งทับรุ่นเดิมในกิจกรรมที่ 9) | [gogo-iot-espnow-red.factory.bin](https://arnans.github.io/iot-training/firmware/gogo-iot-espnow-red.factory.bin) | [gogo-iot-espnow-green.factory.bin](https://arnans.github.io/iot-training/firmware/gogo-iot-espnow-green.factory.bin) | [gogo-iot-espnow-blue.factory.bin](https://arnans.github.io/iot-training/firmware/gogo-iot-espnow-blue.factory.bin) |
| บอร์ดตัวรับ (ESP32-C3) | [farm-receiver-red.factory.bin](https://arnans.github.io/iot-training/firmware/farm-receiver-red.factory.bin) | [farm-receiver-green.factory.bin](https://arnans.github.io/iot-training/firmware/farm-receiver-green.factory.bin) | [farm-receiver-blue.factory.bin](https://arnans.github.io/iot-training/firmware/farm-receiver-blue.factory.bin) |

---

## 4. สิ่งที่ผู้สอนแจกที่โต๊ะ

| ของ | มีอะไรอยู่บนนั้น |
|-----|------------------|
| **บัตรประจำกลุ่ม** | สีโซนของกลุ่ม · ชื่อและรหัส WiFi ของโซน (ชื่อผู้ใช้และรหัสผ่าน Home Assistant ผู้สอนแจ้งในกิจกรรมที่ 3) |
| **ชุดอุปกรณ์ของกลุ่ม** | รายการทั้งหมดอยู่ในหน้า[เริ่มต้นที่นี่](index.md) |
| **ใบบันทึกของกลุ่มแบบพิมพ์** | ฉบับเดียวกับ[ใบบันทึกของกลุ่ม](record-sheet.md)บนเว็บ |

> **บัตรประจำกลุ่มไม่มีชื่อบอร์ด** ชื่อบอร์ดอ่านจากบอร์ดเองในกิจกรรมที่ 1 · ก่อนเริ่มให้ตรวจว่า **สีบนบอร์ด สีบนบัตร และชื่อ WiFi ที่แล็ปท็อปเชื่อมต่อ ตรงกันทั้งหมด**

---

## 5. หลังการอบรม — ถ้าอยากทำต่อเอง

ไม่ต้องใช้ในห้องอบรม แต่เป็นจุดเริ่มต้นสำหรับคนที่อยากสร้างระบบของตัวเองต่อ

| แหล่งข้อมูล | คืออะไร |
|------------|---------|
| [Home Assistant](https://www.home-assistant.io/) | คู่มือและวิธีติดตั้งอย่างเป็นทางการของซอฟต์แวร์ที่เราใช้ |
| [ESPHome](https://esphome.io/) | ซอฟต์แวร์ที่อยู่ในบอร์ดของเรา ใช้เขียนค่าเซนเซอร์และรีเลย์เป็นไฟล์ YAML |
| [ไฟล์ตั้งค่าบอร์ดของการอบรมนี้](https://github.com/arnans/iot-training/tree/main/firmware) | ไฟล์ ESPHome ของบอร์ด GoGo-IoT บอร์ดรีเลย์ และบอร์ดตัวรับ ESP-NOW ที่เราใช้ |
| [ESP-NOW ใน ESPHome](https://esphome.io/components/espnow.html) | เอกสารของส่วนที่บอร์ดใช้คุยกันในช่วงที่ 4 สำหรับคนที่อยากปรับตัวส่งและตัวรับเอง |
| [ไฟล์ตั้งค่า Home Assistant ของการอบรมนี้](https://github.com/arnans/iot-training/tree/main/hass) | `configuration.yaml` ที่อยู่ในเครื่อง Farm Workshop |
| [บอร์ด GoGo-IoT](https://github.com/arnans/gogo-iot-node) | ข้อมูลฮาร์ดแวร์ของบอร์ดเซนเซอร์ที่ใช้ในห้องอบรม |
| [Nabu Casa — Home Assistant Cloud](https://www.nabucasa.com) | บริการเข้าถึง Home Assistant จากนอกฟาร์มที่พูดถึงในกิจกรรมที่ 8 มีค่าบริการรายเดือน |

> เครื่อง Farm Workshop ในแล็ปท็อปยังใช้ต่อได้หลังจบการอบรม เปิด VirtualBox แล้วกด Start ได้เหมือนเดิม แต่บอร์ดจะหาไม่เจอเพราะ WiFi ของโซนมีเฉพาะในห้องอบรม ต้องแก้ WiFi ในบอร์ดด้วย ESPHome ก่อน

## นำไปใช้ที่ฟาร์มอย่างไร

เริ่มจากแบบระบบที่ออกแบบไว้ในกิจกรรมที่ 8 ตรวจสเปกและราคาก่อนซื้อ และจัดให้เครื่องบันทึกข้อมูลมีไฟกับเครือข่ายต่อเนื่อง

**อ่านต่อหลังอบรม:** [คู่มือติดตั้ง](install.md)

- ฝึกตั้งค่า ESPHome และเลือกเซนเซอร์ให้ตรงกับงาน
- ทดลองการป้องกันที่ตัวบอร์ดเมื่อ Home Assistant ติดต่อไม่ได้
- สำรวจสัญญาณและคำนวณแผงกับแบตเตอรี่จากการใช้ไฟจริง
- เลือกวิธีเข้าถึงจากนอกฟาร์มและผู้ดูแลระบบ
