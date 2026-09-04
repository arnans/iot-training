# Bench test plan — ESPHome provisioning

One session at a desk, two boards, one laptop. Purpose: prove the participant flow works
before committing to a firmware image for ~120 boards, and settle the four things the
worksheets currently assume without evidence.

**Time:** about 2 hours if nothing surprises you. Tests A–D are the critical path; E–H can
follow later if time runs short.

## Already done for you

- **ESPHome 2026.6.5 is installed** on this machine.
- **Both images compile clean**, verified end to end:
  `gogo-iot-workshop.yaml` → 992 KB factory image (~4 min), `relay-workshop.yaml` → 1.1 MB.
  The ESP-IDF toolchains for both C3 and C6 are downloaded and the build cache is warm, so
  rebuilds are far quicker than the first run.
- **One expected warning**, not a problem: `GPIO9 is a strapping PIN and should only be used
  for I/O with care`. GPIO9 is the relay board's onboard button, per the vendor datasheet.
  A momentary press while running is harmless; only holding it during power-up enters the
  bootloader.
- **`firmware/secrets.yaml` exists** with a real generated API encryption key, OTA password and
  fallback AP password. It is gitignored.

> **The one thing to do before flashing:** the two WiFi lines in `firmware/secrets.yaml` are
> placeholders (`CHANGE_ME_SSID` / `CHANGE_ME_PASSWORD`). Put in the network you are testing
> against, then `esphome run <file>.yaml`. The rebuild is incremental, not another 4 minutes.
>
> Keep the generated `api_encryption_key` — it is the one shared key that goes on every board and
> onto the team card. Regenerate it only if you want to.

## Before you start

- [ ] GoGo-IoT sensor board, USB-C cable
- [ ] ESP32-C6 relay board, USB-C cable
- [ ] Float switch with its Grove adapter, a glass of water
- [ ] Laptop with Chrome or Edge (Web Serial needs one of those; Firefox will not work)
- [ ] Edit the two WiFi lines in `firmware/secrets.yaml`
- [ ] A WiFi network you control. **Not** a corporate/university SSID — those usually block
      client-to-client traffic and mDNS, which would make tests C and D fail for the wrong reason
- [ ] Home Assistant reachable from the laptop. If it is a VM, **bridged adapter, not NAT**

Record results in the table at the bottom.

```bash
cd firmware
esphome run gogo-iot-workshop.yaml     # sensor board
esphome run relay-workshop.yaml        # relay board
```

---

## A. Flash the workshop image

Compilation is already proven — both images built clean on ESPHome 2026.6.5, including
`spa06_i2c` and `lsm6ds`, so no external components or version pins are needed. This step is
now about flashing and first boot.

```bash
cd firmware
esphome run gogo-iot-workshop.yaml
```

- [ ] Flashes over USB without holding any button (native USB should reset it automatically)
- [ ] Log shows the device name **with a MAC suffix**: `gogo-iot-xxxxxx`
- [ ] All four I2C sensors report values, no `Communication failed` lines
- [ ] Board joins WiFi

> If the board will not enter the bootloader on its own, hold BOOT while plugging in.

**Question this answers:** does the image run on real hardware and see all four sensors?

---

## B. The participant USB lookup — the critical test

This is the step every team performs twice, and the whole no-sticker plan rests on it.

1. Unplug and replug the board so it is freshly booted.
2. Open <https://web.esphome.io> in Chrome/Edge.
3. **Connect** → pick the serial port → **Logs & Console**.

- [ ] The port appears in the browser's picker without installing a driver
- [ ] The log shows the device name clearly enough for a participant to copy it down
- [ ] Note **how far into the log** the name appears — if it scrolls past, participants will
      miss it and the worksheet needs to say "press the reset button, then read the first lines"
- [ ] Time the whole step from plugging in to having the name written down

**Question this answers:** can a non-technical participant get their board's name in under
two minutes, with no software installed?

> If this is awkward, the fallback is a printed sticker per board from `esptool read_mac`
> during the flashing run. Decide now — it changes the kit prep, not the worksheet flow.

