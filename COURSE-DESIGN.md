# IoT Systems in Smart Farming — Course Design

Three hands-on sessions (150 min each, ~7.5 h) delivered inside the CMU Lifelong Education program **“นวัตกรเกษตรอัจฉริยะ AIoT สำหรับเกษตรแม่นยำ” รุ่นที่ 1, 25–29 September 2026**, Empress International Convention Centre, Chiang Mai. Our slots: **Day 1 afternoon (Fri 25 Sep), Day 2 morning and afternoon (Sat 26 Sep)**. Each slot is followed by a 15-min post-test run by the organizers. Materials in Thai (technical terms kept in English). Audience: ปวส. or higher, farmer-innovators with broad backgrounds. Teams of 3–4.

A set of narrated decks (see *Online materials* below) remains as **optional pre-reading and take-home reference**. Nothing in the room depends on it.

**Tool stack:** Home Assistant (logic, dashboards, logging, remote control) **on each team's own laptop** · GoGo-IoT board (ESP32-C3, onboard temperature/humidity/light/pressure/IMU, float switch on port 1) as input · ESP32-C6 relay board driving a 12V pump as output · PWM solar charge controller as the kit's 12V source. Every device on the workshop WiFi. Teams wire the 12V circuit by hand once; no soldering anywhere.

> **Decided — HASS host: participants' laptops.** Home Assistant runs in a VM on each team's laptop (VirtualBox, **bridged** adapter — NAT breaks mDNS and phone access). Consequence: laptops go home, so the between-session history comes from an **instructor Home Assistant** that adopts every team's sensor node alongside their laptop. ESPHome's API accepts multiple simultaneous clients, so this needs no extra hardware on the tables. A pre-workshop install guide becomes a hard prerequisite.

> **Decided — device addressing: DHCP, no static IPs, no per-board setup.** One identical firmware image per board type, with `name_add_mac_suffix` giving each board a unique mDNS hostname. Teams read that name over USB at web.esphome.io, then add the device in Home Assistant as `<name>.local`. See [firmware/](firmware/) and [TEST-PLAN.md](TEST-PLAN.md). This moves the burden onto the network — see [NETWORK-REQUIREMENTS.md](NETWORK-REQUIREMENTS.md).

---

## Program context

| When | Session | Who | Relevance to us |
|------|---------|-----|-----------------|
| Day 1, 09:00–09:30 | Program intro, assessment, **pre-test** | รศ.ดร.นัทธี สุรีย์ | Offer Goal 1 labeling items for the pre-test so pre/post comparison works |
| Day 1, 09:30–12:15 | เทคโนโลยีเซนเซอร์วัดค่าสภาพแวดล้อมและชีวภาพ | รศ.ดร.สงวนศักดิ์ | **Demonstration only, no hands-on.** Goal 2 stays fully ours; Session 1 opens with "you saw these this morning, now measure with them yourself" |
| Day 1, 13:00–16:00 | **Session 1** (ours) | อานันท์ | |
| Day 2, 09:00–12:00 | **Session 2** (ours; drafted under กำพล และคณะ) | to agree with กำพล | |
| Day 2, 13:00–16:00 | **Session 3** (ours; drafted under กำพล และคณะ) | กำพล leads comms/cloud, อานันท์ the rest | |
| Days 3–5 | AI / computer vision / capstone (agenda not yet seen) | others | We are the foundation of the program, not its closing session |

---

## Learning goals → where each is taught

| # | Learning goal | Core | Applied / introduced |
|---|---------------|------|----------------------|
| 1 | Input / Logic / Output model of autonomous systems | Session 1 | Reinforced in every activity; recap in Session 3 wrap-up |
| 2 | Choose sensors & actuators (specs, form factor, price) | Session 1 | Session 3 design challenge |
| 3 | Create & implement logic for smart farm tasks | Session 2 | Session 1 ends with a manual sense → act loop that motivates automation |
| 4 | Choose IoT infrastructure, communication & protocols | Session 3 | Seeded by the Session 2 failure lab (the link that died) |
| 5 | Practical factors: redundancy, fail-safe, safety, maintenance | Session 2 | Introduced in Session 1 (manual override / Auto-Off-Manual control box); Session 3 design challenge rubric |
| 6 | Create dashboards to visualize inputs and control outputs | Session 3 | Introduced in Session 1 (cards, toggle); control panel in Session 2 |

