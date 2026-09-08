"""SVG figures for the network requirements spec.

Layout is defined once; only the labels differ per language, so the Thai and
English editions cannot drift apart visually. Written as plain SVG with no
external dependencies, so the pages stay self-contained and print cleanly.

Two figures:

  zones      Three zone circles, each holding the pair of SSIDs that share its
             VLAN. Shows both design guidelines at once: the pair sees itself,
             the zones do not see each other.
  multicast  What must pass within a zone and what must not cross between
             zones, with the settings that silently break each.
"""

from __future__ import annotations

SANS = ("Sarabun, 'Leelawadee UI', 'Noto Sans Thai', -apple-system, "
        "'Segoe UI', system-ui, sans-serif")
MONO = "'IBM Plex Mono', ui-monospace, Consolas, monospace"

INK = "#14181d"
SOFT = "#5b6570"
RULE = "#d9dee4"
GOOD = "#0f6b63"
STOP = "#b03a2e"

ZONES = [
    # cx, accent, tint, vlan, ssid 2.4, ssid 5
    (160, "#c0392b", "#fdf1ef", "10", "farm-iot-red",   "farm-laptop-red"),
    (480, "#1e8449", "#eef8f1", "20", "farm-iot-green", "farm-laptop-green"),
    (800, "#21618c", "#eef4fa", "30", "farm-iot-blue",  "farm-laptop-blue"),
]

LABELS = {
    "th": {
        "zone_names": ["โซนแดง", "โซนเขียว", "โซนน้ำเงิน"],
        "vlan": "VLAN",
        "band24": "2.4 GHz",
        "band5": "5 GHz",
        "in24a": "บอร์ด",
        "in24b": "~67 ตัว",
        "in5a": "แล็ปท็อป",
        "in5b": "โทรศัพท์",
        "sees": "ติดต่อกันได้ · mDNS",
        "blocked": "ติดต่อกันไม่ได้",
        "zone_caption": "ทุก AP กระจาย SSID ทั้งหกชื่อ · รหัสผ่าน iotfarmer เหมือนกันทุกชื่อ · "
                        "การแบ่งโซนกำหนดจากเครือข่าย ไม่ได้แบ่งตามที่นั่ง",
        # multicast figure
        "pass_title": "ภายในโซนเดียวกัน · ต้องผ่าน",
        "stop_title": "ระหว่างโซน · ต้องไม่ผ่าน",
        "same_vlan": "VLAN และ subnet เดียวกัน",
        "boards": "บอร์ด",
        "laptops": "แล็ปท็อป · โทรศัพท์",
        "mdns": "mDNS",
        "addr": "224.0.0.251 · UDP 5353",
        "no_traffic": "ไม่มี unicast · broadcast · multicast",
        "drop_head": "ตรวจว่าแพ็กเก็ตไม่ถูกกรองโดย",
        "drops": [
            "การกรองหรือระงับ broadcast และ multicast",
            "multicast-to-unicast ที่จัดการ mDNS ไม่ถูกต้อง",
            "IGMP snooping ที่ไม่มี querier บน segment",
            "proxy ARP / ARP suppression",
        ],
        "off_head": "ต้องปิด",
        "offs": [
            "mDNS reflector / Bonjour gateway / AirGroup",
            "mDNS repeater ระหว่าง VLAN",
            "การ route ระหว่าง subnet ของสามโซน",
        ],
        "zone_a": "โซนแดง",
        "zone_b": "โซนเขียว",
    },
    "en": {
        "zone_names": ["Red zone", "Green zone", "Blue zone"],
        "vlan": "VLAN",
        "band24": "2.4 GHz",
        "band5": "5 GHz",
        "in24a": "boards",
        "in24b": "~67",
        "in5a": "laptops",
        "in5b": "phones",
        "sees": "see each other · mDNS",
        "blocked": "no visibility",
        "zone_caption": "Every AP broadcasts all six SSIDs · one password, iotfarmer, on all of "
                        "them · zones are logical, not spatial",
        "pass_title": "Within one zone · must pass",
        "stop_title": "Between zones · must not pass",
        "same_vlan": "same VLAN and subnet",
        "boards": "boards",
        "laptops": "laptops · phones",
        "mdns": "mDNS",
        "addr": "224.0.0.251 · UDP 5353",
        "no_traffic": "no unicast · broadcast · multicast",
        "drop_head": "Must not be dropped by",
        "drops": [
            "broadcast / multicast filtering or suppression",
            "multicast-to-unicast that mishandles mDNS",
            "IGMP snooping with no querier on the segment",
            "proxy ARP / ARP suppression",
        ],
        "off_head": "Must be off",
        "offs": [
            "mDNS reflector / Bonjour gateway / AirGroup",
            "mDNS repeater between VLANs",
            "routing between the three zone subnets",
        ],
        "zone_a": "red zone",
        "zone_b": "green zone",
    },
}

