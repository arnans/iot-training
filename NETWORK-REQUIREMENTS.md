# Workshop Network Requirements

*ฉบับภาษาไทย: [NETWORK-REQUIREMENTS-th.md](NETWORK-REQUIREMENTS-th.md)*

For the network provider. A hands-on IoT workshop needs one thing from the wireless network
that default enterprise configurations do not give: **devices must find and talk to each other
over WiFi, by hostname (mDNS), across bands.** Capacity matters, but every requirement below is
about that.

---

## 1. SSID names and password

The room is divided into three zones. Each zone is its own VLAN and carries one pair of SSIDs:
2.4 GHz for the boards, 5 GHz for laptops and phones.

| Zone | VLAN (suggested) | 2.4 GHz SSID (boards) | 5 GHz SSID (laptops, phones) |
|---|---|---|---|
| red   | 10 | `farm-iot-red`   | `farm-laptop-red`   |
| green | 20 | `farm-iot-green` | `farm-laptop-green` |
| blue  | 30 | `farm-iot-blue`  | `farm-laptop-blue`  |

### Password `farmer`, the same on all six SSIDs · WPA2-PSK (AES/CCMP)

> **These names and this password must be set exactly as written.** They are compiled into the
> firmware of 200 boards ahead of the event and cannot be changed on site. Tell us at once if any
> of them cannot be set as given.

- **Every AP must broadcast all six SSIDs** (three per radio). Zones are logical, not spatial:
  each board's firmware has its zone SSID compiled in, kits are colour-coded to match, and teams
  sit anywhere.
- **Do not add a seventh SSID** on these radios (no guest network). Three per radio is the
  practical beacon-overhead limit on 2.4 GHz.
- **Zones must not reach each other.** The only device that sees all three is the instructor
  server (item 8).
- **Why three zones:** mDNS load in a broadcast domain scales with queriers × responders, so
  three zones cut it roughly ninefold. Because a team's laptop and boards always share a VLAN,
  **no mDNS gateway or reflector is needed anywhere.**

---

## 2. What is on the network

| Device | Count | Connects via | Notes |
|---|---|---|---|
| Sensor boards (ESP32-C3) and relay boards (ESP32-C6) | 100 each | 2.4 GHz SSID **only**, 20 MHz | ~67 per zone. Powered on for the whole event, including overnight |
| Team laptops | 100 (+ spares, + 1 instructor kit) | 5 GHz SSID | Each runs Home Assistant in a **bridged VM**, so one laptop has two MACs and two IPs (item 6) |
| Phones | 100–400 | 5 GHz SSID | Open the team dashboard, which lives in the VM on the laptop rather than on the internet, so they must join their own zone's SSID |
| Instructor server | 1 | **Wired, 802.1Q trunk** | Records every sensor board overnight; must see all three zones (item 8) |
| Presentation laptop | 1 | **Wired**, access port | Slides; needs internet |

**Concurrent clients: ~500 expected, up to ~800** if every participant joins a phone. Size the
5 GHz side for the upper figure. The 2.4 GHz side carries the 200 boards and nothing else.

**The essential behaviour:** each team's laptop on 5 GHz must find its own two boards on 2.4 GHz
by hostname, `name.local`, and hold a TCP connection to each for hours.

---

## 3. Configuration requirements (apply within every zone)

These numbers are referenced from our other documents; please keep them in replies.

**1. Both of a zone's SSIDs bridge to the same VLAN and subnet.** For example `farm-iot-red` and
`farm-laptop-red` land on VLAN 10 together. A laptop on 5 GHz must reach a board on 2.4 GHz as if
on the same wire.

**2. Client-to-client traffic permitted, including between a zone's two SSIDs.** Turn **client
isolation / AP isolation / guest mode OFF on all six SSIDs.** Every sensor reading and every
dashboard view crosses bands.

**3. mDNS forwarded wireless-to-wireless and across a zone's two SSIDs.** Hostname resolution is
multicast DNS on **224.0.0.251 / UDP 5353** and must reach every client in the zone. Check that
none of these drop it: broadcast/multicast filtering or suppression; multicast-to-unicast
conversion that mishandles mDNS; IGMP snooping without a querier on the segment; proxy ARP or
ARP suppression.

> Suppress other multicast as you see fit, **but 5353 must survive.** If your APs do
> multicast-to-unicast conversion that handles mDNS correctly, please enable it — it is the
> biggest airtime win at this density. If you rate-limit multicast, tell us the threshold.

