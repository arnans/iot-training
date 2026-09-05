# Workshop Network Requirements

Hand this to the network provider. It specifies what the IoT workshop needs from the
wireless network beyond raw client capacity.

## Context

A hands-on IoT workshop for **400 participants in 100 teams of four**, all in one room, all
working at the same time.

| Device | Count | Band | Notes |
|---|---|---|---|
| ESP32 sensor boards | **100** | **2.4 GHz only** | Always on, including overnight between session days |
| ESP32 relay boards | **100** | **2.4 GHz only** | Always on, including overnight |
| Participant laptops | **100 minimum** | 5 GHz preferred | One per team runs a Home Assistant server in a VM (two MACs per laptop). Members may bring their own, so plan for more |
| Participant phones | **up to 100** | mobile data preferred, 5 GHz fallback | Used to open the team's own dashboard |
| Instructor server | 1 | **wired, 802.1Q trunk** | Must see all three zones — see §8 |
| Presentation laptop | 1 | wired | |

**Plan for 500 concurrent clients, size for 600.** 500 is the *expected* peak, not headroom.

**The essential behaviour:** each team's laptop must find and hold a persistent connection to
*its own two boards*, by hostname (`name.local`, i.e. mDNS), over the wireless LAN. The boards
are on 2.4 GHz and the laptop is on 5 GHz. Internet is secondary; sessions 1 and 2 need none.

---

## The design: three logical zones

The room is divided into **three zones — red, green, blue**. Each zone is its own VLAN and IP
subnet, and carries **two SSIDs**: one 2.4 GHz for that zone's boards, one 5 GHz for that zone's
laptops.

| Zone | VLAN (suggested) | 2.4 GHz SSID (boards) | 5 GHz SSID (laptops) | Clients |
|---|---|---|---|---|
| red   | 10 | `farm-iot-red`   | `farm-laptop-red`   | ~67 boards, ~34 laptops (×2 MACs), phones |
| green | 20 | `farm-iot-green` | `farm-laptop-green` | ~67 boards, ~33 laptops, phones |
| blue  | 30 | `farm-iot-blue`  | `farm-laptop-blue`  | ~66 boards, ~33 laptops, phones |

**Zones are logical, not spatial.** The zone is compiled into each board's firmware and
colour-coded on each team's kit; a team is told its colour and joins the matching laptop SSID.
Teams sit anywhere. Therefore:

- **Every AP broadcasts all six SSIDs** — three per radio. A board connects to *its* SSID on
  whichever AP is nearest. There are no zone boundaries to plan and no site-survey dependency.
- Three SSIDs per radio is at the practical limit for beacon overhead on 2.4 GHz. **Please do
  not add a seventh SSID** (no guest network on these radios).

**Why three zones rather than one flat network:** mDNS load in a broadcast domain scales with
*queriers × responders*. Three zones cut the per-domain product by roughly nine times, and each
zone is a familiar /24. The zones need **no mDNS gateway or reflector between them** — a team's
laptop and boards are always in the same VLAN.

**Zones do not need to reach each other**, and we would prefer they cannot. The only device that
must see all three is the instructor server (§8).

### Access points

- **2.4 GHz has only three non-overlapping channels (1, 6, 11).** Three APs on 1/6/11 covers a
  room well; more than three in one room means channel reuse, which is only workable as
  spatially separated cells at reduced power. Please plan the 2.4 GHz layer with that in mind —
  we would rather have three well-placed APs than six competing.
- **5 GHz: as many APs as coverage needs.** WiFi 6 / 802.11ax OFDMA helps at this density.
- Even coverage at **table height**; boards sit among people, laptops and water containers.

---

## Hard requirements — apply within every zone

### 1. Both of a zone's SSIDs on the same VLAN and subnet

`farm-iot-red` and `farm-laptop-red` must bridge to the **same** VLAN and IP subnet, and likewise
for green and blue. A laptop on 5 GHz must reach a board on 2.4 GHz in its own zone as if on the
same wire.

### 2. Client-to-client traffic permitted, including between the two SSIDs of a zone

**Client isolation / AP isolation / "guest mode" OFF on all six SSIDs**, and traffic allowed
between the 2.4 and 5 GHz SSIDs of the same zone. Every sensor reading crosses bands.

### 3. mDNS forwarded between wireless clients and across the zone's two SSIDs

Hostname resolution uses multicast DNS on **224.0.0.251 / UDP 5353**. It must reach every client
in the zone, wireless-to-wireless and across both of the zone's SSIDs. Ensure none of these drop it:

- Broadcast/multicast filtering or suppression
- Multicast-to-unicast conversion that does not handle mDNS
- IGMP snooping without a querier on the segment
- Proxy ARP / ARP suppression

> Suppress other broadcast/multicast as you see fit, **but mDNS on 5353 has to survive.** If your
> APs support **multicast-to-unicast conversion that handles mDNS correctly, please enable it** —
> it is the single biggest airtime win at this density. If you rate-limit multicast, tell us the
> threshold.

### 4. The 2.4 GHz SSIDs tuned for simple clients

The ESP32 has one 2.4 GHz radio and a basic supplicant. On `farm-iot-*`:

- **WPA2-PSK (AES/CCMP)**, one shared password per zone. Not WPA3-only, not mixed-mode with PMF
  required, not WPA-Enterprise.
- **PMF / 802.11w optional or disabled**, not required.
- **No 802.11r / k / v fast roaming.** The boards do not move.
- **No band steering**, and no minimum-rate setting that excludes low 802.11n rates.
- **No captive portal, splash page, or periodic re-authentication.** A microcontroller cannot
  accept terms. Association plus the password must grant full LAN access, permanently.

### 5. Long-lived TCP connections must survive

Each laptop holds a persistent TCP session to each of its boards for hours. Disable any **client
idle timeout, session timeout or inactivity disconnect**. Boards must stay associated overnight
with no server connected.

### 6. Multiple MAC addresses behind one wireless client

Laptops run Home Assistant in a **bridged VM**, so one laptop presents **two MACs and two IPs**
over one association. Disable anything that treats this as spoofing — client integrity checks,
MAC-per-station limits, WDS restrictions. *Easy to miss; please confirm explicitly.*

### 7. DHCP per zone

Per zone, count leases: ~67 boards + ~34 laptops × 2 (host + VM) + spare laptops + phones ≈
**170–220**.

- **One /24 per zone** is workable; a **/23 per zone** is comfortable if it costs nothing.
- **Lease time 12–24 hours.** Devices are addressed by hostname, so a changed IP costs nothing,
  and shorter leases stop departed devices holding addresses.
- Reserve a small static range per zone for instructor equipment.

### 8. Instructor server sees all three zones

One instructor server records data from every team's sensor board overnight. It must be
**layer-2 present in all three VLANs** so it can resolve boards by name in each zone.

- Provide its wired port as an **802.1Q trunk carrying VLANs 10, 20 and 30** (plus a native or
  management VLAN if you need one). The server will configure VLAN sub-interfaces itself.
- Alternatively three access ports, one per zone, is acceptable.
- **Please do not solve this with an mDNS reflector between zones.** We specifically want the
  participant zones to stay isolated from each other.

### 9. Association surge

If an AP or controller restarts, up to 200 boards reassociate at once. Confirm no association
rate limit or client-count-per-radio cap would strand some, and that DHCP absorbs a burst.

---

## Physical and operational

- **Powered and running the day before** for a setup and test window.
- **Running continuously overnight** between session days. Confirm no nightly reboot or
  maintenance window.
- **Wired drops:** one trunk (§8) for the instructor server, one access port for the
  presentation laptop.
- On-site or on-call support during the setup window and the first session.
- **All six SSID names and three passwords fixed one week in advance** — they are compiled into
  200 boards and cannot change on the day.

## Internet access

- **Not required** for sessions 1 and 2.
- **Required for one 30-minute block** in the final session, from all three zones: outbound HTTPS
  (443) and MQTT (8883).

---

## Acceptance test

Run with the provider during the setup window. All seven must pass.

| # | Test | Pass criterion |
|---|---|---|
| 1 | Red board on `farm-iot-red`, laptop on `farm-laptop-red`: `ping <boardname>.local` | Resolves and replies — **cross-band mDNS within a zone** |
| 2 | Same ping from inside the laptop's bridged VM | Resolves and replies — **multicast + multi-MAC** |
| 3 | Laptop on `farm-laptop-green` pings the **red** board by name | **Must fail** — proves zones are isolated |
| 4 | Instructor server (trunk) pings a red, a green and a blue board by name | All three resolve — **§8** |
| 5 | Phone on `farm-laptop-red` opens `http://<VM-ip>:8123` | Page loads — client-to-client |
| 6 | Laptop connected to a board, idle 30 minutes | Connection still live |
| 7 | **20–30 boards** across all three zones powered simultaneously; then power-cycle one AP | All associate and get leases; all rejoin after the AP restart |

Tests 1, 2 and 4 are the ones that fail on default enterprise configurations. Please have
someone able to change controller settings present.

> **On what we cannot test in advance.** 20–30 boards is 10–15 % of the final load. It validates
> configuration — SSIDs, VLANs, mDNS, DHCP, the trunk — which is the likely failure mode. It does
> not validate 200 boards on 2.4 GHz. For that we rely on your capacity planning, which is why §9
> and the AP question above matter.

## Fallback if VLANs are not possible

If your equipment cannot provide per-SSID VLANs, the fallback is **one flat subnet (/22)** carrying
two SSIDs (`farm-iot` 2.4 GHz, `farm-laptop` 5 GHz), all other requirements unchanged, and we
would then depend heavily on multicast-to-unicast conversion. Tell us early if this is the case —
the firmware is built differently for it.

---

## Summary for a quick read

Three zones (red / green / blue), each a VLAN + /24 with a 2.4 GHz SSID for boards and a 5 GHz
SSID for laptops; **all six SSIDs on every AP**. Within a zone: **client isolation off, mDNS
forwarded across both SSIDs, WPA2-PSK, no PMF requirement, no fast roaming, no idle timeouts, two
MACs per laptop, 24 h leases.** Zones isolated from each other. **Instructor server on an 802.1Q
trunk of all three.** Runs overnight. Plan 500 clients, size 600.