---

## C. Adopt in Home Assistant by name

**Settings → Devices & services → + Add integration → ESPHome**, Host: `gogo-iot-xxxxxx.local`,
port 6053, then the shared encryption key.

- [ ] `.local` name resolves — **this is the mDNS test**
- [ ] Device is added, entities appear with Thai names
- [ ] Rename the device to a team name; entity IDs stay stable
- [ ] Unplug the board, wait 1 min, plug back in → returns to available on its own

> **If `.local` does not resolve** the problem is almost always the network or the VM's
> adapter mode, not the firmware. Try the IP from the USB log; if that works, mDNS is being
> blocked and NETWORK-REQUIREMENTS.md item 3 is the fix.

**Question this answers:** does hostname adoption work end to end, and does it survive a
reboot the way DHCP-with-mDNS is supposed to?

---

## D. Two boards, no collision

Flash the **same** image to the relay board's slot in your bench setup — or, if the relay
board is not ready, flash the sensor image to any second ESP32 you have.

- [ ] Second board gets a **different** hostname from the same binary
- [ ] Both adopt into Home Assistant simultaneously
- [ ] In **Settings → Devices & services**, note what the *discovered* card list looks like
      with two boards on the network — this is what will show 120 entries on the day

**Question this answers:** is the MAC suffix genuinely unique, and is typing the name really
necessary rather than clicking the discovered card?

---

## E. Chattering is visible — the session 2 lesson

The hysteresis teaching depends on the relay flickering when a hand hovers at the light
threshold. If it does not flicker, the lesson has no problem to solve.

1. In Home Assistant create one automation: light **Below** a threshold near room level →
   switch **turn on**. And a second: **Above** the *same* value → **turn off**.
2. Hold a hand at the height where the reading sits right at the threshold and waver it.

- [ ] The relay audibly clicks repeatedly within a few seconds
- [ ] Count clicks per minute and write it down — the worksheet asks teams to do exactly this
- [ ] Now separate the thresholds and confirm the clicking stops

**Question this answers:** is `update_interval: 1s` on the BH1750 enough, or does the demo
need a faster interval or a filter removed?

> If it will not chatter, try `update_interval: 500ms`. If it still will not, the light
> sensor may be smoothing internally and session 2's ladder needs rethinking — tell me and
> I will rework that block.

---

## F. Overnight survival

The session 2 opener reads a multi-hour graph. This test proves it exists.

1. Leave the sensor board powered with **Home Assistant running** and connected.
2. Separately, leave the relay board powered with **no** Home Assistant connected to it.
3. Come back the next morning.

- [ ] Sensor board: history graph is continuous, no gaps
- [ ] Relay board: check its uptime sensor or log — **it must not have rebooted**. A board
      rebooting every 15 minutes means `reboot_timeout: 0s` did not take effect
- [ ] Light trace shows the room lights going off and on — that is the session 2 hook

**Question this answers:** does the between-session history actually materialise?

---

## G. Float switch on port 1

- [ ] Plug the Grove adapter into **port 1**. Entity appears as a binary sensor
- [ ] Float down (out of water) vs float up (in water) → note which state each gives
- [ ] Confirm `inverted: true` gives **ON = water present**; flip it if not
- [ ] Jiggle the water surface — the 500 ms debounce filters should stop the entity flapping
- [ ] Confirm which Grove pin the adapter actually uses. Config assumes **GPIO0**
      (SPECIALPORT1-A = CN2.1). If it is on **GPIO1** (CN2.2), change the pin number

**Question this answers:** is the pin and polarity in the config right, and is the fail-safe
trigger in session 2 pointing at the correct state?

---

## H. Relay board

Pins are now **confirmed from the vendor datasheet** (see `firmware/ESP32-C6-RELAY-X1.md`):
relay **GPIO19**, programmable LED **GPIO2**, button **GPIO9**, all active high. This test is
confirmation, not discovery.

