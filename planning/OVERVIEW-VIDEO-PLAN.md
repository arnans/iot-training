# Overview video — chapters, inserts and speaker zooms

Pre-workshop viewing: a general overview of designing automation systems that survive real use.
Not a prerequisite and not tied to the worksheet, so inserts must stand on their own for someone
who has not seen the kit.

**Source:** `user-import/automation-iot-overview.mkv` — 27:24, H.264 1080p30 + AAC, single
locked-off talking-head take, no screen content, no cutaways. Everything visual comes from inserts.

**Transcript:** `user-import/overview-video/transcript.md` (faster-whisper `large-v3`, 12,501 words,
one dropped window at 0:59–1:07 recovered by gap repair). Both are gitignored with `user-import/`.

**Insert rule:** pictures, diagrams and real artifacts only. No bullet cards. Text appears only as
a label on a picture, a short caption, or on the cover and chapter cards.

---

## 1. Structure — three videos (decided 21 Sep 2026)

Cut from the one take at sentence ends found in the word stream, not at round numbers. Each video
gets a cover card and an end card; text is allowed on both.

| Video | Title (working) | Source in | Source out | Length | Opens on | Closes on |
|---|---|---|---|---|---|---|
| **V1** | ประกอบระบบอัตโนมัติ | 0:03.3 | 15:01.3 | 14:58 | "สวัสดีครับ วันนี้อยากจะมาพูดถึง…" | "…อาจจะเป็น farm อัจฉริยะ นี่ผมคิดว่าผ่านแล้ว" |
| **V2** | Fail-safe: ทำอย่างไรเมื่อระบบไม่ทำงานอย่างที่คาด | 15:06.2 | 22:41.8 | 7:36 | "งานพวกนี้ครึ่งแรกง่าย…" | "…แยกคนที่เป็นมือใหม่กับคนที่มีประสบการณ์ออกจากกันได้" |
| **V3** | ตัดสินใจด้วยข้อมูล | 22:47.1 | 27:20.8 | 4:34 | "ส่วนสุดท้ายที่อยากจะฝากไว้…" | "…ขอบคุณมากครับ" |

