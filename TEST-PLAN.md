# Bench test plan — ESPHome provisioning

One session at a desk, two boards, one laptop. Purpose: prove the participant flow works
before committing to a firmware image for **200 boards**, and settle the four things the
worksheets currently assume without evidence.

**Time:** about 2 hours if nothing surprises you. Tests A–D are the critical path; E–H can
follow later if time runs short.

## Already done for you

- **ESPHome 2026.6.5 is installed** on this machine.
- **Both sources compile clean, including through the zone pipeline.** Current builds, with the
  embedded `web_server` assets included: `gogo-iot-red.factory.bin` **0.94 MB**,
  `gogo-relay-red.factory.bin` **0.97 MB**, on 4 MB parts — no larger than before `web_server`
  was added, because the embedded page is only ~13 kB (verified, see test J). Plenty of headroom.
  ESP-IDF toolchains for both C3 and C6 are downloaded and the build cache is warm, so rebuilds
  are quick. `build-zones.py` is the production path (six binaries into `dist/`); it refuses to
  run until `zones.yaml` has real passwords.
- **One expected warning**, not a problem: `GPIO9 is a strapping PIN and should only be used
  for I/O with care`. GPIO9 is the relay board's onboard button, per the vendor datasheet.
  A momentary press while running is harmless; only holding it during power-up enters the
  bootloader.
- **`firmware/secrets.yaml` exists** with a real generated OTA password and fallback AP password.
  It is gitignored.

> **The one thing to do before flashing:** `cp zones.example.yaml zones.yaml` and put your bench
> network's SSID/password under the `red:` zone (the other two can stay as placeholders for
> tomorrow — pass `--zone red`). Then `python build-zones.py --zone red` and flash from `dist/`.
> The rebuild is incremental, not another 4 minutes.
>
> The ESPHome API runs **without encryption** — no key to generate, print on a team card, or
> type in during adoption. `firmware/secrets.yaml` no longer carries WiFi lines either; that
> lives entirely in `zones.yaml` now.

## Before you start

- [x] GoGo-IoT sensor board, USB-C cable
- [x] ESP32-C6 relay board, USB-C cable
- [x] Float switch with its Grove adapter, a glass of water
- [x] Laptop with Chrome or Edge (Web Serial needs one of those; Firefox will not work)
- [x] Copy `zones.example.yaml` to `zones.yaml` and fill in your bench network's SSID/password
- [x] A WiFi network you control. **Not** a corporate/university SSID — those usually block
      client-to-client traffic and mDNS, which would make tests C and D fail for the wrong reason
- [x] Home Assistant reachable from the laptop. If it is a VM, **bridged adapter, not NAT**

Record results in the table at the bottom.