_DEFS = f"""  <defs>
    <marker id="arrow-good" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7"
            markerHeight="7" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" fill="{GOOD}"/>
    </marker>
  </defs>"""


def _t(x, y, s, size=12, fill=INK, weight="400", anchor="middle", family=SANS):
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{family}" '
            f'font-size="{size}" font-weight="{weight}" fill="{fill}">{s}</text>')


def zones_svg(lang: str) -> str:
    L = LABELS[lang]
    out = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 430" role="img" '
        f'aria-label="{L["zone_caption"]}">',
        _DEFS,
    ]

    for i, (cx, accent, tint, vlan, ssid24, ssid5) in enumerate(ZONES):
        cy, r = 160, 125
        ax, bx, iy, ir = cx - 58, cx + 58, 155, 52

        out.append(f'  <circle cx="{cx}" cy="{cy}" r="{r}" fill="{tint}" '
                   f'stroke="{accent}" stroke-width="2.5"/>')
        out.append(_t(cx, 24, f'{L["zone_names"][i]} · {L["vlan"]} {vlan}', 15, accent, "700"))

        for ix, band, l1, l2 in ((ax, L["band24"], L["in24a"], L["in24b"]),
                                 (bx, L["band5"], L["in5a"], L["in5b"])):
            out.append(f'  <circle cx="{ix}" cy="{iy}" r="{ir}" fill="#ffffff" '
                       f'stroke="{accent}" stroke-width="1.5" stroke-opacity=".55"/>')
            out.append(_t(ix, iy - 9, band, 13.5, INK, "700"))
            out.append(_t(ix, iy + 9, l1, 11, SOFT))
            out.append(_t(ix, iy + 25, l2, 11, SOFT))

        # the pair sees itself
        out.append(f'  <path d="M{ax},{iy + 50} Q{cx},{cy + 88} {bx},{iy + 50}" fill="none" '
                   f'stroke="{GOOD}" stroke-width="1.8" marker-start="url(#arrow-good)" '
                   'marker-end="url(#arrow-good)"/>')
        out.append(_t(cx, 254, L["sees"], 11.5, GOOD, "600"))

        # SSID names below the zone
        for j, (band, ssid) in enumerate(((L["band24"], ssid24), (L["band5"], ssid5))):
            y = 322 + j * 26
            out.append(
                f'  <text x="{cx}" y="{y}" text-anchor="middle" font-family="{SANS}" '
                f'font-size="11" fill="{SOFT}">{band}&#160;&#160;'
                f'<tspan font-family="{MONO}" font-size="12.5" font-weight="600" '
                f'fill="{INK}">{ssid}</tspan></text>')

    # zones do not see each other
    for bx in (320, 640):
        out.append(f'  <line x1="{bx - 34}" y1="160" x2="{bx + 34}" y2="160" '
                   f'stroke="{STOP}" stroke-width="1.6" stroke-dasharray="5 4"/>')
        out.append(f'  <circle cx="{bx}" cy="160" r="15" fill="#ffffff" '
                   f'stroke="{STOP}" stroke-width="1.8"/>')
        out.append(f'  <path d="M{bx - 6},154 L{bx + 6},166 M{bx + 6},154 L{bx - 6},166" '
                   f'stroke="{STOP}" stroke-width="2" stroke-linecap="round"/>')
        out.append(_t(bx, 197, L["blocked"], 10.5, STOP, "600"))

    out.append(_t(480, 400, L["zone_caption"], 11.5, SOFT))
    out.append("</svg>")
    return "\n".join(out)


