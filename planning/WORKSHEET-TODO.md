# Worksheet — open items before print/publish

The worksheets in `docs/` follow the session structure in [COURSE-DESIGN.md](COURSE-DESIGN.md) but
are written against the **actual kit list** (Sept 2026) rather than the design doc's assumptions.
Where the two differ, the worksheet wins. COURSE-DESIGN was brought back into line after the
bench session (adoption flow, overnight, sabotage cards, instructor machines, install path).

## Decisions taken (worksheet reflects these)

| Decision | Resolution | Consequence in the worksheet |
|---|---|---|
| Home Assistant host | Participants' own laptops, as a **pre-built VirtualBox OVA** (`hass/`) | Session 1 opens with "start the VM, open the IP on its screen"; the install guide shrinks to "install VirtualBox, import, Start" |
| Network zoning | **Three logical zones** (red/green/blue), each a VLAN with a 2.4 GHz board SSID and a 5 GHz laptop SSID; all SSIDs on every AP; zones isolated from each other | Team card carries the zone colour; kits are colour-coded; the zone is in every board's hostname. Session 1 adds a "colour in the name matches your kit" check at the name-reading step |
| Firmware per zone | **One source file per board, built three times** by `firmware/build-zones.py` (`esphome -s zone …`) | Six binaries in `firmware/dist/`. The only cross-zone risk is a wrong-coloured board at a table, and the board's own name reveals it |
| Sensed input for watering | **Air humidity** (onboard) as a stand-in for soil moisture; **float switch** on GoGo-IoT port 1 as the reservoir-low guard | Worksheet says so explicitly ("จำลองสถานการณ์") rather than pretending humidity means soil |
| Hysteresis teaching | **Light sensor → relay → 12V LED module**, framed as night lighting for a flower farm (เบญจมาศ). Since 14 Sep 2026 the lamp is wired and the dark→on / bright→off pair is built in **Session 1**; Session 2 opens on the chatter they cause | Session 2 runs the ladder (chatter, hysteresis, time, notification) on the lamp, then wires the pump and applies the lesson to watering |
| Session 1 shape | **Hardware first, Home Assistant last** (Roger, 7 Sep 2026). Activities: 1 Sense (board's own `web_server` page) · 2 Act (relay as a switch, then the load, which is the **LED module** since 14 Sep 2026) · 3 Logic (adopt both boards, entity history, be-the-Logic on the lamp, first automations = light → lamp on / off, optional time-trigger challenge) · 4 Spec (scenario-card game, the timing buffer). Sessions 2–3 activities renumbered 5–8, then 4–7 on 16 Sep 2026 when the Session 2 recap went | No YAML / I2C reading. No dashboard cards in session 1 — history is read from the entity dialog. No pump and no water on Day 1 except the float's glass. Auto/Off/Manual is a 2-min talking point in Activity 2 and an instructor demo in session 2, never a team build |
| Between-session data | **Dropped** (Roger, 7 Sep 2026). No instructor HA adopting participant nodes: not practical at 100 boards, and the payoff was one 15-min opener. The data teams read is what **their own HA** records across Day 2 morning | The history block moves out of session 2 and into session 3, rewritten around the team's own half-day trace (light dip from a cupped hand, chattering relay before hysteresis, gaps from the sabotage rounds). Session 2 now opens on an automation recap instead. Session 2's last checklist item: do not shut the VM down at lunch |
| Session 2 shape | **Hysteresis first** (Roger, 7 Sep 2026). Automation recap (15 min) → Activity 4 (70 min) → break → Activity 5 (50 min) → debrief (15 min); 75/45 became 70/50 on 14 Sep 2026; the recap was cut on 16 Sep 2026 (see the dry-pump row) | The trigger/condition/action table moves out of Activity 4 into the opener, anchored on the lamp automation built in session 1; since 16 Sep 2026 the opener is gone and condition / And if is one sentence at the top of §4.3 |
| Garden lamp | **A 12V LED module joins the kit** (Roger, 8 Sep 2026): three-lens sign module, red/black leads, photo at `docs/images/led-module-12v.jpg`. **It is the Session 1 load** (Roger, 14 Sep 2026): a lamp is easier to observe than a pump, which needs vibration sensing or someone watching water | One load exchange, in Session 2 §4.5: lamp off, pump on (two wires each), with every lighting rule and the optional timer disabled and the relay Off first. The "aim the lenses away from the GoGo-IoT board" line now lives in Session 1 §2.2, where the lamp is first lit |
| Charge controller | Wired by teams in Activity 2 as the kit's **12V source**: adapter → BATT pair; LOAD pair → terminal block → LED module in Session 1 (+ via COM/NO, − direct), the pump from Session 2 §5.5. **Relay board runs on the controller's USB port, never its 7–60 V input** (Roger, 8 Sep 2026: splitting the 12 V rail to the board was the slow part). The second USB port powers the GoGo-IoT when the laptop leaves (overnight). Panel is added in session 3 | Session 1 calls it "กล่องจ่ายไฟ 12V" with one sentence of orientation; session 3 "เปิดกล่อง: พลังงาน" reads the three terminal pairs, sets battery type, connects the panel |
| 18650 cell | **Stays in** (Roger, 8 Sep 2026). A charged cell keeps the board running when USB is pulled, so "power loss" is simulated with the board's **on/off switch**, never by pulling a cable | Sabotage card 1 and the Fail-safe 3 test say ปิดสวิตช์บนบอร์ด; the Session 3 adapter demo shows the sensor board surviving on its cell; `reference.md` lists the switch first under `unavailable` |
| Dry pump, no recap | **Roger, 16 Sep 2026.** The pump runs dry: no hose, no containers, no tray, no water pumped; the float keeps its Session 1 glass. The recap (Activity 4 at the time) is cut (a warm-up repeating Session 1 does not earn its own section); Session 2 opens on the four checks, then 5.1. Activities renumbered 4–7 the same day (Roger: do not skip 4) | §4.6 is the two-wire swap plus a 10-second dry run heard and felt; the failure lab reads the pump by sound and vibration; `s2.auto1.*` keys removed from the worksheet and record sheet; index.md kit and safety lines, Session 3 pre-start and pack-up, COURSE-DESIGN kit list and risk register, the run sheet and SESSION-OVERVIEW updated the same day. 4.4 was kept and rebuilt by Roger the same day as predict → fix → test (two predictions with reasons, `s2.time.dark_after/_before(_why)`, and `s2.time.fixed`); 4.8 was rebuilt by Roger the same day as the Auto / Manual mode toggle: `Pump Auto Mode` helper, an Overview (Legacy) dashboard to show it, a *Switch is on* condition on `รดน้ำ - เปิดปั๊ม` only, keys `s2.mode.off/on`; the rule-state reset moved into 5.0, which now also requires the toggle on; Session 3's dashboard table gained a Tile for it |
| Activity 5 shape | **Roger, 16 Sep 2026.** Four problems, none optional: the laptop-off-WiFi round is cut ("I don't see it as significant"), and 3 and 4 stop being optional — the instructor decides live whether a table skips one | Worksheet 5.1–5.4 are the problems and 5.5 is the summary table (was 5.6); keys `s2.sab.5.*` dropped from the worksheet and the record sheet; the summary table keeps its laptop/HA-down row, which is still the answer to `s2.fs.none` and to the end-of-activity question, so the point is discussed rather than staged; the run sheet keeps the WiFi-off procedure as an optional demo for tables that finish early |
| Rule-state wording | **Roger, 16 Sep 2026.** State of a rule reads `กฎ xx เปิดอยู่` / `กฎ yy ปิดไว้`, never bare เปิด / ปิด | Applied across sessions 2 and 3; the bare verbs stay where the text is an instruction to turn a rule on or off |
| Failure-lab order | **Roger, 16 Sep 2026.** Problems 2 and 4 swap: the vibration / command-is-not-result problem runs second and the 30 s run-time cutoff last, because the run-time problem gives the paired team nothing to sabotage — they start the pump and wait — and a flat round should not land second | Worksheet 5.2 is now the unscrewed pump lead and 5.4 the run-time cutoff; `s2.sab.N.*` keys stay bound to **position**, so only the record-sheet row labels swapped; the 15 s rule now forward-references the 30 s one instead of back; 5.3's caveat names the vibration rule, and that round is cleaner because no cutoff exists yet (with the board off `pump running` reads unavailable, not Off); the summary table names the rules (กฎน้ำหมด / กฎจำกัดเวลา / กฎเซนเซอร์หาย / กฎสั่งแล้วไม่เดิน) instead of numbering them by problem, and the "if you built it" conditionals are gone now that nothing is optional |
| Session 2 close | **Roger, 16 Sep 2026.** The limits table (5.5) and the debrief section go: both were reading or watching, not doing, and the control-box demo is instructor-run and may not happen as scripted | The maintenance table becomes the new 5.5 so Activity 5 ends on something written (55 min, wrap-up 10); `s2.fs.none` dropped from worksheet and record sheet; the close is `สรุปช่วงที่ 2` (learning points) + `ก่อนจบช่วงที่ 2` (lunch checklist), mirroring Session 1; the limits table survives as the facilitator's model answer to `s2.q5` in the run sheet, which also gained a wrap-up section holding the demo script |
| History reading is an activity | **Roger, 20 Sep 2026.** The Session 3 history block is a complete topic of its own, so it takes an activity number instead of sitting as an unnumbered page — otherwise students skip it. Session 3's activities become 6 (history), 7 (dashboard), 8 (design) | `docs/session-3-history.md` → `docs/activity-6.md`, the old dashboard and design pages → `activity-7.md` / `activity-8.md`, with the anchors (`#a6`…`#a8`), step numbers, banner files and `s3.q6` → `s3.q7` moved with them. `session-3-history.md` and `renders/session-3-history.html` stay as stubs forwarding to `activity-6`. The history page is the only activity without a banner (prompt noted in `activity-banners/PROMPTS.md`). Nav, `render-worksheets.py`, `extra.js` PAGE_SESSION, both worksheet tests, the record sheet, the run sheet, COURSE-DESIGN, SESSION-OVERVIEW and SLIDES-HANDOFF updated the same day; the slide deck's scope now has an eighth activity with no section yet |
| Plain ESP32-C3 nodemcu (item 2) | Spare, unmentioned | — |
| Lamp first, pump second, float rule last | **Roger, 14 Sep 2026.** Session 1 wires the LED module and builds `มืด-เปิดไฟ` / `สว่าง-ปิดไฟ` on one threshold plus an optional `ปิดไฟตามเวลา` (Time trigger, tested, then disabled); the pump, water props and watering rules move to Session 2 §4.5; the float rule is built for the first time as Fail-safe 1 in Activity 5 (sabotage → build → sabotage again); Session 2 §4.2/§4.3 deleted and Activity 4 renumbered 4.1–4.6 | Activity 3's written question is now the threshold-hover hook (answered by §4.1's chatter count); the already-Dry puzzle is gone. Keys: `s1.light.on` (replaces `s1.threshold` and `s2.light.on`), `s1.manual.rounds/correct`, `s1.rule.dark.*`, `s1.rule.bright.*`, `s1.auto.pass`, `s1.timer.at/ok`. The timer rule must appear in every rule-state list, because left on it fires daily at the chosen minute, including in Session 3 with the pump on the relay |

