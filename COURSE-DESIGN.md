# IoT Systems in Smart Farming — Course Design

Two-part training: a **pre-workshop online course** (~55 min of narrated slide decks, six sections) followed by a **3-hour hands-on workshop**. Materials in Thai (technical terms kept in English). Audience: ปวส. or higher, broad backgrounds. Teams of 3–4 in the workshop.

**Tool stack:** Home Assistant (logic, dashboards, logging, remote control) on participants' laptops · ESPHome custom ESP32-C3 board with built-in sensors (input) · ESPHome relay board driving 12V loads such as a water pump (output). No soldering anywhere.

---

## Learning goals → where each is taught

| # | Learning goal | Online course | Workshop |
|---|---------------|---------------|----------|
| 1 | Input / Logic / Output model of autonomous systems | Section 1 (core) | Reinforced in every activity; recap at wrap-up |
| 2 | Choose sensors & actuators (specs, form factor, price) | Sections 2–3 (core) | Activity 5 design challenge (applied) |
| 3 | Create & implement logic for smart farm tasks | Section 5 (preview) | Activities 3–4 (core) |
| 4 | Choose IoT infrastructure, communication & protocols | Section 4 (core) | Activity 5 design challenge (applied) |
| 5 | Practical factors: redundancy, fail-safe, safety, maintenance | Mentioned in Section 4 | Activity 4 failure lab (core) + design challenge rubric |
| 6 | Create dashboards to visualize inputs and control outputs | Section 5 (demo shows entity → card) | Activities 1–2 (core) |

Design principle: **concepts and vocabulary online, integration and judgment in the room.** Nothing in the workshop requires content that wasn't covered online, and nothing online is repeated as lecture in the workshop.

---

## Part 1 — Online course (narrated slide decks, ~55 min total)

Each section: one narrated deck ≤10 min + a 3–5 question self-check quiz. Host decks + quizzes on your LMS or a simple web page; short links/QR for each section.

### Section 1 — ระบบอัตโนมัติทำงานอย่างไร: Input → Logic → Output (8 min) — Goal 1
- Open with familiar examples: air conditioner, ตู้ฟักไข่, automatic street lights — each decomposed into input/logic/output.
- The same three boxes drawn for a smart farm: soil sensor → "if dry" → pump.
- Key vocabulary established here and reused verbatim everywhere: **Input (เซนเซอร์), Logic (ตัวตัดสินใจ), Output (ตัวกระทำ/actuator)**.
- Self-check: given 3 scenarios, label the input, logic, and output.

### Section 2 — เลือกเซนเซอร์ให้ฟาร์ม (10 min) — Goal 2
- Survey of farm-relevant sensors: soil moisture (capacitive vs resistive — why resistive corrodes), temperature/humidity, light, water level, water flow, pH/EC (mention only).
- **How to read a spec sheet:** measurement range, accuracy, interface (analog / I2C / one-wire), operating voltage, IP rating.
- **Form factor & price:** bare module (฿30–150) vs industrial probe (฿1,000+); when each is appropriate. Real listings from Thai marketplaces as examples.
- Self-check: pick the right sensor for 3 scenarios and justify from the spec.

### Section 3 — เลือก actuator และการขับโหลด (8 min) — Goal 2
- Pumps, solenoid valves, fans, grow lights; DC (12/24V) vs AC (220V) loads.
- Why a microcontroller can't drive a pump directly → relay and SSR; reading relay ratings (10A @ 250VAC / 10A @ 30VDC), inductive-load derating in one sentence.
- Sizing a pump: head, flow rate, and matching the power supply.
- Safety framing that Activity 2 will echo: 12V is our classroom voltage; 220V needs an electrician.
- Self-check: match loads to relays/supplies; spot the unsafe pairing.

### Section 4 — โครงสร้างระบบ IoT: การสื่อสารและโปรโตคอล (10 min) — Goal 4
- The decision axes: **distance, power source, data rate, cost**.
- Communication types on those axes: WiFi (our choice — cheap, short range, mains-powered), ESP-NOW, LoRa/LoRaWAN (km-range, battery, tiny data), cellular/NB-IoT, wired RS-485.
- Protocols in one slide each: MQTT (publish/subscribe, the farm workhorse), HTTP, ESPHome native API.
- **Local-first vs cloud:** what happens to each when the internet fails — first seed of Goal 5.
- Self-check: choose comms for 3 farms (backyard greenhouse / 10-rai orchard / remote field with no mains power).

### Section 5 — รู้จักเครื่องมือของเรา: Home Assistant + ESPHome (7 min) — Goals 1, 3, 6 preview
- Map the tools onto Section 1's boxes: ESP32 sensor board = input node, relay board = output node, Home Assistant = logic + dashboard + logging.
- 2-minute screen-recorded demo of the exact finished system they will build: sensor graph, pump toggle, automation firing. This is the motivation hook.
- Show the HASS automation editor: **trigger / condition / action** — vocabulary the workshop uses constantly.
- No quiz; instead a prompt: "list two automations you'd want on a farm you know."

### Section 6 — ติดตั้ง Home Assistant (10 min video + install time) — prerequisite gate
- Step-by-step guided install for participants' own laptops. Recommend **one blessed path per OS** (e.g. HASS OS in VirtualBox for Windows; Docker for those who already have it) — do not present a menu of options.
- Ends with a **verification task**: onboard HASS, create a user, submit a screenshot of the dashboard via a form **at least 3 days before workshop day**.
- Follow-up plan for non-submitters: a reminder + an offer of a 15-min online help slot. Bring 3–4 USB sticks with the VM image as day-of rescue.

**Total runtime: ~53 min.** Suggested release: all sections at once, 2 weeks before the workshop, with Section 6's deadline driving the schedule.

