#!/usr/bin/env python
"""Build (and optionally flash) the workshop firmware for every zone.

One YAML per board type, compiled once per zone with the zone name and WiFi
credentials injected as ESPHome substitutions. Binaries land in dist/ and are
published to docs/firmware/ in the same step; commit and push to make them live.

    python build-zones.py                     # all zones, all four images
    python build-zones.py --zone red          # one zone
    python build-zones.py --board relay       # one image type
    python build-zones.py --board receiver --receiver-console uart0
                                              # session-4 receiver for a C3 devkit
                                              # with a USB-UART chip (default: native USB)
    python build-zones.py --flash red sensor COM7   # flash one built binary

Requires zones.yaml (copy zones.example.yaml) and secrets.yaml. Run it with the
python that has esphome installed, e.g. ~/esphome-venv/bin/python build-zones.py;
the venv need not be activated.
"""
import argparse
import shutil
import subprocess
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).parent
# Served by GitHub Pages; every worksheet and the instructor sheet link here.
PUBLISHED = HERE.parent / "docs" / "firmware"
BOARDS = {
    # key: (yaml file, device base name, esptool chip, published file base)
    # The published base is normally the device base. The session-4 sensor image is
    # the exception: same board, same hostname (so Home Assistant needs no re-adoption
    # after the team flashes it in Activity 9), different file so the pre-flashed
    # sessions 1-3 image keeps its name and links.
    "sensor": ("gogo-iot-workshop.yaml", "gogo-iot", "esp32c3", "gogo-iot"),
    "sensor-espnow": ("gogo-iot-espnow-workshop.yaml", "gogo-iot", "esp32c3", "gogo-iot-espnow"),
    "relay": ("relay-workshop.yaml", "gogo-relay", "esp32c6", "gogo-relay"),
    # session 4: the plain ESP32-C3 in the farmhouse that hears the sensor node over ESP-NOW
    "receiver": ("farm-receiver-workshop.yaml", "farm-receiver", "esp32c3", "farm-receiver"),
}
ZONES = ("red", "green", "blue")
# Where the receiver's log goes; the kit decides once, at purchase (see the YAML header).
RECEIVER_CONSOLES = {"usb": "USB_SERIAL_JTAG", "uart0": "UART0"}


def load_zones():
    p = HERE / "zones.yaml"
    if not p.exists():
        sys.exit("zones.yaml not found - copy zones.example.yaml and fill it in")
    zones = yaml.safe_load(p.read_text(encoding="utf-8"))
    for name, cfg in zones.items():
        if cfg.get("password", "CHANGE_ME") == "CHANGE_ME":
            sys.exit(f"zones.yaml: zone {name!r} still has the placeholder password")
    return zones


def build(board, zone, cfg, extra_subs=()):
    yaml_file, base, _, published = BOARDS[board]
    # Run ESPHome through the interpreter running this script, so a venv works without
    # being activated (a bare `esphome` is only found when the venv is on PATH).
    cmd = [
        sys.executable, "-m", "esphome",
        "-s", "zone", zone,
        "-s", "wifi_ssid", cfg["ssid"],
        "-s", "wifi_password", cfg["password"],
    ]
    for key, value in extra_subs:
        cmd += ["-s", key, value]
    cmd += ["compile", yaml_file]
    print(f"\n=== {board} / {zone}  ({cfg['ssid']}) ===")
    subprocess.run(cmd, cwd=HERE, check=True)

    # ESPHome's build dir is named after the device, so `sensor` and `sensor-espnow`
    # share one; harmless because each binary is copied out right after its compile.
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
    out = f"{published}-{zone}"
    dst = dist / f"{out}.factory.bin"
    shutil.copy2(src, dst)
    print(f"-> {dst}  ({dst.stat().st_size // 1024} KB)")

    # Publish in the same step. docs/firmware/ is what GitHub Pages serves and
    # what every worksheet links to; when this copy was manual it silently went
    # three days stale, so teams flashed firmware that did not match the YAML.
    PUBLISHED.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, PUBLISHED / f"{out}.factory.bin")
    print(f"-> {PUBLISHED / f'{out}.factory.bin'}  (published)")
    return dst


def flash(board, zone, port):
    _, _, chip, published = BOARDS[board]
    binary = HERE / "dist" / f"{published}-{zone}.factory.bin"
    if not binary.exists():
        sys.exit(f"{binary} not built yet - run without --flash first")
    cmd = [sys.executable, "-m", "esptool", "--chip", chip, "--port", port, "--baud", "460800",
           "write_flash", "0x0", str(binary)]
    print(" ".join(cmd))
    subprocess.run(cmd, check=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--zone", choices=ZONES)
    ap.add_argument("--board", choices=list(BOARDS))
    ap.add_argument("--flash", nargs=3, metavar=("ZONE", "BOARD", "PORT"))
    ap.add_argument("--receiver-console", choices=list(RECEIVER_CONSOLES), default="usb",
                    help="receiver board's USB: native (usb, default) or a USB-UART chip (uart0)")
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
            subs = [("console", RECEIVER_CONSOLES[args.receiver_console])] if board == "receiver" else []
            build(board, zone, cfg, subs)
    print("\nAll builds in", HERE / "dist")