## Firmware requirements the worksheet now depends on

1. **Light sensor `update_interval` ≈ 1 s, no averaging filter.** Session 1 §3.4 builds the on/off pair and
   Session 2's chattering demo (§4.1) has the student *waver a hand* at the threshold and count toggles — it never depended on sensor
   noise, and the bench showed the BH1750 is stable anyway. 1 s is fast enough to follow a hand;
   at a 60 s default the demo silently fails. Other sensors can stay slower. See TEST-PLAN test E.
2. **Float switch on port 1 as `binary_sensor`. Polarity now settled on the bench — write it into
   the worksheet as fact, not as something teams discover.**
   - **Wet = มีน้ำ (water present)** · **Dry = น้ำหมด**. The entity carries `device_class: moisture`,
     so HA shows Wet / Dry, never On / Off. Float cylinder flipped on its rod at kit prep (8 Sep
     2026); re-verified on flashed firmware the same day, including a pulled wire and no switch at all
     reading Dry — TEST-PLAN test G, second pass, complete.
   - Wiring for the kit list / session 1: two bare wires from the float switch onto the **outer
     two positions** (Signal, Ground) of the adapter's **4-way terminal block**, then a Grove
     cable from the adapter to **special port 1**.
   - The worksheet may still ask teams to *observe* the two states (it is a good exercise), but
     the fail-safe step must not depend on them getting it right.
   - **Fail-safe wording.** With the float flipped, a cut wire, unseated Grove plug or missing
     switch reads **Dry** (pin floats HIGH through the internal pull-up, inverted), so every wiring
     fault looks like no water. The session 2 fail-safe still requires positive confirmation
     (**Wet**) as a condition so a dead board (`unavailable`) fails safe. See TEST-PLAN.md test G.
2b. **NEW — every board serves its own web page.** `web_server:` is now in both images: live
   sensor values, and a working switch on the relay board, at `http://<board-name>/` with **no
   Home Assistant involved**. Now in all three places it earned:
   - **Session 1**, as the first win — teams watch temperature and light react to a hand before
     the VM is even adopted, instead of waiting out the whole import/onboard/adopt sequence.
   - **`reference.md`**, as the support fallback — it proves a board is alive and sensing when a
     team's Home Assistant is broken.
   - **Session 3** ("open the network box"), where "your board *is* a web server, here is its
     address" is far more concrete than a diagram.

   **Address forms differ between the two boxes teams will type into — say so explicitly, or one
   will break.** Browser: needs a dot or a trailing slash (`gogo-iot-red-6749a4/` or
   `…-6749a4.local`); the bare name becomes a *web search*. Home Assistant's manual-entry Host
   field: needs **neither** — the bare name is what works.
3. **Relay node exposes one `switch`.** The relay's own hard-wired indicator follows the relay, so
   the "lamp" is visible — that is what session 2's garden-lamp framing points at. The board's
   *programmable* LED (GPIO2) is **not** the lamp: it is a **WiFi**-status light — steady lit when
   on WiFi, blinking when WiFi is lost, dark when unpowered. Home Assistant being down does NOT
   blink it; the relay board is meant to run overnight without HA. Bench-decided; see TEST-PLAN.md
   test H.
