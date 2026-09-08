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
| 6 | Create dashboards to visualize inputs and control outputs | Session 3 | Introduced in Session 1 (entity history, toggle from laptop and phone); Session 2 stays on device pages and the Automations page, no dashboard build |

Each post-test targets the two goals that are core in its session.

### Design principles
- **Experience first, vocabulary second.** Participants run a working networked system from Session 1 and only open the network in Session 3. ESPHome + HASS hide it completely: nobody *configures* an address before Session 3 — teams read their board's name and IP off a screen, type that IP into a browser to see the board's own page, and later click the board's card in Home Assistant; nothing is ever assigned by hand. One sentence of orientation at setup — *"your board and your Home Assistant talk over the workshop WiFi, not the hotel WiFi; we open that box on Saturday afternoon"* — and no more.
- **Goal 5 is taught by experiencing failure**, not slides. The sabotage round is the emotional peak and the thing participants will retell.
- **One kit through all three sessions.** Boards stay powered in the room overnight so Day 2 starts ready, not so anything is logged — laptops go home and the recorder goes with them. Teams read *their own* half-day trace on Day 2 afternoon, and the missing night is the evidence for "a farm needs a machine that never closes its lid".
- **Nothing in Sessions 1–2 depends on the cloud.** Boards, Home Assistant and phones talk only on the workshop network. Internet is still needed on the laptop SSIDs throughout: web.esphome.io (name reading, Sessions 1 and 3) and the worksheet site are online. Only Session 3's remote-access demo, on the instructor kit, depends on internet for the *activity* itself, and it has a recorded backup.

---

## Session 1 — Day 1 PM (13:00–15:45, post-test 15:45–16:00)

**ระบบสมองกลฝังตัวในฟาร์ม: รับรู้ ตัดสินใจ สั่งการ (Input → Logic → Output)** — Goals **1, 2** core; 3, 5, 6 introduced

| Time | Block | Goals |
|------|-------|-------|
| 13:00–13:20 | **Live:** Input → Logic → Output with familiar examples — **air conditioner / fridge** (thermostat → "if too warm" → compressor), **automatic street light** (light sensor → "if dark" → lamp), **automatic water tank** (float switch → "if level low" → pump; the bridge example: already a sensor-controlled pump, with a mechanical switch as the logic) — then the same three boxes for a smart farm (the water tank with a different sensor and the logic moved into software), mapped onto the kit: sensor board = input node, relay board = output node, HASS = logic + dashboard + logging. 2-min demo of the finished system as the hook. Vocabulary fixed here and reused verbatim: **Input (เซนเซอร์), Logic (ตัวตัดสินใจ), Output (ตัวกระทำ/actuator)**. | 1, 6 |
| 13:20–13:55 | **Activity 1 — Sense.** Kit handout, zone-colour check; teams start their HA VM and leave it. Read the board's name **and IP** over USB at web.esphome.io, then open the board's own page at `http://<ip>/` — no Home Assistant yet. Mini-challenge on that page: *which entity changes when you breathe on the board? cover it? lift the float?* Count the seconds from covering to the light value moving (feeds Session 2's chatter). Analog vs digital sensors. | 1, 2 |
| 13:55–14:35 | **Activity 2 — Act.** Part A, *the relay is a switch*: relay board on USB, read name + IP, toggle it from the board's page with nothing attached — click, indicator LED, onboard button; unplug USB. Part B, *the load*: wire the 12V load circuit (charge controller LOAD pair → terminal block → COM/NO → pump) and power the relay board from one of the controller's two USB ports — its 7–60 V input is never used, so nothing has to be split off the 12 V rail for the board (decided 8 Sep 2026) — pump A→B once then recirculate, toggle from the board's page. Instructor talking point, 2 min, no equipment: the same junction on a real farm is a **pump control box** with an **Auto / Off / Manual** selector — first seed of Goal 5. Safety framing: **12V is our classroom voltage; 220V needs an electrician.** Written question: *what would change to run a 220V pump?* | 1, 2, 5 |
| 14:35–14:50 | Break | |
| 14:50–15:30 | **Activity 3 — Logic.** Adopt both boards into the team's Home Assistant (discovered cards, six-char suffix). Observe from the device page — click an entity → history graph ("the board only knows *now*; HA remembers") — and toggle the pump from laptop and phone. No custom dashboard: that is Session 3. **Be the Logic yourself** for 5 min (watch humidity, water by hand, lift the float mid-run), then the team writes two rules as *ถ้า … ให้ …*. Build the float rule as the **first automation**: trigger = float switch → Dry, action = relay off; pass criterion: pump stops itself 3 of 3. Hook for Session 2: hold the float switch *out of the water first* (already Dry), then start the pump — nothing stops it (trigger vs condition). Left open on purpose; it returns as problem 1 of the Session 2 failure lab and is fixed there by Fail-safe 1. | 1, 3, 5, 6 |
| 15:30–15:45 | **Activity 4 — Spec (timing buffer).** Paper only, no equipment. Each team draws a scenario card stating a job with numbers; they read the kit's specs (humidity / temperature accuracy, float-switch rating, the relay's printed DC rating, pump current) and rule fit / unfit, naming the single part to change. At least one card exceeds the sensor accuracy, one exceeds the relay rating, one passes. Instructor closes with the five things to read on every spec. Flexes 10–25 min; never skipped — if under 15 min remain, run the short form (relay and pump specs only, one card, one fit/unfit call), as the worksheet says. | 2 |

