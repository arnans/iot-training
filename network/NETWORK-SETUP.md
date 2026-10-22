# Workshop Network Setup

*Supersedes [NETWORK-REQUIREMENTS.md](NETWORK-REQUIREMENTS.md) (the per-SSID VLAN design), retired
21 Sep 2026. That document and its Thai edition stay in the repository for reference only.*

The workshop runs **two separate wireless networks in one room**:

1. **The workshop LAN** — three GL.iNet Flint routers we bring and configure ourselves, one per
   zone (red / green / blue). Each carries that zone's boards on 2.4 GHz and that zone's Home
   Assistant laptop and one phone per team on 5 GHz. This is where boards, Home Assistant and
   dashboards reach each other, by IP address. The boards run with mDNS off (see
   `firmware/README.md`). No VLANs, no controller, no coordination with
   anyone: each Flint is its own subnet, so zone isolation is a property of the hardware.
2. **The internet WiFi** — provided by NT, 5 GHz only, for every other laptop and phone in the
   room. Its job is internet access for the worksheet site and web.esphome.io. **Devices on it
   cannot reach any board or Home Assistant**, and that is by design.

The three Flints plug into NT's gateway by cable for their own internet access (web.esphome.io
from the Home Assistant laptop; the Session 3 remote-access demo).

![The two networks. Three Flint routers, one per zone, each a private subnet with a 2.4 GHz SSID for boards and a 5 GHz SSID for the Home Assistant laptop and one phone. All three plug into NT's gateway by cable. NT's 5 GHz WiFi carries every other laptop and phone and reaches only the internet.](../docs/images/network-setup-en.svg)

Section 1 is what we ask of NT. Sections 2–5 are our own configuration, the rules for
participants, the acceptance test and the risks. Section 6 records why this replaced the VLAN
design.

---

## 1. What we ask of NT

NT is the venue's internet provider for this event, contracted for **500 devices**. Nothing below
asks NT to configure device-to-device traffic, multicast or VLANs; those all live inside our
routers.

### 1.1 Three wired ports for our routers

> **Three RJ45 Ethernet ports, 1 GbE, each giving a DHCP lease with plain internet access.** Each
> port feeds one of our routers, which NATs a zone of roughly 170 clients behind a single MAC and
> IP. On these three ports: **no captive portal, no MAC registration, no login of any kind**, no
> per-MAC bandwidth cap that treats the router as one user, and no idle timeout. Isolation between
> the three ports is fine; they never need to see each other.

The ports can be at one location, in which case we run our own cables (up to ~50 m) to the three
zone positions, or one near each zone position. Bandwidth need is modest, under 50 Mbps per port.
A **fourth port** of the same kind for the presentation laptop, near the stage, if convenient.

Outbound traffic: **unrestricted is preferred.** If NT filters, then at minimum TCP 443, UDP 53
and UDP 123 from all four ports. No inbound access is required anywhere.

### 1.2 The internet WiFi

> **5 GHz only. 2.4 GHz off on every NT access point.** Our three routers are the only 2.4 GHz
> transmitters in the room; 200 microcontroller boards live there and they are the clients that
> cannot cope with interference.

- **Capacity: up to ~600 associations** — 300 laptops plus up to 300 phones, since each team's
  remaining three members join NT rather than our routers. The contract says 500; the difference
  is the phones people may not join.
- **SSID name that says what it is**, for instance `farm-internet`. Participants will see two
  kinds of WiFi and must pick the right one from the name alone. Please do not name it with
  `farm-iot` or `farm-laptop`; those are ours.
- **Login: preferably none.** If a captive portal is required, one login per device for the
  whole two days, no daily re-authentication.
- Client isolation on NT's WiFi is fine, and even preferable: nothing on it talks to anything
  else on it.

### 1.3 Sharing the 5 GHz band

Our routers and NT's access points share 5 GHz in one ballroom. We keep to three narrow,
non-DFS channels so NT keeps the rest of the band:

> **Our routers use 5 GHz channels 36, 44 and 149, each at 20 MHz.** Please keep NT's 5 GHz
> radios off those three channels, or tell us which channel plan NT prefers and we will move.
> Everything else, including all DFS channels (52–144) and 157–165, is NT's.

Please do not mount an NT access point directly above or beside one of our routers; a few metres
apart is enough.

### 1.4 Setup window and support

We ask for the three ports to be live during the **setup window on the afternoon before Day 1**,
with someone on call who can change the NT configuration, and on-site or on-call support through
the first hour of the workshop. The acceptance test in section 4 is what we will run.