Each post-test targets the two goals that are core in its session.

### Design principles
- **Experience first, vocabulary second.** Participants run a working networked system from Session 1 and only open the network in Session 3. ESPHome + HASS hide it completely: nobody types an SSID, an IP or a topic name before Session 3. One sentence of orientation at setup — *"your board and your Home Assistant talk over the workshop WiFi, not the hotel WiFi; we open that box on Saturday afternoon"* — and no more.
- **Goal 5 is taught by experiencing failure**, not slides. The sabotage round is the emotional peak and the thing participants will retell.
- **One kit through all three sessions.** Boards and hosts keep logging overnight; the Day 2 opener is the overnight graph.
- **Sessions 1–2 run fully offline on our router.** Only Session 3 (cloud push) needs venue internet.

---

## Session 1 — Day 1 PM (13:00–15:45, post-test 15:45–16:00)

**ระบบสมองกลฝังตัวในฟาร์ม: รับรู้ ตัดสินใจ สั่งการ (Input → Logic → Output)** — Goals **1, 2** core; 6 introduced

| Time | Block | Goals |
|------|-------|-------|
| 13:00–13:20 | **Live:** Input → Logic → Output with familiar examples — **air conditioner / fridge** (thermostat → "if too warm" → compressor), **automatic street light** (light sensor → "if dark" → lamp), **automatic water tank** (float switch → "if level low" → pump; the bridge example: already a sensor-controlled pump, with a mechanical switch as the logic) — then the same three boxes for a smart farm (the water tank with a different sensor and the logic moved into software), mapped onto the kit: sensor board = input node, relay board = output node, HASS = logic + dashboard + logging. 2-min demo of the finished system as the hook. Vocabulary fixed here and reused verbatim: **Input (เซนเซอร์), Logic (ตัวตัดสินใจ), Output (ตัวกระทำ/actuator)**. | 1, 6 |
| 13:20–13:30 | Kit handout, role cards, teams open their team HASS in a browser. WiFi orientation sentence (see principles). | — |
| 13:30–14:05 | **Activity 1 — Sense.** Adopt the sensor board (add-by-IP), add dashboard cards, watch live values and the history graph. Mini-challenge: *which entity changes when you breathe on the board? cover it?* 5 min on the ESPHome YAML: which pin, ADC, I2C — this is the "embedded" in the title. Compare the soil sensor's spec sheet (range, accuracy, interface, IP rating; capacitive vs resistive) with what they see. | 1, 2, 6 |
| 14:05–14:30 | **Live:** actuators and driving loads. Pumps, valves, fans, lights; DC vs AC; why a microcontroller can't drive a pump → relay / SSR; reading relay ratings; inductive derating in one sentence; sizing a pump (head, flow, supply). **Manual override — never let the logic be the only way to control an actuator:** show a typical pump control box with its **Auto / Off / Manual** selector. Auto = the controller drives the pump; Off = pump cannot run (maintenance, leak found); Manual = pump runs regardless of the controller (sensor faulty, network down, crop still needs water). Standard practice, not an add-on: the person on the farm must be able to stop or start the pump without a laptop. First seed of Goal 5. Safety framing: **12V is our classroom voltage; 220V needs an electrician.** | 2, 5 |
| 14:30–14:45 | Break | |
| 14:45–15:25 | **Activity 2 — Act.** Adopt the relay board; toggle from dashboard and phone; connect the 12V pump (pre-made connectors); pump water between two containers on a drip tray. Recorder question: *what would change to run a 220V pump?* | 1, 2, 6 |
| 15:25–15:45 | **Manual loop.** Irrigate by hand from the dashboard while watching the moisture graph — sets up "why automate" for tomorrow. Recap the three boxes. (This block is the timing buffer for Session 1.) | 1, 3 |

