# Workshop firmware

Two ESPHome images, one per board type, flashed identically to every unit. Board
identity comes from `name_add_mac_suffix`, not from per-board configuration.

| File | Board | Notes |
|---|---|---|
| `gogo-iot-workshop.yaml` | GoGo-IoT sensor node (ESP32-C3) | Derived from `gogo-iot-node` repo bring-up config |
| `relay-workshop.yaml` | ESP32-C6-Relay_X1 v1.1 | Pins confirmed — see `ESP32-C6-RELAY-X1.md` |
| `ESP32-C6-RELAY-X1.md` | — | Hardware reference extracted from the vendor PDF |
| `secrets.example.yaml` | — | Copy to `secrets.yaml` (gitignored) |

The sensor node's authoritative hardware source stays in the
[`gogo-iot-node`](https://github.com/arnans/gogo-iot-node) repo. This directory holds
only the workshop variant; changes to pin assignments or sensor drivers belong upstream.

## Build and flash

```bash
pip install esphome
cp secrets.example.yaml secrets.yaml     # then edit
esphome run gogo-iot-workshop.yaml       # first board, over USB
esphome run relay-workshop.yaml
```

For the production run of **200 boards** (100 sensor + 100 relay), build each binary once and flash it repeatedly
rather than invoking `esphome run` each time:

```bash
esphome compile gogo-iot-workshop.yaml
# binary lands in .esphome/build/gogo-iot/.pioenvs/gogo-iot/firmware.bin
```

Then flash from https://web.esphome.io (Chrome/Edge, no install) or with `esptool`.
Every board gets the same binary; each derives its own hostname from its MAC at boot.

## What participants do

1. Plug the board into a laptop over USB-C.
2. Open <https://web.esphome.io>, click **Connect**, pick the serial port.
3. Read the device name from the log — `gogo-iot-a1b2c3`.
4. In Home Assistant: **Settings → Devices & services → + Add integration → ESPHome**,
   **Host:** `gogo-iot-a1b2c3.local`, then the shared encryption key.
5. Rename the device to the team's name.

Typing the name avoids Home Assistant's discovered-device list, which would show
every board in the room.

## Settings that are load-bearing

Do not change these without reading the reasoning:

- **`name_add_mac_suffix: true`** — the entire provisioning strategy.
- **`reboot_timeout: 0s`** on both `api:` and `wifi:` — otherwise boards reboot every
  15 minutes overnight when no Home Assistant is connected, wrecking the session 2
  history graph.
- **`update_interval: 1s` on the BH1750** — session 2's hysteresis lesson works by
  making the relay chatter. At the default 5s nothing visible happens.
- **`restore_mode: ALWAYS_OFF`** on the relay — a pump must not restart itself after a
  power cut.
- **No `friendly_name`** — so teams can tell 100 identical boards apart in Home Assistant.
- **Every entity name carries an ASCII tag**, e.g. `ความชื้นอากาศ (humidity)`. ESPHome builds the
  Home Assistant `entity_id` by transliterating the name to ASCII, so a Thai-only name becomes a
  row of underscores — and two Thai names of the same character length collide outright and fail
  to compile. The Thai stays first because that is what the worksheet refers to; the English tag
  makes the entity_id unique and greppable. **Do not remove the tags.**

## Unconfirmed

- **Float switch pin and polarity.** Port 1 is CN2 → GPIO0 / GPIO1 per the schematic
  netlist; the config uses GPIO0 with a pullup and `inverted: true` so that
  ON = water present. Confirm which way the switch closes. See TEST-PLAN.md test G.

Relay board pins were unconfirmed until the vendor datasheet arrived; they are now
GPIO19 (relay), GPIO2 (LED), GPIO9 (button), recorded in `ESP32-C6-RELAY-X1.md`.

## Vibration reporter

`gogo-iot-workshop.yaml` includes a vibration reporter: it samples the accelerometer at 40 Hz,
takes the magnitude, subtracts a slow baseline (removing gravity and tilt), RMS-es the remainder
over 1 s, and applies hysteresis plus persistence. It publishes two entities —
`ความสั่นสะเทือน (vibration)` in milli-g and the verdict `ปั๊มกำลังทำงาน (pump running)`.

The point is **commanded state versus actual state**: a relay can be closed while the pump is
seized, unprimed or unplugged. Raw acceleration is never streamed to Home Assistant; the three
axis sensors are `internal`.

Thresholds in the `substitutions:` block are **guesses** and must be calibrated against the real
pump — TEST-PLAN test I. The 40 Hz poll rate aliases vibration above 20 Hz, which is harmless
for a yes/no verdict but means the milli-g figure is not a calibrated measurement.

## Hazard worth knowing

The relay board accepts **either** USB 5 V **or** 7–60 V on the screw terminal, **not both**.
Teams plug in USB once to read the device name, then unplug it before wiring 12 V. The
worksheet says so at that step.