---

## 2. Our routers: configuration per zone

Three GL.iNet Flint routers (Flint 2, GL-MT6000, or Flint 3, GL-BE9300; settings are the same on
both), plus a **fourth as a cold spare** carrying all three zone configurations exported. Configure
all four in advance, at the office, from a single checklist; the only site work is plugging in.

### 2.1 SSIDs, subnets, channels

| Zone | 2.4 GHz SSID (boards) | 5 GHz SSID (HA laptop, one phone) | LAN subnet | Router IP | 2.4 GHz ch. | 5 GHz ch. |
|---|---|---|---|---|---|---|
| red   | `farm-iot-red`   | `farm-laptop-red`   | `10.10.0.0/22` | `10.10.0.1` | 1  | 36  |
| green | `farm-iot-green` | `farm-laptop-green` | `10.20.0.0/22` | `10.20.0.1` | 6  | 44  |
| blue  | `farm-iot-blue`  | `farm-laptop-blue`  | `10.30.0.0/22` | `10.30.0.1` | 11 | 149 |

**Password `iotfarmer` on all six SSIDs. WPA2-PSK (AES/CCMP), not WPA2/WPA3 mixed.**

> **The SSID names and the password are compiled into the firmware of 200 boards** and cannot be
> changed on site. They are unchanged from the VLAN design, so no firmware rebuild is needed.

Why a /22 and not the router's default `192.168.8.0/24`: a /24 is 250 leases, and one zone needs
~170–270 (67 boards, 34 laptops × 2 for the bridged VM, 34 phones, spares). Distinct subnets per
zone also make a wrong-zone device obvious from its address.

### 2.2 Settings checklist, every router

Work through the GL.iNet admin UI (`http://<router IP>`) and, where noted, LuCI (**System → Advanced
Settings**).

**Wireless**

- [ ] 2.4 GHz: SSID and password per the table; **WPA2-PSK**; fixed channel per the table;
      **20 MHz** bandwidth; TX power maximum; mode left at default (b/g/n/ax mixed). If boards
      fail to associate on the bench, force **802.11n** in LuCI.
- [ ] 5 GHz: SSID and password per the table; **WPA2-PSK**; fixed channel per the table;
      **20 MHz**; TX power maximum. Never a DFS channel (52–144): a radar event vacates the
      channel for a minute or more and the whole zone drops.
- [ ] Different SSID per band. Do **not** use "same SSID on both bands" / band steering.
- [ ] **Guest WiFi off** on both bands (the guest network is the only place client isolation
      exists on these routers; the main network has none).
- [ ] PMF / 802.11w: **optional or disabled**, never required. 802.11r off.
- [ ] 6 GHz radio (Flint 3 only): off. Nothing in the room uses it and it is one more thing to
      explain.

**LAN and DHCP**

- [ ] LAN IP and mask per the table.
- [ ] DHCP pool: the whole /22 minus the first 20 addresses. **Lease time 72 hours**, covering both
      days plus the setup window. **This is load-bearing.** Teams add their boards to Home
      Assistant by the IP address the board prints at boot, and Home Assistant cannot follow a
      board whose address moves. A long lease means a board that reboots or rejoins gets its old
      address back. Reservations are not needed.
- [ ] Confirm in LuCI that **IGMP snooping is off** on `br-lan` (OpenWrt default; check it stayed
      that way).
- [ ] The router's DNS resolves DHCP client hostnames, so `http://gogo-iot-red-6749a4/` works from
      any client of that router **without mDNS**. Leave that on (default). Participants are
      taught the IP address; the name is a shortcut for instructors, checked by test #7.

**WAN**

- [ ] WAN as DHCP client. Nothing else: **no VPN client, no AdGuard, no DNS override**, no
      "Internet kill switch", no parental control.
