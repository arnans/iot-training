# IoT Systems in Smart Farming — Course Design

Three hands-on sessions (150 min each, ~7.5 h) delivered inside the CMU Lifelong Education program **“นวัตกรเกษตรอัจฉริยะ AIoT สำหรับเกษตรแม่นยำ” รุ่นที่ 1, 25–29 September 2026**, Empress International Convention Centre, Chiang Mai. Our slots: **Day 1 afternoon (Fri 25 Sep), Day 2 morning and afternoon (Sat 26 Sep)**. Each slot is followed by a 15-min post-test run by the organizers. Materials in Thai (technical terms kept in English). Audience: ปวส. or higher, farmer-innovators with broad backgrounds. **400 participants in 100 teams of four**, all in one room.

A set of narrated decks (see *Online materials* below) remains as **optional pre-reading and take-home reference**. Nothing in the room depends on it.

**Tool stack:** Home Assistant (logic, dashboards, logging, remote control) **on each team's own laptop** · GoGo-IoT board (ESP32-C3, onboard temperature/humidity/light/pressure/IMU, float switch on port 1) as input · ESP32-C6 relay board driving a 12V pump as output · PWM solar charge controller as the kit's 12V source. Every device on the workshop WiFi. Teams wire the 12V circuit by hand once; no soldering anywhere.

> **Decided — HASS host: participants' laptops, as a pre-built VirtualBox OVA.** Home Assistant runs in a VM on each team's laptop. Participants receive an appliance image with a minimal `configuration.yaml` (no `default_config`), a bridged adapter and onboarding already done — see [hass/](hass/). Consequence: laptops go home, so **nothing records overnight** — and that absence is taught rather than patched. The logging teams read is the one their own HA makes across Day 2 morning, opened in the Session 3 afternoon. (Rejected 7 Sep 2026: an instructor Home Assistant on a wired trunk adopting all 100 sensor nodes. It buys one 15-min opener at the cost of a wired trunk in all three zones, a recorder tuned for ~250 writes/s, and a second machine that must not fail.)

> **Decided — network: three logical zones.** The room is split into red / green / blue, each a VLAN with a 2.4 GHz SSID for boards and a 5 GHz SSID for laptops, all six SSIDs on every AP. Zones are logical, not spatial: the zone is compiled into the boards and colour-coded on the kit, and a team is told its colour. This cuts mDNS load per domain ~9× and needs no mDNS gateway. See [NETWORK-REQUIREMENTS.md](NETWORK-REQUIREMENTS.md).

> **Decided — device addressing: DHCP, no static IPs, no per-board setup.** One firmware source per board type, **built three times** by `firmware/build-zones.py` with the zone's SSID and password injected, so the zone colour is part of each board's mDNS hostname (`gogo-iot-red-a1b2c3`). Teams read the name over USB at web.esphome.io, check the colour matches their kit, then pick that board out of Home Assistant's discovered list by its six-character suffix (manual entry of the bare name, no `.local`, is the fallback — bench-verified). See [firmware/](firmware/) and [TEST-PLAN.md](TEST-PLAN.md).

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
| 3 | Create & implement logic for smart farm tasks | Session 2 | Session 1 ends with a hand-run loop and the first automation (float-switch guard) |
| 4 | Choose IoT infrastructure, communication & protocols | Session 3 | Seeded by the Session 2 failure lab (the link that died) |
| 5 | Practical factors: redundancy, fail-safe, safety, maintenance | Session 2 | Introduced in Session 1 (manual override / Auto-Off-Manual control box); Session 3 design challenge rubric |
| 6 | Create dashboards to visualize inputs and control outputs | Session 3 | Introduced in Session 1 (entity history, toggle from laptop and phone); control panel in Session 2 |

Each post-test targets the two goals that are core in its session.