4. **`name_add_mac_suffix: true`, WiFi baked in, no API encryption**, `reboot_timeout: 0s`.
   No static IPs — see "Network and device provisioning" below. The light sensor's
   and the temperature/humidity sensor's `update_interval` (1 s) override the 5s used in the
   current `gogo-iot-node.yaml`; temperature/humidity also carry `delta` + `throttle` filters
   to keep history writes down.
5. ~~**Instructor HA adopts all GoGo-IoT nodes** before the end of session 1.~~ Dropped 7 Sep
   2026 with the between-session data block. Only the team's own laptop connects to a board, so
   the ESPHome `api:` connection budget is one client plus the occasional log stream.
6. **Charge controller load mode set to always-on (`24H` or equivalent) before the room.** These
   PWM controllers commonly default to a dusk-driven or dusk-plus-N-hours load mode keyed off PV
   voltage. Indoors the empty PV pair reads "night" forever, so a timer mode cuts the LOAD pair some
   hours in — the pump loses its supply mid-activity. The USB ports are normally on the battery
   rail and unaffected, and since 8 Sep 2026 both boards run from USB, so a wrong load mode now
   shows as "relay clicks, pump does not run" rather than a dead board — still confusing at 09:00.
   Check the manual's load-mode table and lock it, and bench-confirm the USB ports really are
   independent of load mode.
7. **Adapter leads must terminate in bare wire or ferrules** for the controller's BATT screw
   terminals — a barrel-jack adapter needs a pigtail. Kit item 10 (หัวแปลงสาย) may be this; confirm.
   Also confirm the terminal block (แผงต่อสาย) is in the kit; the worksheet uses it as the 12V
   distribution point (two rows: + and −).

## Needs verification against the real kit

- **Relay board on the controller's USB port** (decided 8 Sep 2026): confirm the board boots,
  connects, and holds the relay energised from the controller's USB output; that both USB ports
  supply at once (relay board + GoGo-IoT overnight); and that USB stays up regardless of the
  load-mode setting. Confirm the kit's USB-C cable reaches from the controller to the board.
- **12V LED module — now gates Day 1** (added 8 Sep 2026; Session 1 load since 14 Sep 2026; TEST-PLAN
  test L): confirm on the bench that it lights from the kit's 12 V rail through the relay, that reversed
  polarity is harmless (the worksheet says so), and that a lit module 30 cm from the GoGo-IoT board,
  lenses aimed away, does not push the light reading over a typical "dark" threshold under a cupped
  hand — if it does, the worksheet's "aim it away" line needs a larger distance. Time the one exchange
  (LED → pump, plus the water setup) with a colleague; it sets the 4.5 estimate below.
- ~~**Relay board terminals.**~~ **Confirmed from the vendor datasheet**, extracted to
  `firmware/ESP32-C6-RELAY-X1.md`: terminals are **NO / COM / NC** as the worksheet assumed,
  power input is a separate 2-way block (7–60 V), relay is **GPIO19**, programmable LED
  **GPIO2**, button **GPIO9**, relay rating `10A 250VAC / 10A 30VDC`. Still confirm the
  supplied harness has two bare wires for the relay side.
- ~~**Relay board takes USB *or* 12 V, not both**~~ **Bench-measured harmless** (TEST-PLAN
  test H): rails 80 mV apart, board and serial port fine with both connected. Moot since 8 Sep
  2026: the worksheet never wires 12 V to the board (USB from the controller only), so the
  measurement now only says a team that wires the 7–60 V input by mistake breaks nothing.
- **Humidity test in class.** Breathing raises humidity fast; decay back is slow. Session 2's
  watering test relies on that decay to cross the "on" threshold. Rehearse the timing; if decay is
  too slow, teams lower the threshold temporarily (the worksheet says so).
- **12V adapter reads as a part-charged battery.** A plain 12.0 V supply sits below the 12.7–13.0 V
  a full lead-acid shows, so the LCD icon will not read "full". The worksheet turns this into a
  teaching point ("the controller sees only what it measures"). If you'd rather it read full, use a
  13.5 V supply. Check the controller's low-voltage load cutoff is below 12.0 V.
- **One adapter.** It lives on the controller's BATT pair from Activity 2 onward and never moves.
  The relay board has no USB from the laptop at all — it runs from the LOAD pair — so the controller
  is load-bearing from session 1, not a session 3 prop.
- **12.0 V on the BATT pair vs the load low-voltage disconnect.** Lead-acid (`b01`) LVD is typically
  10.7–11.1 V, so 12.0 V is safe. Do not set `b02` with the adapter attached: Li-ion thresholds
  differ and a 3S profile may treat 12.0 V oddly. The worksheet has teams view the options and
  return to `b01`.
- **Phone reaching a laptop-hosted HA.** Bench result: with a bridged VM the host's Windows
  firewall is not in the path at all — the phone reached the VM on port 80 first try once the
  right port was used. The residual risk is the AP's handling of two MACs behind one wireless
  client (NETWORK-REQUIREMENTS item 2), not the laptop. Worksheet still tells teams to skip and flag
  it; `session-1.md`'s firewall line is **reworded** (same zone WiFi, same address, then flag it).
- **Water props not on the kit list**: a glass for the float switch, provided at the table. Since
  16 Sep 2026 that is the only water on the table: the pump runs dry, so the containers, hose and tray
  are gone.
- **Handouts referenced but not written**: humidity sensor
  and float switch spec excerpts; equipment price sheet for the design challenge.
- ~~**Worksheet adoption steps still say "IP from the team card"**~~ **Done, and revised again
  after the bench.** `session-1.md`, `reference.md`, `index.md`, `record-sheet.md` and
  `session-3.md` now describe the bench-verified flow: read the name via **Reset device in the
  browser**, **click the discovered card**, bare name (no `.local`) as the manual fallback, no
  encryption key. `homeassistant.local` is now **resolved**: the worksheets use the VM's own IP,
  read off its boot screen and written on the record sheet, because ~34 identically-named VMs per
  zone make the hostname point at a neighbour's machine (see TEST-PLAN).

## Network and device provisioning

Resolved: **no static IPs, no MAC reservations, no per-board configuration.** One identical
firmware image for all boards, with `name_add_mac_suffix: true` so each advertises a unique
mDNS hostname. Workshop SSID baked in; `improv_serial:` and `captive_portal:` included so WiFi
can be set over USB or from a phone at a future delivery.

Adoption flow per board: plug into the laptop over USB → web.esphome.io → Connect → **press
"Reset device" in the browser** (bench-critical: *not* the board's own reset button — native USB
means a hardware reset kills the browser session and the log comes up blank, which looks like a
dead board) → read the board's name from the boot banner and **write down the last six
characters** → in HA, go to
**Settings → Devices & services** and **click the discovered card carrying those six characters**
→ rename the device to the team's name. No encryption key (the API is unencrypted). The
six-character match and the zone colour in the name are what stop a team adopting a neighbour's
board, which otherwise fails silently.

