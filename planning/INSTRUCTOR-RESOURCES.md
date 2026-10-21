# Instructor & TA resources

Every file and link needed to prepare for and run the workshop, in one place.
Participants get a trimmed version at
[รวมไฟล์และลิงก์](https://arnans.github.io/iot-training/renders/resources.html).

Links are absolute so this page works the same whether you read it in the repository or as the
published page at
[arnans.github.io/iot-training/instructor-resources.html](https://arnans.github.io/iot-training/instructor-resources.html).
Rows marked *(repo)* need access to the private `iot-training` repository.

---

## 1. Board firmware — twelve images

One image per board type, per zone colour, plus a second sensor image for Session 4. The zone
colour is baked in: a red-zone image only joins the red SSID. Sensor and relay images built and
verified 12 Sep 2026; the ESP-NOW sensor image and the receiver image are new on 20 Sep 2026 and
**need a build and a bench pass (TEST-PLAN test M) before publishing.** The base sensor image is
unchanged in behaviour (it only gained internal ids) and need not be re-flashed.

| Board | Red zone | Green zone | Blue zone |
|---|---|---|---|
| **GoGo-IoT sensor board** (ESP32-C3) — pre-flashed, sessions 1–3 | [gogo-iot-red.factory.bin](https://arnans.github.io/iot-training/firmware/gogo-iot-red.factory.bin) | [gogo-iot-green.factory.bin](https://arnans.github.io/iot-training/firmware/gogo-iot-green.factory.bin) | [gogo-iot-blue.factory.bin](https://arnans.github.io/iot-training/firmware/gogo-iot-blue.factory.bin) |
| **Relay board** (ESP32-C6-Relay_X1) | [gogo-relay-red.factory.bin](https://arnans.github.io/iot-training/firmware/gogo-relay-red.factory.bin) | [gogo-relay-green.factory.bin](https://arnans.github.io/iot-training/firmware/gogo-relay-green.factory.bin) | [gogo-relay-blue.factory.bin](https://arnans.github.io/iot-training/firmware/gogo-relay-blue.factory.bin) |
| **GoGo-IoT sensor board with ESP-NOW** — same board, same hostname; flashed by the teams over the base image in Activity 9 | [gogo-iot-espnow-red.factory.bin](https://arnans.github.io/iot-training/firmware/gogo-iot-espnow-red.factory.bin) | [gogo-iot-espnow-green.factory.bin](https://arnans.github.io/iot-training/firmware/gogo-iot-espnow-green.factory.bin) | [gogo-iot-espnow-blue.factory.bin](https://arnans.github.io/iot-training/firmware/gogo-iot-espnow-blue.factory.bin) |
| **Receiver** (plain ESP32-C3 devkit, Session 4) — flashed by the teams in Activity 10 | [farm-receiver-red.factory.bin](https://arnans.github.io/iot-training/firmware/farm-receiver-red.factory.bin) | [farm-receiver-green.factory.bin](https://arnans.github.io/iot-training/firmware/farm-receiver-green.factory.bin) | [farm-receiver-blue.factory.bin](https://arnans.github.io/iot-training/firmware/farm-receiver-blue.factory.bin) |

> **Receiver devkits: buy one model.** The log banner only appears on the USB port the image's
> logger writes to; the receiver image is built for native-USB boards (Super Mini, XIAO C3) by
> default and needs `--receiver-console uart0` for boards with a CP2102/CH340 chip (DevKitM-1).
> Sort the receivers by zone and colour-code them like the other boards; they are handed out at
> the start of Session 4, one per team, and returned with the kit.

**To flash a board:** plug it into a laptop over USB-C, open <https://web.esphome.io> in Chrome or
Edge → **Connect** → pick the serial port → **Install** → choose the `.bin` for that board and
zone. Needs internet.

> **The colour on the board must match the colour on the kit and on the team card.** A mismatched
> board joins the wrong WiFi and the team's Home Assistant never sees it. The board says which it
> is — its name reads `gogo-iot-red-a1b2c3`.

Spare boards flashed during the workshop must be flashed to **that table's zone colour**.

---

## 2. Home Assistant virtual machine

The same image participants install. Put it on the instructor kit and on every rescue laptop.

| Laptop | VirtualBox | Farm Workshop VM |
|---|---|---|
| Windows / Intel Mac | [Downloads](https://www.virtualbox.org/wiki/Downloads) | [`Farm-Workshop-win-1.3.ova`](https://github.com/arnans/iot-training/releases/download/vm-1.3/Farm-Workshop-win-1.3.ova) (~2.1 GB, GitHub release `vm-1.3`) |
| Apple Silicon Mac (M1+) | [Downloads](https://www.virtualbox.org/wiki/Downloads) — **7.2 or newer** | [`Farm-Workshop-arm64-1.3.ova`](https://github.com/arnans/iot-training/releases/download/vm-1.3/Farm-Workshop-arm64-1.3.ova) (~2.1 GB, GitHub release `vm-1.3`) |

The two files are not interchangeable and cannot be imported on the wrong host: the ARM64 OVF
declares `<Platform architecture="ARM">`, so VirtualBox on an Intel host rejects the file instead
of importing something that will not boot. Apple Silicon needs VirtualBox **7.2+**; 7.1 and older
cannot run the ARM64 guest. Build notes and the exact settings of both images:
[hass/README.md](https://github.com/arnans/iot-training/blob/main/hass/README.md) *(repo)*.

Import steps, settings and the login are in the participant guide:
**[เตรียมแล็ปท็อป](https://arnans.github.io/iot-training/renders/install.html)**. The two things
that go wrong: Adapter 1 must be **Bridged** and set to the laptop's own WiFi card, and the VM is
reached at `http://<its IP>` — never `homeassistant.local`, because every team's VM answers to
that name. On ARM64 the console's IP line reads `enp0s8`, not `enp0s3`.

Login: `TODO` / `TODO`. **Not on the team card and not in the install guide** — project it at
Activity 3.1, when teams first log in. Until then participants only check that the Login page
loads (install guide step 3, and the pre-start check in Session 1).

---

## 3. Worksheets and printed material

| What | Link |
|---|---|
| Participant site | <https://arnans.github.io/iot-training/> |
| Before the workshop — เตรียมแล็ปท็อป | [install.html](https://arnans.github.io/iot-training/renders/install.html) |
| Session 1 — รับรู้ ตัดสินใจ สั่งการ | [session-1-start.html](https://arnans.github.io/iot-training/renders/session-1-start.html) |
| Session 2 — ควบคุมอัตโนมัติและ Fail-safe | [activity-4.html](https://arnans.github.io/iot-training/renders/activity-4.html) |
| Session 3 — แดชบอร์ดและออกแบบระบบ | [activity-6.html](https://arnans.github.io/iot-training/renders/activity-6.html) |
| Participant file & link list | [resources.html](https://arnans.github.io/iot-training/renders/resources.html) |
| Team record sheet — **the one thing that gets printed** | [record-sheet.md](https://github.com/arnans/iot-training/blob/main/docs/record-sheet.md) *(repo)* |
| Home Assistant menu paths + troubleshooting — **keep this open while roving** | [reference.md](https://github.com/arnans/iot-training/blob/main/docs/reference.md) *(repo)* |

The `renders/` pages are self-contained: open one once and it keeps working with no internet.

---

## 4. Preparing to teach

| What | Link |
|---|---|
| What happens in each session, and why | [SESSION-OVERVIEW.md](https://github.com/arnans/iot-training/blob/main/planning/SESSION-OVERVIEW.md) *(repo)* |
| Full course design — timings, kit list, risks, open decisions | [COURSE-DESIGN.md](https://github.com/arnans/iot-training/blob/main/planning/COURSE-DESIGN.md) *(repo)* |
| Activities 1–8 — Thai workshop presentation, activity covers and instructor notes | [Google Slides — 84 slides](https://docs.google.com/presentation/d/1yoNUpS3mo2z2zOZJHEQtuMfSuLxuXltwDT22UHVSHzo/edit) · [Inventory and build sources](https://github.com/arnans/iot-training/blob/main/planning/slides/README.md) *(repo — edit this same deck in place; Activity 1's native slide `a1_slide_8`, currently ninth, retains its intentional image placeholder)* |
| Reusable slide-generation reference | [Design, Thai writing, image treatment and native Slides workflow](https://github.com/arnans/iot-training/blob/main/planning/SLIDE-GENERATION-GUIDE.md) *(repo)*, with saved cover and equipment-slide previews |
| Known gaps and assumptions in the worksheets | [WORKSHEET-TODO.md](https://github.com/arnans/iot-training/blob/main/planning/WORKSHEET-TODO.md) *(repo)* |
| **Network setup** — the ask for NT, Flint router checklist, who-joins-which-WiFi rules, acceptance test | [network-setup.html](https://arnans.github.io/iot-training/network-setup.html) |
| Old VLAN network spec — **deprecated 21 Sep 2026**, reference only (Thai / English) | [network-requirements.html](https://arnans.github.io/iot-training/network-requirements.html) · [network-requirements-en.html](https://arnans.github.io/iot-training/network-requirements-en.html) |

**Instructor kit** — a spare laptop mirroring a team kit, projected. It also rescues a team whose
laptop dies. Three things teams don't have: the **Auto / Off / Manual pump control box** for the
Session 2 debrief, a Home Assistant Cloud account for the Session 3 remote-access demo, and a saved
morning history graph for teams whose own graph holds too little Session 2 data.

**Kit prep, the two that fail silently:** flip the float cylinder on its rod so it closes when wet
(otherwise a cut wire reads "water present" and a pump can run dry), and colour-code board, kit and
team card as one matching set.

---

## 5. Tools and external links

| Tool | Used for |
|---|---|
| [progress.html](https://arnans.github.io/iot-training/progress.html) | **Team progress board.** Live during the workshop: which activity each team is on, ticks per step, help requests (🙋) and messages. One tab per session (ช่วงที่ 1–3); pick the day at the top if it is not today. Tap a team's cell for its devices and a reset. No login: open it on every TA phone and bookmark it. Design notes in `webapp/PROGRESS-DASHBOARD.md` |
| <https://web.esphome.io> | Flashing boards and reading a board's name from its USB log. Chrome or Edge only |
| <https://www.home-assistant.io/docs/> | Home Assistant reference |
| <https://esphome.io/> | ESPHome reference |
| [github.com/arnans/gogo-iot-node](https://github.com/arnans/gogo-iot-node) | GoGo-IoT sensor board hardware |

---

## 6. Running the activities

Each activity in the worksheet opens with a checklist for the group, **ใบงาน**: one item
per sub-section, holding the question and its answer boxes, with a link down to the steps. This
section follows the same items, so a TA looking at a team's screen can find the matching entry
here. Each item gives **Done when** (what a finished answer looks like) and **If stuck** (what to
check first). Minutes are the design estimate, not a rehearsed timing.

**How to run it.** Project the checklist and talk through it one item at a time; teams work down
it while you talk. The prose under each item is for the team that falls behind or wants the reason.
Keep the [progress board](https://arnans.github.io/iot-training/progress.html) open on a TA phone:
every tick a team makes lands there within seconds, so it shows who is behind before they raise a
hand. A team ticks either the item in the checklist or the **ทำข้อนี้เสร็จแล้ว** box at the foot
of the sub-section; both are the same tick. The three "we understood this" boxes in 8.3 are not
counted.

The two questions from the Activity 4 pilot, `s2.time.trace` and `s2.time.why`, and the Session 1 lighting keys (`s1.light.on`,
`s1.rule.dark.*`, `s1.rule.bright.*`, `s1.auto.pass`, `s1.timer.at`, `s1.timer.ok`) are on the
record sheet like every other answer. Session 1 no longer records the supply voltage, the
wired-right-first-time self-report, the control-box position or the manual-round counts
(Roger, 15 Sep 2026).

### Session 1 · Activity 1 — Sense (35 min)

Teams leave with the sensor board's name and IP, a first reading of every sensor from the board's
own web page, and a sense that the float is a yes/no sensor. No Home Assistant yet.

#### 1.1 Plug in the float switch

**Done when** the float's Grove lead is in **port 1**, the board is on the laptop's USB, and the float
is floating in the glass.

**If stuck** A float in any other port never changes state; only port 1 is configured.

#### 1.2 Read the board's name and IP

**Done when** a name like `gogo-iot-red-a1b2c3` is written down whose colour matches the team card, with an
IP under it. The IP line appears 10–20 seconds after the name.

**If stuck** The log is blank or the name has scrolled past: press **Reset device** *in the web page*.
Unplugging the cable or pressing the board's button drops the browser's connection. Firefox cannot
connect, so use Chrome or Edge. A name but no IP within a minute: the board cannot join WiFi. Check the
colour, and swap the board if it is wrong.

#### 1.3 Open the board's web page

**Done when** `http://<IP>` shows the list of entities, updating without a refresh.

**If stuck** The laptop is not on `farm-laptop-<colour>` for the board's colour. The page lives on the
board, not on the internet.

#### 1.4 What each sensor measures

**Done when** each row has a room value and a test value that visibly differs from it: humidity rises
when breathed on, light drops when covered, vibration rises from a few mg at rest when the table
is knocked. The float reads **ON** floating and **OFF** lifted. The light and humidity values change within
about one to two seconds, because the board reads them once a second. Session 2 uses the
room and covered light numbers to set its thresholds.

**If stuck** Humidity barely moves: breathe slowly for the full five seconds, close to the board. The float
never changes: the lead is not in port 1.

#### End-of-activity question

**A good answer** says humidity decides watering (standing in for soil moisture on a real farm), and
the float tells whether the reservoir still has enough water for the pump. It only says yes or no,
not how much.

### Session 1 · Activity 2 — Act (40 min)

Teams leave with the 12 V lamp circuit wired by their own hands, the relay board powered from the
charge controller's USB, and the LED module lighting on command. No water in Session 1 beyond the
float's glass; the pump is first wired in Session 2 (4.6).

#### 2.1 Know the relay board

**Done when** every member can point at **COM** and **NO** (used) and at **7-60 Input / GND** (never
used) on the real board.

#### 2.1 Read name and IP, click the relay

**Done when** a `gogo-relay-<colour>-…` name and IP are written down. The relay clicks from the web page
switch and from the board's own button. The USB lead is then unplugged from the laptop, but left
in the board.

**If stuck** Same as 1.2. The **LED** blinking means no WiFi; a steady LED means connected.

#### 2.2 Charge controller parts and the relay circuit

**Done when** the team can find the middle pair (battery symbol, where the adapter goes), the right pair
(lamp symbol, the 12 V output) and the two USB ports, and can say from the diagram why the
+12 V lead goes through **COM** and **NO** while the negative lead goes straight to the lamp.

#### 2.2 Wire it

**Done when** all six steps are done and a second person has checked every screw. No bare ends touch, no
wire is in **NC** or **7-60 Input / GND**, and the adapter is still unplugged.

**If stuck** Check for a wire on NC instead of NO (the LED is then lit whenever the relay is Off), and for the
load pair and the battery pair swapped. The LED's red lead belongs on **NO** and the black lead on the
negative row; a reversed LED stays dark but is not damaged.

#### 2.2 Power on and light the lamp

**Done when** the charge controller screen shows about 12 V. The relay board lights and rejoins WiFi. The
LED lights on On and darkens on Off, and its lenses point away from the GoGo-IoT board, at least
30 cm off. A lamp shining onto the light sensor makes the Activity 3 rules fight themselves.

**If stuck** Screen dark: unplug first, then check the adapter is on the middle pair, red to plus. Screen on
but the relay board is dark: reseat its USB lead or try the other port. Relay clicks but the LED stays
dark: swap the LED's two leads. The page will not open after
a minute: move the relay board's USB lead to the laptop briefly to read a new IP (the relay
restarts Off), then move it back.

The **Auto / Off / Manual** control-box talk has no worksheet item any more (removed 15 Sep
2026). If you give it, it is two minutes before the break with nothing to fill in; Session 2's
debrief demo carries the idea.

#### End-of-activity question

**A good answer** says a 220 V pump needs a relay or contactor rated for the pump's AC current,
including its start-up surge. It also needs 220 V-rated wiring, an enclosure and protection
(breaker, RCD), and an electrician to wire it, not the team.
**Before the break** every relay is Off and every lamp is dark.

### Session 1 · Activity 3 — Logic (40 min)

Teams leave with both boards in their own Home Assistant, a light threshold they chose, and two
automations, `มืด-เปิดไฟ` and `สว่าง-ปิดไฟ` on one shared threshold, passing 3 of 3. Fast teams also
leave with a tested (and then disabled) `ปิดไฟตามเวลา`. Cut on 15 Sep 2026 to reduce reading during
the live session: no history graph (Session 3 opens on it) and no "be the Logic yourself" round; 3.3
goes straight from threshold to rule sentences to the two automations.

#### 3.1 Add both boards

**Done when** the representative's laptop is logged in with the credentials you project now, and both
boards are added by IP (*+ Add integration → ESPHome → Setup another instance of ESPHome*, port
6053), with the name HA shows matching the names written down. Renaming the devices is optional.

**If stuck** The Login page no longer loads: the VM's IP changed, so read it again from the VM
window. Boards have mDNS disabled (it flooded the room's WiFi), so **there are no discovered cards
and `.local` names do not resolve** — the IP is the only way. **A mistyped IP that lands on a
neighbour's board looks like success**, but the team then watches the neighbour's sensors and its
automation drives the neighbour's lamp. Check the name HA shows before adding. Cannot connect: the
board's IP moved, so read it again at web.esphome.io (Reset device, `IP ADDRESS` line).

#### 3.2 Test the boards in Home Assistant

**Done when** the GoGo-IoT device page shows the same entities as the board's web page and the light
value drops under a cupped hand, and the lamp toggles from the laptop and from a phone, with both
screens agreeing.

**If stuck** The phone must be on the zone WiFi, not mobile data, and must use the IP from the VM screen,
never `homeassistant.local`. If it still fails, skip this step and flag it to a TA; the rest of the activity
does not need the phone.

#### 3.3 Threshold, rule sentences, two automations

**Done when** the threshold sits roughly halfway between the open and covered readings taken now on the
device page (80 and 7 → about 40), not copied from Activity 1 because the room may have changed. The
two sentences read: dark, "if the light sensor is below the threshold, turn the lamp on"; bright,
"if it is above, turn the lamp off". Then covering the board lights the lamp and uncovering darkens it,
three rounds out of three, with nobody touching the switch. Both rules use the **same** threshold on
purpose. The scenario is the flower-farm night light: the LED is the lamp, a cupped hand is dusk.

**If stuck** The value barely moves: the hand is not over the light sensor (right-hand group on the
board). It never rises again: the lit LED is shining under the hand; turn it away. Covering does
nothing: the reading was already below the threshold when the rule was saved. A crossing trigger
needs the value to go above, then below again, so uncover, set the relay Off and cover again. The
board sends a light value about once a second, so hold the cover for two seconds. Check that the
trigger entity is `ความสว่าง (light)` and the action is the team's own relay. The lamp flickers while
the hand moves slowly: that is expected with one shared threshold, tell them to cover fully and
quickly; it is the opening lesson of Session 2, not a fault.

#### 3.4 Optional: lamp off at a chosen time

**Done when** the lamp, switched On from the device page, goes off by itself at the minute the team
chose, and the team has then **switched the rule off**. Left on, it fires every day at that time,
including during Session 3 with the pump on the relay.

**If stuck** Nothing happens: the chosen time is already past, so pick a new future minute. Home
Assistant runs on Asia/Bangkok time; read the laptop clock. The lamp went off early: `สว่าง-ปิดไฟ`
fired because the sensor was covered then uncovered; start with the sensor open.

#### End-of-activity question

**A good answer** says the lamp switches on and off repeatedly, because one value is both the on and the
off line, so every wobble across it fires a rule. Leave it there: Session 2 opens by measuring it and
fixing it with a second threshold.

### Session 2 · Activity 4 — automations and hysteresis (70 min)

Teams leave with four automations (five if they did the Session 1 timer): two watering rules **on**,
the two garden-lamp rules and the timer **off**, and the pump wired for the first time. They also leave
with their thresholds, two flicker counts and the written answer. Keys go into the team's JSON as
`s2.light.off`, `s2.chatter.*`, `s2.time.*`, `s2.pump_back_t`, `s2.hum.*`, `s2.mode.*`, `s2.q4`; the on-threshold is
Session 1's `s1.light.on`.

**At the start** the lamp rules from Session 1 are live, so anyone shading the board lights the
lamp. That is a free demo, not a fault. There is no recap activity any more (cut 16 Sep 2026): the
session goes from the four checks straight into 5.1.

#### Before start (ก่อนเริ่ม) · ~3 min

**Done when** the four worksheet checks are ticked (they report to the dashboard as one activity,
15 Sep 2026): Home Assistant is up, the sensor board shows values, the relay board switches the
LED, and the team has agreed to leave both boards and Home Assistant on for the half-day
recording. Also confirm what the worksheet no longer asks: `มืด-เปิดไฟ` and `สว่าง-ปิดไฟ` are on
with the same threshold, `ปิดไฟตามเวลา` (if it exists) is off, and covering the board lights the
lamp. Today's VM IP is read off the screen; the record sheet still has a box for it.

**If stuck** The lamp will not light: same as Session 1's 3.4 (no crossing yet, or the room got darker
than the threshold overnight, so raise the threshold or add light).

#### 4.1 Lamp flickers near the threshold · ~5 min

**Done when** the team has a one-minute count with the off rule at the *same* value as the on rule.
It should be clearly higher than the count they get in 5.2. There is no fixed expected number:
TEST-PLAN test E still owes a bench count.

**If stuck** A count of 0–2 means the hand is not crossing the threshold. Have one person watch the
value on the device page while another finds the height where it sits at the threshold, then waver
there.

#### 4.2 Separate the on and off thresholds · ~8 min

**Done when** the off threshold sits above the on-threshold and below the room reading, about a quarter of
the range above (82 / 6 / on 40 → off about 60). Self-check passes on all three: ≤ 2 switches in a
minute, cover → on, uncover → off.

**If stuck** The lamp never goes off: the off threshold is above the room reading. It still flickers:
widen the gap, and turn the LED so it does not shine onto the board's light sensor.

#### 4.3 Time window · 4.4 Lamp on when the time arrives · ~12 min tests, ~5 min fix

**Done when**

- *Traces answer:* the latest run stopped at the condition (the **And if** / Time box). The
  trigger fired but was blocked.
- *Predictions (added 16 Sep 2026, window 18:30–07:30):* dark **after** 18:30 → the lamp comes on
  (the crossing fires inside the window). Dark **before** 18:30 → it stays off: the crossing fired
  outside the window and was blocked, and nothing fires again at 18:30. The second answer is the
  reason 4.4 exists.
- *After the fix:* with the sensor covered before the start time, the lamp comes on at the start
  time (`s2.time.fixed` = ติด).
- *Why re-check light in And if:* the time trigger fires whether or not it is dark. Without the
  light condition the lamp would switch on at the start time in daylight.
- *Tick:* with the sensor kept covered, the lamp turns on at After and off at Before.

**If stuck** Traces shows no new run at all: nothing crossed. Uncover, set the relay Off, then cover
again. The timed test does nothing: the chosen times are already past. Both **After** and the
trigger's **At** must move to a future minute, and the same goes for Before and At on the off rule.
Home Assistant runs on Asia/Bangkok time, so read the laptop clock.

#### 4.5 Notification · ~4 min

**Done when** a message appears under the bell icon, bottom-left, when `มืด-เปิดไฟ` runs.

**If stuck** Covering does nothing now: the time window from 4.3 excludes the current time, so widen it.
*Send a notification via mobile_app* is missing from the list: it only appears after a phone
has logged in through the Companion app. Persistent notification is always available.

#### 4.6 Wire the pump, run it dry · ~8 min

**Done when** both lamp rules and the timer are off and the relay is Off *before* any screw is touched;
the LED's two leads are off the terminal block and the pump's leads sit on the same two points, + on the block terminal fed from **NO**, − on the negative terminal; the float sits in its glass
reading **Wet**; the pump has run dry on a 10-second command, heard and felt, and stopped on Off; and
the changeover time is written down. No hose, containers or tray: the pump runs dry all morning
(16 Sep 2026), so keep every run short. The 30 s cutoff that used to backstop this is built last in
Activity 5 since the 16 Sep reorder, so until then the only limit is the person watching the clock.
Session 3 uses it to tell lamp commands from pump commands on the relay's history graph.

**If stuck** Relay clicks, pump silent: the + lead went to a terminal fed from NC, or the − lead is not on the negative terminal, or
the controller's load pair is off (its load mode; tell the instructor). Pump runs with the relay Off: lead
on NC. The lamp turned the relay on during the swap: a lamp rule was left enabled. Nothing watches the
float yet, and the worksheet says so; the float rule is built in 6.1.

#### 4.7 Watering rules · ~12 min

**Done when** the pump-on threshold sits a little above room humidity; off threshold 5–10 % above that.
The pump does **not** start when the rule is saved. That is expected, because nothing crossed. Blowing on the board
pushes humidity past the off threshold; when blowing stops and it falls back below the on
threshold, the pump starts. How long that takes depends on the room; the worksheet stopped timing it
on 16 Sep 2026 (Roger), so there is no number to record.

**If stuck** The pump never restarts after blowing: the on-threshold is below the
room reading, so the value never crosses it on the way down.

#### 4.8 Auto / Manual mode toggle · ~12 min

**Done when** a Toggle helper `Pump Auto Mode` exists, shows on a dashboard the team added
(**Overview (Legacy)**, any name, on the sidebar), and `รดน้ำ - เปิดปั๊ม` carries the condition
*Switch is on* for it. With the toggle off, the blow-and-wait test from 4.7 no longer starts the
pump while the relay's device page still runs it; with the toggle on, the pump starts again
(`s2.mode.off` = ไม่เริ่ม, `s2.mode.on` = เริ่ม). Rebuilt by Roger on 16 Sep 2026 from "disable a
rule, run the pump by hand": the toggle gates automatic starting only. Manual still allows the
humidity stop rule and every protection rule to operate; switching the toggle off does not stop a
running pump or isolate power. Switching it on while humidity is already below the threshold does
not start the pump until a new crossing occurs. The Automations list ends as: `รดน้ำ - เปิดปั๊ม`,
`รดน้ำ - ปิดปั๊ม` **on**; `มืด-เปิดไฟ`, `สว่าง-ปิดไฟ` and `ปิดไฟตามเวลา` **off**; `Pump Auto Mode` **on**.

**If stuck** The toggle is not on the new dashboard: check the team picked **Overview (Legacy)**, which
lists every entity, and scroll. The default Overview of current Home Assistant releases does not show
helpers, which is the whole reason 4.8 adds the legacy dashboard. The condition search finds nothing: **Create** was
not pressed, so the helper does not exist. Only `รดน้ำ - เปิดปั๊ม` gets the condition; the fail-safes
built in Activity 5 must work in every mode, so they never check it. If a team also gated
`รดน้ำ - ปิดปั๊ม`, remove that condition so its behavior matches the worksheet's definition of Manual.

**Check this list at every table before the break.** Activity 5's sabotage rounds assume exactly
this state. A lamp rule left on switches the relay whenever the room light changes, and a timer rule left on
switches it off at the same minute every day. Those are the likeliest causes of a pump "running by
itself" or stopping unexplained in the failure lab.

#### End-of-activity question · ~3 min

**A good answer** gives the team's own on and off light thresholds. It says that one shared value makes
the output flicker whenever the reading hovers at it, and that watering applies the same fix: the
off threshold is set 5–10 % above the on threshold.

### Session 2 · Activity 5 — Failure lab (50 min)

Every problem runs the same three steps: the paired team sabotages, our team fixes, the paired
team sabotages again. While being sabotaged, the team watches **only its Home Assistant screen**. **Required:**
all four problems seen, fixed and re-tested — nothing is optional since 16 Sep 2026, and the
instructor decides live whether a slow table drops one. Four problems in 50 min is tighter than the
old three-required shape, so watch the clock at problem 2 and keep 5.5 to a read-and-answer. Pairing
is explained live, not in the worksheet.

#### Before every problem

**Done when** both watering rules are on, `Pump Auto Mode` is on, both lamp rules and the timer are
off, the float sits in its glass reading Wet, both boards show values, and the two device pages are open in separate tabs.
No float rule exists yet; problem 1 builds it.

**If stuck** A pump started by hand keeps running because the room never reaches the off threshold. That is
expected; do not let teams change the humidity thresholds to make the pump run.

#### 5.1 Problem 1 — water gone, pump still starts (Fail-safe 1)

**Done when** the sabotage (float lifted until Dry, then the pump commanded On from the board's button or the device page) runs the pump
with nothing stopping it, because no rule looks at the float at all. After the fix, `Fail-safe - น้ำหมด`
(two triggers, one condition, two actions) stops the pump within about a second, with a notification,
whether started from the button or the device page, and lifting the float mid-run stops it too.

**If stuck** The first trigger is *float → Dry* (state, not numeric). The second trigger must be *pump switch → On* with the condition *float → Dry*. The watering
rule's condition is *float → **Wet***, not "not Dry": a cut wire reads Dry and an offline board reads
unavailable, and neither is Wet.

#### 5.2 Problem 2 — commanded but not running (Fail-safe 4)

**Done when** with the pump lead unscrewed from NO, the relay clicks and the screen says On but the pump is
silent and still. After the fix the switch turns itself off within 15 s. With the lead back, the pump runs past
15 s. Moved here from fourth place on 16 Sep 2026 (Roger: unscrewing a lead is a real sabotage act, and
the wait-and-watch problem should not come second).

**If stuck** The rule cuts a pump that *is* running: the sensor board is not touching the pump, or
`ความไวตรวจจับปั๊ม` is too low, so set it to high. The 15 s is deliberately shorter than the 30 s
run-time cutoff built in 5.4, so the two rules can be told apart — but that cutoff does not exist yet at
this point, which is fine: nothing else competes to stop the pump here.

#### 5.3 Problem 3 — sensor board off (Fail-safe 3)

**Done when** the team has chosen open, close or hold, with a reason; *off* is the defensible choice for
a pump. When the board is switched off, its entities go unavailable while the pump runs on. After the
fix, the Traces page of `Fail-safe - เซนเซอร์หาย` shows a run when humidity went unavailable, with the Off and the notification. Judge by Traces, not by which rule stopped the pump (15 Sep 2026). Since the reorder of 16 Sep 2026 the 30 s cutoff does not exist yet, so this round is cleaner than it was: with the board off, `ปั๊มกำลังทำงาน` reads unavailable rather than Off, so 5.2's rule does not fire either, and nothing but the new rule stops the pump.

**If stuck** Pulling USB does nothing because the 18650 cell keeps the board alive, so use the board's
**ON/OFF switch**. If the pump stopped at about 15 s, that was `Fail-safe - สั่งแล้วไม่เดิน` reading the
pump as not running; the sensor-lost rule still counts as working when its Trace shows a run.

#### 5.4 Problem 4 — pump never stops (Fail-safe 2)

**Done when** a pump started by hand and left alone runs on, and after the fix it stops by itself at about
30 s with a notification. It runs last since 16 Sep 2026, because there is nothing for the paired team to
sabotage here — they start the pump and wait — and that makes a weak second round.

**If stuck** The trigger needs **For** 30 seconds on *pump → On*. After the cutoff the pump does not
come back by itself; that is by design, and it is why the notification matters. **The sabotage is cut at
about 15 s instead:** `Fail-safe - สั่งแล้วไม่เดิน` from 5.2 decided the pump is not running, so fix the
board's placement or raise `ความไวตรวจจับปั๊ม` before trying again.

#### 5.5 Maintenance plan · ~5 min

**Done when** all five rows carry a named person, a frequency and a thing to check. Moved here from
the debrief on 16 Sep 2026 so Activity 5 ends on something the group writes, not a table it reads.
A good row is concrete: the float gets lifted and wiped weekly by whoever feeds the fish; the pump
strainer is cleared monthly; someone notices within a day when the network or Home Assistant is
down, because nothing else will tell them. Weak rows say "everyone" and "sometimes".

**If stuck** Start from the four problems just staged: each one names a part that failed and a
person who had to intervene.

**The limits table left the worksheet on 16 Sep 2026** with the laptop-off-WiFi round; both were
reading, not doing. The end-of-activity question still asks the question the table answered, and
the model answer below carries the table for you. The WiFi-off demonstration still works for a
table that finishes early: No team now *sees* the pump run on with
every fail-safe silent; they read it off the last row of this table instead. If a table finishes
early and asks, the demonstration still works: pump On, laptop WiFi off, watch for up to 40 s with
someone at the pump, then stop it with the relay board's **button before** WiFi comes back — the Off
that Fail-safe 2 tried to send while the link was down failed and is not retried, so waiting for a
rule after reconnecting leaves the pump running.

#### End-of-activity question

**A good answer** says no: every fail-safe lives in Home Assistant, so they all stop with it.
Real safety needs something that works without it: a float wired to cut pump power directly, a
**A good answer** says no: every fail-safe lives in Home Assistant, so they all stop with it.
Real safety needs something that works without it: a float wired to cut pump power directly, a
limit built into the board's own firmware, and a manual Auto / Off / Manual switch. Since 16 Sep
2026 the worksheet no longer prints the limits table, so this is the facilitator's copy of it:

| Failure | What Home Assistant sees | What stops the pump |
|---|---|---|
| Float wire cut, or float stuck down | float **Dry** | น้ำหมด rule (stops a pump that may still have water: safe, but someone must go and look) |
| Float stuck floating (algae, tank wall) | float still **Wet** with the tank empty | น้ำหมด rule cannot see it; the 30 s cutoff still cuts each run; the float needs checking |
| Tank already empty, pump started from the device page or the board button | switch On while float **Dry** | น้ำหมด rule, second trigger |
| GoGo-IoT switched off, cell flat, or off WiFi | every entity of the board **unavailable** | เซนเซอร์หาย rule, or the cutoff; the watering rule cannot start a new run without Wet |
| Commanded On, pump does not run | switch On, `pump running` Off | สั่งแล้วไม่เดิน rule |
| Pump runs abnormally long, any cause | switch On too long | จำกัดเวลา rule |
| Laptop off WiFi, or Home Assistant down | it cannot see or command the pump | **nothing** — the pump stays in its last state |

#### Wrap-up · ~10 min

**Done when** every table has walked the lunch checklist: **the VM stays running** (Session 3's
history block reads this morning), `รดน้ำ - เปิดปั๊ม` is off and the relay is Off so a dry pump cannot
run unattended, both boards keep power, answers downloaded. The five learning points are read, not
taught. The worksheet no longer scripts a debrief discussion or the control-box demo (Roger, 16 Sep
2026: instructor-run, may not happen as written).

**The control-box demo, when you run it.** A real Auto / Off / Manual pump box wired to the
instructor kit: flip it while the watering automation runs and the pump obeys the switch, not Home
Assistant. Then one layer down: with Home Assistant shut down, the relay board's own button still
toggles the relay (bench-verified), an override that lives in the board rather than the wiring. It
is the answer to the end-of-activity question and links back to the Session 1 seed; it needs no
worksheet item.

### Session 3 · Activity 6 — Reading the recorded data (20 min)

#### Before start (ก่อนเริ่ม) · ~3 min

**Done when** the four worksheet checks at the top of Activity 6 are ticked (added 20 Sep 2026; they
report to the dashboard as one activity, like Session 2's): Home Assistant is reachable, both boards
are online and the relay still switches, `รดน้ำ - เปิดปั๊ม` is back **on** after the lunch shutdown
with every fail-safe on, and `Pump Auto Mode` is left **off** for the afternoon. Session 2's wrap-up
disabled the watering rule so a dry pump could not run unattended over lunch; nothing turned it back
on before this was added, so Activity 7's `โหมดรดน้ำอัตโนมัติ` tile had no live rule behind it and
Activity 8's pack-up asked teams to switch off rules that were never switched on.

**Why `Pump Auto Mode` stays off.** With the rule enabled and the toggle on, the pump-on threshold
sits just above room humidity (4.7), so every table would run the dry pump in 30-second bursts (the
cutoff from 5.4) for the rest of the afternoon. Off, the rule is complete and inspectable, the
dashboard tile reads Manual, and a team can still drive the pump by hand from its own tile. If you
want the pump live — for a demo, or to let a table watch Auto work — turn the toggle on at that
table and back off afterwards.

**If stuck** Home Assistant will not open: the VM's IP may have changed over lunch, so read it off
the VM screen again. The rule list is **Settings → Automations & scenes**.

#### Open the history

**Done when** History shows humidity, light and the relay switch from the start of Session 2 until now.

**If stuck** Check the selected time range first. A VM shutdown or restart keeps the history (the
recorder stores it in its database) but leaves a gap while it was off; only a rebuilt VM has none.
A team with too little data reads the instructor's projected sample or a neighbour's screen, says
so in its answer, and carries on.

#### Three points on the graph

**Done when** each point has what was seen, a time, what the team was doing, and what a farm would check.
Any three the team can explain are fine; graphs differ between teams.

**If stuck** A relay bar that is On is a **command**, not a running pump. Before the recorded changeover time
(`s2.pump_back_t`), from Session 1 until 4.6, it was driving the lamp. Only vibration shows the pump actually ran.

#### Values the graph always gives

**Done when** the lowest and highest humidity since Session 2 are written down, each with its time.

#### The question the graph cannot answer

**A good answer** says there is no data from the break after Session 1 because the laptop running Home Assistant (the
recorder) was closed or taken away; the board kept measuring, but nobody recorded it. A farm needs
a machine that stays on, with power through the night. This feeds the power step in Activity 8.

### Session 3 · Activity 7 — Dashboard (35 min)

Plan 5 · build 25 · test with someone else 5.

#### 7.1 Who will use it · 7.2 What to show and control

**Done when** the group has named who will use the dashboard (one or several: owner on a phone, worker on a tablet, manager on a big screen).
There are three values to *show* and two things to *control*, written in plain words the user understands
("air humidity", "is the water up to the float?", "start the pump").

#### 7.3 Build

**Done when** the four minimum cards are on a new blank dashboard (the Activity 4 Farm Dashboard is auto-generated and not editable): humidity **Gauge**, float **Tile** named for the
user (the worksheet suggests `ระดับน้ำที่ลูกลอย`), pump **Tile** (`สั่งปั๊ม`), and a **Tile** for `Pump Auto Mode` named so that On reads as Auto
(the worksheet suggests `โหมดรดน้ำอัตโนมัติ`). History graph, severity colours and extra cards are optional and come only after that.

#### 7.4 Someone else tries it

**Done when** someone who did not build the dashboard (a member of the paired team, or a teammate who took no part) answers all
four questions within 30 seconds on a phone: what is the humidity, is the water up to the float,
where is the pump control, is it in Auto or Manual now.

**If stuck** The phone must be on the zone WiFi and use the VM's IP. The new dashboard is in the left menu
under the name the team gave it, not under *Overview*.

#### End-of-activity question

**A good answer** names the question the tester struggled with and the specific change made:
moving a card up, renaming a tile, adding a colour.

### Session 3 · Activity 8 — Design challenge (85 min)

Pick 5 · network 20 · power 15 · design 30 · presentation and exchange 15 (instructor-led). Since 18 Sep 2026
there is no separate design canvas: the design is the four blocks of worksheet step 8.6 (sensor and actuator,
connectivity, power, test plan), filled in the worksheet and mirrored in the record sheet.

#### 8.1 Pick the scenario

**Done when** a scenario is written down (A–E; the worksheet calls them โจทย์, not cards, since 18 Sep 2026) and the farm and its problem are written in 8.1. Recommend **E** (a member's own farm) when one exists. C and D are advanced; teams
choosing them may put the specialist parts under "not sure yet".

#### 8.2 Choose the farm network

**Done when** both links have a distance, whether the far end has power, what was eliminated and why, and what
remains. The instructor models scenario B on screen (400 m, no mains: WiFi and Zigbee out on distance,
cellular out on power; ESP-NOW, LoRa and RS-485 remain). The two rows in 8.2 are filled from the
survivors, with a reason.

**If stuck** The weak answer is "WiFi, because the workshop used WiFi". Ask for the distance and the power
at the far end first.

The worksheet's table carries range figures again since 18 Sep 2026 (Roger: show range, benefits and
limitations), with power draw, benefits, limits and cost per option: WiFi about 30–50 m from the router in
the open, ESP-NOW 100–200 m board to board, Zigbee 10–30 m per hop, LoRa 1–10 km, RS-485 up to about
1 km of cable, cellular wherever there is signal. General estimates; กำพล to confirm against what they teach.

#### 8.3 Remote access and the cloud · instructor talk, listen only

Rewritten 18 Sep 2026 (Roger): no task in the worksheet; the team listens and ticks three boxes to say
it has understood. Make the three points in this order, in the words on the worksheet:

1. **As built, the system is reachable only on the local network.** A phone or computer that wants the
   dashboard must be on the same WiFi as Home Assistant.
2. **Remote access needs an additional access method.** Nabu Casa's paid Home Assistant Cloud is the
   example taught here; a VPN into the farm network is another route. Consumer ecosystems such as Tuya
   and Xiaomi have vendor cloud services with features and charges that depend on the service.
   Home Assistant itself stays on a machine in the farm because it must
   reach the boards and any Zigbee or LoRa receiver locally; never present a cloud-hosted Home Assistant
   as an option. Other approaches (pushing a copy of the data to a cloud platform, port forwarding or a
   tunnel) exist; mention them only if asked, with the warning that a badly set up door exposes the farm.
   The worksheet links nabucasa.com. If asked for smart-farm or IoT platforms that come with a cloud: in
   Thailand, NECTEC's NETPIE (netpie.io, a general IoT platform with a free tier) and HandySense
   (handysense.io, NECTEC's open smart-farm kit and cloud); maker clouds such as Blynk, ThingSpeak and
   Arduino Cloud; consumer device clouds such as Tuya / Smart Life, Xiaomi Mi Home and Sonoff eWeLink;
   irrigation-vendor clouds such as Netafim NetBeat. All of them decide or display in the vendor's cloud,
   so point 3 applies to every one of them.
3. **Our Home Assistant keeps running its local rules when the internet is down;** cloud-only products
   do not. A team that adopts a cloud-only product must give its critical parts a fail-safe of their own.

**Demo, optional, instructor kit** Open **Settings → Home Assistant Cloud**, show the **Remote access**
switch and the address. Phone off WiFi, on mobile data, opens the same dashboard the room saw on the zone
WiFi. Blow on the board, watch the value change on the phone, send one pump command. Point out that the
farm's Home Assistant still decided and recorded; the cloud only carried the connection.

**Done when** all three boxes are ticked and the team can restate point 3 in its own words: with the
internet down, automations, the dashboard on the farm WiFi and logging carry on, while remote viewing and
notifications stop; with Home Assistant down, automations, logging and the dashboard all stop, and only
protection in the board or the wiring, and the manual switch, remain. The team writes its remote-access
choice in 8.6, third communication row; "not needed" is a valid answer.

#### 8.4 Choose a battery for solar

Rewritten 18 Sep 2026 (Roger: focus on the battery types used with solar and how to choose). The box
tour is one step; the controller-settings and LCD-icon steps were cut later the same day as a distraction,
replaced by two sentences and two diagrams: what the controller does and that it must support the battery
type in use; a 220 V AC load needs an inverter. Nothing to do there, just read.

**Done when** the team can say which battery type fits its scenario and why, in this order: does
anything run at night; how many Wh per night and the usable share (about half for lead-acid, 80–90 %
for LiFePO4); who maintains it; first cost against lifetime; weight, place and heat. Nobody touches the
controller's menu: it stays on **b01** (lead-acid), because the adapter is not a battery.

The worksheet's figures are general estimates (cycle life, usable depth of discharge, relative price); กำพล to confirm against what they teach and current Thai prices. Talking points:
LiFePO4 costs 2–3× per Ah but gives 5–10× the cycles, so it is cheaper per cycle and needs no care;
lead-acid still wins for a one-off low budget or where a local shop can service it; NMC (18650,
power banks, EV cells) suits small or portable gear, not a fixed farm install; NiMH only in garden
lamps; sodium-ion is arriving but not yet common. If asked why the type matters to the controller: each type has its own charge voltages, so the
controller has a battery-type setting; lead-acid equalisation would overcharge lithium, gel dries out at
flooded voltages, and LiFePO4 must not be charged below 0 °C. The LCD icon reads not full on the 12.0 V
adapter because a full lead-acid sits at 12.7–13.0 V; the controller judges only from voltage.

**If stuck** Ask two questions first: does anything have to run at night, and will anyone come to top
up water? The answers usually settle the type before price does.

#### 8.5 Work out the power, then choose the source

Rewritten 18 Sep 2026 (Roger): the worksheet now opens with the four calculation steps and two worked
examples; the kit-load table and the folded answer table are gone.

**Done when** the team can run the four steps on its own main load and say which source it leads to:
W = V × A from the label; Wh per day = W × hours; battery at least that much, converted with Ah = Wh ÷ 12
and grossed up for the usable share (about half for lead-acid, 80–90 % for LiFePO4); panels sized for the
worst day, 3 full-sun hours, with W of panel = Wh per day ÷ 3, rounded up to whole panels.

The two examples on the worksheet, in case a team gets a different number: LED 50 W × 8 h at night =
400 Wh, so about 33 Ah usable at 12 V (lead-acid about 70 Ah rated, LiFePO4 about 40 Ah) and 133 W of
panel, one 150 W panel or nine of the kit's 15 W. Pump 1,100 W × 2 h = 2,200 Wh, so about 183 Ah usable
(lead-acid about 370 Ah, LiFePO4 about 220 Ah) and 733 W of panel, five 150 W panels. The pump example
makes the point: run a big pump in daylight straight from the panels and store water, not electricity,
with panels that can deliver more than 1,100 W while it runs and a tank that covers cloudy days.

Kit loads, if a team asks for closer numbers: sensor board 0.5 W × 24 h = 12 Wh per day, one small panel,
a night is 6 Wh which the board's 18650 covers; router plus Home Assistant host 10 W × 24 h = 240 Wh,
about 20 Ah at 12 V for a night; kit pump 18 W × 2 h = 36 Wh, no battery if it runs in daylight.

**If stuck** Start from the label on the device: volts times amps. Then ask whether it runs at night.
Panels are rounded **up** to a whole panel.

#### End-of-block question

**A good answer** splits the team's own loads into daylight-only (pumps) and must-run-overnight
(sensors, network, controller). For three cloudy days it names the numbers needed: each load's
Wh per day, the usable battery capacity (about half the rated capacity for lead-acid), and what the
panels still produce under cloud.

#### 8.6 Design for one pilot point

**Done when** the four blocks read as one plan: a sensor and an actuator named, with a control rule and
a response to sensor/communication failure; the two local communication rows carried over from 8.2,
a remote-access choice informed by 8.3, and the battery/power answers from 8.4–8.5 consistent with the
parts chosen; and a test plan covering normal operation and the chosen failure case, with observable
pass criteria.
Unknowns are written into the block they belong to, not guessed.

#### Presentation and exchange · 15 min, instructor-led

Not in the worksheet since 18 Sep 2026 (Roger: the instructor directs it). Pair the teams. Each team tells
its plan in one minute from the four blocks: the problem, what senses and what acts, how it connects and is
powered, and how they will know it works. The other team has three minutes for two questions: which
decision is best reasoned, and what happens if one part fails. Swap. Teams change their answers in 8.6
directly; there is no separate revision box, no rubric walk and no plenary.

---

### Session 4 · Activity 9 — Reflash the plot board for ESP-NOW (30 min)

The Session 4 story, said once at the start: the plot is beyond WiFi range, so the GoGo board out
there will talk **ESP-NOW** — board to board, no router, further than WiFi — to a cheap board in
the farmhouse, which is the only thing Home Assistant sees. In the room the GoGo board keeps its
WiFi so both paths can be compared; say explicitly that at a real plot it would not have one.

#### Before start (ก่อนเริ่ม) · ~5 min

**Done when** the five checks at the top of Activity 9 are ticked: kit powered, float in its glass,
Home Assistant reachable, both boards online, **every relay-driving rule off** and `Pump Auto Mode`
off (the pump is not used this session), and the team has its receiver devkit but has not plugged
it in. If Session 3 ended on another day, the kit is re-cabled first (Activity 8's closing list).

#### 9.1 Download and install

**Done when** the team has first seen the old image's log (name, IP, no `GOGO,` lines), then
web.esphome.io reports the install complete and the board reboots. The file is the zone's
`gogo-iot-espnow-<colour>.factory.bin` from the resources page; the pre-flashed sessions 1–3 image is
`gogo-iot-<colour>` and stays available for a board that must go back.

**If stuck** Chrome or Edge only. Close the old Logs window before Connect. The GoGo board must be
on the laptop's USB, not the charge controller's. **Wrong colour = board vanishes from Home
Assistant**; reflash with the right file. Do not tick "erase": it wipes the pump-sensitivity choice
for nothing.

#### 9.2 Read the log

**Done when** the team has `DEVICE NAME` unchanged from Activity 1 (`s4.tx.same` = เหมือนเดิม), an
`IP ADDRESS` line, and one `[espnow] >>> GOGO,…` line copied into the worksheet, and has watched
the light field (6th value) fall under a cupped hand. Walk the ten fields on the projector once.

**If stuck** No `>>>` lines: the board did not take the new image — check that the file name says `espnow`, reinstall. `nan`
in the first packets is normal. The name changing is not normal: it is derived from the MAC, so a
changed name means a different board was flashed.

#### 9.3 The two new diagnostics

**Done when** `ช่องสัญญาณ WiFi (channel)` is written down (`s4.tx.channel`) from the board's own page,
`แพ็กเก็ต ESP-NOW ที่ส่ง` is seen to climb, and Home Assistant shows the board back with the two
new diagnostic entities **without re-adoption**. Then the USB cable goes back to the charge
controller so the laptop is free for the receiver.

**A good answer** (end question) lists what the plot board loses without WiFi: its own web page, the
direct Home Assistant entities, OTA updates and the log over the network — and says the fix is to
configure it over USB (or via its fallback hotspot) at the house before carrying it out, or to add a
serial/USB visit to the maintenance table.

### Session 4 · Activity 10 — The receiver in the farmhouse (50 min)

#### 10.1 · 10.2 Flash the receiver, read its name and IP

**Done when** the devkit runs `farm-receiver-<colour>-xxxxxx`, the colour matches the zone, and name
and IP are in `board.rx.name` / `board.rx.ip`. The GoGo board must be powered from the charge
controller so only one serial port shows.

**If stuck** No port at Connect: another USB cable (charge-only cables are common), or hold BOOT while
plugging in. Installed but no log: the board's USB port is the other kind — this is the
`--receiver-console` choice from section 1 and a TA should know which was built. Some DevKitC boards
have two ports; try the other.

#### 10.3 Open the receiver's page and name the sender

**Done when** the team has typed the GoGo board's six-character suffix into `ชื่อบอร์ดที่แปลง`, sees
its full name under `บอร์ดที่รับข้อมูลอยู่`, `รับข้อมูลจากแปลง (link)` ON, values filled, and has
written the receiver's channel, an RSSI (about −30 to −50 dBm on the table) and one **other**
board's name from `บอร์ดอื่นที่ได้ยิน` — the evidence for the end question that the channel is public.

**If stuck, in this order** (1) the suffix — every character, from the GoGo board's real name;
(2) is the GoGo board sending — its own page's `แพ็กเก็ต ESP-NOW ที่ส่ง` climbs; (3) **do the two
boards show the same `ช่องสัญญาณ WiFi`?** If not they are on different access points; power-cycle
the receiver (or move it next to the GoGo board) until the channels agree. This is the one failure
the venue's network can cause and the TA should look for it first when a whole table is stuck.
`บอร์ดอื่นที่ได้ยิน` changing proves the receiver itself works.

#### 10.4 Prove it is our board

**Done when** a cupped hand on the GoGo board moves the receiver's light value within a few seconds
(`s4.rx.delay`, typically 3–5 s: one send interval on top of the Activity 1 figure) and lifting the
float flips the mirrored float switch. Two tabs, GoGo page and receiver page, should agree.

#### 10.5 Distance

**Done when** the GoGo board has been carried to the far end of the room on its 18650 cell (or a
power bank), the far RSSI and whether packets kept arriving are recorded, and `แพ็กเก็ตที่หาย` has
been read back at the table. Tell teams to stay inside the room: leave the WiFi and the board may
change channel while reconnecting. Flat cells are the likely snag — decide before the day whether
kits get charged cells or a power bank (TEST-PLAN test M).

**Point to make** ESP-NOW broadcasts are not acknowledged: what is lost is lost, which is why the
board resends every 3 s. Real range is 100–200 m in the open; the room shows the trend, not the limit.

#### 10.6 The plot goes quiet

**Done when** the team has switched the GoGo board off, watched the link go OFF and the values turn
`NaN` at about **15 s** (`s4.rx.off.sec`), and seen them return after the board rejoined WiFi.
Say the fail-safe sentence: the receiver would rather show *nothing* than a stale number.

**A good answer** (end question) names both halves — a neighbour's board could be mistaken for ours
(so filter by name or MAC), and a neighbour can read our values (so encrypt in a real deployment) —
and might add that a shared channel also carries the neighbour's traffic load.

### Session 4 · Activity 11 — The far plot in Home Assistant (45 min)

#### 11.1 Adopt the receiver

**Done when** the receiver is added by its IP with the name checked (same as Activity 3) and the
team has found its three entity groups: the ESP-NOW sensors plus the link (Connected /
Disconnected), the `sender name` text under Configuration, the link diagnostics.

#### 11.2 Two paths, one sensor

**Done when** humidity and light are written from both the GoGo device page and the receiver's
(`s4.ha.*.direct` / `.espnow`) and agree within one update, and a breath on the board moves both.

#### 11.3 Dashboard `แปลงไกล`

**Done when** a new blank dashboard holds the four cards from the receiver's entities — link
**Tile** on top (`การเชื่อมต่อกับแปลง`), humidity **Gauge**, float **Tile**, RSSI **Tile** — as in
Activity 7. The history graph comparing both humidity entities is optional and pleasing.

#### 11.4 Alert when the plot goes quiet

**Done when** `แปลงเงียบ - เตือน` exists — trigger: State of `รับข้อมูลจากแปลง (link)` To
*Disconnected* For 30 s; action: persistent notification — and switching the GoGo board off produces
the notification about 45 s later (`s4.ha.alert.ok`). This rule drives no relay and may stay on;
the pack-up list has it switched off only so a powered-down kit does not leave a stale alert.

**A good answer** (end question) has the plot board with no WiFi (a fixed ESP-NOW channel matching
the house router, set over USB before it goes out), on solar with a small battery, mounted high and
in line of sight; the receiver near the router and always powered; and names the link tile / the
notification as how the user knows a reading is current, not stale.

#### Wrap-up and kit return

Read the four summary points. The kit-return list moved here from Activity 8 on 20 Sep 2026 and now
includes the receiver and its cable; answers are downloaded and submitted at this point.

## Still missing

**Answer hand-in:** the destination is still to be decided (likely an upload form; confirmed with the
organizer on 19 Sep). Announce the actual destination before the final activity. Ask each recorder to
download the JSON file, check its team number, submit it, and keep a local copy. A TA checks that the
file was received and can be opened for that team; progress on the live board is not answer submission.
Publish the form link in the worksheet and front page once it is available. A printed record sheet
should be collected directly from teams using paper.

**Timed rehearsal:** run Activities 4, 5 and 7 with a novice-paced team before delivery. Record actual
durations, allow for fault recovery, and agree where TAs provide a prepared working setup to keep a
team moving. Check the real venue's zone WiFi, board discovery, VM/phone access, vibration detection,
and progress reporting. Prepare an instructor history graph for teams with insufficient data. Pump
run times must follow the verified limit of the actual model; see the
[readiness action plan](https://github.com/arnans/iot-training/blob/main/planning/WORKSHOP-READINESS-ACTIONS.md).

Nobody has produced these yet:

- The install-guide details participants need: VM login, file size, verification form, help channel
- Slide decks for Sessions 1–3 and the three post-tests
- Expected values that need a bench run: the Activity 4 flicker count (TEST-PLAN test E) and
  typical room readings for Activity 1
- **The LED-module bench check now gates Day 1** (TEST-PLAN test L): it lights through the relay from
  the 12 V rail, a reversed module is harmless, and a lit module 30 cm from the board does not lift
  the light reading over a covered-board threshold
- Real screenshots in the install guide (currently placeholders)
- Bench tests against the built firmware — see
  [TEST-PLAN.md](https://github.com/arnans/iot-training/blob/main/planning/TEST-PLAN.md) *(repo)*, especially
  test B (the boot banner participants read) and test G (float switch polarity)

---

*Building the images rather than using them? The firmware build and the 18-step OVA recipe are in
[firmware/README.md](https://github.com/arnans/iot-training/blob/main/firmware/README.md) and
[hass/README.md](https://github.com/arnans/iot-training/blob/main/hass/README.md) — both repo-only.*
