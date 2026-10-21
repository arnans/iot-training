# Home Assistant configurations

Two `configuration.yaml` files, one per role. Neither is something a participant edits.

| File | Runs on | Purpose |
|---|---|---|
| `configuration.yaml` | each team's laptop VM | Minimal install: no `default_config`, no ssdp/dhcp/bluetooth/usb/cloud |
| `configuration-instructor.yaml` | *(unused since 7 Sep 2026)* | Same diet plus **recorder limits** for 100 adopted boards. Written for an instructor server that adopted every team's sensor node; that plan was dropped — see planning/WORKSHEET-TODO.md. Kept until the delete/keep call is made |

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
    port). If refused, the bridged VM's second MAC is being blocked; on the workshop routers (`network/NETWORK-SETUP.md`) this cannot happen, so it is the office WiFi.
16. **Export**: File → Export Appliance → the master OVA.
17. **Test-import** on a second machine of the same architecture before trusting it.
18. **Write the team card**: VM user/password, zone colour, laptop SSID and password.

### The 1.3 images (21 Oct 2026): PR #6 applied to both architectures

| File | Bytes | SHA-256 |
|---|---|---|
| `Farm-Workshop-win-1.3.ova` | 2,086,696,960 (~1.9 GiB) | `faeb6edfe0372115026d23c05bd60d6b21b4b1a48c65f1e5548d760f05521e32` |
| `Farm-Workshop-arm64-1.3.ova` | 2,069,125,120 (~1.9 GiB) | `3d10b1942de12311c9e8d8e9d6ab93ad20515d9e59fe506c112b70d943d46225` |

Both were made from the 1.2 images, not from scratch. Each 1.2 disk was booted under QEMU on a
Windows x86-64 host: WHPX for x86-64, TCG emulation for ARM64. The NIC sat at PCI slot 3 or 8,
so the guest kept the `enp0s3`/`enp0s8` names. The changes went in through the root console.
The disk was then trimmed and converted back with
`VBoxManage clonemedium --format VMDK --variant Stream`, and packed with the 1.2 OVF and NVRAM
left as they were (only the OVF file name changed). The NIC type, MAC handling and Bridged
Adapter 1 are therefore exactly as in 1.2.

Applied to both images:

- `configuration.yaml` is this directory's copy from the mDNS-off change (`zeroconf:` removed),
  SHA-256 `4a820d20…cb4f4`, byte-equal to `git show HEAD:hass/configuration.yaml`. That is LF,
  so hash the git blob, not a Windows CRLF checkout.
- **Settings → System → Network**: IPv6 `disabled` on the one interface. Supervisor stores this
  as NetworkManager `ipv6.method=link-local`, so an `fe80::` address remains and nothing else.
  HA's adapter selection is pinned to the one NIC: `.storage/core.network` has
  `configured_adapters` set to `["enp0s3"]` on x86-64 and `["enp0s8"]` on ARM64.
- Supervisor 2026.09.2 → **2026.10.2**. Core updates are refused while Supervisor is behind, and
  2026.09.2 already showed as `unsupported: supervisor_version`. `auto_update` stays `false`.
- The workshop user's browser login tokens, the recorder database and the archived host journal
  were deleted, so the images ship no build-time sessions or history.

The x86-64 1.2 image was a leftover bench build, so it also needed bringing level with ARM64.
Core 2026.9.1 → **2026.9.3**. These were removed:

- the `thread` entry, discovered on the builder's home LAN. `thread` *depends on* `zeroconf`, so
  with it in place zeroconf still started ("Starting Zeroconf broadcast") even after the YAML
  change.
- `met`, and the ignored discoveries: Hue, Cast, three Android TVs, a Canon printer, and ESPHome
  `gogo-relay-red-b97c54`.
- the sample automation, the Terminal & SSH add-on, `configuration.yaml.bak`, `.cache`, and
  143 MB of journal that held home-LAN device names and IPs.
