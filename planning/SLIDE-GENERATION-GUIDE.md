# Workshop slide-generation guide

Saved 20 September 2026. This records the design and production decisions used for Activity 1, including the user's revisions. Activities 2–8 have since been completed using this system; see the [84-slide deck inventory and build files](slides/README.md). This remains a reusable reference, not an instruction to generate more slides now.

## How to reuse this guide

For this project, read this guide, [the continuation handoff](SLIDES-HANDOFF.txt), and the current activity worksheet before generating slides. Use the [live Activity 1 deck](https://docs.google.com/presentation/d/1yoNUpS3mo2z2zOZJHEQtuMfSuLxuXltwDT22UHVSHzo/edit) as the editable visual reference. Update the same deck when continuing this workshop.

For another project, copy this guide and adapt the audience, language, content sources, theme and destination. Use a separate deck; authorization to edit the IoT deck does not apply to unrelated presentations. The layout principles and production method transfer; activity numbers, duration, equipment, image sources and speaker notes do not.

The live deck is the editable source. The local previews below preserve two final compositions. They are visual references, not images to insert as whole slides.

- [Cover preview](slide-reference/activity-01-cover-preview.png)
- [First content slide preview](slide-reference/activity-01-equipment-preview.png)
- [Full original cover artwork](slide-reference/activity-01-cover-source.png), preserved outside temporary storage

Later explicit user instructions supersede this guide. Keep this guide updated when the design changes.

## Content and Thai writing

Slides support an instructor-led, hands-on workshop. They should help learners locate the current worksheet section, understand the next action, see the relevant equipment or interface, and interpret what happens. They should not reproduce the worksheet as dense paragraphs.

- Read the current worksheet before authoring. Preserve its section order, technical terms, UI labels, required observations and outputs. Old outlines and archived worksheets are not authoritative.
- Give each slide one clear teaching purpose. Use as many slides as the content needs; do not squeeze a section to meet the old 20–25-slide estimate.
- Use natural Thai with leading and connecting words. Short does not mean clipped or translated-sounding.
- The user rejected “เปลี่ยนทีละอย่าง” as a standalone activity heading and requested “ทดลองใช้งานเซ็นเซอร์”. Use the worksheet's terminology consistently in new content.
- Introduce instructions with phrases such as “ให้ทดลองดังนี้” and connect observations with “แล้วสังเกตค่าต่อไปนี้” when they clarify the sequence. Use the correct spelling “สังเกต”.
- Use concrete Thai instructions and concise subject titles. Preserve exact English UI labels when learners must find them on screen.
- Put demonstration cues, extra explanations, source credits and useful timing in Thai speaker notes. Keep essential learner actions visible on the slide.
- For added technical explanations, verify substantive claims against reliable primary sources. Do not turn approximate radio ranges, battery life or power assumptions into guarantees.

## Visual system

The selected direction is **warm agricultural**: cream, deep green, existing farm imagery and restrained ochre/gold accents. Alternate compositions to suit the content rather than repeating a single slide layout.

| Property | Activity 1 setting |
| --- | --- |
| Canvas | 720 × 405 pt; 16:9 |
| Typeface | Prompt |
| Cream background | `#F6F2E8` |
| Deep green | `#163E33` |
| Main dark text | `#263E34` |
| Sage labels/captions | `#617D6D` |
| Pale sage | `#DCE5D8` |
| Ochre accent | `#A3652C` |
| Gold accent | `#D3AD65` |
| Content titles | Usually 30–32 pt, bold |
| Main content | Usually 19–25 pt |
| Small activity label | Approximately 10.5 pt in the existing deck |
| Section reference | 18 pt, bold, centered in a 44 pt circle |

Use deep green text on cream and cream text on deep green. Green slides and split green/cream slides are intentional variants. Use comfortable margins and preserve Thai diacritics and natural line breaks. Smaller existing labels are not a reason to shrink instructional body text.

### Standard content slide geometry

Coordinates are points from the top-left of the slide. These are starting positions; adapt them to the composition.

| Element | x | y | Width | Height |
| --- | ---: | ---: | ---: | ---: |
| Small activity label | 35 | 9 | 490 | 25 |
| Main title | 30 | 44 | 660 | 52 |
| Short title accent rule | 35 | 99 | 54 | 2 |
| Section circle and centered number | 641 | 9 | 44 | 44 |
| Equipment image on `p` | 35 | 127 | 650 | Approximately 232, proportional |

The section marker contains only the worksheet reference, such as **1.1**. Do not include “ใบงาน”. On cream, use a green circle and white number; on dark green, use a gold circle and green number. It is a worksheet reference, not a slide counter. The cover has no section circle; the closing slide uses “ท้ายกิจกรรม”.

**Do not restore:** the bottom footer bar, repeated section text at the bottom, yellow action/takeaway band, or typed page numbers. No page numbers are currently used. Only add them if they update automatically when slides are inserted or deleted and the user wants them.

### Activity cover

Each activity cover can show its large banner, activity number, title, worksheet duration and a brief purpose. Keep these as editable text. Use the full original artwork where available instead of enlarging an already narrow banner crop.

Activity 1 uses the following composition:

| Element | Geometry / typography |
| --- | --- |
| Farm banner | x=0, y=0, w=720, h=190; native center crop; square corners |
| Activity label | x=30, y=204, w=500, h=26; 14 pt bold ochre; “กิจกรรมที่ 1 / SENSE” |
| Duration | x=580, y=204, w=105, h=26; 14 pt sage, right aligned; “35 นาที” |
| Title | x=30, y=233, w=660, h=91; 34 pt bold deep green; two lines |
| Accent rule | x=35, y=324, w=54, h=2; ochre |
| Purpose | x=30, y=339, w=660, h=55; 17 pt dark text; two lines |

Title: “รู้จักและทดลอง” / “อ่านค่าเซนเซอร์”.

Purpose: “ทดลองอ่านค่าจากบอร์ด แล้วสังเกตเมื่อสภาพรอบตัวเปลี่ยน” / “เพื่อนำข้อมูลไปใช้ตัดสินใจในฟาร์ม”.

The banner occupies nearly half the cover and meets the slide edges. Do not repeat that banner on the first content slide. Read the duration and purpose from the new activity's source; do not carry over Activity 1's 35 minutes.

### Images and screenshots

- For automation concept illustrations, use clearly symbolic representatives without connectors, pin headers or invented circuit details. Use contemporary technical line art with gray outlines and selective blue/yellow accents. If depicting the actual kit instead, match the reference equipment faithfully, including the LED strip. Keep the trigger and observed result visually clear. Slide 24 is the approved exemplar; see `planning/slides/slide-24-review-example.json` and `planning/slides/automation-visuals.json`. Apply this two-scene layout to automation screenshots: a 600 × 200 pt illustration at (60,103), followed by editable headings and Thai instructions in two columns. Preserve useful wiring, History and Dashboard references. The shared `scripts/concept_slide_layout.mjs` implements the layout for all 12 matching slides.

- Prefer existing project images. Keep equipment photographs, annotated diagrams and interface screenshots proportional and fully legible. Do not crop off meaning-bearing labels or controls.
- Use actual **native rounded-rectangle image masks** for inset equipment images and screenshots. Reduce the corner radius to a subtle curve, approximately 7 pt in this deck.
- In Google Slides, select the image, choose **Mask image → Shapes → Rounded Rectangle**, and drag the yellow adjustment handle close to the left edge. The default radius is too large. Judge the result at slide scale; the exact visual radius depends on the image dimensions.
- The mask must cut into the image itself. A white rounded rectangle behind a rectangular photograph does not round that photograph and was explicitly rejected by the user.
- Do not add the discarded white mounts or sage frame outlines around real images. Preserve the existing native masks when duplicating compositions, and verify them after replacing or resizing images.
- Edge-to-edge cover and closing banners stay square, with no inset border or rounded frame. Decorative farm imagery can be cropped to fill; preserve aspect ratio.
- When a needed image is unavailable, use a clearly labeled placeholder describing it. The existing placeholder has a sage surround (`#E9EDDF` fill, `#A8B8A0` outline); this is distinct from the rejected mounts around real images.
- Farm artwork is illustrative, not documentary photography. Credit its source and nature in speaker notes.

## Activity 1 exemplar catalog

The Activity 1 reference section contains **10 slides**, including its cover; the completed Activities 1–8 deck has 84 slides. Native IDs are stable identifiers, not display page numbers. The IDs `a1_slide_2` through `a1_slide_9` predate the cover insertion; do not infer their current position from their suffixes.

| Order | Native slide ID | Purpose and composition |
| ---: | --- | --- |
| 1 | `a1_cover` | Large farm banner, title, duration and purpose |
| 2 | `p` | Board overview; standard cream header and large annotated equipment image |
| 3 | `a1_slide_2` | Float switch setup; green instruction column beside equipment photo |
| 4 | `a1_slide_3` | USB connection; cream instructions and serial-port screenshot |
| 5 | `a1_slide_4` | Board name/IP explanation on deep green |
| 6 | `a1_slide_5` | Open board webpage; cream instructions and complete UI screenshot |
| 7 | `a1_slide_6` | Sensor experiment table with fine sage rules |
| 8 | `a1_slide_7` | Comparison using a cream/green split |
| 9 | `a1_slide_8` | Response-time experiment, numbered instructions and intentional image placeholder |
| 10 | `a1_slide_9` | Closing questions beside a tall, square-edged farm illustration |

Choose an exemplar for its teaching purpose, content density and image orientation. Duplicate it and adapt its content. Do not force every topic into the same structure.

Main project sources include `docs/activity-1.md`, `docs/images/gogo-iot-main-parts.png`, `docs/images/activity1-web-ui.png` and `docs/images/activity-banners/`. The cover's full original PNG is saved in `planning/slide-reference/activity-01-cover-source.png`; the worksheet's narrow WebP banner is a different crop. The editable deck retains the other placed image assets.

## Native Google Slides production workflow

This workshop explicitly uses direct native Google Slides editing, preserving the deck link. Avoid exporting, rebuilding and repeatedly importing PPTX files. Use the applicable presentation and Google Drive/Slides skills available in the current environment; tool installation paths and browser menu IDs may change.

1. **Read sources and the current deck.** Fetch the full presentation with `get_presentation`. Save a private JSON snapshot and inspect slide IDs, element IDs, sizes, transforms, text runs, notes and image roles. Never assume the previous session's revision or IDs are current.
2. **Record the plan.** For each new slide, record its purpose, source worksheet section and exemplar. Map every copied image, label and note to keep, replace or delete. Remove stale topic-specific material.
3. **Parse the reference.** Where provided by the Google Slides skill, use `parse_template_design_system.mjs` on the snapshot to capture the layout catalog and geometry. Confirm interpretation against rendered slides.
4. **Duplicate and adapt native elements.** Use `duplicateObject` with explicit object-ID mappings. Preserve editable text, image proportions, native masks and intentional style variants. Do not rasterize slide text or paste a complete preview as the slide.
5. **Write with revision protection.** Use `batch_update_presentation` and a fresh `write_control.requiredRevisionId` when available. Send native request objects rather than JSON strings.
6. **Use local images correctly.** In this session, the connector accepted an absolute local image path in `image_uris`, matched by the same path in `createImage.url` or `replaceImage.url`. For the cover, the target image frame was sized first, then `replaceImage` with `CENTER_CROP` placed the full original PNG proportionally. Inspect replacement results.
7. **Apply small image masks in the UI when needed.** Native Google Slides Mask image controls were used successfully. Reinspect the selected image and adjustment handle; do not reuse old browser coordinates blindly. The API response alone did not expose a useful small-radius value, so visual verification was essential.
8. **Update speaker notes.** Re-read speaker-note object IDs after duplication. Replace copied notes with the new slide's explanation and sources. Preserve unchanged notes. Remove credits for images no longer on that slide.
9. **Establish order after structural readback.** Complete duplication before reordering. `updateSlidesPosition` lists must follow current presentation order. To establish an arbitrary order, move individual slides to insertion index 0 in reverse desired order, or use valid sequential moves. Moving the new cover alone to index 0 was sufficient here.
10. **Read back and validate.** Save the final presentation snapshot, check slide order/count, and use the skill's `check_output_issues.mjs` when available. Render and inspect the final compositions. Repair concrete defects and inspect the affected result again.

Geometry: API sizes/transforms may be in EMU; **12,700 EMU = 1 pt**. Compute displayed dimensions from size and scale before changing transforms. A source object's nonuniform transform does not by itself prove the displayed image is distorted; compare the displayed aspect ratio with its actual content. Preserve the displayed ratio when enlarging equipment images.

For mixed-format text, record and restore individual style runs instead of blindly applying one uniform style to the entire box. All text added to the cover is editable native text using Prompt.

## Verification and storage

Check Thai wording, wrapping and diacritics; contrast; screenshot readability; image proportions and actual corner cutouts; safe margins; worksheet references; speaker notes; correct order; and absence of manual page counters or discarded bottom bars. The cover and first content slide should not repeat the same banner.

Use the current skill's normal export/render workflow when available. In this Windows session, its usual local runtime/export dependencies were unavailable, so native `get_slide_thumbnail` at `LARGE`, downloading the returned `contentUrl`, and `view_image` provided visual QA. Google rendered the previews at 1600 × 900. This fallback still requires inspecting the images; a successful API response or clean issue checker is not enough.

Temporary snapshots, signed image URLs, mutation requests and intermediate previews belong under ignored `.tmp/workshop-slides/`. Do not commit signed URLs, access tokens or raw connector snapshots. Permanent reference material belongs with this guide; the native deck remains in Drive. Browser tab IDs, menu DOM IDs and absolute tool-cache paths are session details, not reusable configuration.

The saved previews are the final Activity 1 cover and board-overview compositions as of this guide's date. The complete 84-slide deck has been rendered and reviewed. Activity 1 still intentionally contains one image placeholder on `a1_slide_8`; Activities 2–8 are authored with no new image placeholders. Their content and source references are saved in [the manifest](slides/activity-2-8.json).

## Prompts for later use

**Continue this project:**

> Read planning/SLIDE-GENERATION-GUIDE.md, planning/SLIDES-HANDOFF.txt and the current worksheet for Activity [N]. Generate that activity in the existing Google Slides deck using Activity 1's design. Start with its own large-banner cover, use natural Thai and numbered worksheet circles, preserve editable content and speaker notes, and visually verify the result. Follow the latest worksheet rather than old outlines.

**Use the method elsewhere:**

> Use the attached SLIDE-GENERATION-GUIDE.md and reference previews as the starting design system for a new presentation about [topic] for [audience]. Use [source material] and create it in [destination]. Adapt the imagery, palette, language and section labels to this project. Preserve the principles of clear teaching purpose, varied compositions, editable content, subtle image masks and visual verification. Do not modify the original IoT deck or reuse its activity facts.

**Apply a later design change:**

> Update the presentation for [specific change], then revise planning/SLIDE-GENERATION-GUIDE.md and the relevant saved previews so future slides follow the new decision.
