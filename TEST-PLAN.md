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
      5 on the relay, matching the config exactly
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
- [x] Both adopt into Home Assistant simultaneously — 2 devices, 15 entities, both stable
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

**Question this answers:** is the pin and polarity in the config right, and is the fail-safe
trigger in session 2 pointing at the correct state?

---

## H. Relay board

Pins are now **confirmed from the vendor datasheet** (see `firmware/ESP32-C6-RELAY-X1.md`):
relay **GPIO19**, programmable LED **GPIO2**, button **GPIO9**, all active high. This test is
confirmation, not discovery. **All three are now bench-confirmed on real hardware**, not just
read off the PDF.

> **Design change made during this test: the GPIO2 LED now shows connection status.** It
> originally mirrored the relay, but the relay's own hard-wired indicator already does that from
> the coil an inch away, so the mirror added nothing. It is now an ESPHome `status_led:` —
> blinks on WiFi/API loss, quiet when healthy — so a team can tell whether their board is
> connected without a laptop. With ~100 teams that is the support question that matters most.
> Session 2's worksheet text survives unchanged: it says the LED on the relay board stands in
> for the garden lamp, and the relay's own indicator still lights whenever the relay closes.

- [x] Relay clicks when the switch entity is toggled from Home Assistant
- [x] Both LEDs light: the hard-wired relay indicator **and** the GPIO2 programmable LED —
      confirmed, which is what proved `led_pin: GPIO2` correct. **The GPIO2 LED has since been
      repurposed** (see below), so on the current firmware only the relay's own indicator
      follows the relay
- [x] Onboard button toggles the relay, and works with Home Assistant closed — **verified with
      the HA VM shut down**. The toggle is an on-device ESPHome automation, no network involved.
      Session 2's failure lab depends on exactly this
- [ ] **Re-check after the status-LED change:** GPIO2 blinks when WiFi/API is lost and is quiet
      when connected
- [ ] Power from **12 V into the screw terminal with USB unplugged** — board still connects
- [x] `restore_mode: ALWAYS_OFF` — **confirmed: the relay is always off after a boot**, never
      restores its previous state. This is the safety property that stops a pump restarting by
      itself after a power cut, and it is now proven in firmware. (Re-confirm once the board is
      running from 12 V, since that is the real power-loss case on the day.)
- [x] Read the markings on the relay body and confirm they match what the worksheet tells
      teams to expect: `10A 250VAC` / `10A 30VDC` — **they match**

> **Do not power USB and the 12 V terminal at the same time** — the datasheet says choose one.
> The worksheet now tells teams to unplug USB before wiring 12 V; verify nothing bad happens
> if someone forgets, so you know how bad the mistake is on the day.

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

> **If the two readings are indistinguishable**, the pump is too quiet or too decoupled to
> detect at any threshold. That is a real result, not a failure — say so and I will pull the
> two entities from the image rather than ship something that reads noise.

**Question this answers:** what are the real thresholds, and is the signal separable at all?

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

**Decision needed**, since it changes four files:
1. Worksheets instruct the **IP from the VM console** (recommended — no per-team setup, self-healing).
2. Or each team sets a unique hostname at first boot (**Settings → System → Network**), which adds
   a step to session 1 and needs a name per team on the card.

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
| G float switch | ✅ | pin: **GPIO0** · ON = water present ✅ (`inverted: false`) · closes when float is DOWN/dry · internal pull-up only, **no external resistor needed** — 500 ms filters absorb surface jiggle entirely · broken wire reads as "water present" — see fail-safe note |
| H relay board | ⚠️ | pins GPIO19/2/9 bench-confirmed · relay + button + LEDs OK · button works with HA down · `restore_mode: ALWAYS_OFF` ✅ · relay markings match `10A 250VAC` / `10A 30VDC` ✅ · **still open:** status-LED failure case, and 12 V-only boot |
| I vibration calibration | | floor: ___mg  running: ___mg  thresholds set: |
| J board web page | ✅ | live values ✅, relay control ✅, name-as-URL ✅ (trailing slash or `.local` required — bare name becomes a web search). `local: true` verified: 2 requests, both to the board, 13.2 kB page + SSE stream, no CDN — **works with no internet** |

## After the test

Values from G and H go into `firmware/*.yaml`. Of the two worksheet questions this plan existed
to settle:

- **B — settled.** The USB lookup is fast and unambiguous now that the name is an explicit
  banner on line 4. **No printed MAC stickers**, no change to kit prep, and the "press reset and
  read the first lines" hedge is unnecessary.
- **E — still open.** If chattering will not show at 1 s, session 2's hysteresis ladder needs a
  different input or a different demonstration.

Also settled along the way, and feeding the worksheet rewrite: adoption is **pick the discovered
card, manual entry as fallback** (C/D); the float switch reads **ON = water present** with the
wiring recorded in G; the relay board's programmable LED is now a **connection-status light**,
not a relay mirror (H); and every board now serves its own page at `http://<board-ip>/`, which
gives teams live sensor values before any Home Assistant exists.

The worksheet adoption steps have now been rewritten to the bench-verified flow (Reset device in
the browser → discovered card → bare-name fallback, no key) across `session-1.md`, `reference.md`,
`index.md`, `record-sheet.md` and `session-3.md`. Still deliberately untouched, pending a decision:
`homeassistant.local` — see the open risk above.
