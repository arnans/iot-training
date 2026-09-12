#!/usr/bin/env python
"""Build (and optionally flash) the workshop firmware for every zone.

One YAML per board type, compiled once per zone with the zone name and WiFi
credentials injected as ESPHome substitutions. Binaries land in dist/.

    python build-zones.py                     # all zones, both boards
    python build-zones.py --zone red          # one zone
    python build-zones.py --board relay       # one board type
    python build-zones.py --flash red sensor COM7   # flash one built binary

Requires zones.yaml (copy zones.example.yaml) and secrets.yaml.
"""
import argparse
import shutil
import subprocess
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).parent
BOARDS = {
    # key: (yaml file, device base name, esptool chip)
    "sensor": ("gogo-iot-workshop.yaml", "gogo-iot", "esp32c3"),
    "relay": ("relay-workshop.yaml", "gogo-relay", "esp32c6"),
}
ZONES = ("red", "green", "blue")


def load_zones():
    p = HERE / "zones.yaml"
    if not p.exists():
        sys.exit("zones.yaml not found - copy zones.example.yaml and fill it in")
    zones = yaml.safe_load(p.read_text(encoding="utf-8"))
    for name, cfg in zones.items():
        if cfg.get("password", "CHANGE_ME") == "CHANGE_ME":
            sys.exit(f"zones.yaml: zone {name!r} still has the placeholder password")
    return zones


def build(board, zone, cfg):
    yaml_file, base, _ = BOARDS[board]
    cmd = [
        "esphome",
        "-s", "zone", zone,
        "-s", "wifi_ssid", cfg["ssid"],
        "-s", "wifi_password", cfg["password"],
        "compile", yaml_file,
    ]
    print(f"\n=== {board} / {zone}  ({cfg['ssid']}) ===")
    subprocess.run(cmd, cwd=HERE, check=True)

    name = f"{base}-{zone}"
    # ESPHome 2026.x drives ESP-IDF/CMake directly and writes to build/;
    # older PlatformIO-based versions wrote to .pioenvs/<name>/. Accept both.
    build_dir = HERE / ".esphome" / "build" / name
    candidates = [
        build_dir / "build" / "firmware.factory.bin",
        build_dir / ".pioenvs" / name / "firmware.factory.bin",
    ]
    src = next((p for p in candidates if p.exists()), None)
    if src is None:
        sys.exit("expected binary not found, looked in:\n  "
                 + "\n  ".join(str(p) for p in candidates))
    dist = HERE / "dist"
    dist.mkdir(exist_ok=True)
    dst = dist / f"{name}.factory.bin"
    shutil.copy2(src, dst)
    print(f"-> {dst}  ({dst.stat().st_size // 1024} KB)")
    return dst


def flash(board, zone, port):
    _, base, chip = BOARDS[board]
    binary = HERE / "dist" / f"{base}-{zone}.factory.bin"
    if not binary.exists():
        sys.exit(f"{binary} not built yet - run without --flash first")
    cmd = ["esptool", "--chip", chip, "--port", port, "--baud", "460800",
           "write_flash", "0x0", str(binary)]
    print(" ".join(cmd))
    subprocess.run(cmd, check=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--zone", choices=ZONES)
    ap.add_argument("--board", choices=list(BOARDS))
    ap.add_argument("--flash", nargs=3, metavar=("ZONE", "BOARD", "PORT"))
    args = ap.parse_args()

    if args.flash:
        zone, board, port = args.flash
        flash(board, zone, port)
        sys.exit(0)

    zones = load_zones()
    for board in ([args.board] if args.board else BOARDS):
        for zone, cfg in zones.items():
            if args.zone and zone != args.zone:
                continue
            build(board, zone, cfg)
    print("\nAll builds in", HERE / "dist")
