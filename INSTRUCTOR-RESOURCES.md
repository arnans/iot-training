# Instructor & TA resources

Every file and link needed to prepare for and run the workshop, in one place.
Participants get a trimmed version at
[รวมไฟล์และลิงก์](https://arnans.github.io/iot-training/renders/resources.html).

Links are absolute so this page works the same whether you read it in the repository or as the
published page at
[arnans.github.io/iot-training/instructor-resources.html](https://arnans.github.io/iot-training/instructor-resources.html).
Rows marked *(repo)* need access to the private `iot-training` repository.

---

## 1. Board firmware — six images

One image per board type, per zone colour. The zone colour is baked in: a red-zone image only
joins the red SSID. Built and verified 12 Sep 2026.

| Board | Red zone | Green zone | Blue zone |
|---|---|---|---|
| **GoGo-IoT sensor board** (ESP32-C3) | [gogo-iot-red.factory.bin](https://arnans.github.io/iot-training/firmware/gogo-iot-red.factory.bin) | [gogo-iot-green.factory.bin](https://arnans.github.io/iot-training/firmware/gogo-iot-green.factory.bin) | [gogo-iot-blue.factory.bin](https://arnans.github.io/iot-training/firmware/gogo-iot-blue.factory.bin) |
| **Relay board** (ESP32-C6-Relay_X1) | [gogo-relay-red.factory.bin](https://arnans.github.io/iot-training/firmware/gogo-relay-red.factory.bin) | [gogo-relay-green.factory.bin](https://arnans.github.io/iot-training/firmware/gogo-relay-green.factory.bin) | [gogo-relay-blue.factory.bin](https://arnans.github.io/iot-training/firmware/gogo-relay-blue.factory.bin) |

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
| Windows / Intel Mac | [Downloads](https://www.virtualbox.org/wiki/Downloads) | [`farm-workshop-x86-64.ova`](https://drive.google.com/file/d/1OdS3sBFBDT3OUg7olJJABfEBeRGMHrIW/view?usp=sharing) (Google Drive) |
| Apple Silicon Mac (M1+) | [Downloads](https://www.virtualbox.org/wiki/Downloads) | `farm-workshop-arm64.ova` — **not built yet** |

Import steps, settings and the login are in the participant guide:
**[เตรียมแล็ปท็อป](https://arnans.github.io/iot-training/renders/install.html)**. The two things
that go wrong: Adapter 1 must be **Bridged** and set to the laptop's own WiFi card, and the VM is
reached at `http://<its IP>` — never `homeassistant.local`, because every team's VM answers to
that name.

Login: `TODO` / `TODO` (also printed on each team card).

---

## 3. Worksheets and printed material

| What | Link |
|---|---|
| Participant site | <https://arnans.github.io/iot-training/> |
| Before the workshop — เตรียมแล็ปท็อป | [install.html](https://arnans.github.io/iot-training/renders/install.html) |
| Session 1 — รับรู้ ตัดสินใจ สั่งการ | [session-1.html](https://arnans.github.io/iot-training/renders/session-1.html) |
| Session 2 — ควบคุมอัตโนมัติและ Fail-safe | [session-2.html](https://arnans.github.io/iot-training/renders/session-2.html) |
| Session 3 — แดชบอร์ดและออกแบบระบบ | [session-3.html](https://arnans.github.io/iot-training/renders/session-3.html) |
| Participant file & link list | [resources.html](https://arnans.github.io/iot-training/renders/resources.html) |
| Team record sheet + design canvas — **the one thing that gets printed** | [record-sheet.md](https://github.com/arnans/iot-training/blob/main/docs/record-sheet.md) *(repo)* |
| Home Assistant menu paths + troubleshooting — **keep this open while roving** | [reference.md](https://github.com/arnans/iot-training/blob/main/docs/reference.md) *(repo)* |

The `renders/` pages are self-contained: open one once and it keeps working with no internet.

---

## 4. Preparing to teach

| What | Link |
|---|---|
| What happens in each session, and why | [SESSION-OVERVIEW.md](https://github.com/arnans/iot-training/blob/main/SESSION-OVERVIEW.md) *(repo)* |
| Full course design — timings, kit list, risks, open decisions | [COURSE-DESIGN.md](https://github.com/arnans/iot-training/blob/main/COURSE-DESIGN.md) *(repo)* |
| Known gaps and assumptions in the worksheets | [WORKSHEET-TODO.md](https://github.com/arnans/iot-training/blob/main/WORKSHEET-TODO.md) *(repo)* |
| Network spec to hand the venue's provider — Thai | [network-requirements.html](https://arnans.github.io/iot-training/network-requirements.html) |
| Network spec — English | [network-requirements-en.html](https://arnans.github.io/iot-training/network-requirements-en.html) |

**Instructor kit** — a spare laptop mirroring a team kit, projected. It also rescues a team whose
laptop dies. Three things teams don't have: the **Auto / Off / Manual pump control box** for the
Session 2 debrief, a Home Assistant Cloud account for the Session 3 remote-access demo, and a saved
morning history graph for teams that shut their VM down at lunch.

**Kit prep, the two that fail silently:** flip the float cylinder on its rod so it closes when wet
(otherwise a cut wire reads "water present" and a pump can run dry), and colour-code board, kit and
team card as one matching set.

---

## 5. Tools and external links

| Tool | Used for |
|---|---|
| <https://web.esphome.io> | Flashing boards and reading a board's name from its USB log. Chrome or Edge only |
| <https://www.home-assistant.io/docs/> | Home Assistant reference |
| <https://esphome.io/> | ESPHome reference |
| [github.com/arnans/gogo-iot-node](https://github.com/arnans/gogo-iot-node) | GoGo-IoT sensor board hardware |

---

## 6. Running the activities

Each activity in the worksheet opens with a checklist for the team, **สิ่งที่ทีมต้องทำและตอบ**: one item
per sub-section, holding the question and its answer boxes, with a link down to the steps. This
section follows the same items, so a TA looking at a team's screen can find the matching entry
here. Each item gives **Done when** (what a finished answer looks like) and **If stuck** (what to
check first). Minutes are the design estimate, not a rehearsed timing.

**How to run it.** Project the checklist and talk through it one item at a time; teams work down
it while you talk. The prose under each item is for the team that falls behind or wants the reason.

The two new questions added with the checklists, `s1.box.pos` and `s2.fs.none`, and the two
from the Activity 5 pilot, `s2.time.trace` and `s2.time.why`, are on the record sheet like every
other answer.

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
is knocked. The float reads **ON** floating and **OFF** lifted. The light value changes within
about one to two seconds, because the board sends it roughly once a second. Session 2 uses the
room and covered light numbers to set its thresholds.

**If stuck** Humidity barely moves: breathe slowly for the full five seconds, close to the board. The float
never changes: the lead is not in port 1.

#### End-of-activity question

**A good answer** says humidity decides watering (standing in for soil moisture on a real farm), and
the float tells whether the reservoir still has enough water for the pump. It only says yes or no,
not how much.

### Session 1 · Activity 2 — Act (40 min)

Teams leave with the 12 V pump circuit wired by their own hands, the relay board powered from the
charge controller's USB, and water recirculating in container A.

#### 2.1 Know the relay board

**Done when** every member can point at **COM** and **NO** (used) and at **7-60 Input / GND** (never
used) on the real board.

#### 2.1 Read name and IP, click the relay

**Done when** a `gogo-relay-<colour>-…` name and IP are written down. The relay clicks from the web page
switch and from the board's own button. The USB lead is then unplugged from the laptop, but left
in the board.

**If stuck** Same as 1.2. The **LED** blinking means no WiFi; a steady LED means connected.

#### 2.2 The 12 V supply box

**Done when** the team can find the middle pair (battery symbol, where the adapter goes), the right pair
(lamp symbol, the 12 V output) and the two USB ports.

#### 2.2 Wire it

**Done when** all six steps are done and a second person has checked every screw. No bare ends touch, no
wire is in **NC** or **7-60 Input / GND**, and the adapter is still unplugged.

**If stuck** Check for a wire on NC instead of NO (the pump then runs whenever the relay is Off), and for the
load pair and the battery pair swapped.

#### 2.2 Power on and run the pump

**Done when** the charge controller screen shows about 12 V. The relay board lights and rejoins WiFi. The
pump moves water from A to B on command, and the hose is then moved back into A.

**If stuck** Screen dark: unplug first, then check the adapter is on the middle pair, red to plus. Screen on
but the relay board is dark: reseat its USB lead or try the other port. The page will not open after
a minute: move the relay board's USB lead to the laptop briefly to read a new IP (the relay
restarts Off), then move it back.

#### 2.2 The farm pump control box

**Done when** the answer is **Manual**. Auto is the controller in charge, Off is maintenance or a leak,
and Manual is a person running the pump when sensors or the network have failed.

#### End-of-activity question

**A good answer** says a 220 V pump needs a relay or contactor rated for the pump's AC current,
including its start-up surge. It also needs 220 V-rated wiring, an enclosure and protection
(breaker, RCD), and an electrician to wire it, not the team.
**Before the break** every relay is Off and every pump has stopped.

### Session 1 · Activity 3 — Logic (40 min)

Teams leave with both boards in their own Home Assistant and a "be the Logic yourself" round. They
also leave with the first automation, `น้ำหมด หยุดปั๊ม`, passing 3 of 3.

#### 3.1 Add both boards

**Done when** both boards are added from the discovered cards, the last six characters match the names
written down, and both devices are renamed for the team.

**If stuck** Every team in the zone sees every card. **Adding a neighbour's card looks like success**, but
the team then watches the neighbour's sensors and its automation drives the neighbour's pump. Check
the six characters before adding. No card at all: *+ Add integration → ESPHome → Add device → Setup
another instance of ESPHome*, then type the board name without `.local`.

#### 3.2 Current values, history, phone

**Done when** the humidity history graph opens, and the relay toggles from the laptop and from a phone,
with both screens agreeing.

**If stuck** The phone must be on the zone WiFi, not mobile data, and must use the IP from the VM screen,
never `homeassistant.local`. If it still fails, skip this step and flag it to a TA; the rest of the activity
does not need the phone.

#### 3.3 Be the Logic yourself

**Done when** the humidity threshold sits 2–3 % above the room reading, so room air counts as "dry" and
breath counts as "wet enough". There is a count of correct decisions in five minutes, and a number
of seconds from lifting the float to the pump stopping.

*Rules:* humidity: "if humidity is below the threshold, turn the pump on"; float: "if the
float reads no water (Dry), turn the pump off".

#### 3.4 First automation: float Dry → pump off

**Done when** the pump stops by itself three times out of three when the float is lifted. Putting the float
back does not restart the pump, and that is expected.

**If stuck** The automation is switched off, the trigger's **To** is not **Dry**, or the trigger or action
points at the neighbour's entity.

#### End-of-activity question

**A good answer** says the pump runs. The trigger fires only when the float *changes* to Dry, and a
float already Dry never changes. Leave it open: it is problem 1 of the Session 2 failure lab.

### Session 1 · Activity 4 — Spec (15 min)

Paper only. Never skipped: under 15 minutes left, run the short form (relay and pump only, one
card, one pass/fail).

#### 4.1 Sensor and float specs

**Done when** the humidity and temperature accuracy and the float's current and voltage rating are copied
from the handout. The humidity sensor on the board is a GXHT30C (SHT3x-compatible).

#### 4.1 Relay and pump specs

**Done when** the relay's printed ratings are read off the blue relay itself: `10A 30VDC` and `10A 250VAC`.
The pump current comes from its spec, 18 W at 12 V, which is 1.5 A.

**If stuck** Check the comparison uses the DC rating: our pump circuit is 12 V DC.

#### 4.2 Compare with the card

**Done when** each of the card's demands sits next to what the kit offers, with a pass or fail, and a failed card names the one
part to change. The card set is built so one card exceeds the sensor accuracy (change the sensor),
one exceeds the relay rating (change the relay or add a contactor), and one passes.

#### End-of-activity question

**A good answer** names the spec line that decided it, not "it worked on the table". Close with
the five things to read on every spec: range, accuracy, interface, voltage and current, IP rating.

### Session 2 · Activity 5 — automations and hysteresis (75 min)

Teams leave with five automations: the float rule and two watering rules **on**, two garden-lamp
rules **off**. They also leave with their thresholds, two flicker counts and the written answer.
Keys go into the team's JSON as `s2.light.*`, `s2.chatter.*`, `s2.time.*`, `s2.hum.*`, `s2.q5`.

#### 5.2 Swap the pump for the lamp · ~5 min

**Done when** relay On lights the LED and relay Off darkens it. The float rule was switched off and
the relay set Off *before* any screw was touched.

**If stuck** The LED stays dark but the relay clicks: the red lead belongs on **NO** and the black lead on the
negative row. A reversed LED stays dark but is not damaged. The LED is lit while the relay shows Off:
the lead is on **NC**.

#### 5.3 Dark → lamp on · ~15 min

**Done when** the light readings from Session 1 have been re-checked (open and covered). The on-threshold
sits roughly halfway between them (82 and 6 → about 40). Covering the board lights the lamp.
Uncovering does **not** turn it off yet; that is expected, because no off rule exists.

**If stuck** Covering does nothing: the reading was already below the threshold when the rule was
saved. A crossing trigger needs the value to go above, then below again, so uncover, set the relay Off
and cover again. The board sends a light value about once a second, so hold the cover for two
seconds. Check that the trigger entity is `ความสว่าง (light)`.

#### 5.4 Lamp flickers near the threshold · ~5 min

**Done when** the team has a one-minute count with the off rule at the *same* value as the on rule.
It should be clearly higher than the count they get in 5.5. There is no fixed expected number:
TEST-PLAN test E still owes a bench count.

**If stuck** A count of 0–2 means the hand is not crossing the threshold. Have one person watch the
value on the device page while another finds the height where it sits at the threshold, then waver
there.

#### 5.5 Separate the on and off thresholds · ~8 min

**Done when** the off threshold sits above the on-threshold and below the room reading, about a quarter of
the range above (82 / 6 / on 40 → off about 60). Self-check passes on all three: ≤ 2 switches in a
minute, cover → on, uncover → off.

**If stuck** The lamp never goes off: the off threshold is above the room reading. It still flickers:
widen the gap, and turn the LED so it does not shine onto the board's light sensor.

#### 5.6 Time window, and "dark before the window opens" · ~12 min

**Done when**

- *Traces answer:* the latest run stopped at the condition (the **And if** / Time box). The
  trigger fired but was blocked.
- *Why re-check light in And if:* the time trigger fires whether or not it is dark. Without the
  light condition the lamp would switch on at the start time in daylight.
- *Tick:* with the sensor kept covered, the lamp turns on at After and off at Before.

**If stuck** Traces shows no new run at all: nothing crossed. Uncover, set the relay Off, then cover
again. The timed test does nothing: the chosen times are already past. Both **After** and the
trigger's **At** must move to a future minute, and the same goes for Before and At on the off rule.
Home Assistant runs on Asia/Bangkok time, so read the laptop clock.

#### 5.7 Notification · stretch

**Done when** a message appears under the bell icon, bottom-left, when `มืด-เปิดไฟ` runs.

**If stuck** Covering does nothing now: the time window from 5.6 excludes the current time, so widen it.
*Send a notification via mobile_app* is missing from the list: it only appears after a phone
has logged in through the Companion app. Persistent notification is always available.

#### 5.8 Back to watering · ~5 min rewiring, ~12 min rules

**Done when** both lamp rules are off, the relay is Off, the pump is back on NO, the float reads **Wet** and
only then the float rule is back on. The changeover time is written down; Session 3 uses it to tell
lamp commands from pump commands on the relay's history graph.

*Watering rules:* pump-on threshold a little above room humidity; off threshold 5–10 % above that.
The pump does **not** start when the rule is saved. That is expected, because nothing crossed. Blowing on the board
pushes humidity past the off threshold; when blowing stops and it falls back below the on
threshold, the pump starts. The restart time depends on the room, and any measured number is fine.

**If stuck** The pump stops the moment the float rule is re-enabled: the float read Dry, so seat it in
the water and check for Wet first. The pump never restarts after blowing: the on-threshold is below the
room reading, so the value never crosses it on the way down.

#### 5.9 Disable a rule, run the pump by hand · ~5 min

**Done when** with `รดน้ำ - เปิดปั๊ม` disabled and dry air, the pump stays still, but the relay's device
page still runs it. The Automations list ends as: `น้ำหมด หยุดปั๊ม`, `รดน้ำ - เปิดปั๊ม`,
`รดน้ำ - ปิดปั๊ม` **on**; `มืด-เปิดไฟ`, `สว่าง-ปิดไฟ` **off**.

**Check this list at every table before the break.** Activity 6's sabotage rounds assume exactly
this state. A lamp rule left on switches the relay whenever the room light changes. That is the likeliest
cause of a pump "running by itself" in the failure lab.

#### End-of-activity question · ~3 min

**A good answer** gives the team's own on and off light thresholds. It says that one shared value makes
the output flicker whenever the reading hovers at it, and that watering applies the same fix: the
off threshold is set 5–10 % above the on threshold.

### Session 2 · Activity 6 — Failure lab (45 min)

Every problem runs the same three steps: the paired team sabotages, our team fixes, the paired
team sabotages again. While being sabotaged, the team watches **only its Home Assistant screen**. **Required:**
problems 1, 2 and 5 seen, 1 and 2 fixed and re-tested. Problems 3 and 4 when time allows. Pairing
is explained live, not in the worksheet.

#### Before every problem

**Done when** the float rule and both watering rules are on, both lamp rules are off, both boards show
values, and the two device pages are open in separate tabs.

**If stuck** A pump started by hand keeps running because the room never reaches the off threshold. That is
expected; do not let teams change the humidity thresholds to make the pump run.

#### 6.1 Problem 1 — water gone, pump still starts (Fail-safe 1)

**Done when** the sabotage (float lifted until Dry, then the relay board's button pressed) runs the pump
with nothing stopping it. After the fix the pump stops within about a second, with a notification,
whether started from the button or the device page.

**If stuck** The second trigger must be *pump switch → On* with the condition *float → Dry*. The watering
rule's condition is *float → **Wet***, not "not Dry": a cut wire reads Dry and an offline board reads
unavailable, and neither is Wet.

#### 6.2 Problem 2 — pump never stops (Fail-safe 2)

**Done when** a pump started by hand and left alone runs on, and after the fix it stops by itself at about
30 s with a notification.

**If stuck** The trigger needs **For** 30 seconds on *pump → On*. After the cutoff the pump does not
come back by itself; that is by design, and it is why the notification matters.

#### 6.3 Problem 3 — sensor board off (Fail-safe 3) · when time allows

**Done when** the team has chosen open, close or hold, with a reason; *off* is the defensible choice for
a pump. When the board is switched off, its entities go unavailable while the pump runs on. After the
fix the pump stops **before** 30 s, with the `Fail-safe - เซนเซอร์หาย` notification.

**If stuck** Pulling USB does nothing because the 18650 cell keeps the board alive, so use the board's
**ON/OFF switch**. If the pump stopped at 30 s, that was Fail-safe 2, not this rule; check which
notification appeared, or open Traces. Restart the pump before re-testing so the 30 s timer starts
fresh.

#### 6.4 Problem 4 — commanded but not running (Fail-safe 4) · when time allows

**Done when** with the pump lead unscrewed from NO, the relay clicks and the screen says On but no water
flows. After the fix the switch turns itself off within 15 s. With the lead back, the pump runs past
15 s.

**If stuck** The rule cuts a pump that *is* running: the sensor board is not touching the pump, or
`ความไวตรวจจับปั๊ม` is too low, so set it to high. The 15 s is deliberately shorter than Fail-safe 2
so the two rules can be told apart.

#### 6.5 Problem 5 — laptop off WiFi

**Done when** the team has seen the pump run on with every fail-safe silent. There is no fix inside Home
Assistant. When WiFi comes back, Fail-safe 2 cuts the pump at once.

#### 6.6 Which rule stops which problem

**Done when** the "no rule" answer names two cases: a float stuck floating (reads Wet with the tank
empty) and the laptop or Home Assistant down or off WiFi. The self-check (1, 2, 5 seen; 1, 2 fixed)
is ticked.

#### End-of-activity question

**A good answer** says no: every fail-safe lives in Home Assistant, so they all stop with it.
Real safety needs something that works without it: a float wired to cut pump power directly, a
limit built into the board's own firmware, and a manual Auto / Off / Manual switch. The
control-box demo in the debrief answers this.

### Session 3 · Reading the recorded data (20 min)

#### Open the history

**Done when** History shows humidity, light and the relay switch from the start of Session 2 until now.

**If stuck** A team whose VM was shut down or restarted has no Session 2 data. Point them at the
instructor's projected sample graph or a neighbour's screen; they carry on as normal.

#### Three points on the graph

**Done when** each point has what was seen, a time, what the team was doing, and what a farm would check.
Any three the team can explain are fine; graphs differ between teams.

**If stuck** A relay bar that is On is a **command**, not a running pump. Before the recorded changeover time
(`s2.pump_back_t`) it was driving the lamp. Only vibration shows the pump actually ran.

#### Values the graph always gives

**Done when** the lowest and highest humidity since Session 2 are written down, each with its time.

#### The question the graph cannot answer

**A good answer** says there is no data from the break after Session 1 because the laptop running Home Assistant (the
recorder) was closed or taken away; the board kept measuring, but nobody recorded it. A farm needs
a machine that stays on, with power through the night. This feeds the power step in Activity 8.

### Session 3 · Activity 7 — Dashboard (35 min)

Plan 5 · build 25 · test with someone else 5.

#### 7.1 The user, and what they see and control

**Done when** one named user is chosen (owner on a phone, worker on a tablet, manager on a big screen).
There are three things the user must *see* and two they must *control*, written in the user's words
("is the air dry?", "is there water in the tank?"), not entity names.

#### 7.2 Build

**Done when** the four minimum cards are on the dashboard: humidity **Gauge**, float **Tile** named for the
user (such as `น้ำในถัง`), pump **Tile**, and an **Entities** card listing the automations. History graph,
severity colours and icons come only after that.

#### 7.3 Someone else tries it

**Done when** someone who did not build the dashboard (a member of the paired team, or a teammate who took no part) answers all
three questions within 30 seconds on a phone: is the air dry, is there water in the tank, where is
the pump button.

**If stuck** The phone must be on the zone WiFi and use the VM's IP. The new dashboard is in the left menu
under the name the team gave it, not under *Overview*.

#### End-of-activity question

**A good answer** names the question the tester struggled with and the specific change made:
moving a card up, renaming a tile, adding a colour.

### Session 3 · Activity 8 — Design challenge (85 min)

Pick 5 · network 20 · power 15 · fill the canvas 30 · exchange 10 · revise 5. The design canvas
itself is at the end of the team record sheet; the checklist holds the decision steps.

#### 8.1 Pick the scenario

**Done when** a scenario is written down (card A–E) and the farm and its problem are written at the
top of the canvas. Recommend **E** (a member's own farm) when one exists. C and D are advanced; teams
choosing them may put the specialist parts under "not sure yet".

#### 8.2 The network we already use

**Done when** the team has found `ssid`, `name_add_mac_suffix` and `api` in the ESPHome file, and has opened the board's page
from the IP entity Home Assistant shows. There is no fixed IP in the file: the router hands it out.

#### 8.2 Choose the farm network

**Done when** both links have a distance, whether the far end has power, what was eliminated and why, and what
remains. The instructor models card B on screen (400 m, no mains: WiFi and Zigbee out on distance,
cellular out on power; ESP-NOW, LoRa and RS-485 remain). The two canvas rows are filled from the
survivors, with a reason.

**If stuck** The weak answer is "WiFi, because the workshop used WiFi". Ask for the distance and the power
at the far end first.

#### 8.2 If the internet goes down

**Done when**

- *Our system:* automations yes, dashboard on the farm WiFi yes, dashboard from town no, history yes.
- *Cloud-run system:* automations no, farm dashboard no, dashboard from town no, history no.

#### 8.2 Home Assistant Cloud demo

**Done when** the answers are *mobile internet* and *on the farm (laptop)*. The cloud service is only a
door in; the farm's Home Assistant still decides and records.

#### 8.2 Choose remote access for the team's farm

**Done when** need, method and "what is lost if the farm's internet dies" are consistent. For example,
notifications only means only messages are lost; the farm keeps running. The canvas's third
communication row and "where the logic runs" are filled.

#### Question after step 1

**A good answer** says that with the internet down, local automations, the dashboard on the farm WiFi and logging carry on,
while remote viewing and notifications stop. With Home Assistant down, automations, logging and the
dashboard all stop. Only protection in the board or the wiring, and the manual switch, remain.

#### 8.3 The supply box

**Done when** the screen reads about 12 V and the battery icon reads **not full**. A charged lead-acid
battery sits at 12.7–13.0 V. The controller judges only from the voltage it measures, just like Home
Assistant.

#### 8.3 How many panels, and a battery?

**Done when** the table matches the answer key printed on the worksheet:

- *Sensor board:* 12 Wh/day, 1 panel, battery yes. Its night is 6 Wh, which the board's 18650 covers.
- *Router + Home Assistant host:* 240 Wh/day, 4 panels, battery yes, about 20 Ah at 12 V for a night.
- *Kit pump:* 36 Wh/day, 1 panel, no battery if it runs in daylight.
- *Farm pump:* 2,250 Wh/day, 38 of our panels, no battery. It runs direct from the panels in daylight, and the farm stores water, not electricity.
- *One night:* sensor board 6 Wh; farm pump at night 2,250 Wh.

**If stuck** Panels are rounded **up** to a whole panel, and Wh per day is watts × hours (0.5 W × 24 h = 12 Wh).

#### Question after step 2

**A good answer** splits the team's own loads into daylight-only (pumps) and must-run-overnight
(sensors, network, controller). For three cloudy days it names the numbers needed: each load's
Wh per day, the usable battery capacity (about half the rated capacity), and what the panels still
produce under cloud.

#### 8.4 Fill the canvas

**Done when** every canvas section has something: Input, Output (with how the team knows it actually runs),
Logic, at least one fail-safe plus a manual override, care and budget, the first pilot, and what the team is not
sure of yet.

#### 8.5 Paired exchange and revise

**Done when** both teams have pitched in one minute and given three minutes of feedback on two points:
the best-reasoned decision, and the part with no answer to "what happens if it fails". One change is
recorded in `d.revise`. There is no plenary.

#### 8.6 Check against the rubric

**Done when** the team has walked its canvas down the rubric: parts chosen from specs, with real prices;
network chosen on all four factors; power source per location; at least one fail-safe and a manual override; a named
carer and schedule; a budget that fits the farm; open questions and how they will be checked.

---

## Still missing

Nobody has produced these yet:

- **The ARM64 Farm Workshop OVA** (`farm-workshop-arm64.ova`) — blocks sending the install guide
  to participants with Apple Silicon Macs. The x86-64 image is built and hosted on Google Drive
- The install-guide details participants need: VM login, file size, verification form, help channel
- Slide decks for Sessions 1–3 and the three post-tests
- Expected values that need a bench run: the Activity 5 flicker count (TEST-PLAN test E) and
  typical room readings for Activity 1
- Real screenshots in the install guide (currently placeholders)
- Bench tests against the built firmware — see
  [TEST-PLAN.md](https://github.com/arnans/iot-training/blob/main/TEST-PLAN.md) *(repo)*, especially
  test B (the boot banner participants read) and test G (float switch polarity)

---

*Building the images rather than using them? The firmware build and the 18-step OVA recipe are in
[firmware/README.md](https://github.com/arnans/iot-training/blob/main/firmware/README.md) and
[hass/README.md](https://github.com/arnans/iot-training/blob/main/hass/README.md) — both repo-only.*