```bash
cd firmware
cp zones.example.yaml zones.yaml       # fill in the three SSIDs/passwords (for the bench, any
                                       # zone may point at your test network)
python build-zones.py --zone red       # builds sensor + relay for one zone
python build-zones.py --flash red sensor COM7
python build-zones.py --flash red relay  COM8
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

- [x] Flashes over USB without holding any button (native USB should reset it automatically) —
      **confirmed repeatedly**, including reflashing a board that was already running. One
      `esptool` failure was seen once and did not recur; treat it as a busy/held COM port rather
      than a bootloader problem. Good news for the 200-board flashing run
- [x] Log shows the device name **with zone and MAC suffix**: `gogo-iot-red-6749a4`
- [x] All four I2C sensors report values, no `Communication failed` lines
- [x] Board joins WiFi

> If the board will not enter the bootloader on its own, hold BOOT while plugging in.

**Question this answers:** does the image run on real hardware and see all four sensors?

---

## B. The participant USB lookup — the critical test

This is the step every team performs twice, and the whole no-sticker plan rests on it.

1. Open <https://web.esphome.io> in Chrome/Edge.
2. **Connect** → pick the serial port → **Logs & Console**.
3. Press **Reset device** — the button *in the browser window*. **Not** the button on the board,
   and no need to unplug anything. See the bench finding below; this ordering is the whole trick.

- [x] The port appears in the browser's picker without installing a driver
- [x] The log shows the device name clearly enough for a participant to copy it down
- [x] Note **how far into the log** the name appears — if it scrolls past, participants will
      miss it and the worksheet needs to say "press the reset button, then read the first lines"
- [ ] Time the whole step from plugging in to having the name written down

**Question this answers:** can a non-technical participant get their board's name in under
two minutes, with no software installed?

> If this is awkward, the fallback is a printed sticker per board from `esptool read_mac`
> during the flashing run. Decide now — it changes the kit prep, not the worksheet flow.

### Bench result: the name had to be made findable

**The name was not in the log at all** on the first attempt. Nothing prints the hostname at
`INFO`: it appears only in the WiFi component's config dump, tagged `[C]`, and ESPHome's levels
run `NONE < ERROR < WARN < INFO < CONFIG < DEBUG < VERBOSE` — so `logger: level: INFO` filters it
out. The comment in `gogo-iot-workshop.yaml` claiming INFO "keeps the device name visible" was
simply wrong.

Raising the level to `CONFIG` would surface it, but buried among every component's config dump
(i2c, each sensor, api, wifi…) — worse for a participant, not better. Instead both firmware files
now log the name explicitly from `esphome: on_boot:` as a three-line banner at INFO:

```
[15:43:09][I][main:375]: ================================================
[15:43:09][I][main:375]: =====  DEVICE NAME: gogo-iot-red-6749a4  =====
[15:43:09][I][main:375]: ================================================
```

It lands on **line 4 of the boot log, before WiFi even starts scanning**, so the "press reset and
read the first lines" fallback wording is not needed, and neither is the printed-sticker plan.

**Consequence, now resolved.** The board's **IP** sat in that same CONFIG-level dump, so it was
absent at INFO too — which quietly broke test C's "try the IP from the USB log" fallback. Both
firmware files now log the IP as a matching banner, hung off the IP text sensor's `on_value` so
the value is guaranteed to exist (it cannot go in the `on_boot` banner — WiFi has not associated
yet, so there is no address to print):

```
=====  IP ADDRESS: 192.168.8.xxx  =====
```

It appears a second or two after the name banner, when WiFi connects, and re-prints if DHCP ever
hands out a different address. That address is also where the board's own **`web_server`** page
now lives — see the note under test A.

### Bench result: you must reset from the browser, not the board

**An already-running board shows nothing.** Both banners print at boot, so opening Logs & Console
on a board that is already up and connected gives a **blank window** — at `INFO` an idle board
prints essentially nothing. A participant would reasonably conclude it is broken.

The fix is one button, but it has to be the right one:

- ✅ **"Reset device" in the web.esphome.io window** — works. The page keeps its serial session
  across the reset and captures the boot from the first line.
- ❌ **The reset button on the board** — does *not* work. These chips use native USB
  Serial/JTAG, so resetting the chip resets the USB peripheral too: the port re-enumerates, the
  browser's handle dies, and the boot output is gone before anything can reattach.
- ❌ **Unplug and replug** has the same problem, and additionally forces the participant back
  through the port picker — by which time the banners have already scrolled by.

**So the worksheet order is: connect first, then reset from the browser.** That is the opposite
of the instinctive order (reset the board, then go look), and it is the difference between the
name appearing on line 4 and a blank screen.

---

## C. Adopt in Home Assistant

Decided on the bench: **pick the board's discovered card**, matching the six-character suffix from
the USB banner. Manual entry is the fallback. No encryption key either way.

**The exact click path, as walked on the bench** — a worksheet author needs this verbatim, because
the fallback is four levels deep:

1. **Settings → Devices & services.** Discovered boards appear here as cards. **If yours is
   listed, click it and you are done** — this is the path essentially every team will take.
2. Not there? **+ Add integration** → type **ESPHome** (not "ESP-NOW", which is a different
   Espressif protocol and will find nothing).
3. ESPHome's own page opens, listing discovered devices again. Still not there? **Add device**.
4. A popup shows the discovered list once more — pick from it, or choose **"Setup another
   instance of ESPHome"**.
5. That opens a dialog: type the node name, **without `.local`** (`gogo-iot-red-6749a4`). Added.

- [x] The board appears in the discovered picker, named clearly enough to match the suffix —
      **both boards appeared on their own**, no hunting required
- [x] Adopting from the picker works with no key prompt — confirmed, encryption removal is clean
- [x] Manual entry works too — **verified, and the name resolves without the `.local` suffix**.
      Typing the bare `gogo-iot-red-6749a4` adds the board successfully. Since every team's VM is
      a clone of this same image — same OS, same resolver — the bare name is safe to put in the
      worksheet, and it is one less thing for a participant to type.
      (An earlier note here claimed `<name>.local` would not resolve from the Windows browser.
      **That was a wrong diagnosis** — at the time nothing was listening on port 80 because
      `web_server` had not been added yet. Windows resolves these names fine; see test J.)
- [x] Device is added, entities appear with Thai names — 10 entities on the sensor board,
      5 on the relay, matching the config exactly at the time (the sensor board is **11** since
      the pump-sensitivity select was added in test I)
- [x] Rename the device to a team name; entity IDs stay stable — renaming from the UI works
- [x] Unplug the board, wait 1 min, plug back in → returns to available on its own — **confirmed**:
      rejoined by itself and resumed streaming values, no intervention. This is the DHCP-plus-mDNS
      reconnect the whole no-static-IP design rests on, and it is a preview of test F

> **Watch the rename dialog when writing the worksheet.** Renaming a device in HA can offer to
> rename the *entity IDs* to match. Which button a team presses was not recorded here, and it
> decides whether their entities stay `sensor.gogo_iot_red_6749a4_*` or become
> `sensor.<team name>_*`. The instructor recorder globs use wildcards
> (`sensor.*humidity*`) so they survive either way — but any worksheet step that names an
> entity_id does not. Pick one answer and put it in the worksheet.

> **If `.local` does not resolve** the problem is almost always the network or the VM's
> adapter mode, not the firmware. Try the IP — it is now in the USB log (see test B) and on the
> board's own web page; if that works, mDNS is being blocked and NETWORK-REQUIREMENTS.md item 1
> is the fix.

**Question this answers:** does hostname adoption work end to end, and does it survive a
reboot the way DHCP-with-mDNS is supposed to?

---

## D. Two boards, no collision

Flash the **same** image to the relay board's slot in your bench setup — or, if the relay
board is not ready, flash the sensor image to any second ESP32 you have.

- [x] Second board gets a **different** hostname from the same binary — `gogo-iot-red-6749a4`
      (sensor, C3) and `gogo-relay-red-9d8b28` (relay, C6). Suffixes are distinct and the zone
      colour is in both names
- [x] Both adopt into Home Assistant simultaneously — 2 devices, 15 entities (16 now), both stable
- [x] In **Settings → Devices & services**, note what the *discovered* card list looks like with
      two boards on the network. On the day a team sees **only its own zone's** boards, since
      zones are isolated VLANs: 200 boards ÷ 3 ≈ **~67 cards**, not the whole room
- [x] **Is that list searchable/filterable?** **Settled by workflow rather than by measurement.**
      The adopted-devices page has a search box (confirmed); whether it also filters *discovered*
      cards was not measured, and no longer gates anything. The participant flow is: look on
      Devices & services for your card and click it; if you cannot find it, **+ Add integration →
      ESPHome**, which ends in a manual-entry box for the name. Either way a team gets there

**Question this answers:** is the MAC suffix genuinely unique, and how hard is it to find your
own board among a zone's worth of discovered cards? (The pick-vs-type question is settled: pick
from the list, manual entry as fallback — see test C.)

> **Still worth doing at the venue, not on the bench:** the ~67-card case cannot be reproduced
> with two boards. The first real look at a crowded discovered list will be the acceptance test.

> **If you have two networks on the bench**, also build `--zone green` pointed at the second
> network and confirm a green board does **not** appear on a laptop joined to the red network.
> That is the zone-isolation property the whole network design rests on. Not required tomorrow;
> the venue acceptance test covers it.

---

## E. Chattering is visible — the session 2 lesson

**This test's original premise was wrong, and the correction matters.** It assumed the lesson
depends on the relay flickering *by itself* when a hand hovers near the threshold. It does not:
[session-2.md:83](docs/session-2.md#L83) already has the Hardware role deliberately wave a hand up
and down at the threshold for a minute — "เหมือนเมฆบางลอยผ่านตอนพลบค่ำ", like thin clouds drifting
past at dusk — while the Driver counts toggles. The fluctuation is **manufactured by the student
on purpose**, and the worksheet says so.

**Bench observation:** the BH1750 reading is *stable*. It tracks a hand faithfully and does not
jitter on its own. So spontaneous chattering will not happen — and that is fine, because the
worksheet never asked for it.

This also rules out the remedy this section used to suggest. Dropping to
`update_interval: 500ms` was aimed at a value that was too *smoothed*; the value is not smoothed,
it is simply not noisy. Faster sampling would track the hand more closely, not invent fluctuation.
**Leave the interval at 1 s.**

A deterministic, student-driven demo is also the better outcome at this scale: a lesson that
depended on ambient sensor noise would behave differently at all 100 tables depending on their
lighting.

1. In Home Assistant create one automation: light **Below** a threshold near room level →
   switch **turn on**. And a second: **Above** the *same* value → **turn off**.
2. Hold a hand at the height where the reading sits right at the threshold and waver it.

- [ ] With a hand **deliberately wavered** at the threshold, the relay toggles repeatedly
- [ ] Count toggles per minute and write it down — the worksheet asks teams to do exactly this,
      and the number belongs on the record sheet
- [ ] Now separate the thresholds, waver the hand the same way, and confirm the count drops.
      The worksheet's pass mark is **≤2 toggles per minute** ([session-2.md:93](docs/session-2.md#L93))

**Question this answers, restated:** does a deliberately wavered hand produce clearly more than
2 toggles a minute with both thresholds equal, and clearly ≤2 once a gap is opened? That is the
whole lesson — the deadband has to be *felt* as "I now have to move my hand much further."

> **Still to do:** the automations have not been built yet, so the two counts are unmeasured.
> Nothing observed so far suggests the lesson is in trouble.

---

## F. Overnight survival

The session 2 opener reads a multi-hour graph. This test proves it exists.

1. Leave the sensor board powered with **Home Assistant running** and connected.
2. Separately, leave the relay board powered with **no** Home Assistant connected to it.
3. Come back the next morning.

- [ ] Sensor board: history graph is continuous, no gaps
- [ ] Relay board: check the `เวลาทำงาน (uptime)` entity — **it must read the full elapsed
      time**. If it keeps resetting to near zero, `reboot_timeout: 0s` did not take effect
- [ ] Light trace shows the room lights going off and on — that is the session 2 hook

**Question this answers:** does the between-session history actually materialise?

---

## G. Float switch on port 1

- [x] Plug the Grove adapter into **port 1**. Entity appears as a binary sensor
- [x] Float down (out of water) vs float up (in water) → note which state each gives
- [x] Confirm the config gives **ON = water present**; flip it if not
- [x] Jiggle the water surface — the 500 ms debounce filters should stop the entity flapping
- [x] Confirm which Grove pin the adapter actually uses. Config assumes **GPIO0**
      (SPECIALPORT1-A = CN2.1). If it is on **GPIO1** (CN2.2), change the pin number

### Bench result

**Wiring, as actually assembled.** The float switch has two bare wire ends. They land on the
**outer two positions** (Signal, Ground) of the adapter's **4-way terminal block**; a Grove cable
runs from the adapter's other end to **special port 1** on the GoGo-IoT board.

**Pin: GPIO0 confirmed.** The switch moves that pin, so the netlist assumption was right and no
change to `number:` was needed.

**Pull-up: internal only, and it is load-bearing.** There is no external pull-up on the switch or
the adapter. The ESP32-C3 supports internal pull-ups on every GPIO including GPIO0 (it has no
input-only pins), and `pullup: true` was already set — without it the input floats. The internal
pull-up is weak (~45k), so a **10k external pull-up to 3.3 V** was considered as insurance against
noise on a metre of cable beside a water container.

**Not needed.** Jiggling the water surface produced no state change at all — the 500 ms
`delayed_on`/`delayed_off` filters absorb it completely. No external resistor in the kit; the
internal pull-up plus the filters is enough.

**Polarity: the float closes the switch when DOWN (dry), opens when it RISES (wet).** So wet =
open = pin pulled HIGH. `inverted:` is now **`false`**, giving ON = water present, matching what
the worksheets assume. **Re-flashed and re-checked: dry reads OFF, water reads ON.** Confirmed on
the running firmware, not just in config.

> **Fail-safe consequence, and it is the important part.** A cut wire or unseated Grove plug
> leaves the pin HIGH — **identical to "water present"**. A wiring fault therefore reads as
> safe-to-pump, and would let the pump run dry. Flipping `inverted` does not help; this follows
> from which way round the float closes. Two mitigations, not exclusive:
>
> 1. **Kit prep** — if the float can be mounted inverted (many can), closed-when-wet makes a
>    broken wire read "dry" and fail safe. Decide before assembling 100 kits.
> 2. **Session 2's fail-safe automation** must require *positive confirmation* of water and treat
>    `unavailable`/`unknown` as dry, rather than trusting a single OFF. That is a better version
>    of the lesson anyway.

### Second pass (8 Sep 2026) — float cylinder flipped, mitigation 1 taken

Roger pulled the retaining clip and **flipped the float cylinder on its rod**, so the switch now
**closes when the float RISES (wet)** and opens when it drops (dry). Wet = closed = pin LOW.
Firmware changed to `inverted: true` (ON = water present again) and gained
`device_class: moisture`, so Home Assistant shows **Wet / Dry** instead of On / Off — the flip
briefly made "Off = has water", and the device class removes that confusion in either orientation.

Everything in the first pass about pin, pull-up and filters still stands. The fail-safe
consequence above is now reversed: a cut wire, an unseated Grove plug, or no switch at all reads
**Dry**, and the pump stays off. Kit prep must flip the cylinder on **every** float; a kit
assembled with an unflipped float reads backwards, which the first item below catches.

- [x] Re-flash and re-check: float up in water → **Wet**; float lifted out → **Dry**. Confirmed
      on the running firmware (Roger, 8 Sep 2026)
- [x] **No switch plugged in** (Grove cable out of port 1) → **Dry**. This is the fail-safe test
      that was impossible before the flip. Confirmed on the running firmware (Roger, 8 Sep 2026)
- [x] Pull one bare wire out of the adapter's terminal block while wet → **Dry** within ~0.5 s.
      Confirmed on the running firmware (Roger, 8 Sep 2026). Test G complete
- [x] Board's own web page: **ON / OFF**, ON = wet. ESPHome's page ignores the device class,
      so the same switch reads ON/OFF on the board and Wet/Dry in Home Assistant. Session 1's
      Activity 1 note and the trigger step now bridge the two vocabularies (Roger, 8 Sep 2026)

**Question this answers:** is the pin and polarity in the config right, and is the fail-safe
trigger in session 2 pointing at the correct state?

---

## H. Relay board

Pins are now **confirmed from the vendor datasheet** (see `firmware/ESP32-C6-RELAY-X1.md`):
relay **GPIO19**, programmable LED **GPIO2**, button **GPIO9**, all active high. This test is
confirmation, not discovery. **All three are now bench-confirmed on real hardware**, not just
read off the PDF.

> **Design change made during this test: the GPIO2 LED now shows WiFi connection status.** It
> originally mirrored the relay, but the relay's own hard-wired indicator already does that from
> the coil an inch away, so the mirror added nothing. It now reads **steady lit = on WiFi,
> blinking = WiFi lost, dark = no power or no firmware** — so a team can tell whether their board
> is connected without a laptop, and an instructor can read the room from the front. With ~100
> teams that is the support question that matters most. Session 2's worksheet text survives
> unchanged: it says the LED on the relay board stands in for the garden lamp, and the relay's
> own indicator still lights whenever the relay closes.
>
> The first attempt used ESPHome's `status_led:` and **failed on the bench** — see the finding
> below. It is now driven explicitly.

- [x] Relay clicks when the switch entity is toggled from Home Assistant
- [x] Both LEDs light: the hard-wired relay indicator **and** the GPIO2 programmable LED —
      confirmed, which is what proved `led_pin: GPIO2` correct. **The GPIO2 LED has since been
      repurposed** (see below), so on the current firmware only the relay's own indicator
      follows the relay
- [x] Onboard button toggles the relay, and works with Home Assistant closed — **verified with
      the HA VM shut down**. The toggle is an on-device ESPHome automation, no network involved.
      Session 2's failure lab depends on exactly this
- [x] **Re-check on the re-driven LED — confirmed on hardware.** Walked out of WiFi range: GPIO2
      blinks, and returns to steady lit on rejoin. The first version of this failed; see below
- [x] **The blink starts several seconds after the board is actually out of range** — observed
      and **accepted, no change**. The ESP32 does not know it has lost the AP until it has missed
      enough beacons for ESP-IDF's inactive/beacon timeout to fire; only then does the WiFi state
      machine raise the warning the LED reads. So "unreachable by IP" happens first and "blinking"
      follows. Harmless here — nobody is timing it, and a fast-twitch LED would flicker on every
      momentary fade. **Worth knowing for the day:** a board that has just been unplugged or moved
      shows steady-lit for a few seconds before it admits the problem, so tell a helper to look
      twice rather than trust the first glance
- [x] Power from **12 V into the screw terminal with USB unplugged** — **confirmed: the board
      boots and connects normally on 12 V alone.** This is how every relay board runs on the day,
      off the charge controller's LOAD pair, so it is the configuration the whole of session 2
      depends on
- [x] `restore_mode: ALWAYS_OFF` — **confirmed: the relay is always off after a boot**, never
      restores its previous state. This is the safety property that stops a pump restarting by
      itself after a power cut, and it is now proven in firmware. **Confirmed on BOTH supplies —
      5 V over USB and 12 V on the screw terminal.** The relay is off at every power-up regardless
      of how the board is fed, which is the form the property has to hold in on the day
- [x] Read the markings on the relay body and confirm they match what the worksheet tells
      teams to expect: `10A 250VAC` / `10A 30VDC` — **they match**

### Bench result: `status_led:` cannot give a visible blink on an inverted pin

**Observed:** walking away from the WiFi until the board was unreachable by IP, **the LED stayed
lit. It never blinked.**

**Cause, found in the ESPHome source, not guessed.** `status_led:` writes the pin itself, and a
warning — which is what WiFi loss is (`wifi_component.cpp` sets `status_set_warning` for
"waiting to reconnect" / "scanning" / "associating") — is **250 ms on, 1250 ms off**:

```cpp
} else if ((app_state & STATUS_LED_WARNING) != 0u) {
  this->pin_->digital_write(now % 1500 < 250);
```

`inverted: true` was added to make the healthy state the lit one. It does that — but it inverts
**every** write, including those. The blink came out as *lit 83% of the time with a 250 ms wink
once every 1.5 s*, which at a glance, on a small SMD LED, while walking away, is indistinguishable
from steady. **Inverting the pin inverts the duty cycle too.** The healthy state was right and the
fault state was invisible.

Two things ruled out while tracing it, so they need no re-test: it is **not** a stalled component
(`StatusLED::loop()` calls `disable_loop()` when healthy, but `Application::service_status_led_slow_()`
re-dispatches it every 100 ms and re-enables it the moment a warning bit appears), and it is **not**
the fallback AP masking the fault (COOLDOWN/SCANNING/CONNECTING all keep the warning flag set).

**Fix, now in `relay-workshop.yaml` and compiling clean at 0.97 MB — unchanged size.** `status_led:`
is gone; the LED is a plain `output:` plus an `internal:` binary `light:`, driven by a 400 ms
`interval:` that turns it on when `wifi.connected:` and toggles it otherwise. That gives a
**symmetric 0.8 s blink**, which cannot be mistaken for steady. **Re-flashed and re-walked out of
range: confirmed working**, with the beacon-timeout lag noted in the checklist above.

**WiFi only, on purpose — a decision, not an oversight.** `status_led:` also treats "no Home
Assistant client connected" as a warning. The relay board is *designed* to sit on 12 V overnight
with no HA (that is what `reboot_timeout: 0s` and test F exist for), so including the API would
have ~100 boards blinking all night for a condition that is normal. HA being down is already
visible in HA. The LED answers one question: **is my board on the network?**

### Bench result: USB and 12 V together is harmless — keep the instruction, drop the alarm

The datasheet says "DC 7-60V **or** TYPE-C 5V (choose one)", and the worksheet tells teams to
unplug USB before wiring 12 V. This test existed to find out **how bad the mistake is** when a team
forgets, because with ~100 tables somebody will.

**Answer: it is not bad at all.** Measured on the board's 5 V rail:

| Source | 5 V rail |
|---|---|
| USB alone | **5.04 V** |
| 12 V terminal alone | **5.12 V** |

**80 mV apart.** Two sources that close together simply share the rail; there is no voltage fight
to damage anything. Plugging USB into a board already running on 12 V was then tried directly:
**the board carried on normally and the serial port enumerated and worked as usual.**

**Consequences, and the second one is the useful one:**

1. **The worksheet keeps one-supply-at-a-time as the normal practice, but no longer as a
   prohibition.** [session-1.md:102](docs/session-1.md#L102) said `ห้ามต่อพร้อมกัน` ("do not connect
   both"); it now says the board is *designed* for one source, and adds that connecting both by
   accident is harmless — at most the board restarts. Same practice, no false alarm. A helper who
   finds a team with both connected says "tidy that up", not "you may have damaged the board".
   **No board is lost to this mistake.**
2. **Support on the day just got easier.** A helper can plug a laptop into a board that is already
   wired to the 12 V rail — to read the boot banner, check the name, or reflash — **without
   tearing down the team's wiring first.** For a room of ~100 tables that removes a genuinely
   annoying step from every debugging visit.

> **The reverse direction — 12 V applied to a board already on USB — was not separately tried,
> and does not need to be.** Steady state is identical to the case that was; only the turn-on
> transient differs, and the 12 V regulator simply takes over the rail from 80 mV above it.
> **Worst case is that the board resets** — which costs a team nothing but the few seconds it
> takes to reconnect, since `restore_mode: ALWAYS_OFF` means a reset leaves the relay safe anyway.

**Question this answers:** does the board run from the charge controller's LOAD pair with the
pump attached, and does it fail safe on power restore?

---

## I. Calibrate the vibration reporter *(20 min, do last)*

**The reporter is built and in the image.** It answers "is the pump *actually* running?" from
the accelerometer, rather than trusting that the relay was commanded on — a relay can be closed
while the pump is seized, unprimed or unplugged. Two entities appear in Home Assistant:

| Entity | What it is |
|---|---|
| `ความสั่นสะเทือน (vibration)` | RMS deviation from the slow baseline, in milli-g, published every 1 s |
| `ปั๊มกำลังทำงาน (pump running)` | The verdict, with hysteresis and persistence |

What needs your bench time is the **thresholds**, which are guesses right now:
`vib_on_threshold: 25` and `vib_off_threshold: 12` milli-g, both in the `substitutions:` block
at the top of `gogo-iot-workshop.yaml`.

1. Board sitting where it would normally live. Pump **off**. Read the vibration figure for a
   minute — this is your noise floor.
2. Pump **on**. Read it again.
3. Try the board resting against the tubing, and on the drip tray beside the container.

- [ ] Noise floor with pump off: ______ mg
- [ ] Reading with pump on: ______ mg, best position: ______
- [ ] Set `vib_on_threshold` roughly two-thirds of the way from floor to running, and
      `vib_off_threshold` roughly one-third. Re-flash and confirm the verdict flips cleanly
- [ ] Knock the table — does the verdict falsely trip? The 2 s `delayed_on` should absorb it
- [ ] Pump off — does the verdict clear within the 5 s `delayed_off`?

### Bench result: the signal is separable, and the shipped guesses work

**Tried on the real pump: it works.** The verdict entity follows the pump. That settles the
question this test existed to ask — the accelerometer *can* tell a running pump from a still one,
so the two entities stay in the image and the "pull them rather than ship something that reads
noise" fallback is off the table.

It also means **`vib_on_threshold: 25` / `vib_off_threshold: 12` need no change** — see the
measured numbers and the reasoning below.

### The numbers, and why the thresholds stay as they are

- **Noise floor, pump off:** **3-8 mg**
- **Pump running:** **~20-25 mg**, measured with a **deliberately soft, loosely-coupled mounting**

**Kept as the default: 25 / 12.** They are now the **MEDIUM** level of a three-way sensitivity
select — see below — so this *did* become a firmware change after all, but not to the numbers.

Read naively, 20-25 running against a 25 threshold looks like no margin at all, and the arithmetic
this test prescribed would drop `on` to about 16. **That reading is wrong, because of how the
measurement was taken.** The running figures come from a soft mount — a worst case, not the normal
one. Mounted the way a team will actually have it, against the tubing or on the drip tray, the
running figure sits higher, and 25 is a fair operating point rather than a ceiling.

Keeping 25 is also the **conservative** direction. The two failure modes are not symmetric:

| Threshold too high | Threshold too low |
|---|---|
| A very weakly-coupled pump is not noticed | A knocked table reports a pump that is not running |

The first is a diagnostic that stays quiet; the second actively misinforms a team debugging their
watering rule. **`off` at 12 is the number that had to be right**, and it is — 4 mg clear of the
noisiest 8 mg idle reading, so ambient table noise cannot hold the verdict on.

> **Recorded because it was nearly changed:** `vib_on` was briefly set to 16 on the arithmetic
> above, then reverted on the bench-holder's judgement about the mounting. Anyone re-deriving the
> thresholds from the 20-25 figure alone will reach 16 again — the figure is soft-mount data, and
> the number to trust is the floor.

### Then: a sensitivity selector, so a team can fix the verdict without a reflash

The bench argument above — "the real mounting couples harder than the soft-mount figures" — is a
statement about *one* mounting. On the day there are ~100, and the soft-mount case *will* happen
at some tables. Rather than pick one threshold for all of them, the thresholds are now chosen at
runtime from a **`select` entity, `ความไวตรวจจับปั๊ม (pump sensitivity)`**, visible in Home
Assistant (device page → *Configuration*) and on the board's own web page:

| Level | `on` > | `off` < | For |
|---|---|---|---|
| **สูง (high)** | 15 mg | 10 mg | soft mount or quiet pump; `off` is only 2 mg above the noisiest idle, so some knock false-positives are accepted |
| **กลาง (medium)** — default | 25 mg | 12 mg | the bench-checked pair |
| **ต่ำ (low)** | 40 mg | 20 mg | hard-coupled mount or a table that shakes |

**How it is built**, for whoever touches it next: the six numbers are `substitutions:` at the top
of the file; the live pair lives in two `globals:`; the verdict lambda reads the globals; the
select's `on_value` writes them, switching on the option **index** so the Thai labels can change
freely. It is `optimistic` (nothing to confirm against) and `restore_value: true`, and ESPHome
republishes the restored option at boot, which is what seeds the globals before the first verdict
— verified in the installed template-select source, not assumed. Changing level also clears the
hysteresis state so the next 1 s report judges fresh against the new band.

- [x] **Re-flashed**, and the select appears in HA and as a dropdown on the board's web page —
      **confirmed working on the bench**
- [x] Changing the level changes the verdict — **confirmed, "works well"**
- [ ] Boot log shows `pump sensitivity -> กลาง (medium) (on > 25 mg, off < 12 mg)` on startup —
      not separately checked; cosmetic
- [x] Power-cycle with a non-default level selected — **it comes back on the same level.
      Confirmed on hardware.** This is the property that matters on the day: every board goes dark
      overnight, and a team's choice now survives it. `restore_value` verified in source *and* on
      the bench

> **On "the margin is unclear because of the filtered delay":** that is the verdict entity's
> `delayed_on: 2s` / `delayed_off: 5s` doing their job — they deliberately hide short excursions,
> so the binary cannot be used to find the thresholds. The raw
> `ความสั่นสะเทือน (vibration)` number is unfiltered by those delays and is the one to read, which
> is what the figures above are.

**Question this answers, and the answer:** is the signal separable at all? **Yes.** The real
thresholds turn out to be the ones already in the file.

---

## J. The board's own web page

Added after the plan was written. Every board now runs `web_server:` and serves live values —
and, on the relay board, a working switch — at its own address, with no Home Assistant involved.
Three jobs: teams see sensors react in their first fifteen minutes; it is the support fallback
when a team's HA is broken; and session 3's "open the network box" gets a concrete demonstration.

- [x] Page loads and shows live sensor values, updating in real time
- [x] Relay board's page can toggle the relay
- [x] **`local: true` actually embedded the assets — verified.** Devtools → Network, with
      *Disable cache* ticked, shows exactly two requests, both to the board: the document
      (13.2 kB) and an `events` SSE stream (1.5 kB) that pushes live state. **Nothing reaches an
      external CDN**, so the page will work at a venue with no internet.

      This also explains why the binaries did not grow: the whole local bundle is ~13 kB, not the
      hundreds of kB assumed. The "suspicious" sizes were never a problem.

### Addressing it — three forms work, and one has a trap

| What you type | Works? |
|---|---|
| `192.168.8.102` | ✅ |
| `gogo-relay-red-9d8b28/` | ✅ — **the trailing slash is mandatory** |
| `gogo-relay-red-9d8b28.local` | ✅ |
| `gogo-relay-red-9d8b28` | ❌ — becomes a **web search** |

The trap is the last row, and it will hit every participant who does the obvious thing. A string
with no dot and no slash is treated by Chrome/Edge as a search query, not a hostname, so the team
lands on a search results page rather than their board. `http://gogo-relay-red-9d8b28` also works,
for the same reason the slash does: it forces URL interpretation.

> **Two different forms for two different boxes — call this out in the worksheet.** The browser
> needs a dot or a slash. Home Assistant's manual-entry Host field needs **neither** — the bare
> name is what works there (test C). Teaching one form for both boxes will break one of them.

---

## Open risk found on the bench: `homeassistant.local` is not safe as a worksheet instruction

Four worksheet files tell participants to open `http://homeassistant.local`
([session-1.md:16](docs/session-1.md#L16) and [:198](docs/session-1.md#L198),
[session-2.md:12](docs/session-2.md#L12), [reference.md:54](docs/reference.md#L54)).

**Demonstrated broken during this session.** With a second Home Assistant on the bench network (a
Raspberry Pi), `homeassistant.local` resolved to **the Pi**, not the bench VM. Hunting for a
renamed `homeassistant-2.local` found nothing.

On the day this is worse, not better: every team's VM is a clone of the same image with the same
hostname, so **~34 machines per zone all claim `homeassistant`** on one VLAN. mDNS conflict
resolution renames the losers (`homeassistant-2`, `-3`, …) by **boot order** — unpredictable, not
tied to any team, and liable to shuffle after an overnight power cycle. A team could silently open
a neighbour's dashboard.

**The fix is already sitting on screen.** The HAOS boot console prints the VM's IP at every boot,
live and correct (`192.168.8.163` on the bench). The worksheets can say "read the address shown on
your VM's screen" instead of naming a hostname, which is immune to the whole problem and also
survives DHCP handing out a different address between days.

**Decided: option 1 — the IP from the VM console.** No per-team setup, immune to the collision
entirely, and self-healing when DHCP hands out a different lease. The rejected alternative was
having each team rename their VM at first boot, which asks ~100 teams to each perform a config task
correctly to prevent a problem they cannot see, and whose failure mode is the same silent one.

**Done — all four spots changed, plus the record sheet:**

| File | Now says |
|---|---|
| [session-1.md:16](docs/session-1.md#L16) | wait for the VM screen to show the IP, **write it on the record sheet**, then browse to it |
| [session-1.md:206](docs/session-1.md#L206) | the phone opens "the same address you wrote down" |
| [session-2.md:12](docs/session-2.md#L12) | read the address off the VM screen again — **explicitly warns it may differ from yesterday** |
| [reference.md:56](docs/reference.md#L56) | IP first; names `homeassistant.local` only to say **do not use it**, because it is duplicated room-wide |
| [record-sheet.md:9](docs/record-sheet.md#L9) | new field: the team's HA address, with a **second blank for day 2** |

No port is needed — the OVA deliberately serves on **port 80, not 8123**
([hass/README.md:48](hass/README.md#L48)), so a bare `http://<IP>` is the whole address.

---

## Results

| Test | Pass | Notes / values to keep |
|---|---|---|
| A build & flash | ✅ | device name observed: `gogo-iot-red-6749a4` |
| B USB name lookup | ✅ | name is line 4 of the boot log, via the `on_boot` banner added for this. seconds to complete: |
| C adopt | ✅ | adopted from the **discovered card**, no key prompt, entities correct. Manual-entry fallback verified — **bare node name works, no `.local` needed**. Rename OK. Power-cycled 1 min → rejoined and resumed streaming unaided |
| D two boards unique | ✅ | `gogo-iot-red-6749a4` + `gogo-relay-red-9d8b28`, both adopted at once, 15 entities. Crowded-list behaviour deferred to the venue |
| E chattering visible | | clicks/min before hysteresis: |
| F overnight | | relay board reboots overnight: |
| G float switch | ✅ | pin: **GPIO0** · ON = **Wet** = water present (`inverted: true`, `device_class: moisture`) · float cylinder **flipped at kit prep** so the switch closes when UP/wet · internal pull-up only, **no external resistor needed** — 500 ms filters absorb surface jiggle entirely · broken wire / unplugged switch reads **Dry**, fails safe · Wet / Dry and **unplugged switch → Dry** confirmed after the flip · board's own page says **ON/OFF** (ON = wet), HA says Wet/Dry · pulled wire → **Dry** confirmed; all second-pass checks pass (8 Sep 2026) |
| H relay board | ✅ | pins GPIO19/2/9 bench-confirmed · relay + button + LEDs OK · button works with HA down · `restore_mode: ALWAYS_OFF` ✅ · relay markings match `10A 250VAC` / `10A 30VDC` ✅ · **status LED: first version failed** — stayed lit out of range, because `inverted:` also inverts `status_led`'s 250/1250 ms blink; re-driven from an `interval:` as a symmetric 0.8 s blink on `wifi.connected` — **re-flashed and re-walked, works** · blink onset lags going out of range by several seconds (beacon timeout, accepted)  · **12 V-only boot ✅** — runs and connects on the screw terminal with USB unplugged, the day-of configuration · `restore_mode` re-confirmed on **both** supplies · **USB + 12 V together is harmless** — rails measured 5.04 V (USB) vs 5.12 V (12 V), 80 mV apart; board and serial port both fine, so the mistake costs nothing and a helper may plug in a laptop without unwiring the table |
| I vibration calibration | ✅ | **signal is separable — verdict follows the real pump** · floor **3-8 mg**, running **~20-25 mg**, but measured on a deliberately soft mount · 25 / 12 kept as the **MEDIUM default** of a new three-level **sensitivity select** (high 15/10 · medium 25/12 · low 40/20), chosen in HA or on the board's web page · **re-flashed, selector works, choice survives a power cycle** |
| J board web page | ✅ | live values ✅, relay control ✅, name-as-URL ✅ (trailing slash or `.local` required — bare name becomes a web search). `local: true` verified: 2 requests, both to the board, 13.2 kB page + SSE stream, no CDN — **works with no internet** |

## After the test

Values from G and H are already in `firmware/*.yaml`. I's guessed thresholds survived contact
with a real pump and became the MEDIUM default of a runtime sensitivity select, so a soft-mounted
table can fix its own verdict without anyone reflashing. **Eight of the ten tests now pass; only E and F are
open, and neither is a firmware question.** Of the two worksheet questions this plan existed to
settle:

- **B — settled.** The USB lookup is fast and unambiguous now that the name is an explicit
  banner on line 4. **No printed MAC stickers**, no change to kit prep, and the "press reset and
  read the first lines" hedge is unnecessary.
- **E — still open.** If chattering will not show at 1 s, session 2's hysteresis ladder needs a
  different input or a different demonstration.

Also settled along the way, and feeding the worksheet rewrite: adoption is **pick the discovered
card, manual entry as fallback** (C/D); the float switch reads **Wet = water present** (float flipped, `inverted: true`) with the
wiring recorded in G; the relay board's programmable LED is now a **WiFi-status light**
(steady lit = on WiFi, blinking = not), not a relay mirror (H); the pump's vibration **is**
distinguishable from stillness, so the two reporter entities stay in the image (I); USB and 12 V
together turn out to be **harmless**, which softened the worksheet's prohibition into a practice
and lets a helper plug into a wired board without dismantling the table (H); and every board now
serves its own page at `http://<board-ip>/`, which gives teams live sensor values before any Home
Assistant exists.

The worksheet adoption steps have now been rewritten to the bench-verified flow (Reset device in
the browser → discovered card → bare-name fallback, no key) across `session-1.md`, `reference.md`,
`index.md`, `record-sheet.md` and `session-3.md`. **`homeassistant.local` is now resolved too** —
the worksheets use the VM's own IP, read off its screen and written on the record sheet. See the
section above.
