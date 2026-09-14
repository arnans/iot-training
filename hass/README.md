# Home Assistant configurations

Two `configuration.yaml` files, one per role. Neither is something a participant edits.

| File | Runs on | Purpose |
|---|---|---|
| `configuration.yaml` | each team's laptop VM | Minimal install: no `default_config`, no ssdp/dhcp/bluetooth/usb/cloud |
| `configuration-instructor.yaml` | *(unused since 7 Sep 2026)* | Same diet plus **recorder limits** for 100 adopted boards. Written for an instructor server that adopted every team's sensor node; that plan was dropped — see WORKSHEET-TODO.md. Kept until the delete/keep call is made |

## Decided: ship a pre-built VirtualBox OVA

Participants receive a **VirtualBox appliance (OVA)** with this configuration inside, a bridged
adapter preconfigured, and onboarding already done to a known user. The install guide reduces to
"install VirtualBox, import this file, press Start". This replaces the from-scratch install guide
entirely.

**Two master images are required, not one.** Home Assistant OS ships separate builds per CPU
architecture: x86-64 (Windows PCs and Intel Macs) and ARM64 (Apple Silicon M1–M4 Macs). They are
not interchangeable — an Apple Silicon Mac cannot import or boot the x86-64 OVA. Importing the
ARM64 image also needs different VirtualBox settings: **OS Version: Oracle Linux (ARM 64-bit)**
and storage controller **VirtioSCSI** instead of SATA. Both architectures require **UEFI** firmware
enabled on the VM. The install guide must branch on "what kind of computer do you have" before a
participant even opens VirtualBox. See
[home-assistant.io/installation/alternative](https://www.home-assistant.io/installation/alternative/).

### Step-by-step build (repeat once per CPU architecture — x86-64, then ARM64)

1. **Download** the HAOS `.vdi` for the target architecture —
   [home-assistant.io/installation/alternative](https://www.home-assistant.io/installation/alternative/).
2. **Create the VM**: VirtualBox → New → Linux → **Oracle Linux (64-bit)**, or **Oracle Linux
   (ARM 64-bit)** for Apple Silicon. ≥2 GB RAM, ≥2 vCPUs, **Enable EFI**.
3. **Attach the real disk**: Settings → Storage → remove the wizard's placeholder under
   Controller: SATA → Add hard disk → select the downloaded `.vdi`. Use **VirtioSCSI** instead
   of SATA for ARM64.
4. **Resize before first boot**: `VBoxManage modifymedium disk "<path>.vdi" --resize <MB>` — HAOS
   expands its data partition to fill whatever the disk reports, on first boot only.
5. **Network**: Settings → Network → Attached to **Bridged Adapter** → pick the real NIC.
6. **Boot.** Read the **IP** off the console — not the `homeassistant.local` suggestion, which is
   only reliable while this is the sole HA instance on the network.
7. **Onboard**: browse to `http://<IP>`, create the workshop user/password.
8. **Install File editor**: Settings → Add-ons → Add-on Store → *File editor* → Install → Start →
   show in sidebar.
9. **Load the config**: replace `/config/configuration.yaml` with this directory's
   [configuration.yaml](configuration.yaml); create `automations.yaml` (`[]`), `scenes.yaml`
   (`[]`), `scripts.yaml` (`{}`) — the repo doesn't ship these yet and `!include` needs them to exist.
10. **Restart**, then click through Settings, Automations, Dashboards — confirm no errors or
    notifications.
11. **Settings → System → Network**: confirm the port is **80**, not 8123 (deliberate — shorter
    URL, nothing to mistype). This is UI-managed state, not in the YAML, so check it by hand
    every build.
12. **Settings → System → Storage**: confirm the disk resize actually took effect. For reference,
    the bench build reads **~6 GB used of 30.8 GB** once onboarded with the File editor add-on —
    so 10 GB is comfortable and 30 GB is generous. A dynamically-allocated `.vdi` exports at
    roughly the used size, not the cap, so a large cap costs nothing in distribution.
13. **Set up the Overview dashboard.** The bench image ships with farm-themed **Areas** (Flower
    Farm, Corn Farm, Grass) on the landing page, which teams can rename. Only Flower Farm maps to
    the actual kit — session 2's garden-lamp scenario. Corn Farm echoes session 3's paper design
    challenge and has no hardware behind it; decide whether that helps or confuses before it
    ships to 100 laptops.
13. Confirm **UI language is English**.
14. **Disable auto-update**: console → `ha supervisor options --auto-update=false`, confirm with
    `ha supervisor info`. Covers Supervisor; check Core/OS/add-ons separately if you want
    everything pinned (each add-on has its own "Auto update" toggle on its own page).
15. **Reachability check**: from another device on the same LAN, browse to `http://<IP>` (no
    port). If refused, see `NETWORK-REQUIREMENTS.md` item 2 — two MACs behind one wireless client.
16. **Export**: File → Export Appliance → the master OVA.
17. **Test-import** on a second machine of the same architecture before trusting it.
18. **Write the team card**: VM user/password, zone colour, laptop SSID and password.

This also closes the two install-guide risks already in WORKSHEET-TODO: the bridged-vs-NAT
adapter choice (baked in) and port 80 reachability from phones (the VM's firewall is ours).

### What the participant guide assumes about the image

The participant guide is [docs/install.md](../docs/install.md). It is written against these
facts; change one here and the guide (and session 1's ก่อนเริ่ม) must change with it:

- **VM name `Farm Workshop`** — the guide and session 1 tell participants to press Start on it.
- **File names** `farm-workshop-x86-64.ova` (Windows + Intel Mac) and `farm-workshop-arm64.ova`
  (Apple Silicon). Fill in the real download links, the file size, and the workshop
  user/password where the guide says `TODO`.
- **Adapter 1 is Bridged.** The host NIC name inside the OVA is the build machine's, so
  every participant re-picks their WiFi card after import (guide step 2.3). Otherwise Start
  fails with "physical network interfaces were not found".
- **Import with "Generate new MAC addresses for all network adapters".** Participants set this
  explicitly (guide step 2.2). CPU and RAM come from the OVA; participants leave them alone. With "Include all network adapter MAC addresses", every clone
  keeps the build machine's MAC, and 34 identical MACs in one zone break the network.
- **Port 80, IP read from the console.** The guide says to read the `IPv4 addresses` line and
  ignore `homeassistant.local`. Before sending the guide, replace the placeholder screenshots
  with real ones from the final build, and check the banner wording matches, especially on
  ARM64, where the interface name may not be `enp0s3`.

## What the team config removes, honestly

- **`ssdp`** — periodic UPnP M-SEARCH multicast to 239.255.255.250. Pure noise here. Removed.
- **`dhcp`** — passive sniffing; no traffic of its own, but nothing to find. Removed.
- **bluetooth, usb, cloud, stream, media, assist, energy, backup, my, alerts** — unused, and
  several attempt outbound internet at startup on a network that has none. Removed.

What it does **not** remove: zeroconf's browse breadth. Home Assistant browses every service type
in its generated discovery list so it can show "Discovered" cards, and that list does not shrink
when integrations are left out. The ESPHome integration also depends on zeroconf, so it stays.
The residual mDNS cost is therefore the **startup burst** when 100 instances come up and each
queries, and 200 boards answer — see the zoning discussion in `NETWORK-REQUIREMENTS.md`.

## The instructor recorder problem

100 sensor boards × (illuminance at 1 s + vibration at 1 s + pressure at 5 s) is roughly
220 state writes per second, on the order of 10 million rows overnight. SQLite will not cope.
Temperature and humidity are polled at 1 s but filtered on the board (send on a 0.2 °C / 0.5 %RH
change, otherwise every 30 s), so in a still room they add only a few writes per second across
all boards; a room-wide change such as doors opening spikes that briefly.
`configuration-instructor.yaml` excludes vibration and diagnostics entirely and leaves one
decision open: **illuminance from all boards, or from a sample of ten.** The lights-off trace is
session 2's hook, and one board's trace tells that story as well as a hundred. Sample is
recommended; the ten board names get filled in during kit prep.

## Instructor kit: remote-access demo (Session 3)

The instructor kit runs the same team OVA, plus one line so Settings → Home Assistant Cloud exists:

```yaml
cloud:
```

Add it to that one instance only, restart, sign in with the prepared Nabu Casa account, enable
Remote access, and note the remote URL. Initial provisioning can take a while, so do this before
the day and keep a recorded run from mobile data as the backup. Team VMs stay without `cloud:`.

## Not verified yet

- The recorder `exclude`/`include` globs assume the entity-id shape produced by the Thai+ASCII
  entity names in `firmware/`. Confirm one board's actual entity_ids before relying on them.

## Verified on the bench

- HA boots cleanly with this exact component list — no panel quietly needed a dropped
  `default_config` dependency. One fix needed: the deprecated `http:` YAML key throws a
  migration warning now and must be removed (see `configuration.yaml`'s comment on it).