**Fallback, if the card is not there** (bench-walked, and four levels deep — write it out
step by step or teams will not find it): **+ Add integration** → type **ESPHome** (not
"ESP-NOW") → **Add device** → **"Setup another instance of ESPHome"** → type the node name
**without `.local`** (`gogo-iot-red-6749a4`). The bare name resolves; no suffix needed.

Requirements this places on the network are written up in
[NETWORK-REQUIREMENTS.md](../network/NETWORK-REQUIREMENTS.md) for the provider. The two that most often
fail by default: **mDNS forwarded between wireless clients**, and **two MAC addresses allowed
per laptop** (the Home Assistant VM is bridged, so it has its own MAC and IP).

Consequences for the install guide (drafted 11 Sep 2026 as `docs/install.md`):

- **VirtualBox network adapter must be Bridged, not NAT.** With NAT the VM cannot receive
  multicast, `.local` will not resolve, and phones cannot reach it. This is the single decision
  the whole addressing scheme rests on.
- **Docker Desktop on Windows cannot be offered as a path** — no host networking, so no mDNS.
- The phone step reads the address from the **VM's boot console** (or HA Settings → System →
  Network) — the VM's IP, not the laptop's IP. Port 80, so no port number to type.
- Fallback if a laptop cannot resolve a board by name: the board prints its IP in the USB boot
  log (`=====  IP ADDRESS: ...  =====`) and serves its own page there. Leases are 12–24 h, so
  re-read it after an overnight.

`reboot_timeout: 0s` is set on both `api:` and `wifi:` in both images (the 15-minute default
would reboot boards overnight with no Home Assistant connected). TEST-PLAN test F verifies it
held — still to run.

## Built: vibration reporter (accelerometer)

**Built and compiling**, in `gogo-iot-workshop.yaml`. Roger's correction settled it: the design
model is **one board, one purpose** — a board that can do many things is used for one job at a
time, and if you need several functions you use several boards. The physical conflict I had
raised (the board cannot simultaneously see ambient light, sit in open air, hold the float
switch, and be strapped to a pump) is therefore not a blocker. All sensors were previously
bench-tested and work.

It follows the algorithm in `gogo-iot-node/docs/ESPHOME_PLAN.md`: 40 Hz sampling, magnitude,
slow-baseline subtraction, 1 s RMS, hysteresis and persistence. Publishes
`ความสั่นสะเทือน (vibration)` in milli-g and the verdict `ปั๊มกำลังทำงาน (pump running)`.
Raw axes stay `internal`.

**Still open:**

- ~~**Thresholds are guesses**~~ **Calibrated** (TEST-PLAN test I: idle 3–8 mg, running
  20–25 mg on a soft mount; the signal separates). 25/12 stays as the default, now the *medium*
  level of a three-way **sensitivity select** (high 15/10, low 40/20) a team changes from HA or the
  board's page — bench-confirmed, including survival across a power cycle.
- ~~**Not yet in the worksheets.**~~ **In three places now:** session 1's sensor table (tap the
  table → `ความสั่นสะเทือน`, so the entity is familiar before it matters); session 2 **Fail-safe 4**
  (required since 16 Sep 2026; it was optional until then): commanded-on for 15 s (not 30, so it fires before Fail-safe 2 and the test is
  unambiguous) with `ปั๊มกำลังทำงาน` Off → pump off + notification, tested
  by unscrewing the pump lead — the same act as sabotage card 3, which is the point; and the
  `reference.md` "pump won't run" row. The design-canvas prompt in `record-sheet.md` stays.
  Fail-safe 4 tells Hardware to put the board against the tubing first — the sensor is on the
  GoGo-IoT board, which otherwise lives on the charge controller's USB, away from the pump.
- **Cost when unused**: 40 Hz I2C polling runs on every board whether or not anyone looks at the
  vibration entity. Watch during the bench test for any effect on the other sensors' stability or
  on WiFi; if it bites, the answer is a separate image variant rather than a slower poll.

## Found in review, fixed

- **Thai-only entity names collide.** ESPHome builds the Home Assistant `entity_id` by
  transliterating the name to ASCII; a Thai-only name becomes a row of underscores, and two of
  equal character length fail to compile outright. Every entity name now carries a lowercase
  ASCII tag. Would have produced unusable entity_ids on all 200 boards.
- **Activity 2 had teams power the relay board twice at once.** The step order read: connect the
  12 V adapter, *then* read the board name over USB — precisely the "choose one" violation the
  datasheet warns about. The name lookup is now its own block before any wiring, ending with
  "unplug the USB cable".
- **TEST-PLAN test F checked an uptime sensor that did not exist.** Both boards now publish
  uptime, WiFi signal and IP as diagnostic entities.

## Scale: 400 participants in 100 teams

The count correction (100 sensor boards, 100 relay boards, 100+ laptops, 100 phones, 400
participants) is roughly triple what the materials were written against. Three consequences,
two already fixed and one still open.

**Fixed — instructor-check gates.** Three activities gated on "ผู้สอนตรวจแล้ว". One instructor
cannot verify 100 teams. They are now objective self-checks with a stated pass criterion (e.g.
"fewer than 2 relay clicks in a minute of hand-waving"), except the dashboard one, which became
a **peer check** by the neighbouring team — better than the original, because being handed an
unfamiliar dashboard is exactly the test that activity is trying to run.

**Fixed — the sabotage round.** The failure lab had the instructor walking to each team and
breaking their rig unannounced. Impossible across 100 teams in 15 minutes. It is now **paired
teams sabotaging each other** from sealed cards: one team observes their dashboard while a member
of the paired team performs a sabotage, then they swap, four rounds, cards revealed at the end.
This scales flat, and it is arguably better teaching — each team both diagnoses and causes a
failure. The four cards are:

1. Switch the sensor board off with its on/off switch (it has an 18650 cell, so a pulled cable does nothing) → entities go `unavailable`
2. Turn off WiFi on the laptop → Home Assistant loses both boards
3. **Unscrew the pump's positive lead from the relay's NO terminal** → the relay still clicks,
   the LED still lights, Home Assistant still says the pump is on, and no water moves
4. **Lift the float switch out of the water, then press the relay board's onboard button** →
   yesterday's rule turns the pump off, then the pump runs again with the float still Dry

Card 3 is deliberate: it is the only sabotage the dashboard cannot reveal, which is
precisely the case the vibration reporter exists to catch. The record sheet asks which round
looked normal but was not.

Card 4 was added 8 Sep 2026 (Roger). It stages the puzzle Session 1 leaves open — pump started
with the float already Dry — so the team meets the hole and its fix (Fail-safe 1, steps 3–6) in
the same activity. The Session 2 recap no longer raises the puzzle; it only names
trigger / condition / action. Cost: one more round, roughly 3 min inside the 45-min lab. The
between-round reset (saboteur undoes the act, observed team gets the pump running) is now one
sentence in the worksheet; the facilitator run sheet still owns the water and timing details.