- the old OS in the inactive boot slot. The bench image had been updated from HAOS 18.2, so it
  boots from slot B (18.3) and slot A still held 18.2: 226 MiB of incompressible squashfs. Slot
  A is marked bad (`rauc status mark-bad other`) and its partitions discarded. That leaves the
  x86-64 image in the same state as a fresh install, and as ARM64, whose slot B was never written.
  Without this the OVA was 2,331,156,480 bytes, over GitHub's 2 GiB per-asset limit.

These were added: Radio Browser (the ARM64 image already had it from onboarding), File editor
*shown in sidebar*, and display name and person `Farmer`. The x86-64 areas keep their
onboarding ids (`kitchen` = Flower Farm etc.). No worksheet uses area or person ids.

Checked, on both unless stated:

| Check | Result |
|---|---|
| Login | the workshop user, real `/auth/login_flow` round trip |
| `get_config` | Core 2026.9.3, `Farm Workshop`, `Asia/Bangkok`, `TH`, `en`; `zeroconf` and `thread` **not** in `components` |
| Config entries | identical domain set: hassio, sun, analytics, backup, shopping_list, radio_browser, google_translate |
| `ha core check` | passes |
| Repairs | none in HA. Supervisor lists only `no_current_backup`, which the 1.2 images had too |
| mDNS on the wire | 0 packets to or from UDP 5353 leaving the NIC in 120–180 s after startup (AF_PACKET count inside the VM) |
| x86-64 OVA | imported into VirtualBox 7.2.22 on Windows. Boots in ~40 s, banner shows `enp0s3` with only an `fe80::` IPv6 address, `ha os info` shows slot B 18.3 booted and slot A `bad`, login works, `zeroconf` not loaded |
| ARM64 OVA | release download verified against SHA-256, then a plain import on an Apple Silicon Mac in VirtualBox 7.2.22: Bridged to `en0: Wi-Fi`, new MAC, Start needed no changes. Ready in under 80 s, banner `enp0s8` with only an `fe80::` IPv6 address. HAOS 18.3, Core 2026.9.3, Supervisor 2026.10.2. `farmer` logs in through the browser and the API. File editor is in the sidebar. No repairs, no Discovered cards, no build-time tokens. An ESPHome test device added by IP per Activity 3 reported live values, and `zeroconf` stayed unloaded. 0 mDNS packets sent in 2 min idle and in 4 min across a Core restart |

**Shutdown on Apple Silicon:** VirtualBox's *Send the shutdown signal* does nothing on the ARM64
image. The guest got no power-button event, and the VM was still running 2 minutes later. Typing
`host shutdown` at the console's `ha >` prompt shuts it down cleanly in about 13 s, and
`docs/install.md` step 4 now says to do that on Apple Silicon. 1.2 runs the same HAOS 18.3, so it
probably had the same problem; this was not checked.

**Update offer:** Settings shows "1 update: Home Assistant Core 2026.10.2". Supervisor
`auto_update` is off, but nothing stops a participant from tapping it and pulling a large image
over the venue WiFi.

HA core still opens a socket on UDP 5353. `helpers/aiohttp_client.py` creates a zeroconf
instance so it can resolve `.local` names, even when the zeroconf integration is absent. It does
not browse or announce, and the packet count above is 0.