**Post-test 1 (Goals 1, 2):** label input/logic/output in 3 scenarios (see Section 1 self-check below); pick the right sensor from a spec for 3 scenarios; match loads to relays/supplies; spot the unsafe pairing; given a scenario (sensor broken / leak found), pick the Auto/Off/Manual position.

---

## Session 2 — Day 2 AM (09:00–11:45, post-test 11:45–12:00)

**ตรรกะควบคุมอัตโนมัติและการออกแบบ Fail-safe สำหรับฟาร์ม** — Goals **3, 5** core; 6 extended

| Time | Block | Goals |
|------|-------|-------|
| 09:00–09:15 | **Overnight data.** Open the history graph: what happened while we were away? Motivates both automation and logging. | 3 |
| 09:15–09:30 | **Live:** the HASS automation editor — **trigger / condition / action**. Hysteresis explained on yesterday's own graph. | 3 |
| 09:30–10:30 | **Activity 3 — Think.** Ladder: (a) threshold: sensor value → pump ON; (b) hysteresis/deadband so it doesn't chatter; (c) time-window condition; (d) phone notification. Fast teams: templated automation or a second condition. Add a dashboard **control panel**: automation on/off switch + manual override. (a) and (b) are the required core; (c) and (d) are stretch. | 3, 6 |
| 10:30–10:45 | Break | |
| 10:45–11:30 | **Activity 4 — Failure lab.** Instructor sabotage round *while the pump automation is live*: WiFi router unplugged / sensor disconnected / HASS stopped. Teams observe, diagnose, then implement fail-safes: **max pump run-time cutoff** and **sensor-unavailable → safe state**. Keep the network explanation light: "the link died, the entities went unavailable, the pump was on its own." The *why* waits for Session 3. | 5 |
| 11:30–11:45 | **Debrief:** redundancy, watchdogs, maintenance expectations (who checks the system weekly? what corrodes first?). **Instructor demo (not a team task):** a real pump control box wired to the instructor kit — flip **Auto / Off / Manual** while the automation runs and show the pump obey the switch, not HASS. Links back to Session 1. | 5 |

**Post-test 2 (Goals 3, 5):** predict what a given automation does; fix a chattering automation with hysteresis; choose the fail-safe for a scenario; maintenance items.

---

## Session 3 — Day 2 PM (13:00–15:45, post-test 15:45–16:00)

**โครงสร้างระบบ IoT: การสื่อสาร คลาวด์ แดชบอร์ด และการออกแบบระบบ** — Goals **4, 6** core; 2, 5 applied

| Time | Block | Goals |
|------|-------|-------|
| 13:00–13:30 | **Live (กำพล):** open the box — the `wifi:` and `api:` blocks in the ESPHome YAML, the device IP on the integration page, the live ESPHome log. Then the decision axes **distance, power source, data rate, cost**; WiFi (our choice), ESP-NOW, LoRa/LoRaWAN, cellular/NB-IoT, wired RS-485; MQTT (publish/subscribe), HTTP, ESPHome native API in one slide each. **Local-first vs cloud:** what happens to each when the internet fails — link back to yesterday's router failure. | 4 |
| 13:30–14:30 | **Dashboard build** for a real user: gauges, history, controls, automation status, mobile view. Then push kit data to a cloud dashboard / broker for remote access (tool per กำพล). | 6, 4 |
| 14:30–14:45 | Break | |
| 14:45–15:30 | **Activity 5 — Design challenge.** Each team draws a scenario card (greenhouse / 10-rai orchard / hydroponics / remote plot, no mains) and produces a one-page system spec on a printed canvas: sensors + actuators **with real prices**, comms/protocol choice **with reasoning**, and at least **one fail-safe**. 1-minute pitch per team. | 2, 4, 5 |
| 15:30–15:45 | **Wrap-up.** The three boxes across three sessions; where-to-go-next sheet (incl. take-home install guide); feedback form. | 1 |

