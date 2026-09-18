"""SVG figures for Activity 7.4: the charge controller, the battery and the loads.

Two figures, both built around a photo of the workshop's own charge controller (cropped
from docs/images/session2-relay-led-wiring.jpg at build time and embedded as a JPEG data
URI, so each SVG opens on its own and in an <img>):

  power-controller-wiring   panel and battery into the controller, a 12 V LED lamp on its
                            load terminals
  power-inverter            the battery between the controller and an inverter (through a
                            fuse), the inverter driving a 220 V AC pump

    python scripts/power_figures.py        # writes docs/images/power-*.svg

Plain SVG, no external dependencies beyond Pillow for the crop. Layout is in one place;
the labels are Thai because the figures appear only on the participant worksheet.
"""

from __future__ import annotations

import base64
import io
import pathlib

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
PHOTO = ROOT / "docs" / "images" / "session2-relay-led-wiring.jpg"
OUT = ROOT / "docs" / "images"

SANS = ("Sarabun, 'Leelawadee UI', 'Noto Sans Thai', -apple-system, "
        "'Segoe UI', system-ui, sans-serif")
INK = "#14181d"
SOFT = "#5b6570"
RULE = "#d9dee4"
RED = "#c0392b"
BLACK = "#14181d"
AC = "#7d3c98"
PANEL = "#1f4e79"
PANEL_CELL = "#2e75b6"
YELLOW = "#f4d03f"

# The crop, in photo pixels, and where the six screw terminals sit inside it.
CROP = (215, 255, 800, 548)
TERMINALS_X = [186, 226, 266, 306, 346, 385]   # PV+ PV- BAT+ BAT- LOAD+ LOAD-
TERMINALS_Y = 258


def controller_data_uri() -> tuple[str, int, int]:
    im = Image.open(PHOTO).crop(CROP)
    buf = io.BytesIO()
    im.save(buf, format="JPEG", quality=82, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode("ascii"), im.width, im.height


def text(x, y, s, size=16, weight=400, fill=INK, anchor="middle"):
    return (f'<text x="{x}" y="{y}" font-family="{SANS}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" text-anchor="{anchor}">{s}</text>')


def wire(points, color):
    pts = " ".join(f"{x},{y}" for x, y in points)
    return f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="4" stroke-linejoin="round" stroke-linecap="round"/>'


def controller(uri, w0, h0, x, y, width):
    """Place the photo; return (svg, terminal x list, terminal y) in figure coordinates."""
    k = width / w0
    svg = (f'<image href="{uri}" x="{x}" y="{y}" width="{width}" height="{h0 * k:.0f}"/>'
           f'<rect x="{x}" y="{y}" width="{width}" height="{h0 * k:.0f}" fill="none" stroke="{RULE}"/>')
    return svg, [x + tx * k for tx in TERMINALS_X], y + TERMINALS_Y * k


def solar_panel(cx, cy, label):
    w, h = 150, 100
    x, y = cx - w / 2, cy - h / 2
    cells = "".join(
        f'<rect x="{x + 8 + i * 34}" y="{y + 8 + j * 30}" width="30" height="26" fill="{PANEL_CELL}"/>'
        for i in range(4) for j in range(3))
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{PANEL}"/>{cells}'
            + text(cx, y + h + 26, label, 16, 600))


def battery(cx, cy, label):
    w, h = 150, 90
    x, y = cx - w / 2, cy - h / 2
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="#f5f7f9" stroke="{INK}" stroke-width="3"/>'
            f'<rect x="{x + 24}" y="{y - 10}" width="22" height="10" fill="{INK}"/>'
            f'<rect x="{x + w - 46}" y="{y - 10}" width="22" height="10" fill="{INK}"/>'
            + text(x + 35, y + 32, "+", 26, 700, RED) + text(x + w - 35, y + 32, "−", 26, 700, BLACK)
            + text(cx, cy + 18, "12 V", 20, 600, SOFT)
            + text(cx, y + h + 26, label, 16, 600))