**Hosting:** both files and `SHA256.txt` are assets of the GitHub release
[`vm-1.3`](https://github.com/arnans/iot-training/releases/tag/vm-1.3). Each asset must be under
2 GiB, and release downloads have no bandwidth quota. The repository is public, so the links work
without signing in. Visibility can only be changed by a repository admin; making the repo private
again would break every download link in the guide.

### The built ARM64 image (21 Sep 2026)

`Farm-Workshop-arm64-1.2.ova` — 1,981,466,112 bytes (~1.9 GB), SHA-256
`86a23d9e6c7b52928699ad25426c4e753aad8a0e739d5e77f2fe3f4c371450d0`.
Built from HAOS 18.3 `generic-aarch64`, Core **2026.9.3**, Supervisor 2026.09.2, File editor 6.1.0.

What is inside, each item checked on the exported file after re-importing it:

| Checked | Result |
|---|---|
| Login | the workshop user, verified through a real `/auth/login_flow` round trip |
| Core config | name `Farm Workshop`, `Asia/Bangkok`, country `TH`, °C, UI language English |
| Config file | this directory's `configuration.yaml`, SHA-256 equal to the repo copy |
| `ha core check` | passes |
| Areas | `Flower Farm`, `Corn Farm`, `Grass` — onboarding's default `Living Room`/`Kitchen`/`Bedroom` deleted |
| File editor | installed, `started`, `boot: auto`, **shown in sidebar** |
| Updates | Supervisor `auto_update: false`, add-on `auto_update: false`, no update available |
| Port | 80, confirmed in Settings → System → Network |
| Disk | 4.8 GB used of 30.8 GB |
| Health | zero repair issues, zero persistent notifications, state `RUNNING` |
| **Reachability (step 15)** | **passed on the real image**: after a clean import on the M4 host with Adapter 1 bridged to WiFi, the VM answered on `http://<IP>` from a laptop browser **and from a phone on the same WiFi** |

Two things the "deliberately absent" list below does not actually achieve on HAOS, observed here:

- **`backup` loads anyway.** It is pulled in by the Supervisor integration, so leaving it out of
  YAML does not remove it. Harmless — it makes no outbound connection on its own — but the list
  should not claim otherwise.
- **Sidebar still shows Map, Media and To-do lists.** Those panels come from the frontend, not
  from the integrations the config omits. Nothing behind them is loaded.

**Download:** 1.2 was distributed from a Google Drive folder. The current images are on the
GitHub release `vm-1.3`, described above. The download links appear in **three** files; if they
ever change, update all three and re-render:

```sh
# 1. docs/install.md            - the three laptop rows, plus the "wrong file" troubleshooting row
# 2. docs/resources.md          - the same rows in the file-and-link table
# 3. planning/INSTRUCTOR-RESOURCES.md - the VM table rows
python scripts/render-worksheets.py && python scripts/render-network-doc.py
```

The workshop user/password is **not written down in this repo**: `planning/INSTRUCTOR-RESOURCES.md`
renders to a public GitHub Pages page, so the login stays in the image and on the team card only.

### ARM64 specifics, exactly as built (verified 21 Sep 2026 — M4 host, VirtualBox 7.2.18, HAOS 18.3)

Apple Silicon needs VirtualBox **7.2 or newer** (7.1 added Arm Linux guests; 7.2 is a normal
release, not the old developer preview). The x86-64 OVA cannot be imported there at all — there is
no Intel emulation. The ARM64 disk is a separate release asset:
`haos_generic-aarch64-<ver>.vdi.zip` (the `haos_ova-*` files are x86-64 only).

```sh
VM="Farm Workshop"; V=18.3
curl -LO "https://github.com/home-assistant/operating-system/releases/download/$V/haos_generic-aarch64-$V.vdi.zip"
unzip -q "haos_generic-aarch64-$V.vdi.zip"
VBoxManage createvm --name "$VM" --platform-architecture arm --ostype Oracle_arm64 --register
D="$HOME/VirtualBox VMs/$VM/Farm Workshop-disk001.vdi"
VBoxManage modifyvm "$VM" --memory 2048 --cpus 2 --firmware efi \
  --graphicscontroller vmsvga --vram 16 --rtc-use-utc on --audio-driver none \
  --usb-ohci off --usb-xhci on --mouse usbtablet --keyboard usb \
  --nic1 bridged --bridge-adapter1 en0 --nic-type1 virtio
VBoxManage storagectl "$VM" --name VirtioSCSI --add virtio --controller VirtIO --portcount 1 --bootable on
cp "haos_generic-aarch64-$V.vdi" "$D"
VBoxManage internalcommands sethduuid "$D"          # new UUID, or import clashes with the source disk
VBoxManage modifymedium disk "$D" --resize 32768    # before first boot only
VBoxManage storageattach "$VM" --storagectl VirtioSCSI --port 0 --device 0 --type hdd --medium "$D"
```

Every difference from the x86-64 image is forced by the architecture, not taste:

| x86-64 image | ARM64 image |
|---|---|
| `OSType` `Oracle_64` | `Oracle_arm64` |
| chipset PIIX3/ICH9 | `armv8virtual` |
| SATA (AHCI) disk + IDE DVD | VirtioSCSI disk, no IDE controller |
| E1000 (`82540EM`) NIC | virtio-net |
| `ensoniq1371` sound card | no audio device |
| OHCI + EHCI USB | xHCI |
| guest interface `enp0s3` | guest interface **`enp0s8`** |

Same on both: 2 vCPU, 2048 MB RAM, 16 MB VRAM, VMSVGA, EFI, UTC clock, 32 GiB disk, Adapter 1
bridged, HA on port 80.

What the build confirmed on ARM64, beyond the x86 bench:

- HAOS 18.3 aarch64 pulls Core **2026.9.3**, machine `qemuarm-64`, and serves **port 80** with no
  change — the port-80 step is a check, not an edit.
- `ha core check` passes against this directory's `configuration.yaml`, so the no-`default_config`
  diet has no aarch64-only dependency gap.
- File editor (`core_configurator` 6.1.0) installs and starts; its *Show in sidebar*
  (`ingress_panel`) defaults to **false** and must be turned on by hand.

**Provisioning gotcha, hit once on this build:** bridged-over-WiFi worked for ~4 minutes, then the
host lost the guest entirely (`route get` shows `REJECT`, empty ARP) while the guest kept its lease
and its internet access. It did **not** reproduce: the finished image, imported fresh on the same
host and the same WiFi, was reachable from both a laptop browser and a phone. So treat this as a
transient bridged-adapter/AP hiccup, not as the network blocking the VM's second MAC — but it
costs an hour if it strikes mid-build, so do the build over NAT anyway and switch Adapter 1 back
to Bridged just before export:

```sh
VBoxManage controlvm "$VM" nic1 nat
VBoxManage controlvm "$VM" natpf1 "ha,tcp,127.0.0.1,18080,,80"   # then provision via 127.0.0.1:18080
```

Under NAT the guest reaches the build machine at `10.0.2.2`, so config files can be pulled in with
`curl` from a throwaway `python3 -m http.server` instead of retyped into the console. To drive the
console without a GUI: `VBoxManage controlvm "$VM" keyboardputstring '<cmd>'`, then
`keyboardputscancode 1c 9c` for Enter, then `screenshotpng` to read the result. `login` at the
`ha >` prompt drops to a root shell where `jq` is available.

**`controlvm nic1 nat` and `natpf1` persist to the `.vbox` file.** They are not runtime-only: both
forwards turned up as `<Forwarding .../>` entries in a test export, i.e. they would have shipped to
every participant. Delete them explicitly before the real export:

```sh
VBoxManage modifyvm "$VM" --nic1 bridged --bridge-adapter1 en0
VBoxManage modifyvm "$VM" --natpf1 delete ha
```

**Export/import round trip, verified here on a throwaway export taken before onboarding:**

- `VBoxManage export` wrote a **1.98 GB** OVA in 64 s from the 32 GiB dynamic disk — the dynamic
  format exports at used size, so the 32 GiB cap costs nothing (the x86-64 image ships ~2.6 GB).
- The OVF carries `<Platform architecture="ARM">`, so VirtualBox on an Intel host refuses the file
  outright instead of failing later at boot. The wrong-architecture mistake is self-policing in
  both directions, which is worth saying in the guide.
- `Farm Workshop.nvram` (768 KB of EFI variables) is part of the appliance and the re-imported
  clone reached the HA onboarding endpoint in ~12 s, so the ARM EFI boot entry survives export.
- Plain `VBoxManage import` regenerated the adapter MAC (`…AF597E` → `…69E1B3`). The GUI checkbox
  the guide names is the same behaviour; there is no path where a participant silently keeps the
  build machine's MAC unless they choose "include all MAC addresses".
- The clone's `/config/configuration.yaml` SHA-256 matched this repo's file and File editor was
  still `started`, so `/config` and add-on state both survive the round trip.

This also closes the two install-guide risks already in planning/WORKSHEET-TODO: the bridged-vs-NAT
adapter choice (baked in) and port 80 reachability from phones (the VM's firewall is ours).

### What the participant guide assumes about the image

The participant guide is [docs/install.md](../docs/install.md). It is written against these
facts; change one here and the guide (and session 1's ก่อนเริ่ม) must change with it:

- **VM name `Farm Workshop`** — the guide and session 1 tell participants to press Start on it.
- **File names** as actually distributed: `Farm-Workshop-win-1.3.ova` (Windows + Intel Mac —
  the `win` in the name is historical, Intel Macs use it too) and `Farm-Workshop-arm64-1.3.ova`
  (Apple Silicon). Both guide tables (`docs/install.md`, `docs/resources.md`) and the instructor
  handbook name and link them; the workshop user/password is the only placeholder left.
- **Adapter 1 is Bridged.** The host NIC name inside the OVA is the build machine's, so
  every participant re-picks their WiFi card after import (guide step 2.3). Otherwise Start
  fails with "physical network interfaces were not found".
- **MAC addresses regenerate by default.** Verified on the ARM64 build: a plain
  `VBoxManage import` gave the clone a fresh MAC. The import default only preserves NAT-adapter
  MACs, so a participant accepting the defaults cannot end up with the build machine's MAC — the
  34-identical-MACs failure needs someone to actively choose "include all MAC addresses". The
  guide is therefore right to say "leave the import settings alone"; do not add a MAC step to it.
- **Port 80, IP read from the console.** The guide says to read the `IPv4 addresses` line and
  ignore `homeassistant.local`. Before sending the guide, replace the placeholder screenshots
  with real ones from the final build. The ARM64 banner differs: the interface is **`enp0s8`**,
  not `enp0s3`, so a screenshot from the x86-64 image does not match what an Apple Silicon
  participant sees on the same line.

## What the team config removes, honestly

- **`ssdp`** — periodic UPnP M-SEARCH multicast to 239.255.255.250. Pure noise here. Removed.
- **`dhcp`** — passive sniffing; no traffic of its own, but nothing to find. Removed.
- **bluetooth, usb, cloud, stream, media, assist, energy, backup, my, alerts** — unused, and
  several attempt outbound internet at startup on a network that has none. Removed.

- **`zeroconf`** — removed once the boards dropped mDNS (`mdns: disabled: true`, added in HA by
  IP; see `firmware/README.md`). It browsed every service type in HA's generated discovery list
  and announced `_home-assistant._tcp`, ×100 instances, and each ESPHome browse made every board
  in the zone answer. ESPHome lists it only as an after_dependency, so it no longer loads.
  Verified on the 1.3 images: it is absent from `get_config` `components`. A config entry whose
  integration *depends* on zeroconf still pulls it in, though (`thread`, `homekit_controller`,
  `apple_tv`, …), so check again after an HA upgrade or after accepting a discovered integration.

What it does **not** remove: HA OS itself still answers for `homeassistant.local` (systemd-resolved
and the multicast plugin), outside `configuration.yaml`. Small, but not zero. The 1.3 images also
have **Settings → System → Network** set to the one adapter with IPv6 off, so nothing goes out twice.

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