def _panel(x, w, tone, wash, edge, badge, title):
    """One half of the multicast figure: heading, badge and frame."""
    out = [f'  <rect x="{x}" y="8" width="{w}" height="384" rx="10" fill="{wash}" '
           f'stroke="{edge}"/>',
           f'  <circle cx="{x + 28}" cy="44" r="13" fill="{tone}"/>']
    if badge == "check":
        out.append(f'  <path d="M{x + 22},44 l4,4.5 l8.5,-9" fill="none" stroke="#ffffff" '
                   'stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>')
    else:
        out.append(f'  <path d="M{x + 23},39 l10,10 M{x + 33},39 l-10,10" stroke="#ffffff" '
                   'stroke-width="2.2" stroke-linecap="round"/>')
    out.append(_t(x + 50, 49, title, 14.5, INK, "700", anchor="start"))
    return out


def _box(x, y, w, h, title, sub, accent):
    return [f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="#ffffff" '
            f'stroke="{accent}" stroke-width="1.4"/>',
            _t(x + w / 2, y + 27, title, 12, INK, "700"),
            _t(x + w / 2, y + 46, sub, 11, SOFT)]


def _bullets(x, y, items, mark, size=11):
    out = []
    for i, item in enumerate(items):
        yy = y + i * 23
        out.append(f'  <circle cx="{x + 4}" cy="{yy - 4}" r="3" fill="{mark}"/>')
        out.append(_t(x + 16, yy, item, size, SOFT, anchor="start"))
    return out


def multicast_svg(lang: str) -> str:
    L = LABELS[lang]
    out = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 400" role="img" '
        f'aria-label="{L["pass_title"]} / {L["stop_title"]}">',
        _DEFS,
    ]

    # ---- left panel: what must pass inside a zone ------------------------
    out += _panel(8, 439, GOOD, "#f4f9f7", "#cfe3dd", "check", L["pass_title"])
    out.append('  <rect x="32" y="78" width="391" height="122" rx="8" fill="#ffffff" '
               f'stroke="{RULE}" stroke-dasharray="4 4"/>')
    out.append(_t(44, 97, L["same_vlan"], 10.5, SOFT, anchor="start"))
    out += _box(44, 112, 152, 64, L["boards"], L["band24"], "#cfe3dd")
    out += _box(271, 112, 152, 64, L["laptops"], L["band5"], "#cfe3dd")
    out.append(f'  <line x1="202" y1="144" x2="265" y2="144" stroke="{GOOD}" '
               'stroke-width="1.8" marker-start="url(#arrow-good)" '
               'marker-end="url(#arrow-good)"/>')
    out.append(_t(233, 136, L["mdns"], 11, GOOD, "700"))
    out.append(_t(235, 224, L["addr"], 11.5, INK, "600", family=MONO))
    out.append(_t(32, 262, L["drop_head"], 11.5, INK, "700", anchor="start"))
    out += _bullets(32, 288, L["drops"], STOP)

    # ---- right panel: what must not cross between zones ------------------
    out += _panel(505, 447, STOP, "#fdf5f4", "#f0d6d2", "cross", L["stop_title"])
    out += _box(541, 112, 152, 64, L["zone_a"], f'{L["vlan"]} 10', "#f0d6d2")
    out += _box(764, 112, 152, 64, L["zone_b"], f'{L["vlan"]} 20', "#f0d6d2")
    out.append(f'  <line x1="699" y1="144" x2="758" y2="144" stroke="{STOP}" '
               'stroke-width="1.6" stroke-dasharray="5 4"/>')
    out.append(f'  <circle cx="728" cy="144" r="15" fill="#ffffff" stroke="{STOP}" '
               'stroke-width="1.8"/>')
    out.append('  <path d="M722,138 l12,12 M734,138 l-12,12" '
               f'stroke="{STOP}" stroke-width="2" stroke-linecap="round"/>')
    out.append(_t(728, 224, L["no_traffic"], 11.5, STOP, "600"))
    out.append(_t(529, 262, L["off_head"], 11.5, INK, "700", anchor="start"))
    out += _bullets(529, 288, L["offs"], STOP)

    out.append("</svg>")
    return "\n".join(out)


FIGURES = {
    "network-zones": zones_svg,
    "network-multicast": multicast_svg,
}
