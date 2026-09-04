# Worksheet — open items before print/publish

The worksheets in `docs/` follow the session structure in [COURSE-DESIGN.md](COURSE-DESIGN.md) but
are written against the **actual kit list** (Sept 2026) rather than the design doc's assumptions.
Where the two differ, the worksheet wins; COURSE-DESIGN still needs updating to match.

## Decisions taken (worksheet reflects these)

| Decision | Resolution | Consequence in the worksheet |
|---|---|---|
| Home Assistant host | Participants' own laptops | Session 1 opens with an install-verification checklist; the pre-workshop install guide (COURSE-DESIGN Section 6) becomes a hard prerequisite |
| Sensed input for watering | **Air humidity** (onboard) as a stand-in for soil moisture; **float switch** on GoGo-IoT port 1 as the reservoir-low guard | Worksheet says so explicitly ("จำลองสถานการณ์") rather than pretending humidity means soil |
| Hysteresis teaching | **Light sensor → relay**, framed as night lighting for a flower farm (เบญจมาศ). Relay's own LED and click are the output | Session 2 runs two scenarios in sequence on the single relay: lighting first (ladder), then watering (apply the lesson) |
| Between-session data | **Instructor HA adopts every team's sensor node** via ESPHome's multi-client API, stays on in the room | Session 2 opener reads the team's own trace on the instructor instance. Relay nodes are *not* adopted there (no double-driving) |
| Charge controller | Wired by teams in Activity 2 as the kit's **12V source**: adapter → BATT pair; LOAD pair → terminal block → relay board DC-in and pump (+ via COM/NO, − direct). Controller USB powers the GoGo-IoT only when the laptop leaves (overnight). Panel is added in session 3 | Session 1 calls it "กล่องจ่ายไฟ 12V" with one sentence of orientation; session 3 "เปิดกล่อง: พลังงาน" reads the three terminal pairs, sets battery type, connects the panel |
| 18650 cell | Powers the GoGo-IoT board directly; not part of the controller demo | Mentioned once in the kit list and once in the type-selection step |
| Plain ESP32-C3 nodemcu (item 2) | Spare, unmentioned | — |

## Firmware requirements the worksheet now depends on

1. **Light sensor `update_interval` ≈ 1 s, no averaging filter.** The chattering demonstration in
   session 2 needs the relay to flicker while a hand hovers at the threshold. ESPHome's native API
   pushes changes instantly and HA fires on the event, so the sensor's own interval is the only
   throttle. At a 60 s default the demo silently fails. Other sensors can stay slower.
2. **Float switch on port 1 as `binary_sensor`.** Worksheet asks teams to note which state appears
   when the float is lifted and use that as the fail-safe trigger, so either polarity works.
3. **Relay node exposes one `switch`.** Its onboard LED must follow the relay so the "lamp" is visible.
4. **`name_add_mac_suffix: true`, WiFi baked in, shared API encryption key**, `reboot_timeout: 0s`.
   No static IPs — see "Network and device provisioning" below. The light sensor's
   `update_interval` overrides the 5s used by the other sensors in the current
   `gogo-iot-node.yaml`.
5. **Instructor HA adopts all GoGo-IoT nodes** before the end of session 1. Confirm the ESPHome
   `api:` max-connections setting allows the team laptop plus the instructor instance plus a
   dashboard log stream.
6. **Charge controller load mode set to always-on (`24H` or equivalent) before the room.** These
   PWM controllers commonly default to a dusk-driven or dusk-plus-N-hours load mode keyed off PV
   voltage. Indoors the empty PV pair reads "night" forever, so a timer mode cuts the LOAD pair some
   hours in — the relay board dies overnight and, worse, mid-activity. The USB ports are normally on
   the battery rail and unaffected, so the GoGo-IoT overnight logging survives either way, but the
   relay board must not. Check the manual's load-mode table and lock it.
7. **Adapter leads must terminate in bare wire or ferrules** for the controller's BATT screw
   terminals — a barrel-jack adapter needs a pigtail. Kit item 10 (หัวแปลงสาย) may be this; confirm.
   Also confirm the terminal block (แผงต่อสาย) is in the kit; the worksheet uses it as the 12V
   distribution point (two rows: + and −).

## Needs verification against the real kit

- ~~**Relay board terminals.**~~ **Confirmed from the vendor datasheet**, extracted to
  `firmware/ESP32-C6-RELAY-X1.md`: terminals are **NO / COM / NC** as the worksheet assumed,
  power input is a separate 2-way block (7–60 V), relay is **GPIO19**, programmable LED
  **GPIO2**, button **GPIO9**, relay rating `10A 250VAC / 10A 30VDC`. Still confirm the
  supplied harness has two bare wires for the relay side.
- **Relay board takes USB *or* 12 V, not both** (datasheet: "choose one"). Teams read the
  device name over USB, then must unplug before wiring 12 V. Now stated in `session-1.md` and
  in `reference.md` troubleshooting. Worth verifying on the bench how bad the mistake is if
  someone forgets — see TEST-PLAN test H.
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
- **Phone reaching a laptop-hosted HA.** Windows firewall / VM networking often blocks port 8123
  from other devices. Worksheet tells teams to skip and flag it; the install guide should open the
  port, or the step will fail for most Windows teams.