**Post-test 3 (Goals 4, 6):** choose comms for 3 farms (backyard greenhouse / 10-rai orchard / remote field with no mains power); dashboard and local-vs-cloud items. The design canvas is scored separately on the rubric.

---

## Anti-passenger structure for teams of 3–4
Each team gets a **role card** with three rotating roles, swapped at every activity boundary:
- **Driver** — hands on the laptop/HASS
- **Hardware** — boards, wiring, pump
- **Navigator/Recorder** — reads the worksheet, checks off steps, notes answers

The worksheet has one short written question per activity that the Recorder must fill in — this forces the team to verbalize what they did.

---

## Online materials — optional pre-reading and take-home reference

These narrated decks (each ≤10 min + a 3–5 question self-check) were designed as a pre-workshop course. In the program they are **optional** pre-reading, released with the enrollment pack if the organizers can distribute it, and the reference participants take home. Their content is delivered live where marked; the self-check items feed the three post-tests.

### Section 1 — ระบบอัตโนมัติทำงานอย่างไร: Input → Logic → Output (8 min) — Goal 1 · *delivered live in Session 1*
- Familiar examples decomposed into input/logic/output — air conditioner / fridge, automatic street light, automatic water tank (float switch → pump) as the bridge example; the same boxes for a smart farm; the fixed vocabulary.
- Self-check: label the input, logic, and output in 3 scenarios, chosen to be different from the taught examples so learners generalize rather than recall:
  1. **Greenhouse exhaust fan** — a temperature sensor turns the fan on when the greenhouse exceeds 35 °C. *(Straightforward; a different actuator than a pump.)*
  2. **Fish / shrimp pond aerator** — a dissolved-oxygen (DO) sensor switches the paddle-wheel aerator on when oxygen in the pond drops, typically before dawn. *(An unfamiliar sensor and a large motor as the actuator; the three boxes still apply.)*
  3. **Sprinkler with a rain sensor** — a timer starts the sprinkler every morning at 6:00, but not if the rain sensor is wet. *(Two inputs, one of which is a clock; the logic combines them. Previews the conditions they add in Activity 3.)*

### Section 2 — เลือกเซนเซอร์ให้ฟาร์ม (10 min) — Goal 2 · *background to สงวนศักดิ์'s morning; hands-on in Session 1*
- Survey of farm-relevant sensors in two tiers, so learners know what to buy first and what to treat with caution:
  - **Commonly available** — cheap modules on any Thai marketplace, plug straight into an ESP32, good enough for most farm logic: soil moisture (capacitive vs resistive — why resistive corrodes), air temperature/humidity, light, water level (float switch, ultrasonic), water flow, rain. This is the tier the workshop uses.
  - **Specific or technically complex** — know they exist and why they are harder: pH/EC and dissolved oxygen (probes drift, need regular calibration, consumable electrodes), soil NPK probes (RS-485/Modbus interface, accuracy claims often unreliable), CO₂, leaf wetness, weather stations (wind/rain gauges), cameras. What makes them complex is one of three things: **calibration**, **interface** (industrial RS-485 rather than a simple pin), or **price** (฿2,000–20,000+). Rule of thumb: start with tier 1; move to tier 2 only when the logic genuinely needs that measurement.
- **How to read a spec sheet:** measurement range, accuracy, interface (analog / I2C / one-wire), operating voltage, IP rating.
- **Form factor & price:** bare module (฿30–150) vs industrial probe (฿1,000+); when each is appropriate. Real listings from Thai marketplaces as examples.
- Self-check: pick the right sensor for 3 scenarios and justify from the spec.

