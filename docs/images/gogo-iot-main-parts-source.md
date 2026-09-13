# GoGo-IoT main-parts image

- Source: user-supplied PCB render, `user-import/gogo-iot-render.png` (GoGo-IoT v.2B).
- Output: `gogo-iot-main-parts.png`.
- Annotation tool: built-in image generation, using the supplied render as the edit target.
- Style reference: `relay-board-terminals.png` (black labels, red leaders, white background).
- Hardware functions checked against the local GoGo-IoT hardware notes and workshop firmware.
- This is an annotated PCB render, not a photograph. The battery holder is not visible.
- Shipped copy is downscaled to 1600 px wide and colour-reduced to a 256-entry palette (1.35 MB → 0.33 MB). Labels stay crisp at that size, and the worksheet renders inline every image as a data URI, so the page weight is paid three times over.

## Final prompt

Create annotated educational board diagram from input ORIGINAL PCB render. Preserve original board exactly. White margins, black sans serif labels, fine red leader lines, like a technical manual. Use ONLY these six callouts for accuracy and uncluttered readability: "USB-C / Power + programming" leader to leftmost USB connector. "ON / OFF switch" leader to silver slide switch just right of USB. "Grove port 1 / Float switch" leader to four gold pads in upper middle marked 1. "ESP32-C3 / Wi-Fi controller" leader to large silver metal module. "BOOT button" leader to silver pushbutton at bottom right. For ALL FOUR SENSORS use ONE red rectangular outline surrounding the entire rightmost sensor area marked XYZ, Light, Pressure, Temp & Rh, connected to a SINGLE text block outside right edge reading "Onboard sensors; Light; Motion / vibration; Air pressure; Temperature / humidity". NO separate pointers to individual sensor chips. Board centered with generous margins all sides to fit callouts. Top title "GoGo-IoT — Main parts". Bottom footer "18650 battery holder: underside (not visible)". Do not annotate power LEDs or other ports. No invented components. Keep the sensor area as supplied. Wide landscape image.
