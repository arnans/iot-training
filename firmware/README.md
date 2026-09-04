# Workshop firmware

Two ESPHome images, one per board type, flashed identically to every unit. Board
identity comes from `name_add_mac_suffix`, not from per-board configuration.

| File | Board | Notes |
|---|---|---|
| `gogo-iot-workshop.yaml` | GoGo-IoT sensor node (ESP32-C3) | Derived from `gogo-iot-node` repo bring-up config |
| `relay-workshop.yaml` | ESP32-C6 single relay | Relay GPIO **not yet confirmed** |
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

For the production run of ~120 boards, build the binary once and flash it repeatedly
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
- **No `friendly_name`** — so teams can tell 60 boards apart in Home Assistant.

## Unconfirmed

- **Relay GPIO on the ESP32-C6 v1.1 board.** Placeholder is GPIO16 from the WROOM
  variant of the same family. See TEST-PLAN.md test H.
- **Float switch pin and polarity.** Port 1 is CN2 → GPIO0 / GPIO1 per the schematic
  netlist; the config uses GPIO0 with a pullup and `inverted: true` so that
  ON = water present. Confirm which way the switch closes. See TEST-PLAN.md test G.
