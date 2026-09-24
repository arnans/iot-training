"""Labelled relay-board diagram for Activity 2.1.

Draws black sans-serif callouts with thin red leaders over the vendor render of the
ESP32-C6-RELAY-X1 v1.1 board (user-import/relay-board-x1-v1-1.png), in the same style as
the earlier hand-labelled diagram of the v1.0 board it replaces. The v1.1 board has two
push buttons (RST and BOOT); the workshop firmware uses BOOT as the manual relay toggle,
so it is labelled "Manual ON/OFF" and RST is labelled "Reset". The GPIO2 LED is the WiFi
status light in our firmware, so it is labelled "WiFi Status".

    python scripts/relay_board_figure.py        # writes docs/images/relay-board-terminals.png

Needs Pillow only. All positions are in source-image pixels (529 x 495) and are scaled
by SCALE at draw time, so the layout survives a change of output size.
"""

from __future__ import annotations

import pathlib

from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "user-import" / "relay-board-x1-v1-1.png"
OUT = ROOT / "docs" / "images" / "relay-board-terminals.png"

SCALE = 2.0                      # board render is upscaled this much
MARGIN = dict(left=330, right=430, top=140, bottom=150)
FONT = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 40)
BLACK = (20, 24, 29)
RED = (220, 30, 30)
LINE = 3                         # leader width
GAP = 14                         # space between leader end and label text

board = Image.open(SRC).convert("RGB")
bw, bh = int(board.width * SCALE), int(board.height * SCALE)
board = board.resize((bw, bh), Image.LANCZOS)

W = MARGIN["left"] + bw + MARGIN["right"]
H = MARGIN["top"] + bh + MARGIN["bottom"]
canvas = Image.new("RGB", (W, H), "white")
canvas.paste(board, (MARGIN["left"], MARGIN["top"]))
d = ImageDraw.Draw(canvas)


def P(x: float, y: float) -> tuple[float, float]:
    """Source-image pixel -> canvas pixel."""
    return MARGIN["left"] + x * SCALE, MARGIN["top"] + y * SCALE


def dashed_rect(box: tuple[float, float, float, float], dash: int = 8) -> None:
    (x0, y0), (x1, y1) = P(box[0], box[1]), P(box[2], box[3])
    pts = [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)]
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        length = abs(bx - ax) + abs(by - ay)
        n = max(1, int(length // dash))
        for i in range(0, n, 2):
            t0, t1 = i / n, min((i + 1) / n, 1)
            d.line([(ax + (bx - ax) * t0, ay + (by - ay) * t0),
                    (ax + (bx - ax) * t1, ay + (by - ay) * t1)], fill=RED, width=LINE)


def text_size(s: str) -> tuple[int, int]:
    l, t, r, b = d.textbbox((0, 0), s, font=FONT)
    return r - l, b - t


def label_left(s: str, tip: tuple[float, float], x_end: float) -> None:
    """Horizontal leader from the target (source px) leftwards to canvas x_end, label to its left."""
    tx, ty = P(*tip)
    d.line([(tx, ty), (x_end, ty)], fill=RED, width=LINE)
    w, h = text_size(s)
    d.text((x_end - GAP - w, ty - h * 0.72), s, font=FONT, fill=BLACK)


def label_right(s: str, tip: tuple[float, float], x_end: float) -> None:
    tx, ty = P(*tip)
    d.line([(tx, ty), (x_end, ty)], fill=RED, width=LINE)
    _, h = text_size(s)
    d.text((x_end + GAP, ty - h * 0.72), s, font=FONT, fill=BLACK)


def label_top(s: str, tip: tuple[float, float], y_end: float, text_cx: float | None = None) -> None:
    """Vertical leader up from the target to canvas y_end, label centred above (or at text_cx)."""
    tx, ty = P(*tip)
    d.line([(tx, ty), (tx, y_end)], fill=RED, width=LINE)
    w, h = text_size(s)
    cx = tx if text_cx is None else text_cx
    d.text((cx - w / 2, y_end - GAP - h - 8), s, font=FONT, fill=BLACK)


def label_bottom(s: str, tip: tuple[float, float], y_end: float) -> None:
    tx, ty = P(*tip)
    d.line([(tx, ty), (tx, y_end)], fill=RED, width=LINE)
    w, _ = text_size(s)
    d.text((tx - w / 2, y_end + GAP - 6), s, font=FONT, fill=BLACK)


# --- callouts (targets in source pixels) -------------------------------------------

# Top row. The ESP32 module is deliberately unlabelled: participants never touch it, and
# a third label here ran into the other two.
dashed_rect((280, 37, 301, 54))                       # D1, the GPIO2 LED
label_top("WiFi Status", (290, 37), 70, text_cx=P(262, 0)[0])
label_top("Reset", (378, 26), 70, text_cx=P(392, 0)[0])   # RST push button

# BOOT push button: L-shaped leader out to the right margin, above the mounting hole
bx, by = P(425, 26)
turn_y = P(0, 3)[1]
right_x = P(529, 0)[0] + 40
d.line([(bx, by), (bx, turn_y), (right_x, turn_y)], fill=RED, width=LINE)
_, h = text_size("Manual ON/OFF")
d.text((right_x + GAP, turn_y - h * 0.72), "Manual ON/OFF", font=FONT, fill=BLACK)

# Right side
label_right("USB Type-C", (500, 160), right_x)
label_right("7-60 Input", (480, 345), right_x)
label_right("GND", (480, 400), right_x)

# Left side (relay terminals, top to bottom as on the v1.0 diagram and the wiring photo)
left_x = MARGIN["left"] - 30
label_left("NO", (40, 350), left_x)
label_left("COM", (40, 400), left_x)
label_left("NC", (40, 447), left_x)

# Bottom
dashed_rect((299, 407, 320, 442))                     # D2, hard-wired relay indicator
label_bottom("Relay Indicator", (309, 442), P(0, 495)[1] + 40)

# 256-colour palette, as with gogo-iot-main-parts.png: the worksheet is served with this
# image inline, so the file size matters more than the last bit of photo fidelity.
canvas.quantize(colors=256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.FLOYDSTEINBERG).save(OUT, optimize=True)
print(OUT, canvas.size, OUT.stat().st_size // 1024, "KB")