**Revised again, 8 Sep 2026 (Roger, after reading the page).** The blind card round is gone. Too
much logistics prose made the worksheet unattractive, the sabotage procedure was unclear, and the
record (what did you see / what do you think caused it / seconds to notice) was vague. Activity 5
is now **five problems, each sabotage → fix → sabotage again**: every problem opens with
วิธีจำลองปัญหา (the exact act), ถ้าจำลองสำเร็จ (the symptom, and which other rule may mask it),
the fix steps, and ถือว่าแก้ได้เมื่อ (repeat the act; stated pass criterion). Every team is
sabotaged on every problem, so all see the failure before building the rule. The four cards became
problems 1 (float + button → Fail-safe 1), 3 (board off → Fail-safe 3), 4 (NO lead → Fail-safe 4)
and 5 (laptop WiFi off → no fix in HA, feeds the end question; **cut 16 Sep 2026**, see the Activity 5 row); problem 2 (pump left running →
Fail-safe 2) is new so the run-time cutoff also answers a failure the team watched. Record per
problem: จำลองสำเร็จ / เกิดอะไรขึ้น / แก้ได้แล้ว / หมายเหตุ (`s2.sab.<n>.ok|what|fixed|note`); the
old `s2.sab.*.seen/pump/cause/time`, pair/correct/card and `s2.fs*.stop` keys are removed (no
workshop data existed yet). Pairing and turn-taking logistics are the facilitator's spoken
briefing, not worksheet text.

**Still open — facilitator ratio.** 100 teams doing hands-on 12 V wiring needs roving help.
Session 1's "ยกมือ" instruction assumes someone can come. At a plausible 1:10, that is ten
facilitators, and they need briefing on the failure modes in `reference.md`. Not a materials
problem, but it gates the run-sheet.

**Closed — instructor Home Assistant capacity.** The question was whether one instructor
instance could record 100 adopted boards overnight (~1,000 entities, ~250 state writes/second,
order 10 million rows a night, which default SQLite would not enjoy). Resolved 7 Sep 2026 by
dropping the requirement rather than engineering around it: no instructor instance adopts
participant nodes. The data session 3 reads is each team's own HA recording its own two boards
across Day 2 morning — one client per board, a few writes a second, and no shared machine whose
failure costs 100 teams their activity.

Falling out of that: `hass/configuration-instructor.yaml` (recorder limits sized for 100 boards)
and NETWORK-REQUIREMENTS.md requirement 3 (instructor server on an 802.1Q trunk, present in all
three zones) no longer have a consumer. **Open**: whether to delete the config and drop
requirement 3 from the network spec, which would also remove the wired-trunk ask from the venue.
The network document may already be with the provider.

## WiFi power save disabled on both boards

ESPHome defaults ESP32 to `power_save_mode: light`: the radio sleeps between beacons and wakes
only at DTIM to collect buffered broadcast and multicast. **mDNS is multicast.** In a room with
200 boards, 100 chatty Home Assistant instances and heavy broadcast, that is precisely the
traffic most likely to be dropped — and the symptom is `<name>.local` resolving intermittently,
which looks like a network fault rather than a client power-save setting.

Both images now set `power_save_mode: none`. The boards run on mains power through the charge
controller, so there is nothing to save. Confirm during the bench test that this does not raise
board temperature noticeably.

## Multicast noise: what we control and what the network must

Three levers, in order of leverage:

1. **Phones on mobile data.** Removes the chattiest client class (iOS Bonjour) entirely. Already
   in the network design.
2. **Network zoning — adopted.** mDNS load scales with queriers × responders per broadcast domain.
   Three zones, each with its own 2.4 + 5 GHz SSID pair on one VLAN, cut the per-domain product
   ~9× with no mDNS gateway anywhere. **Zones are logical, not spatial:** the zone SSID is baked
   into each board, every AP broadcasts all six SSIDs, and teams sit anywhere. That removes the RF-
   boundary failure mode entirely; the remaining risk is a wrong-coloured board at a table, which
   the board's own hostname (`gogo-iot-red-…`) exposes at the name-reading step. Alternatives
   considered and rejected: one image with all three networks listed and per-AP SSID broadcast (RF
   decides the zone — boundary spillover); MAC→VLAN on the controller (200-row table, vendor
   feature dependency); participants provisioning the zone SSID over USB via Improv (one image,
   but 200 password entries by participants — kept as the re-provisioning fallback, since
   `improv_serial` is in the image anyway).
3. **Home Assistant diet.** `hass/configuration.yaml` drops `default_config` and with it `ssdp`
   (periodic UPnP multicast), `dhcp`, bluetooth, usb, cloud and the integration tail. Real, but
   smaller than it looks: HA's zeroconf browses its entire generated service-type list regardless,
   for "Discovered" cards, and the ESPHome integration needs zeroconf anyway. The residual cost is
   the startup burst when 100 instances query and 200 boards answer — which is what zoning
   addresses.

**Delivery recommendation that falls out of (3): ship a pre-built VirtualBox OVA**, not an
install guide. The config only helps if it is on 100 laptops; a from-scratch install by 100
teams will not put it there. An appliance image also bakes in the bridged adapter and the VM
firewall for port 80, closing two install-guide risks already listed above. See `hass/README.md`.

**Instructor recorder** — `hass/configuration-instructor.yaml` was sized for 100 adopted boards
and is unused since 7 Sep 2026; see the closed capacity item above. The team image
(`hass/configuration.yaml`) records two boards and needs no such limits.

## Reuse across deliveries

The worksheets carry no dates, venue names, or weekday references. Session pages refer to each other
as ช่วงที่ 1/2/3. Since the history block moved into session 3 and reads the team's own morning,
**no between-session gap is required at all** — the data it needs is generated inside ช่วงที่ 2.
The only carry-over between sessions is the kit staying wired, and if a delivery has to break that,
the cost is re-cabling, not a lost activity.

## Images

`docs/images/relay-board-terminals.png` is the labelled board diagram cropped from the vendor
datasheet (page 7) — NO/COM/NC, the 7–60 V input, USB, button, and both LEDs, all called out.
It is the one image in the worksheet that is not a placeholder, and it directly serves "students
must see clearly where to connect the wires." `relay-board.jpg` is the clean unlabelled photo
from the same PDF, kept as the source for a Thai-annotated version if you want one later.

These are vendor product images of hardware we bought, used in our own training material. Fine
for the workshop; if the worksheets are ever published more widely, retake them ourselves.

The earlier `relay-board-generic-x1.webp` was **deleted** — it was the WROOM variant from
devices.esphome.io, a different board.

All other images are `placeholder.png` with alt text describing the shot. Three alt texts were
rewritten after the bench (web.esphome.io with the Reset device button and the DEVICE NAME
banner; the discovered card on Devices & services; the YAML `api:` block with no encryption).
Shot list still to write — parked until the worksheet text settles. Bench screenshots exist but
carry bench-specific state (SSID `Annie`, `192.168.8.x`, browser extensions): reference only,
retake on a clean profile once the config is frozen.

## Print artifact

`docs/record-sheet.md` is the only page meant for paper, one copy per team. It keeps dotted
fill-in lines (the exception to the web-Markdown conventions). Print from the rendered page.

## Not yet written

- **Scenario cards for the archived spec game (Session 1 Activity 4 until 15 Sep 2026)** — one job per card with the numbers it needs.
  Set of at least three: one exceeds the onboard humidity–temperature accuracy, one exceeds the
  relay's printed DC rating (a 12V pump drawing more than 10 A, or a 220V load), one passes as-is.
  Answer key names the single part to change.