### Design principles
- **Experience first, vocabulary second.** Participants run a working networked system from Session 1 and only open the network in Session 3. ESPHome + HASS hide it completely: nobody *configures* an address before Session 3 — teams read their board's name and IP off a screen, type that IP into a browser to see the board's own page, and later click the board's card in Home Assistant; nothing is ever assigned by hand. One sentence of orientation at setup — *"your board and your Home Assistant talk over the workshop WiFi, not the hotel WiFi; we open that box on Saturday afternoon"* — and no more.
- **Goal 5 is taught by experiencing failure**, not slides. The sabotage round is the emotional peak and the thing participants will retell.
- **One kit through all three sessions.** Boards stay powered in the room overnight so Day 2 starts ready, not so anything is logged — laptops go home and the recorder goes with them. Teams read *their own* half-day trace on Day 2 afternoon, and the missing night is the evidence for "a farm needs a machine that never closes its lid".
- **Nothing in Sessions 1–2 depends on the cloud.** Boards, Home Assistant and phones talk only on the workshop network. Internet is still needed on the laptop SSIDs throughout: web.esphome.io (name reading, Sessions 1 and 3) and the worksheet site are online. Only Session 3's cloud push depends on internet for the *activity* itself.

---

## Session 1 — Day 1 PM (13:00–15:45, post-test 15:45–16:00)

**ระบบสมองกลฝังตัวในฟาร์ม: รับรู้ ตัดสินใจ สั่งการ (Input → Logic → Output)** — Goals **1, 2** core; 3, 5, 6 introduced

| Time | Block | Goals |
|------|-------|-------|
| 13:00–13:20 | **Live:** Input → Logic → Output with familiar examples — **air conditioner / fridge** (thermostat → "if too warm" → compressor), **automatic street light** (light sensor → "if dark" → lamp), **automatic water tank** (float switch → "if level low" → pump; the bridge example: already a sensor-controlled pump, with a mechanical switch as the logic) — then the same three boxes for a smart farm (the water tank with a different sensor and the logic moved into software), mapped onto the kit: sensor board = input node, relay board = output node, HASS = logic + dashboard + logging. 2-min demo of the finished system as the hook. Vocabulary fixed here and reused verbatim: **Input (เซนเซอร์), Logic (ตัวตัดสินใจ), Output (ตัวกระทำ/actuator)**. | 1, 6 |
| 13:20–13:55 | **Activity 1 — Sense.** Kit handout, role cards, zone-colour check; teams start their HA VM and leave it. Read the board's name **and IP** over USB at web.esphome.io, then open the board's own page at `http://<ip>/` — no Home Assistant yet. Mini-challenge on that page: *which entity changes when you breathe on the board? cover it? lift the float?* Count the seconds from covering to the light value moving (feeds Session 2's chatter). Analog vs digital sensors. | 1, 2 |
| 13:55–14:35 | **Activity 2 — Act.** Part A, *the relay is a switch*: relay board on USB, read name + IP, toggle it from the board's page with nothing attached — click, indicator LED, onboard button; unplug USB. Part B, *the load*: wire the 12V distribution (charge controller → terminal block → relay board + pump), pump A→B once then recirculate, toggle from the board's page. Instructor talking point, 2 min, no equipment: the same junction on a real farm is a **pump control box** with an **Auto / Off / Manual** selector — first seed of Goal 5. Safety framing: **12V is our classroom voltage; 220V needs an electrician.** Recorder question: *what would change to run a 220V pump?* | 1, 2, 5 |
| 14:35–14:50 | Break | |
| 14:50–15:30 | **Activity 3 — Logic.** Adopt both boards into the team's Home Assistant (discovered cards, six-char suffix). Observe from the device page — click an entity → history graph ("the board only knows *now*; HA remembers") — and toggle the pump from laptop and phone. No custom dashboard: that is Session 3. **Be the Logic yourself** for 5 min (watch humidity, water by hand, lift the float mid-run), then the Recorder writes two rules as *ถ้า … ให้ …*. Build the float rule as the **first automation**: trigger = float switch → Dry, action = relay off; pass criterion: pump stops itself 3 of 3. Hook for Session 2: hold the float switch *out of the water first* (already Dry), then start the pump — nothing stops it (trigger vs condition). Left open on purpose; it returns as sabotage card 4 in Session 2 and is fixed in Fail-safe 1. | 1, 3, 5, 6 |
| 15:30–15:45 | **Activity 4 — Spec (timing buffer).** Paper only, no equipment. Each team draws a scenario card stating a job with numbers; they read the kit's specs (humidity / temperature accuracy, float-switch rating, the relay's printed DC rating, pump current) and rule fit / unfit, naming the single part to change. At least one card exceeds the sensor accuracy, one exceeds the relay rating, one passes. Instructor closes with the five things to read on every spec. Flexes 10–25 min; becomes a take-home if Activity 3 overruns. | 2 |