Dropped between videos: 15:02.2–15:06.0 *"ก็ส่วนที่เหลือก็คือส่วนของ detail"* (a bridge that only
reads in the continuous cut) and 22:41.5–22:43.3 *"เรื่องของ Failsafe นี้"* (tail of V2's topic).

V1 is twice the length of the others. It could split again at 8:34 (components / logic & HA) if
15 minutes proves too long for pre-workshop viewing.

Chapter markers within each video, source timecodes:

| # | Chapter | In | Out | Beat |
|---|---|---|---|---|
| 1 | เปิดเรื่อง | 0:00 | 0:48 | Sharing experience; automation is not only a technical problem |
| 2 | องค์ประกอบ 3 ส่วน | 0:48 | 1:51 | Input / Actuator / Logic; logic used to be the barrier |
| 3 | เซ็นเซอร์ | 1:51 | 4:30 | Golden age of sensors; resolution, packaging, how it communicates |
| 4 | แอคชูเอเตอร์ | 4:30 | 8:34 | 80–90% is on/off; relay & contactor, terminals, load spec, safety |
| 5 | โลจิก & Home Assistant | 8:34 | 11:07 | PLC and ladder vs open-source HA; "Home" but fine for farm |
| 6 | รัน HA จริง | 11:07 | 13:11 | Always-on server, recording, Raspberry Pi, browser & mobile app |
| 7 | สร้าง Automation | 13:11 | 15:01 | Wizard, no code; Trigger then Action |
| | **— end V1 —** | | | |
| 8 | ครึ่งหลังที่ยากกว่า | 15:06 | 15:41 | **V2 cold open.** The easy half is done; making it work for real is the rest |
| 9a | น้ำหมด | 15:41 | 16:44 | Pump runs dry; float switch |
| 9b | ต่อลูกลอยสองแบบ | 16:44 | 18:45 | Through HA vs wired into the pump's power |
| 9c | ปั๊มไม่เดิน | 18:45 | 20:34 | Commanded on, not running; vibration, flow |
| 9d | เซ็นเซอร์หาย | 20:34 | 21:35 | Battery dies unnoticed |
| 9e | Timeout | 21:35 | 22:41 | Always cap the run time |
| | **— end V2 —** | | | |
| 10 | ตัดสินใจด้วยข้อมูล | 22:47 | 26:32 | **V3.** The payoff is learning something new; DO in ponds, rain from pressure |
| 11 | สรุป | 26:32 | 27:20 | What to go and study; close |

As its own video, V2's five fail-safe beats each earn a chapter marker.

---

## 2. Inserts

Status: **HAVE** already in the repo · **MAKE** I draw it · **SHOOT** needs you · **SOURCE** stock/CC, credited.

Every still is composited to exactly 1920×1080 before it goes on V2, per the pipeline rule.

### Chapter 2 — องค์ประกอบ 3 ส่วน

| In | What is said | Insert | Status |
|---|---|---|---|
| 0:52 | "ส่วนประกอบหลักๆ มีอยู่แค่ 3 ส่วน" | **Spine diagram:** Sensor → Logic → Actuator, three boxes, isometric to match the kit art. Recurs later as a small locator with the current box lit. | MAKE |
| 1:19 | "ถ้าดินแห้ง … จะไปรดน้ำ" | Trigger→action illustration, soil-dry variant of `a3-05-trigger-action-isometric-v4.png` | MAKE (restyle of HAVE) |
| 1:39 | "ใช้ระบบที่ชื่อ Home Assistant" | First look at the HA automation editor | HAVE `hass create new automation.mp4` |

### Chapter 3 — เซ็นเซอร์

| In | What is said | Insert | Status |
|---|---|---|---|
| 1:57 | "ยุคทองของเซ็นเซอร์" | Shopee/Lazada search results grid for "เซ็นเซอร์" | SHOOT (screenshot) |
| 2:26 | temp, air humidity, soil moisture, salinity, light, pressure | 2×3 tiles, one illustrated icon + one-word label per quantity (the kit photo only shows four of the six, and is workshop-specific) | MAKE |
| 2:41 | "ความละเอียดที่เราต้องการ … ±1–2 องศา vs ทศนิยม 2 ตำแหน่ง" | **Chart:** same temperature trace at three resolutions, side by side | MAKE |
| 3:11 | "ถ้ามันเป็นวงจรเปลือยเปล่า … วันสองวันก็พังแล้ว" | Bare module next to a potted/IP67 probe | HAVE (bare) + SOURCE (sealed) |
| 3:45 | "ระบบไร้สายก็มีหลากหลาย ไม่ใช่มีแค่ WiFi" | **Diagram:** coverage radius vs battery life, WiFi / Zigbee / LoRa, drawn as overlapping range circles on a plot of land | MAKE |

### Chapter 4 — แอคชูเอเตอร์

| In | What is said | Insert | Status |
|---|---|---|---|
| 4:56.8 | "สองอย่างนี้ถ้าเลือกอุปกรณ์ควบคุมเป็น…" (after the zoom on "เปิดปิด") | Two photos: a lamp, and a pump/solenoid valve | SOURCE |
| 5:16 | "relay หรือ contactor" | Relay board and a real contactor | HAVE `relay-board.jpg` + SOURCE (contactor) |
| 5:32 | "หลักการข้างในจริงๆ ก็คล้ายกัน แค่เราคุมได้ผ่านคอมพิวเตอร์" | **Diagram:** wall switch vs relay in the same circuit, finger on one, signal wire on the other | MAKE |
| 5:47 | "ต้องตัดสายก่อน … common, normally open, normally close" | Terminal close-up and wiring diagram | HAVE `relay-board-terminals.png`, `activity2-2-relay-wiring-diagram.png` |
| 6:33 | "กี่ Watt กี่ Amp … ปั๊มน้ำ 1–2 แรงใช้ไฟเท่าไหร่" | Pump nameplate next to the relay's rating stamp, both readable | SHOOT |
| 6:48 | "ใช้ได้ไม่นานก็พัง … ความร้อนสะสม เกิดไฟไหม้" | Photo of a burnt/charred relay contact | SOURCE |
| 7:18 | "ต้องกันน้ำกันฝนไหม" | Bare module vs the same in an IP65 enclosure | SHOOT |
| 8:17 | "เรื่อง actuator มันเกี่ยวข้องกับไฟ … 220 โวลต์" | **No insert.** A safety warning lands better face to face — zoom. | — |

### Chapter 5 — โลจิก & Home Assistant

| In | What is said | Insert | Status |
|---|---|---|---|
| 9:05 | "ในโรงงานเราก็เรียกว่า PLC" | PLC in a control cabinet | SOURCE (Wikimedia) |
| 9:20 | "เหมือนเข้ารหัสมา" | Ladder-logic screenshot — then hard-cut to the HA wizard at 9:51. The contrast is the point. | SOURCE + HAVE |
| 9:51 | "Home Assistant … open source โหลดมาติดตั้งได้ฟรี" | HA dashboard | HAVE `activity1-web-ui.png` |
| 10:21 | "ตามชื่อเลย Home … แต่เอามาใช้กับ Smart Farm ได้สบายๆ" | Split screen: home dashboard vs farm dashboard | HAVE `a4-8b-farm-dashboard.mp4`, `a6-3-build-dashboard.png` |
| 10:52 | "สนับสนุนมาตรฐานต่างๆ มากมาย" | HA integrations page, scrolling | SHOOT (VM screen capture) |

### Chapter 6 — รัน HA จริง

| In | What is said | Insert | Status |
|---|---|---|---|
| 11:22 | "เปิดทิ้งไว้ตลอดเวลา … เป็นแม่ข่าย" | **Diagram:** always-on hub with sensors in and phone/laptop out | MAKE |
| 11:37 | "บันทึกค่า … 24 ชั่วโมง ในสัปดาห์ที่ผ่านมา ค่ามันขึ้นลงอย่างไร" | History graph | HAVE `hist-1-history-graph.mp4`, `sensor-log-view.png` |
| 12:10 | "Raspberry Pi ราคาหลักพัน … สักสามพัน" | Photo of a Pi with the case, sense of scale | SOURCE |
| 12:40 | "ผ่าน web browser … หรือ Mobile App" | Browser and phone side by side, same dashboard | HAVE (browser) + SHOOT (phone) |

### Chapter 7 — สร้าง Automation

| In | What is said | Insert | Status |
|---|---|---|---|
| 13:42 | "มีเมนูให้เลย กดเข้าไปสร้าง automation" | The create-automation flow | HAVE `hass create new automation.mp4` |
| 13:57 | "เป็นเหมือน wizard … ไม่ต้องเขียน code ไม่ต้องลากวาง block" | Wizard walkthrough | HAVE `a3-5-dark-lights-on.mp4` |
| 14:12 | "ถ้า sensor ดินมันแห้ง … หรือถ้าถึงเวลาที่กำหนด" | Soil-dry trigger → watering action, held 8 s (a second clip for the time trigger 2.5 s later would only flash) | HAVE `a4-7-watering-on.mp4` |

### V2 cold open — ครึ่งหลังที่ยากกว่า (15:06–15:41)

Cover card, then **no insert.** Roger wide for 7 s, punch in on the thesis, back wide. The punch
needs a wide shot before it to register.

### Chapter 9 — Fail-safe

| In | What is said | Insert | Status |
|---|---|---|---|
| 15:41 | "ถ้าเกิดสมมติน้ำมันหมด ทำอย่างไร … ปั๊มมันเดินยาวเลย" | **Diagram:** tank, intake, level falling below it, pump still running | MAKE |
| 16:28 | "ต้องเพิ่มลูกลอยเข้าไปในแหล่งน้ำ" | Float switch, real part | HAVE `gogo-iot-float-switch.jpg` |
| 16:59 | "มีสองทางที่ทำได้" | **The key diagram of the video.** Two panels: float → HA → relay → pump, versus float wired in series with pump power. | MAKE |
| 17:15 | "แบบที่สอง … มันไปตัดไฟจริงๆ ไม่ต้องผ่านโปรแกรม" | Panel 2 of the same diagram, held | MAKE |
| 17:55.3 | "น้ำหมด / เน็ตดับ / Home Assistant วันนั้นล่มพอดี" (after the zoom on "โชคร้ายจังเลย") | Panel 1 again, the three failures lighting up **one per phrase** in sync with the speech, pump taking damage at 18:00.4 | MAKE |
| 19:03 | "ไม่ว่าปั๊มจะผิดพลาด … ไฟเข้าแต่ไม่ทำงาน" — held until Z6, so the art cuts straight to the punch-in on "อันนี้อันตรายเลย" | Pump with power in, no motion, alert | HAVE `a5_05-vibration-sensor-v2.png` |
| 20:04 | "ปั๊มทำงานปุ๊บมันจะสั่น … เซ็นเซอร์พวกนี้ถ้าเราไปแตะ" | Vibration-sensor automation in HA | HAVE `a5-2-pump-not-running.mp4` |
| 20:34 | "เซ็นเซอร์วัดการไหลของน้ำในท่อ" | **Diagram:** flow sensor inline, pump on but no flow | MAKE |
| 21:04 | "เผลอทิ้งไว้หลายเดือน … แบตก็หมด" | Sensor-unavailable automation | HAVE `a5-3-sensor-unavailable.mp4` |
| 21:35 | "เรามักจะมีการตั้ง timeout ไว้เสมอ" — out before 22:30 | Timeout automation, and the timeline art | HAVE `a5-4-pump-timeout.mp4`, `a4_07-timeline-v2.png` |
| 22:32 | "เรื่องนี้สำคัญมาก มันจะแยกคนที่เป็นมือใหม่…" | **No insert.** V2's closing line, on camera with a punch-in, then end card. | — |

### Chapter 10 — ตัดสินใจด้วยข้อมูล

| In | What is said | Insert | Status |
|---|---|---|---|
| 23:20 | "เอากราฟมาดู เอามาวิเคราะห์" | History graph, then zoom into one anomaly | HAVE `hist-1-history-graph.mp4` |
| 23:51 | "ถ้าเราเลี้ยงปลา … ออกซิเจนในน้ำ Dissolved Oxygen" | Fish pond with a paddlewheel aerator | SOURCE |
| 24:06 | "เห็นความสอดคล้องของค่า DO กับอุณหภูมิ ความนิ่งของน้ำ" | **Chart:** DO and temperature on one time axis, the nightly dip marked. A real correlation, not a mock-up. | MAKE |
| 24:36 | "การเปิดน้ำบางทีเป็นต้นทุนที่สูง" | Sprinkler running | SOURCE |
| 25:00 | "Home Assistant มันลิงก์ไปยังระบบพยากรณ์อากาศได้" | HA weather integration card | SHOOT (VM) |
| 25:15 | "ความกดอากาศ … แบบไหนที่ส่อให้เห็นว่าอาจจะกำลังมีฝน" | **Chart:** pressure trace falling, rain onset marked, over 48 h | MAKE |
| 25:46 | "ไม่ใช่แค่ skill … ต้องมี knowledge ด้วย" → 26:42 | **No insert.** Stay wide; the punch-in comes at 26:23 on the stronger line. | — |

### Cold-open hooks (×3, added 22 Sep 2026)

Each video opens on ~5 s of its own strongest moment, then cuts to the cover card. The hook is the
finished edit over that span, so zooms, inserts and callouts appear just as they will later in the
body. It keeps its own audio, with a 40 ms fade in and a 150 ms fade out because it is lifted out
of running speech. The cover plays silent. Each span starts and ends on a pause in the audio.

| Video | Source | Length | Line | What's on screen |
|---|---|---|---|---|
| V1 | 6:57.2–7:02.9 | 5.7 s | "ใช้ได้ไม่นานก็พัง … ความร้อนสะสมสูง เกิดไฟไหม้…" | burnt-relay photo (i14), held to the cut |
| V2 | 17:53.5–17:59.3 | 5.8 s | "ถ้าบังเอิญวันนั้นโชคร้ายจังเลย — น้ำหมด เน็ตดับ Home Assistant วันนั้นล่มพอดี" | punched in (Z5), then the failure diagram lighting up (i33) |
| V3 | 24:45.9–24:50.8 | 4.9 s | "แล้วปรากฏว่าฝนตกตามมาทีหลัง ก็เสียน้ำเปล่า" | wide, then the punch-in (Z8f) held to the cut |

Two rules keep a hook from flashing a shot for a few frames. An insert that would show for under
1 s is dropped, and the talk shows instead. A still, or a zoom, that ends just before the hook
ends is held to the cut. The chapter times in `<V>-chapters.txt` shift by the hook's length.

### Cover and end cards (×3)

Text is allowed here. Each cover: video title, series position (1/3, 2/3, 3/3), one picture from
that video's own inserts — V1 the spine diagram, V2 the two-wiring diagram, V3 the dissolved-oxygen
chart (switched from the pressure chart: in Chiang Mai's real data the pressure-before-rain signal
is weak — the daily pressure tide is as large as the weather signal, and in the best window found
in 2019–2025 rain arrives ~16 h after the pressure low — so it reads less cleanly on a cover).
Each end card: "ตอนต่อไป" and the next video's title; V3 closes on "ขอบคุณที่รับชม". No workshop link, QR or event mention: the videos stand on their own (media review, 22 Sep 2026). MAKE.

### What has to be gathered

**SHOOT — you (6):**

| # | For | Shot | Notes |
|---|---|---|---|
| S1 | V1 1:57 | Shopee or Lazada search results for "เซ็นเซอร์" | Desktop browser, grid view, 1920-wide window. Logged out so no account name shows. |
| S2 | V1 6:33 | Pump nameplate and relay rating stamp, both legible | Any real pump. Two tight stills, or one frame with both side by side. Shows amps, not just HP. |
| S3 | V1 7:18 | Same bare module, then inside an IP65 box | Two stills from the same angle and lighting so they cut together. |
| S4 | V1 10:52 | HA Settings → Devices & services → Add integration, scrolling the list | VM screen recording, ~10 s. The Farm Workshop VM is fine to use. |
| S5 | V1 12:40 | HA companion app on a phone showing the farm dashboard | Screen recording or screenshot. Pairs with the browser still we have. |
| S6 | V3 25:00 | HA weather forecast card | VM screenshot, Chiang Mai location. |

**SOURCE — me, CC/Wikimedia, credited in the description (9):** sealed/IP67 sensor probe · lamp and
pump/solenoid valve · contactor · burnt relay contacts · PLC in a control cabinet · ladder logic
screen · Raspberry Pi · fish pond with paddlewheel aerator · sprinkler running.

**MAKE — me (14 + 6 cards):** spine diagram · soil-dry trigger→action · sensor grid · resolution
chart · wireless range map · switch-vs-relay · always-on hub · tank running dry · two float wirings
(3 states) · flow sensor · DO vs temperature chart · pressure-before-rain chart · 3 covers · 3 end cards.

**HAVE — repo (17 slots):** HA walkthrough clips, kit photos, wiring diagrams, fail-safe concept art.

---

## 3. Speaker zooms

Grammar adopted from the MKBHD study (22 Sep 2026, Roger's choices: "mix, his way", ~23 punches,
punch-out on topic change, two-tier build-ups, number callouts). Full study:
[STYLE-STUDY-MKBHD.md](STYLE-STUDY-MKBHD.md).

- **Base 115%, centred** for all talking head (approved 21 Sep) — a medium shot, desk edge and
  empty wall trimmed, every gesture inside.
- **Punch = instant cut to 132%** (1.15× the base, matching his 1.15–1.26× relative punches).
- **Signature line = fast eased push to 140%** over 0.4 s (smoothstep), for each video's thesis and
  closer. 140% of a 1080p source is visibly softer at 1:1 but holds up for these few holds.
- **Two tiers** when Roger escalates: 115 → 132 → 140, as contiguous zooms.
- **Every zoom ends with an instant cut back to 115%** — on a topic change or list start where
  there is one, otherwise at the next insert (a cutaway resets the framing, as in the reference).
- **Callouts:** five hard numbers get a small label card beside Roger during their punch
  (80–90%, 220 V, ~3,000 บาท, 2–3 ชม., 30–60 นาที) — a label, not a slide.
- Chosen only where Roger is on camera, by the reference's triggers: reveals, numbers, warnings,
  jokes and asides, punchlines, principles, callbacks.

**26 punch moments** — V1 12, V2 9, V3 5 (up from 8; one per ~38 s of on-camera time, against his
29 s). Resolved times, lengths and moves are in `xml/<V>-report.md`; the plan lives in
`overview-video-edit.json` as phrase cues, not timecodes.

| Video | Punches (source time · line) |
|---|---|
| V1 | 0:36 **push** thesis · 1:24 "เป็นตัวที่ท้าทาย" · 3:12 "ยิ่งความละเอียดสูง…" · 4:38 "พอทำอาหารกินได้แล้ว" · 4:46 "80–90%" → **tier 2** "คำตอบมักจะเป็นการเปิดปิด" · 5:10 "แค่เปิดปิดไฟได้…" · 6:26 "แต่การเลือกใช้ในชีวิตจริง" · 6:50 "Relay ตัวที่เล็กเกินไป" · 8:16 "มันเกี่ยวข้องกับไฟ" → **tier 2** "220 V" · 9:46 "ระบบที่ผมคิดว่าน่าสนใจ" · 12:25 "~3,000 บาท" · 14:40 "HA ฝึกใช้งานได้ง่าย" → **push** closer "…นี่ผมคิดว่าผ่านแล้ว" |
| V2 | 15:13 **push** thesis · 16:51 "ตัดการทำงานแบบไม่เกี่ยวกับระบบคอม" · 17:52 "โชคร้ายจังเลย" · 18:46 "อ๋อ ลูกลอยเมื่อวานนี้ตัด" · 19:18 "อันนี้อันตรายเลย" · 19:42 "proactive ไม่ใช่ react" · 20:22 "มันก็อื้ออยู่แหละ แต่มันไม่สูบน้ำ" · 22:12 "2–3 ชม." · 22:32 "เรื่องนี้สำคัญมาก" → **push** closer |
| V3 | 23:09 "ไม่ใช่แค่ประหยัดแรง" → **push** "แต่เราได้เรียนรู้เรื่องใหม่ๆ" · 24:46 "ฝนตกตามมาทีหลัง ก็เสียน้ำเปล่า" · 25:39 "30–60 นาที" · 25:54 "ไม่ใช่แค่ skill" · 26:23 → **push** closer "มือสมัครเล่น … มืออาชีพ" |

**In the FCP7 XML** the talk is razored at every zoom boundary: a cut punch is a clip with a
fixed Basic Motion scale; a push carries one Scale keyframe per ramp frame. Callouts are PNGs
with alpha on a third video track. Audio stays one piece. **Unverified:** whether Premiere counts a
keyframe's `<when>` from the start of the source media (the default here) or from the clip's
in-point. After importing, scrub V2 at 0:09 (Z4 push): if it ramps there, it's right; if not,
rebuild with `--zoom-keys clip`. Cut punches don't depend on this.

**Transcript repair (22 Sep):** 15 hidden ASR dropouts — single words whose timing was stretched
over 5–15 s of real speech, invisible to the wordless-gap check — hid ~2.5 min of speech. Repaired
by `user-import/overview-video/repair_stretched.py` (1,316 words recovered); three of the punches
above (18:46, 20:22, 24:46) are lines that were in those gaps.

---

## 4. Output

Everything is built by `scripts/overview_video.py` from `planning/overview-video-edit.json`:

```
python scripts/overview_video.py planning/overview-video-edit.json [--only V2] [--render preview|h264|h265]
```

Per video it writes to `user-import/overview-video/xml/`: `<V>.xml` (FCP7, for Premiere),
`<V>-chapters.txt` (YouTube description format, on the finished video's clock) and
`<V>-report.md` (every zoom and insert with its resolved time, status and on-screen length).
Missing art becomes a grey PLACEHOLDER still, so the cut is reviewable before all art exists;
dropping a file into `make/`, `shoot/` or `sourced/` and re-running replaces it.

- **Source:** the MKV is remuxed losslessly to `automation-iot-overview.mp4` (stream copy) so
  Premiere doesn't depend on Matroska support. All three sequences reference that one file.
- **Cues, not timecodes:** inserts and chapters name the phrase that triggers them; the builder
  finds it in the ASR word stream. Video in/out points snap to the quietest 30 ms within ±0.12 s.
- **Validation:** an insert starting inside a zoom is an error, except in the zoom's last 0.5 s,
  where the zoom is trimmed to meet it (reported). Inserts under 2.5 s are warned.
- **`--render`** encodes the finished video straight from the same decisions: `preview` (540p) for
  review, `h264` / `h265` 1080p deliverables; `--max-seconds N` renders a test slice. It works in
  three stages so memory stays flat: (1) the talk alone with the eased zoom, keyframes forced at
  every insert boundary; (2) each insert, cover and end card as an exact-length clip; (3) the
  concat demuxer joins them in order with the talk audio underneath. Every cut is on the 30 fps
  grid. Every ffmpeg call runs under a **memory watchdog** (`render_mem_gb`, default 8) that kills
  it rather than let it exhaust the machine.
  - *Why:* on 21 Sep 2026 the one-filtergraph design (split → per-segment zoom → concat, plus
    10–27 overlays) grew to 119 GB and crashed VS Code. Removing the split still left the
    overlays decoding ahead (8.7 GB and rising, caught by the watchdog). No fan-out, no overlays.
- **Stills:** photos and screenshots are rounded-corner cards (28 px) on the cream with a Thai
  label under device photos and, for Wikimedia photos, the attribution line from
  `sourced/CREDITS.md`. Claude-made diagrams and charts carry "Image generated with Claude
  Fable 5.1" bottom-left; older concept art made with another tool carries "AI-generated
  illustration". Screen recordings get the same rounded corners.
- **V1 starts at 3.3 s:** the first 2.8 s held an off-mic count and a pause before "สวัสดีครับ".
- **Thai text** on cards and diagrams renders through headless Chrome with Prompt. This Pillow
  build has no raqm and drops tone marks stacked on upper vowels (เมื่อ → เมือ).
- **Encoder:** NVENC by default. The builder probes it first and falls back to libx264/libx265,
  because on 21 Sep 2026 it crashed inside the NVIDIA driver (`nvcuda64.dll`) until a clean
  reinstall of the Studio driver fixed it.

## 5. Building on another computer

The code and edit decisions are in git. The media is not: `user-import/` is gitignored, and the
source take alone is 1.6 GB. To regenerate the XML elsewhere, clone the repo and copy these from
`user-import/overview-video/` to the same place on the new machine (≈1.7 GB):

| Copy | Size | What it is |
|---|---|---|
| `automation-iot-overview.mp4` | 1.6 GB | The take, remuxed from the original MKV. The XML points at this file. |
| `asr-gpu-large/automation-iot-overview.json` | 3 MB | Word timings, repaired. Every cue resolves against it. Expensive to redo. |
| `wav/automation-iot-overview.wav` | 51 MB | 16 kHz mono of the take; cut points snap to its quietest 30 ms. |
| `make/` | 9 MB | Claude-drawn diagrams, charts and HA clips; `make/src/` has their HTML, data and build scripts. |
| `sourced/` | 22 MB | Wikimedia photos; `CREDITS.md` feeds the on-screen attributions. |
| `images/` | 44 MB | Roger's own photos and screen recordings (`have:user-import/overview-video/images/…`). |
| `shoot/`, `music/` | — | Empty or absent now. Anything dropped here is picked up. |

Then:

```
python scripts/overview_video.py planning/overview-video-edit.json --check   # lists anything missing, writes nothing
python scripts/overview_video.py planning/overview-video-edit.json           # writes xml/, inserts/, cards/
```

The build rewrites `inserts/`, `cards/` and `xml/`, and the XML points at files by absolute path,
so there is no need to copy those folders. Tested 22 Sep 2026 on a clean tree holding only the
repo and the folders above: the three XMLs and chapter lists came out identical apart from the
paths, and so did every card and insert still.

**Needs on the machine:** Python with numpy and Pillow, ffmpeg and ffprobe on PATH, Chrome (found
automatically, or set `$CHROME`), and Windows' Leelawadee UI font. Prompt is in `scripts/fonts/`.

**Not needed for the XML:** `premiere/` (Roger's Premiere projects, 3.8 GB; copy it to keep editing
there, then relink media to the new paths), `render/` (previews), `_scratch/` (review frames and
contact sheets), the original MKV in `user-import/`, and `repair_stretched.py`, which is only for
re-running ASR and imports from the separate video-pipeline repo.
