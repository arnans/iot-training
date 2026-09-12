# Instructor & TA resources

Every file and link needed to prepare for and run the workshop, in one place.
Participants get a trimmed version at
[รวมไฟล์และลิงก์](https://arnans.github.io/iot-training/renders/resources.html).

Links are absolute so this page works the same whether you read it in the repository or as the
published page at
[arnans.github.io/iot-training/instructor-resources.html](https://arnans.github.io/iot-training/instructor-resources.html).
Rows marked *(repo)* need access to the private `iot-training` repository.

---

## 1. Board firmware — six images

One image per board type, per zone colour. The zone colour is baked in: a red-zone image only
joins the red SSID. Built and verified 12 Sep 2026.

| Board | Red zone | Green zone | Blue zone |
|---|---|---|---|
| **GoGo-IoT sensor board** (ESP32-C3) | [gogo-iot-red.factory.bin](https://arnans.github.io/iot-training/firmware/gogo-iot-red.factory.bin) | [gogo-iot-green.factory.bin](https://arnans.github.io/iot-training/firmware/gogo-iot-green.factory.bin) | [gogo-iot-blue.factory.bin](https://arnans.github.io/iot-training/firmware/gogo-iot-blue.factory.bin) |
| **Relay board** (ESP32-C6-Relay_X1) | [gogo-relay-red.factory.bin](https://arnans.github.io/iot-training/firmware/gogo-relay-red.factory.bin) | [gogo-relay-green.factory.bin](https://arnans.github.io/iot-training/firmware/gogo-relay-green.factory.bin) | [gogo-relay-blue.factory.bin](https://arnans.github.io/iot-training/firmware/gogo-relay-blue.factory.bin) |

**To flash a board:** plug it into a laptop over USB-C, open <https://web.esphome.io> in Chrome or
Edge → **Connect** → pick the serial port → **Install** → choose the `.bin` for that board and
zone. Needs internet.

> **The colour on the board must match the colour on the kit and on the team card.** A mismatched
> board joins the wrong WiFi and the team's Home Assistant never sees it. The board says which it
> is — its name reads `gogo-iot-red-a1b2c3`.

Spare boards flashed during the workshop must be flashed to **that table's zone colour**.

---

## 2. Home Assistant virtual machine

The same image participants install. Put it on the instructor kit and on every rescue laptop.

| Laptop | VirtualBox | Farm Workshop VM |
|---|---|---|
| Windows / Intel Mac | [Downloads](https://www.virtualbox.org/wiki/Downloads) | `farm-workshop-x86-64.ova` — **not built yet** |
| Apple Silicon Mac (M1+) | [Downloads](https://www.virtualbox.org/wiki/Downloads) | `farm-workshop-arm64.ova` — **not built yet** |

Import steps, settings and the login are in the participant guide:
**[เตรียมแล็ปท็อป](https://arnans.github.io/iot-training/renders/install.html)**. The two things
that go wrong: Adapter 1 must be **Bridged** and set to the laptop's own WiFi card, and the VM is
reached at `http://<its IP>` — never `homeassistant.local`, because every team's VM answers to
that name.

Login: `TODO` / `TODO` (also printed on each team card).

---

## 3. Worksheets and printed material

| What | Link |
|---|---|
| Participant site | <https://arnans.github.io/iot-training/> |
| Before the workshop — เตรียมแล็ปท็อป | [install.html](https://arnans.github.io/iot-training/renders/install.html) |
| Session 1 — รับรู้ ตัดสินใจ สั่งการ | [session-1.html](https://arnans.github.io/iot-training/renders/session-1.html) |
| Session 2 — ควบคุมอัตโนมัติและ Fail-safe | [session-2.html](https://arnans.github.io/iot-training/renders/session-2.html) |
| Session 3 — แดชบอร์ดและออกแบบระบบ | [session-3.html](https://arnans.github.io/iot-training/renders/session-3.html) |
| Participant file & link list | [resources.html](https://arnans.github.io/iot-training/renders/resources.html) |
| Team record sheet + design canvas — **the one thing that gets printed** | [record-sheet.md](https://github.com/arnans/iot-training/blob/main/docs/record-sheet.md) *(repo)* |
| Home Assistant menu paths + troubleshooting — **keep this open while roving** | [reference.md](https://github.com/arnans/iot-training/blob/main/docs/reference.md) *(repo)* |

The `renders/` pages are self-contained: open one once and it keeps working with no internet.

---

## 4. Preparing to teach

| What | Link |
|---|---|
| What happens in each session, and why | [SESSION-OVERVIEW.md](https://github.com/arnans/iot-training/blob/main/SESSION-OVERVIEW.md) *(repo)* |
| Full course design — timings, kit list, risks, open decisions | [COURSE-DESIGN.md](https://github.com/arnans/iot-training/blob/main/COURSE-DESIGN.md) *(repo)* |
| Known gaps and assumptions in the worksheets | [WORKSHEET-TODO.md](https://github.com/arnans/iot-training/blob/main/WORKSHEET-TODO.md) *(repo)* |
| Network spec to hand the venue's provider — Thai | [network-requirements.html](https://arnans.github.io/iot-training/network-requirements.html) |
| Network spec — English | [network-requirements-en.html](https://arnans.github.io/iot-training/network-requirements-en.html) |

**Instructor kit** — a spare laptop mirroring a team kit, projected. It also rescues a team whose
laptop dies. Three things teams don't have: the **Auto / Off / Manual pump control box** for the
Session 2 debrief, a Home Assistant Cloud account for the Session 3 remote-access demo, and a saved
morning history graph for teams that shut their VM down at lunch.

**Kit prep, the two that fail silently:** flip the float cylinder on its rod so it closes when wet
(otherwise a cut wire reads "water present" and a pump can run dry), and colour-code board, kit and
team card as one matching set.

---

## 5. Tools and external links

| Tool | Used for |
|---|---|
| <https://web.esphome.io> | Flashing boards and reading a board's name from its USB log. Chrome or Edge only |
| <https://www.home-assistant.io/docs/> | Home Assistant reference |
| <https://esphome.io/> | ESPHome reference |
| [github.com/arnans/gogo-iot-node](https://github.com/arnans/gogo-iot-node) | GoGo-IoT sensor board hardware |

---

## Still missing

Nobody has produced these yet:

- **The two Farm Workshop OVAs**, and a file host for them — blocks sending the install guide to
  participants
- The install-guide details participants need: VM login, file size, verification form, help channel
- Slide decks for Sessions 1–3, the three post-tests, and the facilitator run-sheet
- Real screenshots in the install guide (currently placeholders)
- Bench tests against the built firmware — see
  [TEST-PLAN.md](https://github.com/arnans/iot-training/blob/main/TEST-PLAN.md) *(repo)*, especially
  test B (the boot banner participants read) and test G (float switch polarity)

---

*Building the images rather than using them? The firmware build and the 18-step OVA recipe are in
[firmware/README.md](https://github.com/arnans/iot-training/blob/main/firmware/README.md) and
[hass/README.md](https://github.com/arnans/iot-training/blob/main/hass/README.md) — both repo-only.*
