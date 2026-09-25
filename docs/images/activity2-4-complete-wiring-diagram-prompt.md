# Wiring diagram generation

Tool: built-in image_gen

## Generation prompt

Generate a NEW very simple precise wiring diagram on white background, blue sans serif text, black outlines, red positive wires and black negative wires. Landscape. Use only simple rectangular component blocks, no circuit board illustration. Title "12 V LED workshop wiring". Layout deliberately avoids all wire crossings:
Adapter at far left top. Charge controller at upper centre. LED module at far right top. Relay block below controller and LED. USB cable route in lower left free space.
Controller block has six labelled circular terminals: solar +/- unused; battery +/- accepts two wires from adapter via clearly drawn two-pole barrel connector; load + and load - on RIGHT edge, separated vertically. USB port on LEFT edge lower down.
Critical exact network:
adapter positive to battery positive RED; adapter negative to battery negative BLACK.
Load - BLACK goes horizontally directly to a two-pole connector's upper negative pole and continues horizontally to LED -.
Load + RED goes down to relay COM terminal positioned on LEFT edge of relay block. Relay NO terminal on RIGHT edge sends RED wire to lower positive pole of the two-pole connector and onwards to LED +. Route NO red upwards on right of relay to reach connector. NO and COM are circles on opposite edges and their wires directly touch circles. NC is separate empty terminal on bottom edge. Within relay block you can draw a tiny open-switch symbol between COM and NO to indicate switching, not a permanent wire.
USB-A on controller LEFT edge connects by thick grey cable in free lower left area to USB-C on relay LEFT LOWER edge, distinct from COM. Cable clearly connects ports.
Relay label "ESP32-C6 relay board"; empty pair bottom edge labelled "7–60 V / GND: unused". Use plenty of space. LED box has three yellow circles. White two-pole connector has two distinct rows, black upper pole and red lower pole, no link between rows.
No wire may stop at text. No decorative wires. Each required conductor must be continuous from exact terminal to exact terminal. No overlapping conductors. No photorealism, shadows, or detailed electronics. Footer "Keep the adapter unplugged while connecting wires." Make a clean instructional schematic rather than imitating physical positions.

## Final correction prompt

Edit this diagram retaining ALL wiring routes and component locations. Make background solid pure white, opaque across entire canvas, not transparent/black. Clean crisp solid lines, no artifacts. Fix these labels and terminals precisely: controller upper right BLACK terminal label MUST be "Load −" (minus), lower right RED terminal label stays "Load +". Relay bottom currently conflates NC and power input. Replace bottom with THREE empty terminals: a single circle labelled "NC (unused)" at bottom center; then a separate group of TWO circles further to right labelled "7–60 V" and "GND", with "Unused" beneath that pair. Enlarge relay rectangle and space these if necessary; no wires on these three empty terminals. Keep COM to red controller Load + and NO to red LED + via connector, black Load − direct LED −, and USB power cable exactly as shown. At left, adapter + red should be ONE single clean line through top barrel connector pole to battery +; adapter − black ONE single clean line through lower pole to battery −. Remove duplicated strokes and spurious branching there. All text dark blue and readable on solid white. Simplified line illustration matching educational textbook.

