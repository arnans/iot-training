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

**On Windows, build from PowerShell or cmd — not Git Bash.** ESP-IDF's installer refuses to run
under MSYS/MinGW and fails with `ERROR: MSys/Mingw is not supported` before compiling anything.

For a single bench board without the script:

```bash
esphome -s zone red -s wifi_ssid farm-iot-red -s wifi_password <pw> run gogo-iot-workshop.yaml
# over the air, no cable, once the board is on WiFi:
esphome -s zone red -s wifi_ssid farm-iot-red -s wifi_password <pw> run gogo-iot-workshop.yaml --device gogo-iot-red-6749a4.local
```

A plain `esphome compile` without the `-s` values builds with the placeholder credentials from the
`substitutions:` block — it validates the YAML but the image will never join a network. After a
re-flash, Home Assistant picks up new entities on its own when the board reconnects; do not
remove and re-add the device (that discards the team's rename).

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
  level instead — CONFIG dumps every component and buries the name. See planning/TEST-PLAN.md test B.
- **`reboot_timeout: 0s`** on both `api:` and `wifi:` — otherwise boards reboot every
  15 minutes overnight when no Home Assistant is connected, wrecking the session 2
  history graph.
- **`update_interval: 1s` on the BH1750** — session 2's hysteresis lesson works by
  making the relay chatter. At the default 5s nothing visible happens.
- **`update_interval: 1s` on the SHT3x, with `delta` + `throttle` filters** — a breath shows
  within about a second, which makes session 2's blow-on-it watering loop feel immediate. The
  sensor's own humidity response (~8 s to 63 %) is unchanged; only the lag before the first
  reading goes. The filters are not optional: without them the last decimal changes nearly every
  second and every change is a history row. With them a reading goes out when temperature moves
  0.2 °C or humidity 0.5 %RH, and otherwise every 30 s. Network cost is a couple of ~13-byte API
  messages a second per board, negligible.
- **`restore_mode: ALWAYS_OFF`** on the relay — a pump must not restart itself after a
  power cut.
- **No `friendly_name`** — so teams can tell 100 identical boards apart in Home Assistant.
- **Every entity name carries an ASCII tag**, e.g. `ความชื้นอากาศ (humidity)`. ESPHome builds the
  Home Assistant `entity_id` by transliterating the name to ASCII, so a Thai-only name becomes a
  row of underscores — and two Thai names of the same character length collide outright and fail
  to compile. The Thai stays first because that is what the worksheet refers to; the English tag
  makes the entity_id unique and greppable. **Do not remove the tags.**
- **The relay board's LED is driven by an `interval:`, not by `status_led:`.** `status_led:`
  blinks 250 ms on / 1250 ms off for a warning, and inverting the pin to get lit-when-healthy
  inverts that too — the bench saw a "steady" LED with a 250 ms wink and called it broken. The
  explicit interval gives a symmetric 0.8 s blink on WiFi loss and steady lit on WiFi. The API is
  deliberately not part of it: the board is meant to run overnight with no Home Assistant, and
  `status_led:` would have blinked all night. See planning/TEST-PLAN.md test H.
- **Top-level keys go at the end of the file, never mid-list.** Inserting `select:` after
  `pump_running` silently re-parented the float switch (the next `- platform: gpio` item) under
  `select:` and failed with `Platform not found: 'select.gpio'`. YAML gives no other warning.

## Confirmed on the bench

- **Float switch: GPIO0, internal pull-up, `inverted: true`, `device_class: moisture`, ON = Wet =
  water present.** The float cylinder is **flipped on its rod at kit prep** (Roger, 8 Sep 2026) so
  the contact closes when the float *rises* (wet): wet = closed = pulled low, and `inverted: true`
  gives the polarity the worksheets assume. Consequence: a cut wire, an unseated Grove plug, or no
  switch at all reads **Dry**, so every wiring fault fails safe. As shipped the float closed when
  *down*; a kit assembled without the flip reads backwards — check the cylinder, not the YAML. The
  moisture device class makes Home Assistant show **Wet / Dry** rather than On / Off. Session 2's
  watering rule still requires **Wet** as a condition, so a dead board (`unavailable`) fails safe
  too. planning/TEST-PLAN.md test G.
- **Relay board pins GPIO19 (relay), GPIO2 (LED), GPIO9 (button)**, from the vendor datasheet and
  confirmed on hardware — `ESP32-C6-RELAY-X1.md`.
- **`restore_mode: ALWAYS_OFF` holds on both supplies** (USB and 12 V): the relay is off after
  every power-up. On the day the board runs on **USB from the charge controller** (decided
  8 Sep 2026); the 7–60 V input stays empty.

## Vibration reporter

`gogo-iot-workshop.yaml` includes a vibration reporter: it samples the accelerometer at 40 Hz,
takes the magnitude, subtracts a slow baseline (removing gravity and tilt), RMS-es the remainder
over 1 s, and applies hysteresis plus persistence. It publishes two entities —
`ความสั่นสะเทือน (vibration)` in milli-g and the verdict `ปั๊มกำลังทำงาน (pump running)`.

The point is **commanded state versus actual state**: a relay can be closed while the pump is
seized, unprimed or unplugged. Raw acceleration is never streamed to Home Assistant; the three
axis sensors are `internal`.

Thresholds were calibrated against the real pump (planning/TEST-PLAN.md test I: idle 3–8 mg, running
~20–25 mg on a deliberately soft mount) and are now chosen at runtime from a three-level
**`select`**, `ความไวตรวจจับปั๊ม (pump sensitivity)`:

| Level | on > | off < | For |
|---|---|---|---|
| สูง (high) | 15 mg | 10 mg | soft mount or quiet pump; accepts some knock false-positives |
| กลาง (medium) — default | 25 mg | 12 mg | the bench-checked pair |
| ต่ำ (low) | 40 mg | 20 mg | hard-coupled mount or a table that shakes |

It appears in Home Assistant under the device's *Configuration* section and on the board's web
page, and the choice survives a power cut (`restore_value`, bench-confirmed). The six numbers are
`substitutions:`; the live pair lives in two `globals:` that the select's `on_value` writes,
switching on the option index so the Thai labels can change freely. The 40 Hz poll rate aliases
vibration above 20 Hz, which is harmless for a yes/no verdict but means the milli-g figure is not
a calibrated measurement.

## Two supplies at once — measured harmless, habit kept

The relay board's datasheet says USB 5 V **or** 7–60 V on the screw terminal, "choose one".
Bench-measured: the 5 V rail reads 5.04 V from USB and 5.12 V from the 12 V input — 80 mV apart —
and plugging USB into a board already running on 12 V changes nothing; the serial port enumerates
and works. The other order can at most reset the board, which `restore_mode: ALWAYS_OFF` makes
safe. Since 8 Sep 2026 the worksheet never wires 12 V to the board at all — it runs on the charge
controller's USB port — so this only matters if a team wires the 7–60 V input by mistake, which
the measurement shows is harmless. To read a log, move the board's USB cable to the laptop. Details in `ESP32-C6-RELAY-X1.md`.

## What each board exposes

Entities visible in Home Assistant and on the board's own page (everything else is `internal`):

| GoGo-IoT sensor node (11) | Relay board (5) |
|---|---|
| ความสว่าง (light) · อุณหภูมิ (temperature) · ความชื้นอากาศ (humidity) · ความกดอากาศ (pressure) | รีเลย์ (relay) — switch |
| สวิตช์ลูกลอย (float switch) — binary | ปุ่มบนบอร์ด (button) — binary |
| ความสั่นสะเทือน (vibration) · ปั๊มกำลังทำงาน (pump running) — binary · ความไวตรวจจับปั๊ม (pump sensitivity) — select | |
| เวลาทำงาน (uptime) · ความแรงสัญญาณ WiFi · หมายเลข IP — diagnostics | เวลาทำงาน (uptime) · ความแรงสัญญาณ WiFi · หมายเลข IP — diagnostics |

The raw accelerometer axes are never published — the worksheet's "tap the table" step reads
`ความสั่นสะเทือน`, not an axis.
