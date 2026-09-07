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

| Zone | VLAN (suggested) | 2.4 GHz SSID (boards) | 5 GHz SSID (laptops, phones) | Password |
|---|---|---|---|---|
| red   | 10 | `farm-iot-red`   | `farm-laptop-red`   | `iotfarmer` |
| green | 20 | `farm-iot-green` | `farm-laptop-green` | `iotfarmer` |
| blue  | 30 | `farm-iot-blue`  | `farm-laptop-blue`  | `iotfarmer` |

**The same password, `iotfarmer`, on all six SSIDs. WPA2-PSK (AES/CCMP).**

> **These names and this password must be set exactly as written.** They are compiled into the
> firmware of 200 boards ahead of the event and cannot be changed on site. Tell us at once if any
> of them cannot be set as given.

Every AP must broadcast all six SSIDs (three per radio). Zones are logical, not spatial: each
board's firmware has its zone SSID compiled in, kits are colour-coded to match, and teams sit
anywhere. Please do not add a seventh SSID on these radios.

### Key design guidelines

**1. Within one zone's SSID pair, devices must all see each other**, unicast and mDNS alike, across
bands. So both of a zone's SSIDs bridge to the **same VLAN and subnet**, and **client isolation /
AP isolation / guest mode is OFF on all six SSIDs.** Requirement 1 covers the mDNS half.

**2. Across different zones' SSID pairs, devices must not see each other at all**: no unicast, no
broadcast, no multicast. So:

- **No mDNS reflector, Bonjour gateway, AirGroup or mDNS repeater between VLANs.** Several
  vendors' controllers enable this by themselves once they see multiple VLANs, and it is the most
  common trap for this design. We want none of it, because a team's laptop and boards already
  share a VLAN.
- **No routing between the three zone subnets.** If your topology has to route them, block it with
  an ACL at the gateway.

Guideline 2 is not about security, it is about **multicast volume**. mDNS load in a broadcast
domain scales with queriers × responders, so genuinely separating three zones cuts it roughly
ninefold. If any two zones can see each other, the load returns to that of one flat 500-client
network, which is the single thing the zoning exists to avoid.

No device on this network needs to reach across zones, so there is no exception to make room for.

---

## 2. Expected devices and counts on the network

| Device | Count | Connects via | Notes |
|---|---|---|---|
| Sensor boards (ESP32-C3) and relay boards (ESP32-C6) | 100 each | 2.4 GHz SSID **only**, 20 MHz | ~67 per zone. Powered on for the whole event, including overnight |
| Team laptops | 100 (+ spares, + 1 instructor kit) | 5 GHz SSID | Each runs Home Assistant in a **bridged VM**, so one laptop has two MACs and two IPs (requirement 2) |
| Phones | 100–400 | 5 GHz SSID | Open the team dashboard, which lives in the VM on the laptop rather than on the internet, so they must join their own zone's SSID |
| Presentation laptop | 1 | **Wired**, access port | Slides; needs internet |

**Concurrent clients: ~500 expected, up to ~800** if every participant joins a phone. Size the
5 GHz side for the upper figure. The 2.4 GHz side carries the 200 boards and nothing else.

> **Please give each zone a private /16** — for instance `10.10.0.0/16` red, `10.20.0.0/16` green,
> `10.30.0.0/16` blue. Count DHCP leases, not devices: roughly **170–270 per zone** (~67 boards +
> ~34 laptops × 2 for the bridged VMs + phones + spares). A /24 leaves no margin once phones join,
> and no headroom for the long leases in requirement 4. **A /23 per zone is the workable minimum**
> if your addressing plan cannot spare a /16.
>
> The wider mask costs nothing in airtime: broadcast and multicast load scales with the number of
> hosts, which is unchanged, not with the size of the subnet.

**The essential behaviour:** each team's laptop on 5 GHz must find its own two boards on 2.4 GHz
by hostname, `name.local`, and hold a TCP connection to each for hours.

---

## 3. Key configuration settings

These are the ones that decide whether the workshop works. Everything else has moved to
section 5.

**1. mDNS forwarded wireless-to-wireless and across a zone's two SSIDs.** Hostname resolution is
multicast DNS on **224.0.0.251 / UDP 5353**. It must reach every client in the zone and, per
guideline 2, no further. Check that none of these drop it: broadcast/multicast filtering or
suppression; multicast-to-unicast conversion that mishandles mDNS; IGMP snooping without a
querier on the segment; proxy ARP or ARP suppression.

> Suppress other multicast as you see fit, **but 5353 must survive.** If your APs do
> multicast-to-unicast conversion that handles mDNS correctly, please enable it — it is the
> biggest airtime win at this density. If you rate-limit multicast, tell us the threshold.