- [ ] Double NAT (ours behind NT's) is expected and fine for everything we do.

**System**

- [ ] **Auto-update off. Scheduled reboot off.** No maintenance of any kind for the duration.
- [ ] Admin password set and written on the router with tape; the same on all four.
- [ ] Export the configuration (**System → Backup**) and load all three exports onto the spare
      and onto the instructor's USB stick.
- [ ] Label each router with its zone colour, both sides, large.

### 2.3 Placement

- **One router per zone area, at the zone's centre**, on a stand about 2 m up, antennas
  vertical. Boards sit at table height among people, laptops and water glasses; height beats
  power for even coverage.
- **Mains power at each position** (the Flints are not PoE-powered). Bring a 10 m extension lead
  and gaffer tape per router.
- Ethernet from NT's port to each router: bring a 50 m cable per router in case the ports are
  all in one corner.
- The spare stays with the instructor kit, powered, on the bench, WAN unplugged.

### 2.4 Kit handout follows the router

The zone is compiled into each board, so the zone is now **spatial as well as logical**: a red
team must sit where the red router is. Practically:

- Divide the floor into three areas before the room opens. Signs in each colour.
- Hand red kits out only in the red area, and so on. The kit colour is the check.
- All three routers will be audible from anywhere in a ballroom, so a red kit in the green area
  still works, only with a weaker signal. "Stay in your zone" is about signal quality, not
  connectivity.

---

## 3. Rules for participants: who joins which WiFi

This goes on the team card and is said aloud at the start of Session 1.

| Device | Joins | Why |
|---|---|---|
| The team's **Home Assistant laptop** (the one running the VM) | The team's zone 5 GHz SSID, `farm-laptop-<colour>` — **and nothing else** | It must reach the team's boards by IP address; those addresses exist only on the zone network |
| **One phone per team** (for the dashboard) | The team's zone 5 GHz SSID | Same reason; the dashboard is on the laptop, not on the internet |
| Every **other laptop and phone** | NT's internet WiFi | Worksheet site and web.esphome.io are online; nothing else is needed |
| The two boards | Nothing to do: the zone 2.4 GHz SSID is compiled in | |

> **The Home Assistant laptop must not have NT's WiFi saved.** If it does, Windows and macOS will
> hop to it whenever the zone signal dips, Home Assistant loses its boards, and nothing on screen
> says why. Forget the NT network on that laptop, or never join it.

Each zone SSID has room for the HA laptop and one phone per team only. If a whole team of four
joins the zone WiFi with every device, the router carries ~200 clients instead of ~140; it may
cope, but the bench test (section 4) does not cover it.

**Instructor kit and stage.** The instructor kit laptop joins its own kit's zone SSID like any
team, and gets internet through that router for the Session 3 Home Assistant Cloud demo. The
presentation laptop uses NT's fourth wired port, or NT's WiFi.

---

## 4. Acceptance test

Run during the setup window, before anything is handed out. Tests 1–4 need only NT's three ports
to be live; the rest need our routers in position. All must pass.

| # | Test | Pass criterion |
|---|---|---|
| 1 | Each router's WAN, plugged into its NT port | Gets a lease; router's own diagnostics reach the internet — **no portal, no MAC auth** (1.1) |
| 2 | Laptop on `farm-laptop-red` opens <https://web.esphome.io> and the worksheet site | Both load — internet through the router |
| 3 | Laptop on NT's WiFi opens the same two sites | Both load — NT WiFi works for the other three members |
| 4 | WiFi scanner on a laptop in each zone area | NT's 5 GHz radios are **not** on 36, 44 or 149; **no 2.4 GHz** network other than our three (1.2, 1.3) |
| 5 | Board on `farm-iot-red`, laptop on `farm-laptop-red`: `ping <board IP>`, the IP read from the boot log at web.esphome.io | Replies — cross-band traffic inside a zone |
| 6 | Same ping from inside the laptop's bridged VM, then add the board in that VM's Home Assistant by IP, port 6053 | Replies; Home Assistant connects and shows the board's name — two MACs behind one client |
| 7 | Same laptop: `http://<boardname>/` (no `.local`) | Loads — the router's DNS resolves DHCP hostnames (instructor shortcut, 2.2) |
| 8 | Phone on `farm-laptop-red` opens `http://<VM-ip>` | Dashboard loads — client-to-client, port 80 |
| 9 | Laptop on `farm-laptop-green` pings the red board's IP | **Fails** — zones isolated (should be true by construction; proves nothing is bridged by mistake) |
| 10 | Laptop on NT's WiFi opens `http://<VM-ip>` | **Fails** — documents the rule in section 3 for anyone who doubts it |
| 11 | Laptop connected to a board, idle 30 minutes | Connection still live |
| 12 | **20–30 boards** on one router, note five boards' IPs, then power-cycle that router | All associate and get leases; all rejoin within two minutes of the restart; **the five keep their IPs** |
| 13 | **Spare swap drill**: unplug the red router, plug the spare in, restore the red export | Boards and laptop reconnect; under five minutes end to end; boards added in Home Assistant come back without being re-added |
| 14 | Laptop with both `farm-laptop-red` and NT's WiFi saved, walk to the far side of the room | Note what it does. This is the failure the team-card rule prevents; the point is to have seen it |
| 15 | Laptop on `farm-laptop-red`, boards from the handout batch powered: `dns-sd -B _esphomelib._tcp` for 10 seconds | **Lists nothing** — the boards run with mDNS off. A board listed here still has old firmware; re-flash it |

> **What this cannot test.** 20–30 boards is about a third of one router's 2.4 GHz load and none
> of its 5 GHz load. It validates configuration. Router capacity at ~140 clients is the one open
> question in this design (section 5) and is what the office bench test before the event is for:
> as many boards, laptops and phones as can be borrowed, on one router, with the power-cycle.

---

## 5. Risks and what covers them

| Risk | Cover |
|---|---|
| **A Flint at ~140 associated clients** (67 boards + ~34 laptops × 2 + ~34 phones). No published figure; consumer routers are rarely run this way | Office bench test with as many real clients as possible. Keep the 5 GHz side to HA laptop + one phone (section 3). If the bench test worries us, split each zone across two routers with a second SSID pair, which needs a firmware rebuild, so decide **at least a week out** |
| **One router dies = a third of the room stops** | Fourth router, configured, on the bench; swap drill in the acceptance test (#13) |
| NT's port turns out to have a captive portal or MAC registration | Found by test #1 in the setup window, with NT on call. Fallback for the laptops: the board work in Sessions 1–2 needs no internet at all; only web.esphome.io and the worksheet site are lost, and an instructor phone hotspot covers the Session 3 demo |
| HA laptop hops to NT's WiFi mid-session | Team-card rule and test #14. Symptom to teach the TAs: entities go `unavailable` on a laptop that still has internet |
| 5 GHz channel overlap with NT, or a DFS event | Fixed non-DFS channels (2.1); NT told which ones (1.3); test #4 |
| DHCP pool exhaustion | /22 per zone, 72 h lease |
| A board's IP moves, so Home Assistant shows it `unavailable` | 72 h lease (2.2); tests #12 and #13 check addresses survive a router restart and a spare swap. If one moves anyway, the team reads the new IP at web.esphome.io and enters it under the board's **Reconfigure** in Home Assistant, which keeps the device and its name |
| A team sits in the wrong colour area | Works anyway, weaker signal. Move them if the TAs notice; not an emergency |
| Router firmware auto-updates or reboots overnight | Both off in the checklist (2.2). Boards rejoin on their own regardless (`reboot_timeout` is disabled in the firmware), so even an unplanned reboot costs a minute |
| NT has 2.4 GHz on after all | Test #4. Ask for it off; if NT cannot, our three channels 1/6/11 still work, with more retries |

---

## 6. Why this replaced the VLAN design

The VLAN design ([NETWORK-REQUIREMENTS.md](NETWORK-REQUIREMENTS.md)) asked the provider to build
three VLANs, broadcast six SSIDs on every AP, forward mDNS inside each VLAN and not between them,
tolerate two MACs per client and hold long DHCP leases. Every one of those is off by default on
managed enterprise WiFi, the acceptance test existed to catch them, and one wrong controller
setting (an mDNS reflector turned on "helpfully") would have silently collapsed the zoning into a
flat 500-client multicast domain.

With three routers we own:

- **Zone isolation is physical.** Separate subnets behind separate NATs; nothing to reflect.
- **The 2.4 GHz plan is exactly the ideal one**: three radios on 1 / 6 / 11, one per zone, and
  with NT's 2.4 GHz off they are alone in the band.
- **mDNS across bands works by default** on an OpenWrt bridge; there is no controller feature to
  turn off. (Since 21 Oct 2026 the boards run with mDNS off and are added to Home Assistant by
  IP, because ~100 Home Assistant instances browsing for boards made every board answer by
  multicast and the storm took the WiFi down. Cross-band unicast still relies on the same bridge.)
- **NT's job shrinks to the thing enterprise WiFi is good at**: internet for 600 laptops and
  phones, plus three cable ports.
- **The firmware does not change.** Same SSIDs, same password, same zone build.

What it costs: zones become spatial (kits handed out by area), a team's HA laptop must stay off
the NT WiFi, and one consumer router per zone carries a client count nobody publishes a figure
for. Section 5 covers each.

Dropped from the old spec, no longer needed anywhere: VLAN IDs, per-SSID isolation settings,
mDNS-reflector prohibition, multicast-to-unicast conversion, association-rate limits, the
"fallback flat subnet" (section 6 of the old document) and outbound 8883, since the Session 3
remote-access demo is Home Assistant Cloud over 443 and MQTT left the worksheet.
