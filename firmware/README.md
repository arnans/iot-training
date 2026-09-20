# Workshop firmware

Four ESPHome source files — three board types plus a Session 4 variant of the sensor node — each
**built three times**, once per network zone (red, green, blue) with that zone's SSID and password
injected as substitutions. Twelve binaries. Within a zone, board identity comes from
`name_add_mac_suffix`; the zone colour is part of the hostname (`gogo-iot-red-a1b2c3`) so a board
announces where it belongs.

| File | Board | Notes |
|---|---|---|
| `gogo-iot-workshop.yaml` | GoGo-IoT sensor node (ESP32-C3) | Derived from `gogo-iot-node` repo bring-up config. **Pre-flashed on every board; the sessions 1–3 image** |
| `gogo-iot-espnow-workshop.yaml` | the same GoGo-IoT | The base file as a `packages:` include, plus an **ESP-NOW broadcast** of the readings every 3 s. Same hostname, so Home Assistant needs no re-adoption. Published as `gogo-iot-espnow-<zone>`; **teams flash it over the base image in Activity 9** — see below |
| `relay-workshop.yaml` | ESP32-C6-Relay_X1 v1.1 | Pins confirmed — see `ESP32-C6-RELAY-X1.md` |
| `farm-receiver-workshop.yaml` | Any plain ESP32-C3 devkit, no sensors | **Session 4's receiver**: hears the sensor node over ESP-NOW, mirrors its readings as entities, adopted in Home Assistant like the others. Teams flash it themselves in Activity 10 |
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
                                         #    dist/gogo-iot-espnow-{red,green,blue}.factory.bin
                                         #    dist/gogo-relay-{red,green,blue}.factory.bin
                                         #    dist/farm-receiver-{red,green,blue}.factory.bin
                                         #    and the same twelve into ../docs/firmware/