**Post-test 1 (Goals 1, 2):** label input/logic/output in 3 scenarios (see Section 1 self-check below); pick the right sensor from a spec for 3 scenarios; match loads to relays/supplies; spot the unsafe pairing; given a scenario (sensor broken / leak found), pick the Auto/Off/Manual position.

---

## Session 2 — Day 2 AM (09:00–11:45, post-test 11:45–12:00)

**ตรรกะควบคุมอัตโนมัติและการออกแบบ Fail-safe สำหรับฟาร์ม** — Goals **3, 5** core; 6 extended

| Time | Block | Goals |
|------|-------|-------|
| 09:00–09:15 | **Automation recap.** Confirm both boards are back and the VM is recording, then open yesterday's float automation in the editor and name its three parts — **trigger / condition / action** — with one sentence on what each answers. The Session 1 puzzle is *not* raised here (decided 8 Sep 2026): it comes back as sabotage card 4 in the failure lab, so the team meets the hole and the fix in the same activity rather than carrying an open question through Activity 5. No new build. | 3 |
| 09:15–10:30 | **Activity 5 — Think.** Night-light scenario first, on a real lamp: the team swaps the pump off the relay's NO terminal and wires in the kit's **12V LED module** (red → NO, black → negative row; about 5 min, Hardware wires, Recorder reads), so chatter is a visibly flickering lamp rather than a relay indicator. Ladder: (a) threshold: light value → lamp ON; (b) hysteresis/deadband so it doesn't chatter; (c) time-window condition; (d) phone notification. Then swap the LED out and the pump back (another ~5 min) and carry the pattern to watering: humidity threshold with hysteresis. Fast teams: templated automation or a second condition. Add a dashboard **control panel**: automation on/off switch + manual override. (a) and (b) are the required core; (c) and (d) are stretch. | 3, 6 |
| 10:30–10:45 | Break | |
| 10:45–11:30 | **Activity 6 — Failure lab.** Paired-team sabotage from sealed cards *while the pump automation is live* — one instructor cannot reach 100 teams, so neighbouring teams sabotage each other, four rounds, cards revealed at the end. The four cards: sensor board switched off with its on/off switch — it has an 18650 cell, so a pulled cable does nothing (entities go `unavailable`) / laptop WiFi off (HA loses both boards) / pump lead unscrewed from the relay's NO terminal (relay clicks, indicator lights, dashboard says "on", no water moves — the one failure a dashboard cannot show) / float switch lifted out of the water, then the relay board's onboard button pressed (yesterday's rule stops the pump, then the pump runs again with the float still Dry — the Session 1 puzzle, staged). Teams observe, diagnose, then implement fail-safes. Fail-safe 1 **upgrades the session 1 float rule in place** (rename, add a notification) and adds a float-**Wet** condition to the watering rule — trigger vs condition, answering card 4. Then **max pump run-time cutoff** and **sensor-unavailable → safe state**. Fail-safe 1 also gains a second trigger (pump switch → On, condition float Dry) so a dashboard or onboard-button start with no water is switched back off — the worksheet then names what is still unprotected: anything when HA itself is down. Stretch, and the answer to card 3: **command ≠ result** — the sensor board's accelerometer publishes a `pump running` verdict (three-level sensitivity select, bench-calibrated), and a rule that turns the pump off when it has been *commanded* on for **15 s** with no vibration catches the one failure the dashboard cannot show (15 s, not 30 s, so it fires before the max-run cutoff and the test is unambiguous). Required self-check: Fail-safes 1 and 2 both demonstrated; 3 and 4 when time allows. Keep the network explanation light: "the link died, the entities went unavailable, the pump was on its own." The *why* waits for Session 3. | 5 |
| 11:30–11:45 | **Debrief:** redundancy, watchdogs, maintenance expectations (who checks the system weekly? what corrodes first?). Closes with the lunch instruction that makes Session 3's opener possible: **do not shut the VM down** — HA has been recording all morning; disable the watering automation and leave the relay off so nothing pumps unattended. **Instructor demo (not a team task):** a real pump control box wired to the instructor kit — flip **Auto / Off / Manual** while the automation runs and show the pump obey the switch, not HASS. Then the same idea one layer down: the relay board's **onboard button** toggles the relay with Home Assistant shut down (bench-verified) — an override that lives in the board rather than the wiring. Links back to Session 1. | 5 |

**Post-test 2 (Goals 3, 5):** predict what a given automation does; fix a chattering automation with hysteresis; choose the fail-safe for a scenario; maintenance items.

---

## Session 3 — Day 2 PM (13:00–15:45, post-test 15:45–16:00)

**โครงสร้างระบบ IoT: การสื่อสาร คลาวด์ แดชบอร์ด และการออกแบบระบบ** — Goals **4, 6** core; 2, 5 applied

| Time | Block | Goals |
|------|-------|-------|
| 13:00–13:20 | **Live (กำพล):** open the box — the `wifi:` and `api:` blocks in the ESPHome YAML (no encryption key, no IP anywhere in the file), the device IP on the integration page, the live ESPHome log, and the board's **own web page** at `http://<name>/` — "your board *is* a web server on this network" is the most concrete thing in the block. Then the decision axes **distance, power source, data rate, cost**; WiFi (our choice), ESP-NOW, LoRa/LoRaWAN, cellular/NB-IoT, wired RS-485; MQTT (publish/subscribe), HTTP, ESPHome native API in one slide each. **Local-first vs cloud:** what happens to each when the internet fails — link back to yesterday's sabotage card 2, the laptop's WiFi switched off. | 4 |
| 13:20–13:40 | **Open the power box.** The "12 V supply" teams wired on Day 1 is a PWM charge controller with the adapter standing in for the battery. Read the three terminal pairs, read the LCD (12.0 V never shows "full" — the controller sees only what it measures), view the battery-type menu and leave it on lead-acid, connect the 15 W panel and watch charge current indoors vs by a window. **Instructor demo only, projected:** pull the adapter for 10 s with the panel connected — the system dies, because a panel without a battery is a night with no storage. Teams do not repeat it: it breaks the controller's disconnect order. | 4 |
| 13:40–13:50 | **Our own half-day.** Open History over this morning and find four things the team caused: the light dip from a cupped hand, the fast relay toggling before hysteresis, the gaps from the sabotage rounds, the pump's runs. Then the question the graph cannot answer — *the board ran all night, so why is there no night on this graph?* The recorder went home in a laptop bag. Motivates both logging and "a farm needs a machine that stays on". | 6, 4 |
| 13:50–14:35 | **Activity 7 — Dashboard build** for a real user: gauges, history (now populated with that morning), controls, automation status, mobile view; peer-tested by the neighbouring team. Then push kit data to a cloud dashboard / broker for remote access (tool per กำพล — **procedure still to be written once the tool is chosen**). | 6, 4 |
| 14:35–14:50 | Break | |
| 14:50–15:35 | **Activity 8 — Design challenge.** Each team draws a scenario card (greenhouse / 10-rai orchard / hydroponics / remote plot, no mains) or uses a team member's own farm (card E, seeded by the one-sentence problem written on the record sheet at the start of Session 1) and produces a one-page system spec on a printed canvas: sensors + actuators **with real prices**, comms/protocol choice **with reasoning**, at least **one fail-safe**, and a small pilot plan (benefit, measure, first trial, owner, review date). 30 min design · 5 min paired pitches with the neighbouring team, two feedback questions · 10 min plenary, three or four teams nominated by their pair. 100 one-minute pitches to the room would take 100 minutes. | 2, 4, 5 |
| 15:35–15:45 | **Wrap-up.** The three boxes across three sessions; where-to-go-next sheet (incl. take-home install guide); feedback form. | 1 |

**Post-test 3 (Goals 4, 6):** choose comms for 3 farms (backyard greenhouse / 10-rai orchard / remote field with no mains power); dashboard and local-vs-cloud items. The design canvas is scored separately on the rubric.

---

## Anti-passenger structure for teams of four
Each team gets a **role card** with four rotating roles, swapped at every activity boundary:
- **Driver** — hands on the laptop/HASS
- **Hardware** — boards, wiring, pump
- **Navigator/Recorder** — reads the worksheet, checks off steps, notes answers
- **Tester** — states the expected result before every test, times it, calls pass/fail against the worksheet's criterion; holds the phone dashboard; is the one who walks over to sabotage the paired team in Session 2. Added 8 Sep 2026: three roles left the fourth member as a spectator with a phone. A team of three folds Tester into Recorder.

The worksheet has one short written question per activity that the Recorder must fill in — this forces the team to verbalize what they did. Individual learning is still evidenced by the post-tests, not by team completion.

---

## Online materials — optional pre-reading and take-home reference

These narrated decks (each ≤10 min + a 3–5 question self-check) were designed as a pre-workshop course. In the program they are **optional** pre-reading, released with the enrollment pack if the organizers can distribute it, and the reference participants take home. Their content is delivered live where marked; the self-check items feed the three post-tests.

### Section 1 — ระบบอัตโนมัติทำงานอย่างไร: Input → Logic → Output (8 min) — Goal 1 · *delivered live in Session 1*
- Familiar examples decomposed into input/logic/output — air conditioner / fridge, automatic street light, automatic water tank (float switch → pump) as the bridge example; the same boxes for a smart farm; the fixed vocabulary.
- Self-check: label the input, logic, and output in 3 scenarios, chosen to be different from the taught examples so learners generalize rather than recall:
  1. **Greenhouse exhaust fan** — a temperature sensor turns the fan on when the greenhouse exceeds 35 °C. *(Straightforward; a different actuator than a pump.)*
  2. **Fish / shrimp pond aerator** — a dissolved-oxygen (DO) sensor switches the paddle-wheel aerator on when oxygen in the pond drops, typically before dawn. *(An unfamiliar sensor and a large motor as the actuator; the three boxes still apply.)*
  3. **Sprinkler with a rain sensor** — a timer starts the sprinkler every morning at 6:00, but not if the rain sensor is wet. *(Two inputs, one of which is a clock; the logic combines them. Previews the conditions they add in Activity 5.)*

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
- **Now a hard prerequisite, not optional pre-reading**, since Home Assistant runs on participants' laptops. **One path only: install VirtualBox, import the pre-built OVA, press Start.** No from-scratch install, no Docker (Docker Desktop on Windows has no host networking, so no mDNS). The OVA carries the bridged adapter, the minimal config and a completed onboarding. **Two OVAs, not one:** x86-64 for Windows and Intel Macs, ARM64 for Apple Silicon — the guide branches on "what kind of computer do you have" before anything else (see `hass/README.md`). Verification screenshot via a form **at least 3 days before Day 1**, reminder + 15-min online help slot for non-submitters, 3–4 laptops with the VM pre-imaged as day-of rescue.

---

## Kit list (per team) and room logistics

**Per team. 100 teams of four, 400 participants. Plan 100 kits + 5 spares:**
- Team's **own laptop** running Home Assistant in a bridged VM (installed before Day 1)
- 1 × GoGo-IoT sensor board (ESP32-C3; temperature, humidity, light, pressure, IMU; 18650 cell)
- 1 × float switch (two bare wires → the outer two terminals of the Grove adapter's 4-way block) → board port 1, as the reservoir-low guard. Float cylinder flipped on its rod at kit prep so the contact closes when wet; reads **Wet** = water present, **Dry** for no water or any wiring fault
- 1 × ESP32-C6 single-channel relay board
- 1 × 12V aquarium pump + tubing + 2 water containers + drip tray + towel
- 1 × 12V LED module (three-lens sign module, red/black leads; photo in `docs/images/led-module-12v.jpg`) — the "garden lamp" for Session 2's night-light ladder, swapped onto the relay's NO terminal in place of the pump for Activity 5 and swapped back for the watering scenario (added 8 Sep 2026; replaces watching the relay indicator LED)
- 1 × PWM charge controller (12V 10A, USB out) + 12V adapter standing in for the battery
  + terminal block + hook-up wire — the kit's 12V distribution, wired by the team in Activity 2
- 1 × 12V 15W solar panel, added to the controller in Session 3
- USB-C cables, power strip, printed role cards + record sheet + design canvas
- Team card: zone colour, zone WiFi SSID + password, Home Assistant VM user/password. **No encryption key** — the ESPHome API runs unencrypted, so there is nothing to type at adoption

**Not in the kit any more:** soil moisture sensor (air humidity stands in for it), per-team
Raspberry Pi, per-board IP labels.

**Room (convention-centre ballroom, not a lab):**
- **Dedicated workshop network**, built by the network provider to [NETWORK-REQUIREMENTS.md](NETWORK-REQUIREMENTS.md): three zone VLANs, six SSIDs on every AP, no captive portal, client isolation off, mDNS forwarded, internet on the laptop SSIDs (web.esphome.io and the worksheet site are online). Do not rely on venue WiFi. Boards and Home Assistant never touch the internet before the Session 3 cloud push.
- Firmware pre-provisioned with the zone SSID; **DHCP, 12–24 h leases**, boards addressed by mDNS hostname so a changed IP costs nothing. Full network spec for the provider in [NETWORK-REQUIREMENTS.md](NETWORK-REQUIREMENTS.md); the two requirements most likely to be missed are mDNS forwarding between wireless clients and allowing two MAC addresses per laptop (bridged VM).
- **Overnight:** boards and charge controllers stay powered in the room between Day 1 and Day 2; laptops go home. Nothing is recorded overnight and nothing needs to be — Day 2 opens on the automation editor, not on a graph. Power staying on only buys a ready-to-go kit at 09:00; confirm it with the venue anyway, and if the room is cleared the cost is ten minutes of re-cabling, not a lost activity.
- **One instructor machine: the instructor kit** — a spare laptop mirroring a team kit, projected, for demos, and the rescue instance if a team's host dies. It adopts only its own two boards. (The separate wired-trunk instructor *server* is dropped along with the adopt-everything opener; `hass/configuration-instructor.yaml` and network requirement 3 exist for it and are now unused — see the open item in WORKSHEET-TODO.md.) On the kit, **one pump control box (Auto/Off/Manual)** wired between the relay board and pump, for the Session 2 debrief only — teams do not get or build one.
- Venue internet on the laptop SSIDs all three sessions (web.esphome.io, worksheet site); the Session 3 cloud push is the only *activity* that fails without it, and an instructor phone hotspot covers that one.
- Water discipline: pumps and containers stay on trays at the end of the table, boards and laptops at the other end. Confirm the venue allows water on tables.

## Risk register

| Risk | Mitigation |
|------|-----------|
| HASS host decision slips → host images and worksheets blocked | Decide first; it gates the whole production list |
| Venue cuts power or clears the room overnight | Confirm in writing. No activity depends on it any more — worst case, teams re-cable and re-adopt at the start of Session 2 |
| Venue internet flaky during the Session 3 cloud push | Phone hotspot for the instructor; pre-recorded backup of the cloud demo |
| Day 2 shape not agreed with กำพล | Agree the "30-min lecture + hands-on on the same kit" split and the cloud tool early, so firmware can be pre-provisioned for it |
| Venue network blocks device-to-device traffic | Own router, always |
| mDNS fails on a laptop | Fall back to the IP, which the board now prints in its USB boot log and serves its own page from; 12–24 h leases mean re-reading it after an overnight is cheap |
| Network provider leaves client isolation or multicast filtering on | Acceptance test in NETWORK-REQUIREMENTS.md, run during the setup window with someone who can change controller settings |
| Participant laptop arrives without Home Assistant installed | Install guide sent ahead + verification form; spare laptops with the VM pre-imaged |
| Apple Silicon Mac can't boot the x86-64 master OVA | Build and test a second ARM64 master image (different VirtualBox OS type + storage controller); install guide branches by CPU, not just by OS — see `hass/README.md` |
| Relay chattering demo does not show | Resolved in principle: the worksheet has the student *make* the fluctuation by wavering a hand, not wait for sensor noise (the BH1750 is stable). 1 s interval stays. TEST-PLAN test E still owes the before/after toggle counts |
| Teams of 4 → passengers | Role cards with forced rotation + Recorder's written questions |
| A board bricks / a pump leaks | 2 spare kits; drip trays; pumps only run during Activities 2–6 and the dashboard build |
| Session 1 runs long — HA adoption and the first automation both sit in Activity 3 | Activity 4 (spec game) runs last and is paper-only, but it is Goal 2's only hands-on and is **never cut**: the worksheet defines a short form (relay + pump spec only, one card, one verdict) with a 10-min floor. The flex comes from Activity 3's phone toggle and history steps. The VM is started in *Before you begin* so a broken laptop surfaces two hours before it is needed |
| **18650 cell in the GoGo-IoT keeps the board alive when USB is pulled** | The board has a battery path with source selection, so with a charged cell installed the board never goes `unavailable` from a pulled cable. **Closed** (Roger, 8 Sep 2026): the cell stays in, and every "power loss" step uses the board's **on/off switch** instead — sabotage card 1, the Fail-safe 3 test, the reference table. The Session 3 adapter demo now points the other way: the sensor board *survives* the adapter pull on its cell, which is scenario D's night-time node |
| Session 3 timed blocks overrun the slot | Reconciled 8 Sep 2026: network 20 + power 20 + history 10 + dashboard 45 + design 45 + wrap-up 10 = 150. The worksheet and this table now carry the same numbers |
| `homeassistant.local` resolves to a neighbour's VM | ~34 identical-hostname VMs per zone; demonstrated on the bench with a single extra HA on the network. **Closed** — the worksheets now use the VM's on-screen IP, written on the record sheet on day 1 and re-read on day 2. See TEST-PLAN.md |
| Float switch fails *unsafe* | As shipped the float closes when *down*, so a cut wire read as "water present" and the pump could run dry. **Closed** — the float cylinder is flipped on its rod at kit prep (8 Sep 2026), so the contact closes when wet and a cut wire, unseated plug or missing switch reads **Dry**. Firmware `inverted: true` + `device_class: moisture` (Wet / Dry in HA). Session 2's Fail-safe 1 still adds a float-**Wet** condition to the watering rule, so `unavailable` fails safe too — TEST-PLAN test G. Residual risk: a kit assembled without the flip reads backwards; the kit-prep checklist must flip every float |
| Vibration verdict wrong at a table (soft mount, quiet pump, shaky table) | Three-level sensitivity select on the board, changeable from HA or the board's own page and restored across power cuts; the worksheet has Hardware put the board against the tubing first — TEST-PLAN test I |
| A team shuts the VM down at lunch, losing Session 3's opener | Last checklist item of Session 2 says do not; the block is 10 min and a team without data reads a neighbour's graph |
| Facilitator ratio for 100 teams doing 12 V wiring | ~10 roving facilitators briefed on the `reference.md` failure modes; gates the run-sheet |

## Assessment & evidence per goal
- **Pre-test (Day 1 AM, run by นัทธี):** contribute the Goal 1 labeling items and one comms-choice item so there is a baseline.
- **Post-test 1:** Goals 1, 2 · **Post-test 2:** Goals 3, 5 · **Post-test 3:** Goals 4, 6 — items reuse the online self-checks, shuffled.
- **Goal 3:** working automation with hysteresis demonstrated in Activity 5 (facilitator checklist per team)
- **Goal 5:** fail-safe implemented in Activity 6 + at least one fail-safe on the canvas
- **Goal 6:** facilitator checklist in Sessions 1 and 3 — team shows an entity's history graph from the device page and toggles the pump from laptop and phone (S1); a complete farm dashboard with controls and automation status (S3)
- **Goals 2, 4, 5 applied:** design-challenge canvas scored on a simple rubric (spec justified? price realistic? comms reasoning sound? fail-safe present?)

## Production task list (suggested order)
1. **Bench-test the provisioning flow** ([TEST-PLAN.md](TEST-PLAN.md)), then finalise the two firmware images in [firmware/](firmware/) and flash the production run. Longest lead time, gates everything.
1b. **Write the pre-workshop Home Assistant install guide** (VirtualBox bridged, one blessed path per OS **and per CPU architecture — Apple Silicon Macs need a separate ARM64 image and different import settings from Windows/Intel**, and a phone-reaches-the-VM check on port 80 — bridged, so no firewall to open) and get it to participants with a verification step. This is now a hard prerequisite, not optional pre-reading.
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
- **Overview Areas baked into the master image** — Flower Farm matches the kit; Corn Farm and Grass have no hardware behind them. Keep, trim, or rename?
- ~~**Float switch mounting orientation**~~ **Decided** (8 Sep 2026): flip the float cylinder on its rod so it closes when wet. Add the flip to the kit-prep checklist for all 100 kits
- Whether the VM credential decided on the bench (`farmer` / `farmer`) is written into the repo, or lives only on the team card
- ~~**18650 cell: installed or not?**~~ **Decided** (Roger, 8 Sep 2026): the cell stays in; power-loss steps use the board's on/off switch. Bench check still owed: switch off → entities `unavailable` within a few seconds, switch on → entities back without re-adoption
- **Adapter-out demo with the panel connected** (Session 3 power block, instructor kit only): bench-check once, when the controller is to hand, what it puts on the LOAD pair and USB when the battery pair goes open with the panel lit, and whether the battery-type setting survives. Panel open-circuit is 18–22 V even in weak light; the relay board tolerates it, the pump does not. If the LOAD pair sees panel voltage, run the demo with the pump lead unscrewed or drop it and keep the question
- **Cloud push tool and procedure** (กำพล): until chosen, the worksheet says "the instructor walks it on screen" and the remote-access outcome is optional, not core