def led_lamp(cx, cy, label):
    w, h = 170, 44
    x, y = cx - w / 2, cy - h / 2
    dots = "".join(f'<circle cx="{x + 40 + i * 45}" cy="{cy}" r="13" fill="{YELLOW}" stroke="#b7950b" stroke-width="2"/>'
                   for i in range(3))
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="#ffffff" stroke="{INK}" stroke-width="3"/>{dots}'
            + text(cx, y + h + 26, label, 16, 600))


def inverter(x, y, w, h):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="#f5f7f9" stroke="{INK}" stroke-width="3"/>'
            + text(x + w / 2, y + 36, "อินเวอร์เตอร์", 20, 700)
            + text(x + w / 2, y + 66, "12 V DC → 220 V AC", 17, 600, SOFT)
            + text(x + 14, y + h - 14, "DC เข้า", 14, 600, SOFT, "start")
            + text(x + w - 14, y + h - 14, "AC ออก", 14, 600, SOFT, "end"))


def pump(cx, cy, label):
    r = 44
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#eef4fa" stroke="{INK}" stroke-width="3"/>'
            f'<circle cx="{cx}" cy="{cy}" r="10" fill="{INK}"/>'
            + "".join(f'<path d="M{cx},{cy} m-4,0 a4,4 0 0 1 8,0 l14,-20 a30,30 0 0 0 -22,-6 z" fill="{INK}" '
                      f'transform="rotate({a} {cx} {cy})"/>' for a in (0, 90, 180, 270))
            + f'<rect x="{cx + r - 4}" y="{cy - 8}" width="26" height="16" fill="{INK}"/>'
            + text(cx, cy + r + 30, label, 16, 600))


def figure(width, height, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" '
            f'font-family="{SANS}"><rect width="{width}" height="{height}" fill="#ffffff"/>{body}</svg>\n')


def wiring_figure(uri, w0, h0) -> str:
    parts = []
    parts.append(text(480, 32, "แผงชาร์จแบตเตอรี่ผ่าน charge controller แล้ว controller จ่ายไฟให้โหลด", 20, 700))
    ctrl, tx, ty = controller(uri, w0, h0, 240, 52, 480)
    parts.append(ctrl)
    ybus = ty + 60
    # solar panel, left
    px, py = 130, 430
    parts.append(solar_panel(px, py, "แผงโซลาร์เซลล์ 12 V"))
    parts.append(wire([(tx[0], ty + 6), (tx[0], ybus), (px - 30, ybus), (px - 30, py - 50)], RED))
    parts.append(wire([(tx[1], ty + 6), (tx[1], ybus + 14), (px + 30, ybus + 14), (px + 30, py - 50)], BLACK))
    # battery, centre
    bx, by = 480, 440
    parts.append(battery(bx, by, "แบตเตอรี่ (ในชุดอบรมใช้อะแดปเตอร์ 12 V แทน)"))
    parts.append(wire([(tx[2], ty + 6), (tx[2], ybus + 28), (bx - 40, ybus + 28), (bx - 40, by - 55)], RED))
    parts.append(wire([(tx[3], ty + 6), (tx[3], ybus + 42), (bx + 40, ybus + 42), (bx + 40, by - 55)], BLACK))
    # LED lamp, right
    lx, ly = 830, 430
    parts.append(led_lamp(lx, ly, "โหลด DC 12 V (หลอด LED)"))
    parts.append(wire([(tx[4], ty + 6), (tx[4], ybus + 14), (lx - 30, ybus + 14), (lx - 30, ly - 22)], RED))
    parts.append(wire([(tx[5], ty + 6), (tx[5], ybus), (lx + 30, ybus), (lx + 30, ly - 22)], BLACK))
    parts.append(text(480, 528, "สีแดง = ขั้วบวก · สีดำ = ขั้วลบ · ต่อแบตเตอรี่ก่อน แล้วจึงต่อแผง ตามลำดับในคู่มือของรุ่นนั้น", 14, 400, SOFT))
    return figure(960, 545, "".join(parts))