### Section 3 — เลือก actuator และการขับโหลด (8 min) — Goal 2 · *delivered live in Session 1*
- Pumps, solenoid valves, fans, grow lights; DC (12/24V) vs AC (220V) loads; relay and SSR; reading relay ratings; inductive-load derating; sizing a pump.
- **Manual override:** the Auto / Off / Manual pump control box — why every actuator needs a way to be stopped (maintenance) or run (sensor fault) without the controller. First seed of Goal 5.
- Self-check: match loads to relays/supplies; spot the unsafe pairing; given a scenario, pick the selector position.

### Section 4 — โครงสร้างระบบ IoT: การสื่อสารและโปรโตคอล (10 min) — Goal 4 · *delivered live in Session 3*
- Decision axes; communication types; MQTT / HTTP / ESPHome API; local-first vs cloud.
- Self-check: choose comms for 3 farms.

### Section 5 — รู้จักเครื่องมือของเรา: Home Assistant + ESPHome (7 min) — Goals 1, 3, 6 · *delivered live in Session 1*
- Map the tools onto Section 1's boxes; 2-min screen-recorded demo of the finished system; the automation editor's trigger / condition / action.
- Prompt instead of quiz: "list two automations you'd want on a farm you know."

### Section 6 — ติดตั้ง Home Assistant (10 min video) — *take-home install guide*
- Step-by-step guided install for participants' own machines, **one blessed path per OS** (e.g. HASS OS in VirtualBox for Windows; Docker for those who already have it) — do not present a menu of options.
- **Now a hard prerequisite, not optional pre-reading**, since Home Assistant runs on participants' laptops. One blessed path per OS, **VirtualBox with a bridged adapter** (NAT breaks mDNS and phone access; Docker Desktop on Windows cannot work). Verification screenshot via a form **at least 3 days before Day 1**, reminder + 15-min online help slot for non-submitters, 3–4 laptops with the VM pre-imaged as day-of rescue.

---

## Kit list (per team) and room logistics

**Per team (plan for N teams + 2 spare kits):**
- Team's **own laptop** running Home Assistant in a bridged VM (installed before Day 1)
- 1 × GoGo-IoT sensor board (ESP32-C3; temperature, humidity, light, pressure, IMU; 18650 cell)
- 1 × float switch with Grove adapter → board port 1, as the reservoir-low guard
- 1 × ESP32-C6 single-channel relay board
- 1 × 12V aquarium pump + tubing + 2 water containers + drip tray + towel
- 1 × PWM charge controller (12V 10A, USB out) + 12V adapter standing in for the battery
  + terminal block + hook-up wire — the kit's 12V distribution, wired by the team in Activity 2
- 1 × 12V 15W solar panel, added to the controller in Session 3
- USB-C cables, power strip, printed role cards + record sheet + design canvas
- Team card: shared API encryption key, workshop SSID, instructor HA address

**Not in the kit any more:** soil moisture sensor (air humidity stands in for it), per-team
Raspberry Pi, per-board IP labels.

**Room (convention-centre ballroom, not a lab):**
- **Dedicated WiFi router** (our own, no captive portal, 2.4 GHz on, printed SSID/password per table). Do not rely on venue WiFi. Sessions 1–2 need no internet at all.
- Firmware pre-provisioned with the workshop SSID; **DHCP with week-long leases**, boards addressed by mDNS hostname. Full network spec for the provider in [NETWORK-REQUIREMENTS.md](NETWORK-REQUIREMENTS.md); the two requirements most likely to be missed are mDNS forwarding between wireless clients and allowing two MAC addresses per laptop (bridged VM).
- **Overnight:** hosts and boards stay powered in the room between Day 1 and Day 2. Confirm with the venue that power stays on and the room is not cleared. Fallback: the instructor kit goes to the hotel room overnight and its data is the Day 2 opener.
- Instructor station: HASS on a spare laptop mirroring a team kit, projected — also the rescue instance if a team's host dies. Also **one pump control box (Auto/Off/Manual)** wired between the instructor relay board and pump, for the Session 2 debrief demo only — teams do not get or build one.
- Venue internet (or an instructor phone hotspot) is needed only for the Session 3 cloud push.
- Water discipline: pumps and containers stay on trays at the end of the table, boards and laptops at the other end. Confirm the venue allows water on tables.

