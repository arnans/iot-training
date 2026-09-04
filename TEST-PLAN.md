# Bench test plan — ESPHome provisioning

One session at a desk, two boards, one laptop. Purpose: prove the participant flow works
before committing to a firmware image for ~120 boards, and settle the four things the
worksheets currently assume without evidence.

**Time:** about 2 hours if nothing surprises you. Tests A–D are the critical path; E–H can
follow later if time runs short.

## Before you start

- [ ] GoGo-IoT sensor board, USB-C cable
- [ ] ESP32-C6 relay board, USB-C cable
- [ ] Float switch with its Grove adapter, a glass of water
- [ ] Laptop with Chrome or Edge (Web Serial needs one of those; Firefox will not work)
- [ ] Python with `pip install esphome`
- [ ] A WiFi network you control. **Not** a corporate/university SSID — those usually block
      client-to-client traffic and mDNS, which would make tests C and D fail for the wrong reason
- [ ] Home Assistant reachable from the laptop. If it is a VM, **bridged adapter, not NAT**
- [ ] `firmware/secrets.yaml` filled in from `secrets.example.yaml`

Record results in the table at the bottom.

---

## A. Build and flash the workshop image

```bash
cd firmware
esphome run gogo-iot-workshop.yaml
```

- [ ] Compiles without error
- [ ] Flashes over USB
- [ ] Log shows the device name **with a MAC suffix**: `gogo-iot-xxxxxx`
- [ ] All four I2C sensors report values, no `Communication failed` lines

> **If `spa06_i2c` or `lsm6ds` fail to compile**, the bring-up config may depend on an
> ESPHome version or an external component not pinned here. Check the version that worked
> upstream and pin it in `esphome:` before debugging anything else.

**Question this answers:** does one image build clean and produce a unique name?

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

## H. Relay board pins

The relay and LED GPIOs in `relay-workshop.yaml` are placeholders taken from the WROOM
variant of the same product family. The C6 board's pin map is different.

- [ ] Find the real relay GPIO — vendor listing, wiki, or by toggling candidates from the
      ESPHome console and listening for the click
- [ ] Confirm the onboard button's GPIO and that it toggles the relay
- [ ] Confirm the status LED follows the relay. If the LED is hard-wired to the relay coil,
      delete the `output:`/`light:` blocks
- [ ] Power the board from **12 V into the DC input** (not USB) and confirm it still connects
- [ ] Verify `restore_mode: ALWAYS_OFF` — cut power with the relay on, restore, relay stays off

**Question this answers:** can the relay board be driven from the charge controller's LOAD
pair with the pump attached, and does it fail safe on power restore?

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
| H relay pins | | relay GPIO: ___ LED GPIO: ___ button GPIO: ___ |

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