- [ ] Relay clicks when the switch entity is toggled from Home Assistant
- [ ] Both LEDs light: the hard-wired relay indicator **and** the GPIO2 programmable LED
- [ ] Onboard button toggles the relay, and works with Home Assistant closed
- [ ] Power from **12 V into the screw terminal with USB unplugged** — board still connects
- [ ] `restore_mode: ALWAYS_OFF` — cut the 12 V with the relay on, restore, relay stays off
- [ ] Read the markings on the relay body and confirm they match what the worksheet tells
      teams to expect: `10A 250VAC` / `10A 30VDC`

> **Do not power USB and the 12 V terminal at the same time** — the datasheet says choose one.
> The worksheet now tells teams to unplug USB before wiring 12 V; verify nothing bad happens
> if someone forgets, so you know how bad the mistake is on the day.

**Question this answers:** does the board run from the charge controller's LOAD pair with the
pump attached, and does it fail safe on power restore?

---

## I. Can the board feel the pump? *(optional, 15 min, do last)*

Groundwork for a possible **vibration reporter** — the board inferring "the pump is actually
running" from the accelerometer, rather than trusting that the relay was commanded on.
Pedagogically this is the strongest unused idea in the kit: it is the difference between
**commanded state and actual state**, which is exactly session 2's fail-safe theme. A relay can
be ON while the pump is seized, unprimed, or unplugged, and nothing in the current design would
notice.

**This test needs no new firmware.** The config already publishes accelerometer values. The
question is purely physical, and it decides whether writing the RMS code is worth anything.

1. Put the sensor board where it would actually live during the workshop, then also try it
   resting against the tubing and on the drip tray beside the container.
2. In Home Assistant, watch the raw acceleration entities. Toggle the pump on and off a few times.

- [ ] Is there **any** visible difference in the acceleration trace between pump on and pump off?
- [ ] If yes, roughly how big, and in which position? Note the best mounting spot
- [ ] Does the difference survive someone bumping the table?

> **The catch to watch for.** The board has a job already: it needs ambient light for the
> flower-farm lighting scenario, open air for humidity, and it carries the float switch. Strapping
> it to a submerged pump conflicts with all three. If vibration is only detectable when the board
> is taped to the pump body, the feature cannot coexist with the rest of session 1 on one board —
> and the honest answer is to drop it, or give the instructor kit a second board for a demo.

**Question this answers:** is there a signal at all, before anyone writes signal processing?

If there is a usable signal, tell me and I will write the vibration component against the
algorithm already specified in `gogo-iot-node/docs/ESPHOME_PLAN.md` — sample at 104 Hz, take
magnitude, remove the gravity baseline, RMS over ~1 s, then hysteresis and persistence. That is
a lambda plus a template sensor, and it needs its own debugging loop, which is why it is not in
tomorrow's image.

---

## Results

| Test | Pass | Notes / values to keep |
|---|---|---|
| A build & flash | | device name observed: |
| B USB name lookup | | seconds to complete: |
| C adopt by `.local` | | resolved: yes / no |
| D two boards unique | | |
| E chattering visible | | clicks/min before hysteresis: |
| F overnight | | relay board reboots overnight: |
| G float switch | | pin: GPIO___ · ON = water present? |
| H relay board | | 12V-only boot OK? · restore_mode OK? |
| I pump vibration | | signal visible? best position: |

## After the test

Values from G and H go into `firmware/*.yaml`. Values from B and E decide two worksheet
questions still open:

- **B** — if the USB lookup is slow or fiddly, we switch to printed MAC stickers and the
  session 1 adoption steps change.
- **E** — if chattering will not show at 1 s, session 2's hysteresis ladder needs a different
  input or a different demonstration.

Either way, the worksheet adoption steps still say "type the IP from the team card"
(`session-1.md` in two places, `session-3.md`, `reference.md`, `index.md`, `record-sheet.md`).
I will rewrite them to the USB-name flow once the test confirms it — that edit is queued in
WORKSHEET-TODO.md and deliberately not done yet, to avoid doing it twice.