- ~~**Session 2 knock-on**~~ **Reworked twice.** Since 14 Sep 2026 Fail-safe 1 **builds** the float rule
  from scratch (`Fail-safe - น้ำหมด`: float→Dry trigger, pump→On trigger with float-Dry condition, off +
  notification), then adds a float-**Wet** condition to `รดน้ำ - เปิดปั๊ม` and tests the lifted-first
  case, which makes `unavailable` fail safe, as TEST-PLAN test G required. The Session 1 already-Dry
  hook is gone; Session 1's written question now hooks the chatter lesson instead.
- Scenario cards for Activity 7 (content is in `session-3.md`)
- ~~Role cards~~ dropped 8 Sep 2026: no named roles, teams decide who does what (see COURSE-DESIGN.md)
- Team cards: zone colour, zone laptop SSID + password, HA VM user/password. No instructor HA
  address, no board names or IPs (read from the board), no encryption key
- Pre-workshop Home Assistant install guide for participant laptops (COURSE-DESIGN Section 6),
  including opening port 80 so phones can reach it
- Equipment price sheet for the design challenge — prices marked as dated examples; the worksheet now
  promises it under that name (ใบราคาอุปกรณ์ที่แจก)
- Instructor's sample History graph from the instructor kit's own Session 2 morning, projected for teams
  whose VM lost the recording (Session 3 history block)
- Decide whether the instructor kit gets a real 12 V battery for a lit-vs-shaded charging demo; if not,
  decide whether the 15 W panel stays in 100 kits as a prop (COURSE-DESIGN open decisions)
- The three post-tests. Include one individual transfer item in post-test 2: *your pump is on, but the
  dashboard stops updating — what can you conclude, and what do you check?*
- **Take-home page: one worked farm example** — from a named problem to sensor choice, placement,
  threshold, control rules, equipment, maintenance, and what must be re-measured before copying
  the classroom thresholds. No session time for it; it is the bridge from air-humidity stand-in to
  a real irrigation decision (review item, 8 Sep 2026)
- ~~**Cloud push procedure**~~ replaced 8 Sep 2026 by the **Home Assistant Cloud remote-access demo**
  on the instructor kit (worksheet section ดูข้อมูลฟาร์มจากนอกพื้นที่). Still owed: instructor account and
  remote URL prepared ahead, `cloud:` on the instructor kit's HA (see `hass/README.md`), a recorded
  backup run from mobile data, and กำพล's sign-off since it sits in their block
- **Facilitator run sheet** — help-request signal, escalation owner, spare-kit policy, water and
  reset procedure between failure-lab problems, timing checkpoints, and the **"swap who is on the
  laptop" cue at every activity boundary** (announced, not on the worksheet — Roger, 9 Sep 2026). Ratio assumption ~1:10 still to confirm
- **Facilitator briefing for the failure lab** — pairing, who sabotages first, turn-taking and
  reset between problems are spoken, not on the worksheet (8 Sep 2026); sealed cards are no longer
  needed, the acts are printed in the worksheet
- ~~COURSE-DESIGN.md update to reflect the decisions above~~ done after the bench session; keep in step from here

## Session 2 review, 8 Sep 2026 (SESSION-2-REVIEW-FOR-CLAUDE.md)

Acted on, all in `docs/session-2.md` unless noted:

- **No dashboard build in Session 2.** The แผงควบคุม card is gone; the enable/disable lesson now
  runs on the Automations page with the relay commanded from its device page. The Failure Lab
  observes two browser tabs (sensor device page, relay device page); phone optional. Observers
  may look at the physical pump after they have written what the screen showed, before the
  saboteur restores. Record sheet columns say หน้าอุปกรณ์, not แดชบอร์ด. COURSE-DESIGN and
  SESSION-OVERVIEW rows updated.
- **Rule state at every transition** is now explicit (rewritten 14 Sep 2026): the two lighting rules
  arrive from Session 1 on, the optional timer off; disable both lighting rules including their time
  triggers and the timer before the pump is wired; no float rule exists until Activity 5; re-enable
  `รดน้ำ - เปิดปั๊ม` after the disable exercise; and a stated Automations-list state before the
  Failure Lab. The lab starts the pump from the relay device page; no more "raise the threshold".
- **Load exchange is two wires each way**, both directions, no fixed 5-min budget.
- **Time-condition tests** reset from a known state, use the editor's Traces button (verified on
  the s2-a5-15 screenshot), give 2 min lead, and when repeated after the time trigger update both
  After and At and also watch the Before cutoff.
- **Hysteresis** pass = ≤2 switches in a minute *and* the lamp still turns on when covered and off
  when uncovered; counts go on the record sheet as before.
- **Fail-safe limits**: stuck-floating float (still Wet) is its own table row with no rule;
  Wet condition prevents a new start only; vibration = motor moving, not water delivered;
  Fail-safe 3 test restarts the pump first and checks which rule's notification fired.
- Copy edits: กฎ, โดย, ชีวิตจริง, หลอดไฟ, เซนเซอร์.
- COURSE-DESIGN's spec game (Session 1 Activity 4 at the time) now matches the worksheet (short form, never homework).

**Activity 4 internal breakdown, estimate only, not timed (revised 14 Sep 2026, 70 min):** state check
3 · chatter count 5 · hysteresis 8 · time-condition tests 12 · time-trigger fix 5 · notification 4 ·
pump wiring, water setup, first run and changeover time 10 · watering rules and test 12 ·
disable/enable exercise 5 · written question 3 = 67, leaving 3. The lamp swap (5) and the dark→on
build with screenshots (15) moved to Session 1, which is what made the (ค) fix and (ง) core. Failure
Lab (50 min): problem 1 now builds the float rule from scratch (~3 min more than the old upgrade).
Session 1 Activity 3: adopt 8 · history + phone 6 · be-the-Logic and rules 7 · two automations 14 ·
question 2 = 37 of 40, the optional timer ~5 for fast teams. All need a timed rehearsal before anyone
calls them verified.

Not acted on, decisions pending (review items 9–12): delivery materials and the take-home worked farm
example — listed above. The cloud tool and the solar-demo disconnection order were settled by the
Session 3 review below.

## Session 3 review, 8 Sep 2026 (SESSION-3-REVIEW-FOR-CLAUDE.md)

Roger's steer: the session was too dense; the design challenge needs real time to think, work and
exchange. Acted on, in `docs/session-3.md`, `docs/record-sheet.md`, COURSE-DESIGN and SESSION-OVERVIEW:

- **Timetable** network + remote demo 20 · power 10 · history 20 · dashboard 35 · break · design 55 ·
  wrap-up 10 = 150. The worksheet opens with this table. Design went from 45 (30 design + 5 pair +
  10 plenary) to 55 (40 + 10 + 5), the plenary is gone, and the first half lost 25 min.
- **Comms block condensed**: the blank 30-cell มาก/กลาง/น้อย table became a completed reference table
  with a limitation column and a caveat line; the only written record is one choice (card B) after
  the instructor's worked example (card A). Protocol table kept as read-only. Zigbee row kept.
