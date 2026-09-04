# ESP32-C6-Relay_X1 v1.1 — hardware reference

Extracted from the vendor PDF (LC Tech / "ESP32-C6 single relay module", board silkscreen
`5437314A_Y726_241122`). Kept here because the PDF is not reliably reachable online and the
pin assignments are load-bearing for `relay-workshop.yaml`.

The vendor's own demo firmware is ESP-IDF + ESP RainMaker with a phone app. **We do not use
any of it** — we flash ESPHome. Only the hardware facts below matter.

## Pin assignments — confirmed

| Function | GPIO | Active | Notes |
|---|---|---|---|
| **Relay control** | **GPIO19** | **High** | |
| **Programmable LED** | **GPIO2** | **High** | Separate from the relay indicator |
| **Programmable button** | **GPIO9** | — | Also the BOOT/burn key |
| WS2812 (vendor demo default) | GPIO10 | — | Not populated on this board; ignore |

> **There are two LEDs.** The **relay indicator** is hard-wired to the relay coil — "lit when
> sucked", i.e. it lights whenever the relay is energised, with no GPIO involved. The
> **programmable LED on GPIO2** is independent. For the session 2 flower-farm lighting
> scenario this is a bonus: the relay indicator lights on its own, and we drive GPIO2 in step
> with it so the "lamp" is unmistakable across a room.

## Terminals

Two green screw terminal blocks.

**Relay output** (3-way, left side of the board):

| Terminal | Behaviour |
|---|---|
| **NO** | Normally open — floating before the relay pulls in, shorted to COM after |
| **COM** | Common |
| **NC** | Normally closed — shorted to COM before the relay pulls in, floating after |

The worksheet wires the pump through **COM** and **NO**, so the pump is off when the relay is
de-energised and off after a power cut.

**Power input** (2-way, right side): **7–60 V DC** and **GND**.

## Power — pick one, not both

> The datasheet states power is **"DC 7-60V or TYPE-C 5V (choose one)"**.
>
> This has a direct workshop consequence. Teams plug the board into a laptop over USB to read
> its device name, then wire it to the 12 V rail. **The USB cable must come out before the
> 12 V is connected.** The worksheet says so at that step.

## Relay ratings

Relay part: **SRD-05VDC-SL-C**. Silkscreen rating:

```
10A 250VAC    10A 125VAC
10A  30VDC    10A  28VDC
```

Datasheet text says loads below **AC250V / DC30V**. Our 12 V aquarium pump is far inside this.
Teams read these markings off the relay body in session 1 — the numbers above are what they
should find.

## Other specifications

- Module: **ESP32-C6-WROOM-1**, 2.4 GHz WiFi 6, BT 5.3, Zigbee/Thread, 4 MB flash
- 30 programmable GPIO, all broken out to headers `JP2` / `JP3`
- Board size **57.5 × 53.7 mm**, 3 mm mounting holes
- USB Type-C (5 V supply and native USB serial)
- Separate 5-pin "burn interface" header `JP1` (GND/RX/TX/5V) for an external TTL adapter —
  not needed, the C6's native USB works

## Flashing

Normally unnecessary: ESPHome resets the board into the bootloader over native USB. If a board
ever refuses to enter download mode, the manual sequence from the datasheet is:

1. Hold **BOOT**, briefly press **RST**, release BOOT after ~1 s. Or hold BOOT while applying
   power. Or tie **IO9** to GND, flash, then remove the link.

## What this changed

Before this PDF, `relay-workshop.yaml` carried placeholder pins (GPIO16/GPIO23) taken from the
ESP32 Relay X1 **WROOM** variant on devices.esphome.io. Those were wrong for the C6 board.
TEST-PLAN test H is now a confirmation, not a discovery.