- **Water props not on the kit list**: two containers, a glass for the float switch, drip tray,
  towel. Worksheet says the instructor provides them at the table.
- **Handouts referenced but not written**: ESPHome YAML printout for both boards; humidity sensor
  and float switch spec excerpts; equipment price sheet for the design challenge.
- ~~**Worksheet adoption steps still say "IP from the team card"**~~ **Done.** Rewritten across
  `session-1.md` (new "อ่านชื่อบอร์ด" block plus both adoption steps), `session-3.md` (the network
  section now teaches that the config contains no IP at all), `reference.md` (menu path plus a
  `.local`-fails fallback row), `index.md` and `record-sheet.md` (team card no longer carries IPs;
  the record sheet has fields for the two board names). Safe to do before the bench test because
  both possible outcomes of test B end in typing `<name>.local` — only *where the name comes from*
  is still open (USB log vs a printed sticker), and that is four lines in one block.

## Network and device provisioning

Resolved: **no static IPs, no MAC reservations, no per-board configuration.** One identical
firmware image for all boards, with `name_add_mac_suffix: true` so each advertises a unique
mDNS hostname. Workshop SSID baked in; `improv_serial:` and `captive_portal:` included so WiFi
can be set over USB or from a phone at a future delivery.

Adoption flow per board: plug into the laptop over USB → web.esphome.io → Connect → read the
board's name from the log → in HA, **Add integration → ESPHome → Host:** `<name>.local` →
shared encryption key → rename the device to the team's name. Typing the name avoids the
discovered-device list, which would show every board in the room.

Requirements this places on the network are written up in
[NETWORK-REQUIREMENTS.md](NETWORK-REQUIREMENTS.md) for the provider. The two that most often
fail by default: **mDNS forwarded between wireless clients**, and **two MAC addresses allowed
per laptop** (the Home Assistant VM is bridged, so it has its own MAC and IP).

Consequences for the install guide, still to be written:

- **VirtualBox network adapter must be Bridged, not NAT.** With NAT the VM cannot receive
  multicast, `.local` will not resolve, and phones cannot reach it. This is the single decision
  the whole addressing scheme rests on.
- **Docker Desktop on Windows cannot be offered as a path** — no host networking, so no mDNS.
- The phone step reads the address from **HA Settings → System → Network** (the VM's IP), not
  the laptop's IP.
- Fallback if a laptop cannot resolve `.local`: use the IP shown in the USB log. Week-long DHCP
  leases keep it valid for the workshop.

Also still to verify: the ESPHome `api:` and `mqtt:` `reboot_timeout` default of 15 minutes must
be set to `0s` on both boards, or they will reboot every 15 minutes overnight when no Home
Assistant is connected.

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

- **Thresholds are guesses** (`vib_on_threshold: 25`, `vib_off_threshold: 12` milli-g). TEST-PLAN
  test I calibrates them. If the pump-off and pump-on readings turn out indistinguishable, pull
  the two entities rather than ship something that reports noise.
- **Not yet in the worksheets.** Session 2's failure lab already runs three fail-safes and the
  sabotage rounds in 45 minutes; a fourth hands-on item would overflow it. Two cheaper options,
  both pending calibration:
  - *Instructor demo* in the session 2 debrief, next to the Auto/Off/Manual control box — both
    are about the layer that does not trust the controller. Roughly 3 minutes.
  - *Design-canvas prompt* in session 3: "how does your system know the actuator actually did
    something?" Pure text, no hardware time. **Added** — see the Output table in `record-sheet.md`.
- **Cost when unused**: 40 Hz I2C polling runs on every board whether or not anyone looks at the
  vibration entity. Watch during the bench test for any effect on the other sensors' stability or
  on WiFi; if it bites, the answer is a separate image variant rather than a slower poll.

## Reuse across deliveries

The worksheets carry no dates, venue names, or weekday references. Session pages refer to each other
as ช่วงที่ 1/2/3. The between-session gap now only needs to be long enough for the room lights to
have gone off and on (the light trace is the opener's hook) and for humidity to have drifted — an
overnight gap is ideal, a lunch break still shows something.

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


`docs/images/relay-board-generic-x1.webp` is the ESP32 Relay X1 product photo from
[devices.esphome.io](https://devices.esphome.io/devices/esp32-relay-x1/) — the WROOM variant, same
terminal layout, blue PCB. Replace with a photo of the actual C6 v1.1 board when one is in hand;
`session-1.md` references `images/relay-board.jpg` for that slot. All other images are
`placeholder.png` with alt text describing the shot. New shots this revision: GoGo-IoT board with
port 1 labelled; COM/NO wiring diagram and photo; charge controller face and terminal pairs; the
four-step connection sequence; instructor HA history with a team's light trace.

## Print artifact

`docs/record-sheet.md` is the only page meant for paper, one copy per team. It keeps dotted
fill-in lines (the exception to the web-Markdown conventions). Print from the rendered page.

## Not yet written

- Scenario cards for Activity 6 (content is in `session-3.md`)
- Role cards (content is in `index.md`)
- Team cards: both board IPs, workshop SSID, instructor HA address
- Pre-workshop Home Assistant install guide for participant laptops (COURSE-DESIGN Section 6),
  including opening port 8123 so phones can reach it
- Equipment price sheet for the design challenge
- The three post-tests
- COURSE-DESIGN.md update to reflect the decisions above
