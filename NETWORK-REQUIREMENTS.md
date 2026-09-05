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
| Participant laptops | **100 minimum** | 5 GHz preferred | One per team runs a Home Assistant server in a VM. Individual members may bring their own, so plan for more |
| Participant phones | **up to 100** | mobile data preferred, 5 GHz fallback | Used to open the team's own dashboard |
| Instructor equipment | 2–3 | **wired** | Presentation laptop + a Home Assistant server |

**Plan for 500 concurrent clients, and size headroom to 600.** Note that 500 is the *expected*
peak, not a comfortable ceiling: 200 microcontrollers plus at least 100 laptops plus phones
already reaches 400, before any participant connects a second device.

**The essential behaviour:** each laptop must discover and hold a persistent connection to *its
own two boards*, by hostname, over the wireless LAN — and the boards are on a different SSID and
band from the laptops. This is device-to-device traffic **across two SSIDs**. Internet access is
secondary; sessions 1 and 2 need none at all.

---

## Proposed design

This is the design we would like built. Please confirm it is achievable on your equipment, or
propose an equivalent.

| SSID | Band | Clients | Notes |
|---|---|---|---|
| `farm-iot` | **2.4 GHz only** | 200 ESP32 boards | Must not be broadcast on 5 GHz at all |
| `farm-laptop` | **5 GHz** | 100+ laptops, phones that need it | WiFi 6 strongly preferred for device density |

Phones are asked to use their own mobile data, and fall back to `farm-laptop` only if capacity
allows. The instructor's presentation laptop takes **wired Ethernet**.

Separating the microcontrollers onto their own 2.4 GHz SSID is deliberate: it lets that SSID be
tuned conservatively for simple clients (see §4) without holding the laptops back.

### Access points

- **2.4 GHz: 3 to 6 APs.** Note that 2.4 GHz has **only three non-overlapping channels (1, 6 and
  11)** — six APs cannot each be on a different frequency. Six is workable only as *two* cells per
  channel, spatially well separated with **reduced transmit power** so the co-channel cells do not
  hear each other. If that separation is not achievable in this room, **three APs on 1/6/11 is
  better than six**, because co-channel interference in a single room reduces capacity rather than
  adding it. We would rather have three well-planned APs than six fighting each other.
- **5 GHz: 6 APs or as many as coverage needs.** Plenty of non-overlapping channels here, and
  802.11ax/WiFi 6 OFDMA genuinely helps at this device density. Use it if available.
- Even coverage at **table height**. Boards sit among people, laptops and water containers, not in
  clear line of sight.

---

## Hard requirements

Deal-breakers. If any one is not met, the workshop cannot run as designed.

### 1. Both SSIDs on one layer-2 broadcast domain

`farm-iot` and `farm-laptop` must bridge to the **same VLAN and the same IP subnet**. A laptop on
5 GHz must reach a board on 2.4 GHz as if they were on the same wire.

If your architecture requires separate VLANs per SSID, then an **mDNS gateway / Bonjour
forwarding service must relay between them**, and unicast routing between the subnets must be
open. Please tell us which of the two approaches you are using.

### 2. Client-to-client traffic permitted, including between SSIDs

**Client isolation / AP isolation / "guest mode" must be OFF on both SSIDs, and traffic must be
allowed between them.** This is the single most common default that breaks this kind of event.
Every sensor reading crosses from the 2.4 GHz SSID to the 5 GHz SSID.

### 3. mDNS forwarded between wireless clients and across both SSIDs

Devices are addressed by hostname (`devicename.local`), which uses multicast DNS on
**224.0.0.251 / UDP 5353**. This must reach all clients on the subnet, **wireless-to-wireless and
across the two SSIDs**.

Ensure none of these silently drops it:

- Broadcast/multicast filtering or suppression
- "Multicast enhancement" / multicast-to-unicast conversion that does not handle mDNS
- IGMP snooping without a querier on the segment
- Proxy ARP / ARP suppression

> With ~500 clients in one broadcast domain, we accept that broadcast load needs managing. Please
> suppress what you must, **but mDNS on 5353 has to survive.** If you need to rate-limit
> multicast, tell us the limit so we can check it is above what 200 announcing devices generate.

### 4. `farm-iot` tuned for simple clients

The ESP32 has one 2.4 GHz radio and a basic supplicant. On that SSID specifically:

- **WPA2-PSK (AES/CCMP)**, one shared password. Not WPA3-only, not WPA2/WPA3 mixed with PMF
  required, not WPA-Enterprise.
- **PMF / 802.11w must be optional or disabled**, not required.
- **No 802.11r / k / v fast roaming.** These confuse simple clients; the boards do not move.
- **No band steering** (there is nothing to steer to) and no minimum-data-rate setting that
  excludes low 802.11n rates.
- **No captive portal, no splash page, no periodic re-authentication.** A microcontroller cannot
  accept terms. Association plus the password must grant full LAN access, permanently.

### 5. Long-lived TCP connections must survive

Each laptop holds a persistent TCP session to each of its two boards for hours. Disable any
**client idle timeout, session timeout or inactivity disconnect**. Boards must stay associated
overnight with no server connected to them.

### 6. Multiple MAC addresses behind one wireless client

Participant laptops run Home Assistant in a VM with a **bridged network adapter**, so one laptop
presents **two MAC addresses and two IP addresses** over a single association. Any feature that
treats this as MAC spoofing — client integrity checking, a MAC-per-station limit, WDS
restrictions — must be disabled.

*Easy to miss. Please confirm explicitly.*

### 7. DHCP scope large enough — a /24 will not do