**4. The 2.4 GHz SSIDs tuned for microcontrollers.** Not WPA3-only and not WPA-Enterprise ·
**PMF / 802.11w** optional or disabled · **no 802.11r / k / v**, no band steering, and no
minimum-rate setting that excludes low 802.11n rates, since the boards never move · **no captive
portal, splash page or periodic re-authentication** — association plus the password must grant
full LAN access permanently · **rogue-AP containment off**, because each board raises a small
setup hotspot if its zone SSID disappears, and an instructor phone hotspot is our internet
fallback.

**5. Long-lived connections survive.** Each laptop holds a TCP session to each of its boards for
hours, and boards stay associated overnight with no client connected. **Disable client idle,
session and inactivity timeouts**, and schedule **no nightly reboot, maintenance window or
config push** for the duration of the event.

**6. Two MAC addresses behind one wireless client.** Home Assistant runs in a bridged VM, so one
laptop presents two MACs and two IPs over a single association. Disable anything that treats this
as spoofing: client integrity checks, MAC-per-station limits, WDS restrictions. *Easy to miss —
please confirm explicitly.*

**7. DHCP per zone.** Count leases, not devices: roughly **170–270 per zone** (~67 boards +
~34 laptops × 2 + phones + spares). A **/23 per zone** is the safe choice; a /24 only works if
phones are held to one per team. Set **lease time 12–24 h** — devices are addressed by hostname,
so a changed IP costs nothing. Reserve a small static range per zone for instructor equipment.

**8. Instructor server present in all three zones.** It resolves and connects to every sensor
board by name, in every zone, overnight. Provide its wired port as an **802.1Q trunk carrying
VLANs 10, 20 and 30** and the server will configure its own sub-interfaces; three access ports,
one per zone, is an acceptable alternative. **Not an mDNS reflector between zones** — the
participant zones must stay isolated.

**9. Association surge.** If an AP or controller restarts, up to 200 boards reassociate at once.
Confirm that no association rate limit or client-per-radio cap strands some, and that DHCP
absorbs the burst.

---

## 4. Access points and internet

**2.4 GHz** has only three non-overlapping channels (1/6/11), so three well-placed APs beat six
competing ones. If more than three are needed, make them spatially separated co-channel cells at
reduced power. **5 GHz:** as many APs as coverage needs; WiFi 6 / OFDMA helps at this density.
Coverage must be even at **table height**, since boards sit among people, laptops and water
containers.

**Internet** is needed only on the laptop SSIDs and the presentation laptop's port. The board
SSIDs need none, and no inbound access is required anywhere.

| When | What for | Outbound ports | If it fails |
|---|---|---|---|
| Throughout | The worksheets are a website, and Session 1 reads board names via <https://web.esphome.io> | 443 | Inconvenient, not fatal: printed worksheets instead |
| **Session 3, about one hour** | Pushing data to a cloud dashboard, from all three zones | **443 and 8883** (MQTT/TLS) | **That block fails.** Fallback is an instructor phone hotspot |

---

## 5. Acceptance test

Run during the setup window before the event, with someone able to change controller settings.
All eight must pass. We also ask for on-site or on-call support through the setup window and the
first hour of the workshop.

| # | Test | Pass criterion |
|---|---|---|
| 1 | Board on `farm-iot-red`, laptop on `farm-laptop-red`: `ping <boardname>.local` | Resolves and replies — **cross-band mDNS within a zone** (items 1–3) |
| 2 | Same ping from inside the laptop's bridged VM | Resolves and replies — **multicast + two MACs** (item 6) |
| 3 | Laptop on `farm-laptop-green` pings the **red** board by name | **Must fail** — zones are isolated |
| 4 | Instructor server on the trunk pings a red, a green and a blue board by name | All three resolve (item 8) |
| 5 | Phone on `farm-laptop-red` opens `http://<VM-ip>` | Dashboard loads — client-to-client, port 80 |
| 6 | Laptop connected to a board, idle 30 minutes | Connection still live (item 5) |
| 7 | **20–30 boards** across all zones powered at once; then power-cycle one AP | All associate and get leases; all rejoin after the restart (item 9) |
| 8 | Laptop on `farm-laptop-red` opens <https://web.esphome.io> | Page loads — internet from the laptop SSID |

Tests 1, 2 and 4 are the ones that fail on default enterprise configurations.

> **What this cannot test.** 20–30 boards is 10–15 % of the final load. It validates
> configuration (SSIDs, VLANs, mDNS, DHCP, the trunk), which is the likely failure. It does not
> validate 200 boards on 2.4 GHz; for that we rely on your capacity planning (item 9 and
> section 4).

---

## 6. Fallback if per-SSID VLANs are not possible

One flat subnet (/22) with two SSIDs, `farm-iot` on 2.4 GHz and `farm-laptop` on 5 GHz, password
`farmer` as before. All other requirements unchanged, with heavy reliance on multicast-to-unicast
conversion. **Tell us early** — the firmware is built differently for it.