def battery_side(cx, cy, label):
    """Battery drawn with its terminals on the sides, so the charger can feed the left and the inverter the right."""
    w, h = 150, 90
    x, y = cx - w / 2, cy - h / 2
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="#f5f7f9" stroke="{INK}" stroke-width="3"/>'
            f'<rect x="{x - 12}" y="{cy - 11}" width="12" height="22" fill="{INK}"/>'
            f'<rect x="{x + w}" y="{cy - 11}" width="12" height="22" fill="{INK}"/>'
            + text(x + 22, cy + 9, "+", 26, 700, RED) + text(x + w - 22, cy + 9, "−", 26, 700, BLACK)
            + text(cx, cy + 8, "12 V", 20, 600, SOFT)
            + text(cx, y + h + 26, label, 16, 600))


def fuse(x, y, label):
    """A small fuse on a horizontal wire centred at (x, y)."""
    return (f'<rect x="{x - 22}" y="{y - 9}" width="44" height="18" rx="9" fill="#ffffff" stroke="{INK}" stroke-width="2.5"/>'
            f'<line x1="{x - 12}" y1="{y}" x2="{x + 12}" y2="{y}" stroke="{INK}" stroke-width="2.5"/>'
            + text(x, y - 16, label, 13, 600, SOFT))


def inverter_figure(uri, w0, h0) -> str:
    parts = []
    parts.append(text(480, 32, "อุปกรณ์ที่ใช้ไฟบ้าน 220 V AC ต้องมีอินเวอร์เตอร์ ต่อจากแบตเตอรี่โดยตรง", 20, 700))
    ctrl, tx, ty = controller(uri, w0, h0, 40, 50, 300)
    parts.append(ctrl)
    # battery, terminals on its sides: controller on the left terminal pair, inverter on the same terminals
    bx, by = 520, 250
    parts.append(battery_side(bx, by, "แบตเตอรี่ 12 V"))
    left, right = bx - 75 - 12, bx + 75 + 12
    parts.append(wire([(tx[2], ty + 6), (tx[2], by), (left, by)], RED))
    parts.append(wire([(tx[3], ty + 6), (tx[3], by + 95), (right + 33, by + 95), (right + 33, by), (right, by)], BLACK))
    parts.append(text(40, by + 124, "ช่องแบตเตอรี่ของ controller", 15, 600, SOFT, "start"))
    # inverter to the right, fed from the same two terminals; fuse on the positive lead
    ix, iy, iw, ih = 690, 176, 190, 130
    parts.append(inverter(ix, iy, iw, ih))
    parts.append(wire([(left - 6, by), (left - 6, 170), (ix - 30, 170), (ix - 30, iy + 50), (ix, iy + 50)], RED))
    parts.append(fuse(560, 170, "ฟิวส์"))
    parts.append(wire([(right + 33, by), (ix, by)], BLACK))
    # 220 V pump below the inverter
    px, py = 785, 420
    parts.append(pump(px, py, "ปั๊ม 220 V AC"))
    parts.append(wire([(ix + 60, iy + ih), (ix + 60, py - 20), (px - 34, py - 20)], AC))
    parts.append(wire([(ix + 130, iy + ih), (ix + 130, py - 46), (px + 6, py - 46), (px + 6, py - 44)], AC))
    parts.append(text(ix + 46, py - 26, "220 V AC", 15, 600, AC, "end"))
    parts.append(text(480, 508, "แผงต่อกับ controller เหมือนแผนภาพแรก · อินเวอร์เตอร์ไม่ต่อผ่านช่องโหลดของ controller เพราะจ่ายกระแสได้จำกัด", 14, 400, SOFT))
    return figure(960, 525, "".join(parts))


def main() -> None:
    uri, w0, h0 = controller_data_uri()
    for name, fn in (("power-controller-wiring", wiring_figure), ("power-inverter", inverter_figure)):
        path = OUT / f"{name}.svg"
        path.write_text(fn(uri, w0, h0), encoding="utf-8", newline="\n")
        print(f"wrote {path.relative_to(ROOT)}  ({path.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
