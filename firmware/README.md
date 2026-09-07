# Workshop firmware

Two ESPHome source files, one per board type, each **built three times** — once per network
zone (red, green, blue) with that zone's SSID and password injected as substitutions. Six
binaries, two YAMLs to maintain. Within a zone, board identity comes from `name_add_mac_suffix`;
the zone colour is part of the hostname (`gogo-iot-red-a1b2c3`) so a board announces where it
belongs.

| File | Board | Notes |
|---|---|---|
| `gogo-iot-workshop.yaml` | GoGo-IoT sensor node (ESP32-C3) | Derived from `gogo-iot-node` repo bring-up config |
| `relay-workshop.yaml` | ESP32-C6-Relay_X1 v1.1 | Pins confirmed — see `ESP32-C6-RELAY-X1.md` |
| `ESP32-C6-RELAY-X1.md` | — | Hardware reference extracted from the vendor PDF |
| `secrets.example.yaml` | — | Copy to `secrets.yaml` (gitignored): OTA password, fallback AP password |
| `zones.example.yaml` | — | Copy to `zones.yaml` (gitignored): per-zone SSID + password |
| `build-zones.py` | — | Builds all six binaries into `dist/`; can also flash one |

The sensor node's authoritative hardware source stays in the
[`gogo-iot-node`](https://github.com/arnans/gogo-iot-node) repo. This directory holds
only the workshop variant; changes to pin assignments or sensor drivers belong upstream.

## Build and flash

```bash
pip install esphome esptool pyyaml
cp secrets.example.yaml secrets.yaml     # OTA + fallback AP passwords
cp zones.example.yaml zones.yaml         # three SSIDs + passwords
python build-zones.py                    # -> dist/gogo-iot-{red,green,blue}.factory.bin
                                         #    dist/gogo-relay-{red,green,blue}.factory.bin
python build-zones.py --flash red sensor COM7
```

For a single bench board without the script:

```bash
esphome -s zone red -s wifi_ssid farm-iot-red -s wifi_password <pw> run gogo-iot-workshop.yaml
```

**Production run:** flash ~34 sensor + ~34 relay boards per zone from `dist/`, and colour-code
each board (tape or sticker) as you go. **The colour on the board must match the colour on the
kit and the team's laptop SSID.** That is the only cross-zone risk, and the board's own hostname
reveals it at the name-reading step.

## What participants do

1. Plug the board into a laptop over USB-C.
2. Open <https://web.esphome.io>, click **Connect**, pick the serial port, open **Logs & Console**.
3. Press **Reset device** *in the browser window*. **Not the button on the board** — these chips
   use native USB, so a hardware reset kills the browser's serial session and the boot output is
   lost. An already-running board otherwise shows a blank log and looks broken.
4. Read the device name from the banner — `gogo-iot-red-6749a4`. **Write down the last six
   characters** (`6749a4`); that is what the next step matches against. The board's IP prints a
   couple of seconds later, when WiFi connects.
5. In Home Assistant: **Settings → Devices & services**. The board is already there as a
   discovered card — **find the one carrying your six characters** and add it. No encryption key,
   nothing to type. Same path for both boards.
6. Rename the device to the team's name.

**Decided: pick the discovered card, with manual entry as the fallback.** Boards appear on the
Devices & services page on their own, before any ESPHome integration exists, so there is nothing
to set up first and no difference between adding the first board and the second.

The fallback, for a board that does not appear, is four levels deep — worth writing out because a
participant will not find it by guessing:

1. **+ Add integration** → type **ESPHome** (not "ESP-NOW" — different Espressif protocol).
2. ESPHome's page opens, listing discovered devices again. Still missing? **Add device**.
3. The popup lists discovered devices once more — or choose **"Setup another instance of ESPHome"**.
4. Type the node name **without `.local`** — `gogo-iot-red-6749a4`. Bench-verified; the bare name
   resolves, and it is one less thing to type. Port 6053.

The risk this trades into, and the mitigation: clicking the *wrong* card fails **silently** — a
team adopting a neighbour's board sees entities appear and graphs populate, and nothing looks
wrong. Typing the name was self-verifying; picking is not. So the six-character suffix is what
makes the pick safe, and the zone colour in the name (`gogo-iot-**red**-…`) is a second free
check: a red-zone team seeing `green` in the name knows immediately. Both belong in the worksheet
wording, not just here.

## Settings that are load-bearing

Do not change these without reading the reasoning:

- **`name_add_mac_suffix: true`** — the entire provisioning strategy.
- **The `on_boot:` logger banner printing `DEVICE NAME`** — this is the line participants read at
  web.esphome.io, and nothing else prints it. The hostname appears only in WiFi's config dump at
  `[C]`/CONFIG level, which `logger: level: INFO` filters out (ESPHome levels run
  `INFO < CONFIG < DEBUG`). Do not delete the banner, and do not "simplify" it by raising the log
  level instead — CONFIG dumps every component and buries the name. See TEST-PLAN.md test B.
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