**Post-test 1 (Goals 1, 2):** label input/logic/output in 3 scenarios (see Section 1 self-check below); pick the right sensor from a spec for 3 scenarios; match loads to relays/supplies; spot the unsafe pairing; given a scenario (sensor broken / leak found), pick the Auto/Off/Manual position.

---

## Session 2 — Day 2 AM (09:00–11:45, post-test 11:45–12:00)

**ตรรกะควบคุมอัตโนมัติและการออกแบบ Fail-safe สำหรับฟาร์ม** — Goals **3, 5** core; 6 extended

| Time | Block | Goals |
|------|-------|-------|
| 09:00–09:15 | **Automation recap.** Confirm both boards are back and the VM is recording, then open yesterday's float automation in the editor and name its three parts — **trigger / condition / action** — with one sentence on what each answers. The Session 1 puzzle is *not* raised here (decided 8 Sep 2026): it comes back as problem 1 of the failure lab, so the team meets the hole and the fix in the same activity rather than carrying an open question through Activity 5. No new build. | 3 |
| 09:15–10:30 | **Activity 5 — Think.** Night-light scenario first, on a real lamp: disable the Session 1 float rule, set the relay Off, then exchange the pump's two leads for the kit's **12V LED module** (red → NO, black → negative row; a two-wire exchange, timed at rehearsal, not budgeted), so chatter is a visibly flickering lamp rather than a relay indicator. Ladder: (a) threshold: light value → lamp ON, with screenshot chips; (b) hysteresis/deadband, counted over one minute before and after; (c) time-window condition, including the "already dark when the window opens" test that shows a condition never fires a rule, read on the Traces page; (d) phone notification. Then disable the lighting rules, exchange the leads back, re-enable the float rule once the float reads Wet, and carry the pattern to watering: humidity threshold with hysteresis. Enable/disable rules from the Automations page and command the relay from its device page; no dashboard build here. (a), (b) and (c) tests 1–3 are the required core; the (c) time-trigger fix and (d) are stretch. | 3, 6 |
| 10:30–10:45 | Break | |
| 10:45–11:30 | **Activity 6 — Failure lab.** Five problems, each in three steps — **sabotage → fix → sabotage again** — so every team sees each failure before building the rule that answers it and proves the fix by repeating the act (revised 8 Sep 2026 from four sealed-card observation rounds followed by the fixes: the card round asked teams to diagnose blind and record guesses, which made the worksheet long and the record vague). A member of the paired team performs each sabotage while our team watches only the Home Assistant screen; pairing logistics are explained live, not in the worksheet. Each problem states *how to sabotage*, *what happens if it succeeds*, and *how to tell it is fixed*; the record is four fields (worked? / what happened / fixed? / note). **1** float lifted, then the relay board's onboard button pressed — the Session 1 puzzle, staged → Fail-safe 1 upgrades the float rule in place (rename, notification, second trigger pump→On with condition float Dry) and adds a float-**Wet** condition to the watering rule. **2** pump started by hand and left alone runs forever → 30 s run-time cutoff. **3** sensor board switched off with its on/off switch (18650 cell, a pulled cable does nothing) — entities `unavailable`, pump keeps running, only Fail-safe 2 eventually stops it and for the wrong reason → unavailable/unknown → off; the team first decides open/close/hold. **4** pump lead unscrewed from NO — relay clicks, screen says On, no water — the one failure a dashboard cannot show → **command ≠ result**: the sensor board's accelerometer publishes `pump running`; commanded On for **15 s** with no vibration → off (15 s, not 30 s, so it fires before the cutoff and the test is unambiguous). **5** laptop WiFi off — every fail-safe goes silent, the pump runs on; no fix exists inside HA, which is the end-of-activity question and the control-box demo. Required self-check: 1, 2 and 5 sabotaged and seen; 1 and 2 fixed and re-tested; 3 and 4 when time allows. Keep the network explanation light: "the link died, the entities went unavailable, the pump was on its own." The *why* waits for Session 3. | 5 |
| 11:30–11:45 | **Debrief:** redundancy, watchdogs, maintenance expectations (who checks the system weekly? what corrodes first?). Closes with the lunch instruction that makes Session 3's opener possible: **do not shut the VM down** — HA has been recording all morning; disable the watering automation and leave the relay off so nothing pumps unattended. **Instructor demo (not a team task):** a real pump control box wired to the instructor kit — flip **Auto / Off / Manual** while the automation runs and show the pump obey the switch, not HASS. Then the same idea one layer down: the relay board's **onboard button** toggles the relay with Home Assistant shut down (bench-verified) — an override that lives in the board rather than the wiring. Links back to Session 1. | 5 |