- **Remote access** is an instructor demo of Home Assistant Cloud (Nabu Casa), placed at the end of
  the network block. Fields for tool / URL / what / interval / where were removed; two observations
  and one written question replace them. Subscription stated. Session intro, index.md and the
  overview now say "explain how", not "each team tested".
- **Power** is 10 min instructor-led at the team's own box: terminals, LCD, produce/store/supply,
  "who needs power all night". Teams do not wire the panel, do not open the battery menu; the
  adapter-pull demo and the "18650 → b02" line are gone. Record fields cut to volt, icon, night list.
- **History** is 20 min: relay On is a *command*, counted only after the pump went back on the relay
  (new `s2.pump_back_t` field in Session 2 step 2 of the exchange-back, and on the record sheet);
  "not observed" allowed; time window explained; sample graph fallback; new two-event interpretation
  table (what / when / which experiment / what a farm would check). Overnight-gap question kept.
- **Dashboard** 35 min: plan reduced on 9 Sep to two questions (see / control) in the user's words, the card·entity·position table cut as impractical; minimum vs optional steps stated; the two tests merged into one by someone who
  did not build it, half-minute pass criterion; written question is about what the tester missed.
- **Design**: framed as a first pilot; C and D marked advanced; new canvas box "สิ่งที่ยังไม่แน่ใจ"
  and a rubric line for it; note that classroom humidity thresholds are a stand-in; paired exchange
  1 + 3 min each way with the "what happens next if it fails" question; `d.revise` field.
- **Kit return** order fixed: automations off, relay Off, isolate power, then drain.
- `hass/README.md` gains the instructor-kit `cloud:` note; the team config comment points to it.

## Session 3, Roger's own review, 9 Sep 2026

Three steers, all acted on in `docs/session-3.md`, `docs/record-sheet.md`, COURSE-DESIGN and SESSION-OVERVIEW:

1. **Network and power had too little participation for an after-lunch slot.** Both are now decision
   steps *inside* the design challenge (85 min: scenario 5 · network 20 · power 15 · fill 30 ·
   exchange 10 · revise 5), and the afternoon opens with the two hands-on blocks, history (20) and
   dashboard (35). Total still 150.
2. **Power got a participation exercise**: panel sizing for four loads by two rules (15 W ≈ 60 Wh/day;
   Wh/day = W × h), plus one-night storage for the node and the pump, with a self-check answer. The
   point it lands: a farm pump is direct daylight DC solar with a water tank, no battery; batteries
   are for small loads that must last the night. Fields `s3.pwr.size.*`.
4. **History made open-ended** (later on 9 Sep): "find three points on the graph you can link to
   something we did" replaces the four scripted finds and the relay/gap counts, because 100 teams
   run differently and the scripted events will not all exist on every graph. Fields
   `s3.hist.ev{1,2,3}.*` plus humidity min/max; `s3.hist.relay_on/gaps/gap_max` removed.
3. **Network reframed as local network vs access from outside.** Local: the six technologies stay,
   chosen by **elimination** (distance, then power at the far end) for the team's own two links —
   fields `s3.net.{1,2}.*`; instructor works card B on screen. MQTT and HTTP are gone from the
   worksheet. Access from outside: a five-way menu (notifications only, Home Assistant Cloud, private
   VPN, opening a door yourself, IoT cloud platform) so Nabu Casa is one option, not the only one;
   the instructor still demos it. Fields `s3.remote.need/method/lost`; `s3.comm.choice.*` removed.

Not acted on: the review's "readiness 5 min" and "recovery 10 min" rows — no room once design took
the time; the ก่อนเริ่ม checklist stays untimed and the 5-min revise slot is the buffer. The network
block stays at 20 rather than the review's implied cut because it is กำพล's live block and now also
carries the remote demo; confirm with them. Dashboard build time (25 min) still needs a novice timing.

## Codex pass on Sessions 2 and 3, 15 Sep 2026 — accepted, with items to reconsider

