# Home Assistant configurations

Two `configuration.yaml` files, one per role. Neither is something a participant edits.

| File | Runs on | Purpose |
|---|---|---|
| `configuration.yaml` | each team's laptop VM | Minimal install: no `default_config`, no ssdp/dhcp/bluetooth/usb/cloud |
| `configuration-instructor.yaml` | instructor server | Same diet plus **recorder limits** for 100 adopted boards |

## Ship a VM image, not an install guide

The team config only has value if it is actually on 100 laptops. Asking 100 teams to install
Home Assistant and then hand-edit YAML will not produce that. The reliable path is a
**pre-built VirtualBox appliance (OVA)** with this configuration inside, a bridged adapter
preconfigured, and onboarding already done to a known user. The install guide then reduces to
"install VirtualBox, import this file, press Start" — which is also far more likely to survive
contact with 100 heterogeneous laptops than a from-scratch install.

This also closes the two install-guide risks already in WORKSHEET-TODO: the bridged-vs-NAT
adapter choice (baked in) and port 8123 reachability from phones (the VM's firewall is ours).

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

100 sensor boards × (illuminance at 1 s + vibration at 1 s + three sensors at 5 s) is roughly
250 state writes per second, on the order of 10 million rows overnight. SQLite will not cope.
`configuration-instructor.yaml` excludes vibration and diagnostics entirely and leaves one
decision open: **illuminance from all boards, or from a sample of ten.** The lights-off trace is
session 2's hook, and one board's trace tells that story as well as a hundred. Sample is
recommended; the ten board names get filled in during kit prep.

## Not verified yet

- That Home Assistant boots cleanly with this exact component list on the current release.
  `default_config` occasionally acquires a new dependency that some UI panel quietly assumes.
  Build the image, click through Settings and the automation editor, and fix whatever complains.
- The recorder `exclude`/`include` globs assume the entity-id shape produced by the Thai+ASCII
  entity names in `firmware/`. Confirm one board's actual entity_ids before relying on them.