**2. Two MAC addresses behind one wireless client.** Home Assistant runs in a bridged VM, so one
laptop presents two MACs and two IPs over a single association. Disable anything that treats this
as spoofing: client integrity checks, MAC-per-station limits, WDS restrictions. *Easy to miss —
please confirm explicitly.*

**3. Association surge.** If an AP or controller restarts, up to 200 boards reassociate at once.
Confirm that no association rate limit or client-per-radio cap strands some, and that DHCP
absorbs the burst.

**4. DHCP leases long enough that addresses hold for the whole event.** Set the lease to span the
workshop, a week for instance, or use reservations. **Desirable rather than essential:**
everything is addressed by hostname, so a changed IP breaks nothing on its own. It matters
because a team that writes its board's IP down as a fallback on the first day should still find
that address valid on the second. The address space in section 2 is what makes a long lease affordable.

---

## 4. Acceptance test

Run during the setup window before the event, with someone able to change controller settings.
All of them must pass. We also ask for on-site or on-call support through the setup window and
the first hour of the workshop.

| # | Test | Pass criterion |
|---|---|---|
| 1 | Board on `farm-iot-red`, laptop on `farm-laptop-red`: `ping <boardname>.local` | Resolves and replies — **cross-band mDNS within a zone** (requirement 1) |
| 2 | Same ping from inside the laptop's bridged VM | Resolves and replies — **multicast + two MACs** (requirement 2) |
| 3 | Laptop on `farm-laptop-green` pings the **red** board by name | **Must fail** — zones are isolated (guideline 2) |
| 3b | Same laptop runs an mDNS browser (`dns-sd -B _esphome._tcp`, or a Discovery app on a phone) | **Only green boards appear.** No name containing `red` or `blue` shows up, proving no mDNS reflector is running (guideline 2) |
| 4 | Phone on `farm-laptop-red` opens `http://<VM-ip>` | Dashboard loads — client-to-client, port 80 |
| 5 | Laptop connected to a board, idle 30 minutes | Connection still live (section 5) |
| 6 | **20–30 boards** across all zones powered at once; then power-cycle one AP | All associate and get leases; all rejoin after the restart (requirement 3) |
| 7 | Laptop on `farm-laptop-red` opens <https://web.esphome.io> | Page loads — internet from the laptop SSID |

Tests 1, 2 and 3b are the ones that fail on default enterprise configurations.

> **What this cannot test.** 20–30 boards is 10–15 % of the final load. It validates
> configuration (SSIDs, VLANs, mDNS, DHCP), which is the likely failure. It does not
> validate 200 boards on 2.4 GHz; for that we rely on your capacity planning (requirement 3 and
> the radio note in section 5).

---

## 5. Secondary notes

Standard practice for a network like this. They are listed because a default setting in any of
them would cost us time on the day, not because we expect them to be contentious.

- **The 2.4 GHz SSIDs suit simple clients.** Not WPA3-only and not WPA-Enterprise · PMF / 802.11w
  optional or disabled · no 802.11r / k / v, no band steering, and no minimum-rate setting that
  excludes low 802.11n rates, since the boards never move · no captive portal, splash page or
  periodic re-authentication, because a microcontroller cannot accept terms.
- **Long-lived connections survive.** Each laptop holds a TCP session to each of its boards for
  hours, and boards stay associated overnight with no client connected. Disable client idle,
  session and inactivity timeouts, and schedule no nightly reboot or maintenance window for the
  duration of the event.
- **Rogue-AP containment off.** Each board raises a small setup hotspot if its zone SSID
  disappears, and an instructor phone hotspot is our internet fallback.
- **Radio planning.** 2.4 GHz has only three non-overlapping channels (1/6/11), so three
  well-placed APs beat six competing ones; beyond three, use spatially separated co-channel cells
  at reduced power. On 5 GHz use as many APs as coverage needs, where WiFi 6 / OFDMA genuinely
  helps. Coverage must be even at **table height**, since boards sit among people, laptops and
  water containers.
- **Internet** is needed on the laptop SSIDs and the presentation laptop's port only. Outbound 443
  throughout, plus outbound **8883 (MQTT/TLS)** for about an hour in session 3, from all three
  zones. The board SSIDs need none, and no inbound access is required anywhere.

---

## 6. Fallback if per-SSID VLANs are not possible

One flat subnet (/22) with two SSIDs, `farm-iot` on 2.4 GHz and `farm-laptop` on 5 GHz, password
`iotfarmer` as before. All other requirements unchanged, with heavy reliance on
multicast-to-unicast conversion. **Tell us early** — the firmware is built differently for it.
