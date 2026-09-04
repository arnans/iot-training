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
4. **Static IPs, add-by-IP**, encryption key on the team card if enabled. Unchanged.
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

- **Relay board terminals.** Worksheet wires the pump through **COM** and **NO**, the standard
  labels on the ESP32 Relay X1 family. Confirm the C6 v1.1 board prints the same, and that the
  supplied harness (item 10) has two bare wires for the relay side.
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

## Reuse across deliveries

The worksheets carry no dates, venue names, or weekday references. Session pages refer to each other
as ช่วงที่ 1/2/3. The between-session gap now only needs to be long enough for the room lights to
have gone off and on (the light trace is the opener's hook) and for humidity to have drifted — an
overnight gap is ideal, a lunch break still shows something.

## Images

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