## Risk register

| Risk | Mitigation |
|------|-----------|
| HASS host decision slips → host images and worksheets blocked | Decide first; it gates the whole production list |
| Venue cuts power or clears the room overnight | Confirm in writing; instructor-kit fallback for the Day 2 opener |
| Venue internet flaky during the Session 3 cloud push | Phone hotspot for the instructor; pre-recorded backup of the cloud demo |
| Day 2 shape not agreed with กำพล | Agree the "30-min lecture + hands-on on the same kit" split and the cloud tool early, so firmware can be pre-provisioned for it |
| Venue network blocks device-to-device traffic | Own router, always |
| mDNS fails on a laptop | Fall back to the IP shown in the board's USB log; week-long DHCP leases keep it valid for the workshop |
| Network provider leaves client isolation or multicast filtering on | Acceptance test in NETWORK-REQUIREMENTS.md, run during the setup window with someone who can change controller settings |
| Participant laptop arrives without Home Assistant installed | Install guide sent ahead + verification form; spare laptops with the VM pre-imaged |
| Relay chattering demo does not show at 1s sampling | TEST-PLAN.md test E settles this before firmware is committed |
| Teams of 4 → passengers | Role cards with forced rotation + Recorder's written questions |
| A board bricks / a pump leaks | 2 spare kits; drip trays; pumps only run during Activities 2–4 and the dashboard build |
| Session 1 runs long now that sensor hands-on is ours too | The 15:25 manual-loop block is the buffer; Activity 1's YAML/spec segment is the first thing to trim |

## Assessment & evidence per goal
- **Pre-test (Day 1 AM, run by นัทธี):** contribute the Goal 1 labeling items and one comms-choice item so there is a baseline.
- **Post-test 1:** Goals 1, 2 · **Post-test 2:** Goals 3, 5 · **Post-test 3:** Goals 4, 6 — items reuse the online self-checks, shuffled.
- **Goal 3:** working automation with hysteresis demonstrated in Activity 3 (facilitator checklist per team)
- **Goal 5:** fail-safe implemented in Activity 4 + at least one fail-safe on the canvas
- **Goal 6:** facilitator checklist in Sessions 1 and 3 — team dashboard shows a live sensor graph and a working pump toggle (S1); a complete farm dashboard with controls and automation status (S3)
- **Goals 2, 4, 5 applied:** design-challenge canvas scored on a simple rubric (spec justified? price realistic? comms reasoning sound? fail-safe present?)

## Production task list (suggested order)
1. **Bench-test the provisioning flow** ([TEST-PLAN.md](TEST-PLAN.md)), then finalise the two firmware images in [firmware/](firmware/) and flash the production run. Rehearse overnight logging on the instructor instance. Longest lead time, gates everything.
1b. **Write the pre-workshop Home Assistant install guide** (VirtualBox bridged, one blessed path per OS, opening port 8123 for phones) and get it to participants with a verification step. This is now a hard prerequisite, not optional pre-reading.
1c. **Send [NETWORK-REQUIREMENTS.md](NETWORK-REQUIREMENTS.md) to the network provider** and book the setup-window acceptance test.
2. Agree the Day 2 shape and cloud tool with กำพล; agree pre-test items and post-test logistics with นัทธี.
3. Worksheets for 3 sessions + role cards + design canvas + scenario cards.
4. Three post-tests (+ pre-test items).
5. Live slide decks for Sessions 1–3, reusing the online-deck content.
6. Facilitator run-sheet: sabotage-round script, control-box demo script, timing checkpoints, overnight procedure.
7. Full dress rehearsal with one team of colleagues — time Session 1 (sensor hands-on is now ours) and the failure lab.
8. Online decks: record only if time remains; they are off the critical path.

## Open decisions
- Who leads Session 2, and กำพล's cloud tool for Session 3
- Whether the organizers can distribute optional pre-reading before Day 1
- Venue confirmations: overnight power, water on tables, internet for Session 3