---

## Part 2 — Hands-on workshop (3 hours, teams of 3–4)

### Anti-passenger structure for teams of 3–4
Each team gets a **role card** with three rotating roles, swapped at every activity boundary:
- **Driver** — hands on the laptop/HASS
- **Hardware** — boards, wiring, pump
- **Navigator/Recorder** — reads the worksheet, checks off steps, notes answers

The worksheet has one short written question per activity that the Recorder must fill in — this forces the team to verbalize what they did.

### Agenda (180 min)

| Time | Activity | Goal focus |
|------|----------|-----------|
| 0:00–0:15 | **Setup & check-in.** Join dedicated workshop WiFi, confirm HASS runs, kit handout, role cards. | — |
| 0:15–0:40 | **Activity 1 — Sense.** HASS discovers the pre-flashed ESP32-C3 sensor board; add dashboard cards; watch live values and history graphs. Mini-challenge: *"which entity changes when you breathe on the board? cover it?"* | 1, 2, 6 |
| 0:40–1:05 | **Activity 2 — Act.** Adopt the relay board; toggle from dashboard and phone; connect the 12V pump (pre-made connectors); pump water between two containers on a drip tray. | 1, 2, 6 |
| 1:05–1:15 | **Break** (boards keep logging — a talking point after) | — |
| 1:15–1:55 | **Activity 3 — Think.** Build automations in the HASS editor, as a ladder: (a) threshold: sensor value → pump ON; (b) add hysteresis/deadband so it doesn't chatter; (c) add a time-window condition; (d) send a phone notification. Fast teams: templated automation or a second condition. | 3 |
| 1:55–2:20 | **Activity 4 — Failure lab.** Instructor sabotage round: WiFi router unplugged / sensor disconnected / HASS stopped — *while the pump automation is live*. Teams observe, diagnose, then implement fail-safes: **max pump run-time cutoff** and **sensor-unavailable → safe state** automations. Debrief: redundancy, watchdogs, maintenance expectations (who checks the system weekly? what corrodes first?). | 5 |
| 2:20–2:50 | **Activity 5 — Design challenge.** Each team draws a scenario card (greenhouse / 10-rai orchard / hydroponics / remote plot, no mains) and produces a one-page system spec on a printed canvas: sensors + actuators **with real prices**, comms/protocol choice **with reasoning**, and at least **one fail-safe**. 1-minute pitch per team. | 2, 4, 5 |
| 2:50–3:00 | **Wrap-up.** Recap the three boxes; post-quiz (same items as online self-checks, shuffled); where-to-go-next sheet; feedback form. | 1 |

### Why this shape works
- Activities 1→2→3 physically walk the Input → Output → Logic model — the workshop *is* Goal 1.
- Goal 5 is taught by **experiencing failure**, not slides: the sabotage round is the emotional peak and the thing participants will retell.
- Activity 5 makes goals 2 and 4 assessable: the canvas + pitch is your evidence they can choose components and infrastructure, and it must include what they learned in Activity 4.

---

## Kit list (per team) and room logistics

**Per team (plan for N teams + 2 spare kits):**
- 1 × ESP32-C3 sensor board (pre-flashed, labeled with team number)
- 1 × ESPHome relay board (pre-flashed, labeled)
- 1 × 12V pump + tubing + 2 water containers + drip tray + towel
- 1 × 12V power supply, USB cables, printed role cards + worksheet + design canvas

**Room:**
- **Dedicated WiFi router** (your own, no captive portal, 2.4 GHz on, printed SSID/password per table). Do not rely on venue WiFi.
- Firmware pre-provisioned with the workshop SSID; **assign static IPs** in ESPHome — mDNS discovery is flaky from inside VMs, so worksheets should include the "add ESPHome device by IP" path as the primary route.
- Instructor station: HASS on a spare laptop mirroring a team kit, projected — plus it's the rescue instance if a team's laptop dies.
- Water discipline: pumps and containers stay on trays at the end of the table, boards and laptops at the other end.

## Risk register

| Risk | Mitigation |
|------|-----------|
| Participants arrive without working HASS | Section 6 verification gate + reminder; VM-image USB sticks; rescue = pair with the instructor instance |
| Venue network blocks device-to-device traffic | Own router, always |
| mDNS/discovery fails in VMs | Static IPs + add-by-IP as the documented default path |
| Teams of 4 → passengers | Role cards with forced rotation + Recorder's written questions |
| A board bricks / a pump leaks | 2 spare kits; drip trays; pumps only run during Activities 2–4 |
| Activity 3 overruns (it's the deep one) | Ladder design — (a) and (b) are the required core; (c) and (d) are stretch |

## Assessment & evidence per goal
- **Goal 1:** post-quiz labeling items (compare against online self-check scores)
- **Goals 2, 4:** design-challenge canvas scored on a simple rubric (spec justified? price realistic? comms reasoning sound?)
- **Goal 3:** working automation demonstrated in Activity 3 (facilitator checklist per team)
- **Goal 5:** fail-safe implemented in Activity 4 + at least one fail-safe on the canvas
- **Goal 6:** facilitator checklist item in Activities 1–2 — team dashboard shows a live sensor graph and a working pump toggle

## Production task list (suggested order)
1. Section 6 install guide + verification form — longest lead time, gates everything
2. Firmware: ESPHome YAML for both boards (workshop SSID, static IPs, friendly entity names in Thai)
3. Workshop worksheet + role cards + design canvas + scenario cards
4. Slide decks for Sections 1–5, then record narration (Thai)
5. Facilitator run-sheet with the sabotage-round script and timing checkpoints
6. Full dress rehearsal with one team of colleagues — timing Activity 3 especially