python build-zones.py --board receiver --receiver-console uart0   # receiver boards with a USB-UART chip
python build-zones.py --flash red sensor COM7
```

The build also writes into `docs/firmware/`, which is what GitHub Pages serves and what every
worksheet links to. **Commit and push those twelve files to publish** — building alone does not
update the site. Session 4 depends on it twice over: Activities 9 and 10 have participants
download `gogo-iot-espnow-<zone>` and `farm-receiver-<zone>` from there and flash them at
web.esphome.io. The pre-flashed `gogo-iot-<zone>` image is unchanged in behaviour (it only gained
`id:`s) and is also the way back for a board that misbehaves after Activity 9. Check `git status` after a build; if the binaries are unchanged there, the site
is already current.

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
each board (tape or sticker) as you go. The receiver boards need no pre-flash — flashing them is
Activity 10 — but do sort them by zone and colour-code them the same way, and flash one per zone
yourself to check the console setting (next section) before the day.

### The receiver board's USB (Session 4)

`farm-receiver-workshop.yaml` runs on any ESP32-C3 devkit, but the log banner participants read
(`DEVICE NAME`, `IP ADDRESS`, the `<<< GOGO,` packets) only appears on the port the logger writes
to, and C3 devkits come in two kinds:

| Board | USB wiring | Build with |
|---|---|---|
| ESP32-C3 "Super Mini", Seeed XIAO ESP32C3, DevKitC-02 v1.1 USB-C | native USB Serial/JTAG straight to the chip | default (`--receiver-console usb`) |
| ESP32-C3-DevKitM-1, DevKitC-02 via its UART port, most NodeMCU-style C3 boards | CP2102 / CH340 USB-UART chip | `--receiver-console uart0` |

Flashing at web.esphome.io works either way; only where the log appears differs. **Decide once at
purchase, buy one kind, build with the matching flag.** The sample devkit checked on 20 Sep 2026
enumerates as Espressif `USB JTAG/serial debug unit` — native USB, the default build. Also check the
bundled cables: the first one tried was charge-only and the board never enumerated. The worksheet links one file name per
zone and says nothing about console types; if the log stays blank on the day, this is why.
Boards with both ports (some DevKitC-02) show the log on whichever port matches the build. **The colour on the board must match the colour on the
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
- **`power_save_mode: none`** on the sensor node and the receiver — first for mDNS, now also for
  ESP-NOW: a radio dozing between beacons misses broadcast frames on both ends.
- **`gogo-iot-espnow-workshop.yaml` includes the base file; it never copies it.** Anything the
  sensor node needs goes in `gogo-iot-workshop.yaml` and reaches both images; only the ESP-NOW
  block lives in the variant. Its `device_base_name` must stay `gogo-iot` (same hostname).
- **The receiver listens in `on_unknown_peer`, never with `auto_add_peer`** — the 20-entry peer
  table versus ~100 boards on the air. See "ESP-NOW link" above.
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

## ESP-NOW link (Session 4)

Session 4's story: the plot is out of WiFi range, so the GoGo-IoT board **broadcasts** its
readings over ESP-NOW and a plain ESP32-C3 in the farmhouse (`farm-receiver-workshop.yaml`)
hears them and is the device Home Assistant talks to. Both YAMLs carry the full reasoning in
their ESP-NOW blocks; the shape:

- **Sender** (`gogo-iot-espnow-workshop.yaml` = the base image + this block): every 3 s
  (`espnow_interval`), one plain-text CSV frame to `FF:FF:FF:FF:FF:FF`:
  `GOGO,<name>,<seq>,<temp>,<hum>,<light>,<pressure>,<vibration>,<float>,<pump>` — ~70 bytes,
  readable in the USB log as `[espnow] >>> GOGO,...`. Two diagnostics were added for it:
  `ช่องสัญญาณ WiFi (channel)` and `แพ็กเก็ต ESP-NOW ที่ส่ง (espnow sent)`. It is a separate image so
  the boards carry the plain one through sessions 1–3 and Activity 9's flash is a visible upgrade
  (no `>>>` lines before, one every 3 s after); the hostname is the same, so Home Assistant picks
  the board up again without re-adoption. The base file only gained `id:`s for the packet lambda.
- **Receiver**: listens in `on_unknown_peer` — deliberately, because ESP-NOW's peer table holds
  20 entries and a ballroom has ~100 GoGo boards on the air, so `auto_add_peer` would fill it
  with the wrong boards. It filters frames by the **name in the payload** against the
  `ชื่อบอร์ดที่แปลง (sender name)` text entity a team types (suffix match, case-insensitive: the
  six characters they already use for adoption), mirrors the readings as entities tagged
  `ESP-NOW`, and keeps link diagnostics: RSSI, packets received, packets lost (from `seq` gaps),
  the last raw frame, and `บอร์ดอื่นที่ได้ยิน (other boards heard)` for the worksheet's
  "the channel is public" question. A 1 s watchdog flips `รับข้อมูลจากแปลง (link)` off after
  `link_timeout_ms` (15 s) of silence and publishes NaN to the mirrored sensors, so Home
  Assistant shows unknown rather than a stale number — the fail-safe habit from Session 2.
- **Channel.** With `wifi:` configured, ESPHome refuses `espnow.channel`; ESP-NOW rides the
  channel the access point put the board on. Both boards join the same zone SSID, so they
  normally share it, but a room with several APs on 1/6/11 can split them, and then the receiver
  hears nothing. That is why both boards expose `ช่องสัญญาณ WiFi (channel)`, why Activity 10's
  troubleshooting compares the two, and why the receiver's `power_save_mode: none` is
  load-bearing (a dozing radio misses broadcast frames). If the venue can pin all 2.4 GHz radios
  of a zone to one channel, do it.
- **No encryption, by design**: the "other boards heard" lesson needs the channel to be
  readable. A real deployment would set a PMK/LMK or use `packet_transport` with `encryption`.
- **Why not `packet_transport`** (ESPHome's built-in state-over-ESP-NOW): its consumer must name
  the provider at compile time, and every GoGo board has a different MAC-suffixed name, so one
  receiver image per zone could not work. The hand-rolled text frame also has the teaching
  advantage that participants can read it in the log on both ends.

Bench-check before the day (planning/TEST-PLAN.md test M): one sender and one receiver on the
same zone SSID, type the suffix, values within 5 s; switch the sender off, link down at ~15 s;
carry the sender across the room on its 18650 cell and watch RSSI and the lost counter.

## What each board exposes

Entities visible in Home Assistant and on the board's own page (everything else is `internal`):

| GoGo-IoT sensor node (11; 13 with the ESP-NOW image) | Relay board (5) | Farm receiver (17) |
|---|---|---|
| ความสว่าง (light) · อุณหภูมิ (temperature) · ความชื้นอากาศ (humidity) · ความกดอากาศ (pressure) | รีเลย์ (relay) — switch | อุณหภูมิ · ความชื้นอากาศ · ความสว่าง · ความกดอากาศ · ความสั่นสะเทือน, each `(…, ESP-NOW)` |
| สวิตช์ลูกลอย (float switch) — binary | ปุ่มบนบอร์ด (button) — binary | สวิตช์ลูกลอย (float switch, ESP-NOW) · ปั๊มกำลังทำงาน (pump running, ESP-NOW) · รับข้อมูลจากแปลง (link) — binary |
| ความสั่นสะเทือน (vibration) · ปั๊มกำลังทำงาน (pump running) — binary · ความไวตรวจจับปั๊ม (pump sensitivity) — select | | ชื่อบอร์ดที่แปลง (sender name) — text, config · บอร์ดที่รับข้อมูลอยู่ (receiving from) — text sensor |
| เวลาทำงาน (uptime) · ความแรงสัญญาณ WiFi · หมายเลข IP — diagnostics · ESP-NOW image adds ช่องสัญญาณ WiFi (channel) · แพ็กเก็ต ESP-NOW ที่ส่ง (espnow sent) | เวลาทำงาน (uptime) · ความแรงสัญญาณ WiFi · หมายเลข IP — diagnostics | ความแรงสัญญาณ ESP-NOW (rssi) · แพ็กเก็ตที่รับ · แพ็กเก็ตที่หาย · ข้อมูลล่าสุดที่รับ (last packet) · บอร์ดอื่นที่ได้ยิน (other boards heard) · ช่องสัญญาณ WiFi (channel) · เวลาทำงาน · ความแรงสัญญาณ WiFi · หมายเลข IP — diagnostics |

The raw accelerometer axes are never published — the worksheet's "tap the table" step reads
`ความสั่นสะเทือน`, not an axis. The receiver's `ข้อมูลล่าสุดที่รับ` changes every 3 s (the `seq`
is in it), so it writes a Home Assistant history row per packet; it is a diagnostic and can be
excluded from the recorder if that ever matters.
