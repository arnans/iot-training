# Workshop Network Requirements

Hand this to the network provider. It specifies what the IoT workshop needs from the
wireless network beyond raw client capacity.

## Context

A hands-on IoT workshop. On the network at the same time:

| Device | Count | Band | Notes |
|---|---|---|---|
| ESP32 sensor boards | ~60 | **2.4 GHz only** | Battery/USB powered, always on, incl. overnight |
| ESP32 relay boards | ~60 | **2.4 GHz only** | Always on, incl. overnight |
| Participant laptops | ~30 | 2.4 or 5 GHz | Each runs a Home Assistant server in a VM |
| Participant phones | ~40 | 2.4 or 5 GHz | Browser access to their own laptop's server |
| Instructor equipment | 2–3 | Wired preferred | Server + spare kit |

Peak: roughly **190 concurrent clients**, of which ~120 are 2.4 GHz-only microcontrollers.

**The essential behaviour:** each laptop must discover and hold a persistent connection to
*its own* boards, by hostname, over the wireless LAN. This is device-to-device traffic within
the LAN. Internet access is secondary — sessions 1 and 2 need none at all.

---

## Hard requirements

These are deal-breakers. If any one is not met, the workshop cannot run as designed.

### 1. Single layer-2 broadcast domain

All clients — boards, laptops, phones, instructor — on **one SSID, one VLAN, one IP subnet**.
No guest network, no per-SSID segmentation, no separate VLAN per band.

### 2. Client-to-client traffic permitted

**Client isolation / AP isolation / "guest mode" must be OFF.** Laptops must be able to open
TCP connections to boards and receive connections from phones. This is the most common default
that breaks this kind of workshop.

### 3. mDNS / multicast forwarded between wireless clients

Devices are addressed by hostname (`devicename.local`), which uses multicast DNS on
**224.0.0.251 / UDP 5353**. This must reach all clients on the subnet, including
**wireless-to-wireless**.

Depending on the platform this means enabling an **mDNS gateway / Bonjour forwarding /
multicast repeater**, or simply permitting multicast between clients. Please confirm which
applies and that it is enabled.

Specifically ensure these are **not** silently dropping mDNS:

- Broadcast/multicast filtering or suppression
- "Multicast enhancement" / multicast-to-unicast conversion, if it does not handle mDNS
- IGMP snooping without a querier on the segment
- Proxy ARP / ARP suppression

### 4. 2.4 GHz enabled, WPA2-PSK

- **2.4 GHz must be available.** The microcontrollers have no 5 GHz radio.
- **WPA2-PSK (AES/CCMP)**, one shared password. **Not** WPA3-only, **not** WPA2/WPA3 mixed with
  PMF required, **not** WPA-Enterprise / 802.1X.
- Protected Management Frames (PMF/802.11w) must be **optional or disabled**, not required.
- If 2.4 and 5 GHz share an SSID, both must bridge to the same VLAN and subnet.

### 5. No captive portal, no splash page, no periodic re-authentication

Microcontrollers cannot accept terms or click a button. Association plus the WPA2 password must
be sufficient for full LAN access, permanently. No time-based session expiry, no daily
re-login.

### 6. Long-lived TCP connections must not be torn down

Each laptop holds a persistent TCP session to each of its boards for hours. Please disable any
**client idle timeout, session timeout, or inactivity disconnect** that would drop an
associated-but-quiet client. Boards must stay associated overnight with no server connected.

### 7. Multiple MAC addresses behind one wireless client

Participant laptops run Home Assistant in a virtual machine with a **bridged network adapter**,
so one laptop may present **two MAC addresses / two IP addresses** over a single wireless
association. Any feature that blocks this as MAC spoofing — client integrity checking, MAC
address limit per station, WDS restrictions — must be disabled.

*This is the requirement most likely to be missed. Please confirm explicitly.*

### 8. DHCP sized and long-leased

- Pool of **at least 300 usable addresses**
- **Lease time 7 days** (or the longest available, minimum 48 hours)
- Reserve a small static range outside the pool for instructor equipment

---

## Capacity and coverage

- Sustained **190+ concurrent clients**, with ~120 on 2.4 GHz. Please confirm the 2.4 GHz radio
  budget specifically, not just the total; band steering cannot help devices with no 5 GHz radio.
- Even coverage across the room at table height. Boards sit on tables among people and water
  containers, not in clear line of sight.
- Traffic per device is tiny (a few hundred bytes every few seconds). **Client count and
  multicast behaviour matter; bandwidth does not.** No per-client rate limiting needed, but
  nothing should throttle or deprioritise chatty small-packet clients.

## Physical and operational

- **Powered and running the day before** the first session, for a setup and test window.
- **Left running continuously overnight** between session days. Boards log data overnight; the
  network must stay up. Please confirm no scheduled nightly reboot or maintenance window.
- **One wired Ethernet drop** on the same subnet for the instructor server.
- On-site or on-call support during the setup window and the first session.
- SSID and password fixed and known **one week in advance** — they are compiled into the device
  firmware and cannot be changed on the day.

## Internet access

- **Not required** for sessions 1 and 2.
- **Required for one 30-minute block** in the final session (outbound HTTPS to a cloud service).
- Outbound HTTPS (443) and MQTT (8883) should not be blocked during that block.

---

## Acceptance test

We will run this with the provider during the setup window. All five must pass before the
network is accepted.

| # | Test | Pass criterion |
|---|---|---|
| 1 | Two boards and one laptop associated. From the laptop, `ping <boardname>.local` | Resolves and replies |
| 2 | From the laptop's VM (bridged), same ping | Resolves and replies — **this is the multicast + multi-MAC test** |
| 3 | Phone on WiFi opens `http://<VM-ip>:8123` | Page loads — client-to-client test |
| 4 | Laptop connected to a board, left idle 30 minutes | Connection still live, no reconnect in logs |
| 5 | All boards powered simultaneously | All obtain DHCP leases; none drop over 30 minutes |

Test 2 is the one that fails on default enterprise configurations. Please have someone
authorised to change controller settings present when we run it.

---

## Summary for a quick read

Everything on **one flat subnet**. **Client isolation off.** **mDNS forwarded between wireless
clients.** **2.4 GHz with WPA2-PSK, no captive portal.** **No idle timeouts.** **Allow two MACs
per laptop.** **DHCP 300+, week-long leases.** **Runs overnight.**