Count the leases, not the devices. **Each laptop takes two**, because Home Assistant runs in a
bridged VM with its own MAC and IP:

| | Leases |
|---|---|
| 200 ESP32 boards | 200 |
| 100 laptops × 2 (host + VM) | 200 |
| extra laptops members bring | up to 100 |
| phones that fall back to WiFi | up to 100 |
| **Total** | **500–600** |

- **A /23 (510 usable) is the practical minimum and is tight. A /22 (1022) is the comfortable
  choice** and leaves room for lease churn over a two-day event.
- **Lease time 12–24 hours.** *(Revised down from the 7 days requested earlier — see the note
  below.)* Devices are addressed by hostname, not IP, so a changed lease costs nothing, and
  shorter leases stop departed devices holding addresses.
- Reserve a small static range outside the pool for instructor equipment.

> **Why the lease time changed.** An earlier draft asked for week-long leases so board addresses
> would stay stable. That is no longer needed: Home Assistant stores `<name>.local` and re-resolves,
> so a board may change IP freely. Shorter leases relieve pool pressure, which matters more.

> **A /22 is not exotic** — large flat wireless subnets are routine at conference scale. But the
> prefix length is not what carries risk here; the size of the **broadcast domain** is. See §9.

### 8. Multicast load in a 500-client broadcast domain

This is the part of the design we are least able to predict, and where we most want your advice.

Putting every client in one broadcast domain is what makes `<name>.local` work across the two
SSIDs. The cost is that **every broadcast and multicast frame reaches every client**, and at
2.4 GHz multicast is sent at a low basic rate, so it consumes disproportionate airtime.

The mDNS talkers are not just our boards:

- 200 ESP32s announcing their own service records — modest, and mostly at boot
- **100 Home Assistant instances**, which actively probe for many integrations over mDNS — chatty
- **phones**, if any fall back to WiFi; iOS in particular is very chatty with Bonjour

What we are asking for:

- **Keep mDNS on UDP 5353 working**, but suppress other broadcast/multicast you judge unnecessary
- If your APs support **multicast-to-unicast conversion that correctly handles mDNS**, please
  enable it — it converts the flood to per-client unicast at proper data rates and is the single
  biggest win available here
- If you apply a **multicast rate limit**, tell us the threshold so we can sanity-check it against
  what ~400 announcing devices generate
- Tell us if you would rather **split into several VLANs with an mDNS gateway** between them. We
  will accept that if you prefer it, but only if the gateway is proven, because a flaky mDNS
  reflector fails in ways that look exactly like our own bugs

> **On our side:** the boards are configured with WiFi power save **disabled**, so they stay awake
> and do not depend on DTIM timing to collect buffered multicast. That removes the most common
> reason an ESP32 misses mDNS traffic in a dense room.

### 9. Association surge

If an AP or controller restarts, **200 ESP32s will attempt to reassociate at once**. Please
confirm there is no association rate limit or client-count-per-radio cap that would leave some
boards unable to rejoin, and that the DHCP server can absorb a burst of 200 requests.

---

## Physical and operational

- **Powered and running the day before**, for a setup and test window.
- **Left running continuously overnight** between session days. Boards log data overnight. Please
  confirm no scheduled nightly reboot or maintenance window.
- **One wired Ethernet drop** on the same subnet for the instructor position.
- On-site or on-call support during the setup window and the first session.
- **SSID names and passwords fixed and known one week in advance** — they are compiled into the
  firmware of 200 boards and cannot be changed on the day.

## Internet access

- **Not required** for sessions 1 and 2.
- **Required for one 30-minute block** in the final session (outbound HTTPS to a cloud service).
- Outbound HTTPS (443) and MQTT (8883) should not be blocked during that block.

---

## Acceptance test

To be run with the provider during the setup window. All six must pass.

| # | Test | Pass criterion |
|---|---|---|
| 1 | Two boards on `farm-iot`, one laptop on `farm-laptop`. From the laptop, `ping <boardname>.local` | Resolves and replies — **this is the cross-SSID mDNS test** |
| 2 | Same ping from inside the laptop's bridged VM | Resolves and replies — **multicast + multi-MAC test** |
| 3 | Phone on `farm-laptop` opens `http://<VM-ip>:8123` | Page loads — client-to-client test |
| 4 | Laptop connected to a board, left idle 30 minutes | Connection still live, no reconnect in logs |
| 5 | **20–30 boards powered simultaneously** | All associate and obtain leases; none drop over 30 minutes |
| 6 | Power-cycle one AP with those boards associated | All rejoin without manual intervention |

Tests 1 and 2 are the ones that fail on default enterprise configurations. Please have someone
authorised to change controller settings present.

> **On the untestable part.** We can bring 20–30 boards to the setup window, which is 10–15 % of
> the final load. That validates the channel plan, mDNS across SSIDs, association and DHCP — it
> catches configuration errors, which are the likely failure mode. It does **not** validate
> behaviour at 200 boards. For that we are relying on your capacity planning, which is why §8 and
> the 2.4 GHz AP question above matter.

---

## Summary for a quick read

Two SSIDs, **one flat subnet**. `farm-iot` 2.4 GHz for 200 microcontrollers, WPA2-PSK, no fast
roaming, no PMF requirement. `farm-laptop` 5 GHz WiFi 6 for 100+ laptops. **Client isolation off,
including between the two SSIDs.** **mDNS forwarded across both.** **No idle timeouts.** **Two
MACs per laptop.** **DHCP /23 minimum with week-long leases.** **Runs overnight.** Plan for 500
clients, size for 600.