**Post-test 2 (Goals 3, 5):** predict what a given automation does; fix a chattering automation with hysteresis; choose the fail-safe for a scenario; maintenance items.

---

## Session 3 — Day 2 PM (13:00–15:45, post-test 15:45–16:00)

**โครงสร้างระบบ IoT: การสื่อสาร คลาวด์ แดชบอร์ด และการออกแบบระบบ** — Goals **4, 6** core; 2, 5 applied

Restructured 8 Sep 2026 after the Session 3 review (SESSION-3-REVIEW-FOR-CLAUDE.md) and Roger's steer that the session was too dense and the design challenge needed real thinking and exchange time. The first half is trimmed to 85 min; the whole second half is the design challenge. Total still 150.

| Time | Block | Goals |
|------|-------|-------|
| 13:00–13:20 | **Live (กำพล):** open the box — the `wifi:` and `api:` blocks in the ESPHome YAML (no encryption key, no IP anywhere in the file), the device IP on the integration page, the live ESPHome log, and the board's **own web page** at `http://<name>/` — "your board *is* a web server on this network" is the most concrete thing in the block. Then the decision axes **distance, power source, data rate, cost** taught by **one worked choice** (card A, greenhouse with mains and WiFi) against a **completed reference table** on the worksheet — WiFi, ESP-NOW, Zigbee (the showroom demo set), LoRa/LoRaWAN, cellular/NB-IoT, wired RS-485, each with its limitation — and the team makes one choice of its own (card B, orchard at 400 m) as the only written record. MQTT / HTTP / ESPHome native API are on the worksheet to read, not taught. **Local-first vs cloud:** what happens to each when the internet fails — link back to failure-lab problem 5. Closes with the **remote-access demo** on the instructor kit: Settings → Home Assistant Cloud, remote URL, phone on mobile data, same dashboard, blow on the board, one pump command; state that it is a paid subscription and that the farm's HA is still the machine doing the work. Recorded backup if venue internet fails. | 4 |
| 13:20–13:30 | **Open the power box, instructor-led.** The "12 V supply" teams wired on Day 1 is a PWM charge controller with the adapter standing in for the battery. Read the three terminal pairs at their own box, read the LCD (12.0 V never shows "full" — the controller sees only what it measures; the icon is an estimate), name the three roles produce / store / supply, and answer "which of our devices needs power to keep recording all night" (the sensor board survives on its cell; the relay board, router and HA host do not). **Teams do not wire the panel** and do not open the battery-type menu (dropped 8 Sep 2026: indoor charge current is indistinguishable from zero, an adapter on the BATT pair is not a documented substitute for a battery while charging, and "18650 → b02" was a wrong shortcut). The adapter-pull demo is gone with them. If a manufacturer-compatible battery is to hand, the instructor shows charge current lit vs shaded with the battery connected throughout; otherwise the panel is a prop. | 4, 1 |
| 13:30–13:50 | **Our own half-day.** Open History since the start of Session 2 (explain that the window only holds what was recorded) and find four things the team caused: the light dip from a cupped hand, the fast relay toggling before hysteresis, the gaps from the failure lab, and relay **commands** after the pump went back on the relay — never "pump runs": the relay drove the lamp earlier that morning, the changeover time is recorded in Session 2, and even after it a relay On is a command, not water (failure-lab problem 4). "Not observed" is a valid answer. Then the interpretation step that earns the extra ten minutes: pick two events, name the experiment behind each, and say what a farm would check or change on seeing it. Then the question the graph cannot answer — *why is there no lunch break on this graph?* The recorder went home in a laptop bag. Teams whose VM lost the morning read the instructor's projected sample. | 6, 4 |
| 13:50–14:25 | **Activity 7 — Dashboard build** for a named real user: 5 min plan on the worksheet table, 25 min build (minimum = gauge, float tile, pump tile, automations list; history graph, severity colours and icons only after that), 5 min usability test by **someone who did not build it** — a member of the paired team on a phone, three questions, pass = all three within half a minute. No cloud push here any more: remote access is the demo in the first block. Written question: what did the tester miss and what did we change. | 6 |
| 14:25–14:40 | Break | |
| 14:40–15:35 | **Activity 8 — Design challenge, 55 min.** Each team draws a scenario card (A greenhouse / B 10-rai orchard / C hydroponics and D remote plot, both marked *advanced* / E a member's own farm, seeded by the Session 1 sentence and recommended when available) and produces a one-page **first-pilot** spec on the canvas: sensors + actuators with prices from the handed-out sheet (dated examples; live shopping optional), comms and power with reasoning against the four axes, at least one fail-safe and a manual override, a pilot plan, and a new **"what we are not sure of and how we will check"** box — recognising a gap is rewarded, not penalised. The worksheet says plainly that the classroom humidity thresholds are a stand-in, not an irrigation prescription. **40 min design · 10 min paired exchange** (1-min pitch, 3 min on two questions — best-reasoned decision, and which part has no answer to "what happens next if it fails" — then swap) **· 5 min revise and record one change.** The plenary pitches are dropped: only the paired exchange gives every team feedback, and a 400-seat ballroom microphone round costs more than it returns; the instructor mentions ideas seen at the tables during wrap-up. | 2, 4, 5 |
| 15:35–15:45 | **Wrap-up.** The three boxes across three sessions; where-to-go-next sheet (incl. take-home install guide, and the remote-access options); feedback form; kit return in the safe order (**disable every automation that can drive the relay, relay Off, isolate power, then drain**). | 1 |

**Post-test 3 (Goals 4, 6):** choose comms for 3 farms (backyard greenhouse / 10-rai orchard / remote field with no mains power); dashboard and local-vs-cloud items; remote access is *explain how it works*, not *configure it*, since it is demonstration-only. The design canvas is scored separately on the rubric.

---

## Anti-passenger structure for teams of four
**Decided 8 Sep 2026: no named roles.** An earlier draft assigned four rotating roles (Driver, Hardware, Recorder, Tester) and had each worksheet step address one of them. The role names read poorly in Thai and made the steps stilted, so the worksheet now lets each team decide who does what. What remains:
- The intro page asks teams to decide among themselves and to **swap at every activity boundary** so everyone touches both the screen and the kit; each activity opens with a one-line "swap who is on the laptop" callout.
- Steps that need two people at once ("one person does X while another watches the page") say so in plain words without naming a role.
- The intro page keeps the Tester habit as a team habit: say what you expect before each test, then watch.
- The Session 2 failure lab sends a member of the paired team to perform each sabotage; pairing logistics are explained live.

The worksheet has one short written question per activity that the team must fill in — this forces the team to verbalize what they did. Individual learning is still evidenced by the post-tests, not by team completion.

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
- 1 × PWM charge controller (12V 10A, **2× USB out**: one powers the relay board from Activity 2 on, the other the GoGo-IoT overnight) + 12V adapter standing in for the battery
  + terminal block + hook-up wire — the kit's 12V distribution for the pump, wired by the team in Activity 2
- 1 × 12V 15W solar panel — shown and handled in Session 3, **not wired by teams** (8 Sep 2026: no real battery in the kit, so nothing for a panel to charge; see the power block). Kept in the kit until Roger decides whether it stays
- USB-C cables, power strip, printed record sheet + design canvas
- Team card: zone colour, zone WiFi SSID + password, Home Assistant VM user/password. **No encryption key** — the ESPHome API runs unencrypted, so there is nothing to type at adoption

**Not in the kit any more:** soil moisture sensor (air humidity stands in for it), per-team
Raspberry Pi, per-board IP labels.

**Room (convention-centre ballroom, not a lab):**
- **Dedicated workshop network**, built by the network provider to [NETWORK-REQUIREMENTS.md](NETWORK-REQUIREMENTS.md): three zone VLANs, six SSIDs on every AP, no captive portal, client isolation off, mDNS forwarded, internet on the laptop SSIDs (web.esphome.io and the worksheet site are online). Do not rely on venue WiFi. Boards and team Home Assistants never touch the internet; only the instructor kit's HA does, for the Session 3 remote-access demo.
- Firmware pre-provisioned with the zone SSID; **DHCP, 12–24 h leases**, boards addressed by mDNS hostname so a changed IP costs nothing. Full network spec for the provider in [NETWORK-REQUIREMENTS.md](NETWORK-REQUIREMENTS.md); the two requirements most likely to be missed are mDNS forwarding between wireless clients and allowing two MAC addresses per laptop (bridged VM).
- **Overnight:** boards and charge controllers stay powered in the room between Day 1 and Day 2; laptops go home. Nothing is recorded overnight and nothing needs to be — Day 2 opens on the automation editor, not on a graph. Power staying on only buys a ready-to-go kit at 09:00; confirm it with the venue anyway, and if the room is cleared the cost is ten minutes of re-cabling, not a lost activity.
- **One instructor machine: the instructor kit** — a spare laptop mirroring a team kit, projected, for demos, and the rescue instance if a team's host dies. It adopts only its own two boards. (The separate wired-trunk instructor *server* is dropped along with the adopt-everything opener; `hass/configuration-instructor.yaml` and network requirement 3 exist for it and are now unused — see the open item in WORKSHEET-TODO.md.) On the kit, **one pump control box (Auto/Off/Manual)** wired between the relay board and pump, for the Session 2 debrief only — teams do not get or build one.
- Venue internet on the laptop SSIDs all three sessions (web.esphome.io, worksheet site); the Session 3 remote-access demo is the only *activity* that fails without it; an instructor phone hotspot or the recorded backup covers that one.
- Water discipline: pumps and containers stay on trays at the end of the table, boards and laptops at the other end. Confirm the venue allows water on tables.

## Risk register

| Risk | Mitigation |
|------|-----------|
| HASS host decision slips → host images and worksheets blocked | Decide first; it gates the whole production list |
| Venue cuts power or clears the room overnight | Confirm in writing. No activity depends on it any more — worst case, teams re-cable and re-adopt at the start of Session 2 |
| Venue internet flaky during the Session 3 remote-access demo | Phone hotspot for the instructor; pre-recorded backup of the Home Assistant Cloud demo; a screenshot talk is the last fallback, with the outcome stated as "explain how remote access works" |
| Day 2 shape not agreed with กำพล | Agree the "30-min lecture + hands-on on the same kit" split and the cloud tool early, so firmware can be pre-provisioned for it |
| Venue network blocks device-to-device traffic | Own router, always |
| mDNS fails on a laptop | Fall back to the IP, which the board now prints in its USB boot log and serves its own page from; 12–24 h leases mean re-reading it after an overnight is cheap |
| Network provider leaves client isolation or multicast filtering on | Acceptance test in NETWORK-REQUIREMENTS.md, run during the setup window with someone who can change controller settings |
| Participant laptop arrives without Home Assistant installed | Install guide sent ahead + verification form; spare laptops with the VM pre-imaged |
| Apple Silicon Mac can't boot the x86-64 master OVA | Build and test a second ARM64 master image (different VirtualBox OS type + storage controller); install guide branches by CPU, not just by OS — see `hass/README.md` |
| Relay chattering demo does not show | Resolved in principle: the worksheet has the student *make* the fluctuation by wavering a hand, not wait for sensor noise (the BH1750 is stable). 1 s interval stays. TEST-PLAN test E still owes the before/after toggle counts |
| Teams of 4 → passengers | Swap-at-every-activity callouts (no named roles, decided 8 Sep 2026) + the team's written questions |
| A board bricks / a pump leaks | 2 spare kits; drip trays; pumps only run during Activities 2–6 and the dashboard build |
| Session 1 runs long — HA adoption and the first automation both sit in Activity 3 | Activity 4 (spec game) runs last and is paper-only, but it is Goal 2's only hands-on and is **never cut**: the worksheet defines a short form (relay + pump spec only, one card, one verdict) with a 10-min floor. The flex comes from Activity 3's phone toggle and history steps. The VM is started in *Before you begin* so a broken laptop surfaces two hours before it is needed |
| **18650 cell in the GoGo-IoT keeps the board alive when USB is pulled** | The board has a battery path with source selection, so with a charged cell installed the board never goes `unavailable` from a pulled cable. **Closed** (Roger, 8 Sep 2026): the cell stays in, and every "power loss" step uses the board's **on/off switch** instead — failure-lab problem 3, the reference table. The Session 3 adapter demo now points the other way: the sensor board *survives* the adapter pull on its cell, which is scenario D's night-time node |
| Session 3 timed blocks overrun the slot | Restructured 8 Sep 2026 (evening): network + remote demo 20 + power 10 + history 20 + dashboard 35 + design 55 + wrap-up 10 = 150. The worksheet, SESSION-OVERVIEW and this table carry the same numbers. Still owed: a novice team timing the 25-min dashboard build on the real VM, and the packing sequence |
| `homeassistant.local` resolves to a neighbour's VM | ~34 identical-hostname VMs per zone; demonstrated on the bench with a single extra HA on the network. **Closed** — the worksheets now use the VM's on-screen IP, written on the record sheet on day 1 and re-read on day 2. See TEST-PLAN.md |
| Float switch fails *unsafe* | As shipped the float closes when *down*, so a cut wire read as "water present" and the pump could run dry. **Closed** — the float cylinder is flipped on its rod at kit prep (8 Sep 2026), so the contact closes when wet and a cut wire, unseated plug or missing switch reads **Dry**. Firmware `inverted: true` + `device_class: moisture` (Wet / Dry in HA). Session 2's Fail-safe 1 still adds a float-**Wet** condition to the watering rule, so `unavailable` fails safe too — TEST-PLAN test G. Residual risk: a kit assembled without the flip reads backwards; the kit-prep checklist must flip every float |
| Vibration verdict wrong at a table (soft mount, quiet pump, shaky table) | Three-level sensitivity select on the board, changeable from HA or the board's own page and restored across power cuts; the worksheet has Hardware put the board against the tubing first — TEST-PLAN test I |
| A team shuts the VM down at lunch, losing Session 3's history block | Last checklist item of Session 2 says do not; the worksheet tells a team without data to read the instructor's projected sample or a neighbour's graph and carry on. Prepare that sample from the instructor kit's own morning |
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
2. Agree the Day 2 shape with กำพล, including the trimmed 20-min network block and the Home Assistant Cloud remote-access demo it now ends with (account, subscription, `cloud:` on the instructor kit's HA, recorded backup); agree pre-test items and post-test logistics with นัทธี.
3. Worksheets for 3 sessions + design canvas + scenario cards.
4. Three post-tests (+ pre-test items).
5. Live slide decks for Sessions 1–3, reusing the online-deck content.
6. Facilitator run-sheet: sabotage-round script, control-box demo script, timing checkpoints, overnight procedure.
7. Full dress rehearsal with one team of colleagues — time Session 1 (sensor hands-on is now ours) and the failure lab.
8. Online decks: record only if time remains; they are off the critical path.

## Open decisions
- Who leads Session 2. Session 3's remote-access tool is written as **Home Assistant Cloud (Nabu Casa), instructor demo only** — Roger's working choice on 8 Sep 2026, to confirm with กำพล
- Whether the organizers can distribute optional pre-reading before Day 1
- Venue confirmations: overnight power, water on tables, internet for Session 3
- **Overview Areas baked into the master image** — Flower Farm matches the kit; Corn Farm and Grass have no hardware behind them. Keep, trim, or rename?
- ~~**Float switch mounting orientation**~~ **Decided** (8 Sep 2026): flip the float cylinder on its rod so it closes when wet. Add the flip to the kit-prep checklist for all 100 kits
- Whether the VM credential decided on the bench (`farmer` / `farmer`) is written into the repo, or lives only on the team card
- ~~**18650 cell: installed or not?**~~ **Decided** (Roger, 8 Sep 2026): the cell stays in; power-loss steps use the board's on/off switch. Bench check still owed: switch off → entities `unavailable` within a few seconds, switch on → entities back without re-adoption
- ~~**Relay board supply**~~ **Decided** (Roger, 8 Sep 2026): **USB from the charge controller, never the 7–60 V terminal.** Feeding the board from the 12 V rail meant splitting that rail to the board and to the load, which was the slow, error-prone part of Activity 2; the controller has two USB outputs, so the board takes one and the GoGo-IoT the other overnight. Bench check still owed: relay board boots and holds the relay energised from the controller's USB port, both USB ports live at once, and USB stays up whatever the load-mode setting
- ~~**Adapter-out demo with the panel connected**~~ **Dropped** (8 Sep 2026, Session 3 review): it broke the controller's documented disconnect order and did not reproduce a battery-backed system at night. **Replacement question:** does the instructor kit get a manufacturer-compatible 12 V battery so the panel can be shown charging (lit vs shaded, battery connected throughout)? If not, the panel is a prop in every kit and could leave the kit list
- **Remote-access demo** (Home Assistant Cloud): prepare the instructor account and remote URL before the day (initial provisioning can take a while), add `cloud:` to the instructor kit's HA configuration (`hass/README.md`), record a backup run from mobile data, and confirm the venue's laptop SSID reaches the internet from the instructor kit. Teams do not configure anything