Codex rewrote `docs/session-2.md` and `docs/session-3.md` (commit 4abd1a0, "Simplify Sessions 2 and 3
Thai worksheets and clarify teaching flow"). Roger kept the result as is. Claude rechecked it the same
evening: renders regenerated, strict MkDocs build clean, the field-sync test passing on all four
pages, every session key present on the record sheet, no broken anchors, images or links. The
planning docs (INSTRUCTOR-RESOURCES, COURSE-DESIGN, SESSION-OVERVIEW, TEST-PLAN) were then brought
into line with the new worksheet, including the renumbered sub-steps (4.1–4.8, 6.1–6.4, 7.1–7.6).

**Codex changes that are improvements, now propagated to the run sheet**

- 5.5 (the laptop-WiFi round, cut 16 Sep 2026; the note is kept for the run sheet's optional demo): stop the pump with the relay board's button before turning WiFi back on. The old text
  claimed Fail-safe 2 would cut the pump on reconnect; the failed service call is not retried.
- 5.3: the 30 s cutoff may fire before the board is marked unavailable, so the sensor-lost rule is
  judged by its Trace, not by which rule stopped the pump.
- History: a VM shutdown or restart keeps the recorded history and only leaves a gap. The old
  note said such a team has no Session 2 data.
- 4.6: the pump's leads go onto the terminal block where the lamp's were, which matches how
  Session 1 wired the lamp; the old text put the + lead directly on NO.

**Codex changes Roger may want to reconsider** (none blocking; the run sheet covers each live)

1. **Network table lost its range figures.** Step 7.2 asks teams to eliminate options by distance,
   but the table no longer states any distance (WiFi 30–50 m, ESP-NOW 100–200 m, Zigbee 10–30 m per
   hop, LoRa 1–10 km, RS-485 ~1 km). The 9 Sep handoff kept them pending กำพล's confirmation. The
   instructor now gives them on screen (INSTRUCTOR-RESOURCES 7.2). Restoring one column to the table
   would let the exercise stand on its own. **Resolved 18 Sep 2026:** the table now has range, power,
   benefits, limitations and cost columns.
2. **Remote-access menu went from five ways to four.** "Opening a door yourself" (port forwarding,
   DDNS, a tunnel) was dropped, along with the Tailscale/WireGuard, LINE/Telegram examples.
   Mentioned live; SESSION-OVERVIEW and COURSE-DESIGN now say four. The menu table itself was cut on
   18 Sep 2026 (item 14).
3. **The take-home shopping table is gone** (Raspberry Pi / Home Assistant Green, ESP32 relay
   module, capacitive soil probe, DC solar pump, VPN options) and nothing on `docs/resources.md`
   replaces it. Cheapest fix: move that table to `resources.md`, which Session 3's closing already
   links.
4. **The feedback form is no longer mentioned anywhere on the site** (its QR placeholder was
   removed with the other placeholders). Hand out or project.
5. **Summary-table (5.6 then, 5.5 now) stuck-float row:** now credits the 30 s run-time cutoff with catching a float stuck
   floating, so the "no rule stops it" answer has one case (laptop / Home Assistant down) instead of
   two. Defensible, and the run sheet says so, but it softens the maintenance point.
6. **Session 2 debrief lost the watchdog discussion bullet;** 5.2 lost "10–20 min on a real farm";
   the sizing answer lost the 18650 ≈ 9 Wh, 20 Ah and 400 W-panel remarks (kept in the run sheet).
7. **Numbering:** the Session 2 recap was headed กิจกรรมที่ 4, the number the archived spec game
   held. Since 16 Sep 2026 the recap is gone too and the activities are renumbered 4–7 (Roger: do not
   skip 4). Anchors (`#a4…#a7`), banner files, `s2.q4`, `s2.q5`, `s3.q6` and every reference in the
   planning docs moved with them; every number in this file was rewritten to the new scheme, including
   entries dated before 16 Sep. Step-image filenames such as `s2-a5-04-add-trigger.png` were left alone.
8. **Sub-step numbers changed** (4.3 split into 4.3/4.4, 4.5 into 4.6/4.7, 6.1 into 6.1/6.2, 7.2/7.3
   into 7.2–7.8, now 7.2–7.5). Anchors were kept, so old links still land; only prose references had to move.
9. **7.2 "Survey the room network" cut on 18 Sep 2026** (Roger: no clear point). It had teams find
   `ssid`, `name_add_mac_suffix` and `api` in the ESPHome file and open the board's own page by the IP
   Home Assistant shows; nothing later used it. 7.3–7.11 became 7.2–7.10 in the worksheet, the run
   sheet and the assessment references; anchors (`#a7-2b`…) were kept. The network block still
H. **7.4 "Home Assistant Cloud demo" and 7.5 "Choose remote access" cut on 18 Sep 2026** (Roger:
    the block is instructor-led; 7.3 covers it, no need for separate sub-activities). The demo script now
    lives only in the run sheet (7.3); the one written output, the canvas row "จากฟาร์มถึงเจ้าของนอกฟาร์ม"
    (`d.comm.3.*`), became step 3 of 7.3. 7.6–7.10 became 7.4–7.8; anchors kept; assessment
    references moved. The network block still says 20 min. Cut text in
    `archive/session-3-activity-7-4-7-5-remote-access.md`.
11. **Design canvas, 7.7 and 7.8 cut on 18 Sep 2026** (Roger: the instructor directs the peer presentation, it
    need not be in the workbook; with four design dimensions there is no need for a separate แบบร่างระบบ,
    students fill the worksheet directly). 7.6 is now four blocks with fields inline: sensor and actuator
    (`d.in.1.sensor`, `d.out.1.device`), connectivity (the `d.comm.*` rows from 7.2–7.3, shown again),
    power (`d.power*` from 7.5, shown again) and a test plan (`d.test.how`, `d.test.pass`, new). 7.1 now
    holds `d.problem`. The record sheet's canvas section became a plain Activity 7 mirror of those fields; the
    other canvas keys (`d.in.1.qty/spec`, `d.out.1.va/driver/verify`, `d.rule.*`, `d.logic.*`, `d.fs1.*`,
    `d.manual`, `d.care.*`, `d.budget.*`, `d.unknown`, `d.pilot.*`) no longer exist. The presentation and
    exchange (15 min) is described in the run sheet only. Cut text in
    `archive/session-3-activity-7-canvas-and-exchange.md`.
12. **7.4 rewritten on 18 Sep 2026** (Roger: focus on battery types for solar and how to choose; the charge
    controller matters because each type needs its own charge parameters). Now: one-step box tour; a table of
    flooded and sealed lead-acid, LiFePO4 and NMC (price per Ah, usable share, cycle life, weight and care,
    cautions), NiMH and sodium-ion in one line; a choosing order (night use, Wh per night and usable share, who
    maintains, first cost against lifetime, weight and heat); the controller's b01/b02 option with a
    per-type charge-voltage table; the LCD icon point kept as one step; new field `d.battery`, also shown
    in 7.6 and the record sheet. All figures are general estimates for กำพล to confirm. The power block is
    still budgeted at 15 min; 7.4 grew, so watch it in rehearsal.
13. **18 Sep 2026, wording and cloud framing.** The scenarios are โจทย์, not บัตร (Roger). 7.2's table now
    shows range, power draw, benefits, limitations and cost per option. 7.3 no longer compares "our system"
    with a system that decides on the cloud as if Home Assistant could live there: Home Assistant must reach
    boards and gateways locally (WiFi LAN, USB Zigbee or LoRa receiver), so it sits on a machine in the farm and
    the cloud is only a door in or a copy of the data (Roger: never make students feel a cloud-hosted Home
    Assistant is a possibility). The vendor-cloud contrast that S3-POST-03 relies on is kept as a callout about
    ready-made products.
14. **7.3 became listen-only on 18 Sep 2026** (Roger: no action; students only listen to the instructor
    explain the cloud concept; the worksheet holds only checkboxes to acknowledge the key points). Three
    boxes: local-only access as built; remote access needs a cloud door that depends on the framework (paid
    Nabu Casa for Home Assistant, free vendor clouds for Tuya or Xiaomi); our local rules keep running when
    the internet is down, so cloud-only products need their own fail-safes. The four-way menu table, the
    choice step with `d.comm.3.*` and the end-of-block question are gone from the worksheet; the choice is
    written in 7.6's third communication row (the keys survive there and in the record sheet). The
    instructor talk, the optional cloud demo and the model answer are in the run sheet. Cut text in
    `archive/session-3-activity-7-3-remote-access-menu.md`.
    `scripts/test_worksheet_steps.cjs` accepts such a section when its source has checkbox items and no
    numbered step, and then requires the render to show checkboxes and no `<ol>`.
15. **7.4 lost its charge-controller steps on 18 Sep 2026** (Roger: a distraction). The b01/b02 menu
    step, the per-type charge-voltage table and the LCD-icon step are gone; 7.4 is now the box tour,
    the battery table, the choosing order and the `d.battery` field. Charge voltages per type and the
    icon point stay in the run sheet as if-asked notes. Cut text in
    `archive/session-3-activity-7-4-controller-steps.md`. Replaced the same day by two sentences and two SVG
    figures from `scripts/power_figures.py` (the workshop controller's photo, cropped from the Activity 2
    wiring photo, with panel, battery and LED lamp; and an inverter on the battery terminals, through a fuse, driving
    a 220 V AC pump; Roger first asked for it on the controller's load output, then moved it to the battery the
    same day).
16. **7.5 rewritten on 18 Sep 2026** (Roger: start with how to calculate). Four steps: W = V × A; Wh per
    day = W × h; battery at least that (Ah = Wh ÷ 12, grossed up for the usable share from 7.4); panels for
    the worst day, 3 full-sun hours, rounded up. Two worked examples in a table: LED 50 W × 8 h at night
    (400 Wh, 133 W of panel) and a 1,100 W pump 2 h a day (2,200 Wh, 733 W of panel), with the
    store-water-not-electricity callout. The 15 W panel ≈ 60 Wh/day rule, the kit-load table and the folded
    answer table are gone from the worksheet; the kit numbers survive in the run sheet. Fields unchanged.

Pre-existing, not from Codex: History is opened "from the start of Session 2", yet the gap
question asks about the overnight break before it. Opening from the end of Session 1 would show the
gap on the graph; as written the question is answered by reasoning, not by looking.
