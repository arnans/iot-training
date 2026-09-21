# Workshop presentation source

[Native Google Slides deck — Activities 1–8](https://docs.google.com/presentation/d/1yoNUpS3mo2z2zOZJHEQtuMfSuLxuXltwDT22UHVSHzo/edit)

Completed 20 September 2026: **84 slides**, with editable Thai text, worksheet-section circles and Thai speaker notes. Activity 1's ten slides were preserved; 74 slides were added for Activities 2–8. Every activity has a large-banner cover. Slide counts are descriptive and are not printed as manual page numbers in the deck.

| Activity | Slides | Current positions | Coverage |
| --- | ---: | --- | --- |
| 1 — Sense | 10 | 1–10 | Cover; 1.1–1.5; closing question |
| 2 — Act | 8 | 11–18 | Relay terminals, unloaded test, power/wiring, physical lamp test, closing question |
| 3 — Logic | 9 | 19–27 | Device identity, two screens, thresholds, rules, three-cycle test, optional timer, end-of-session preparation |
| 4 — Think | 14 | 28–41 | Chattering, hysteresis, conditions, time triggers, notifications, pump changeover, humidity simulation, Auto/Manual |
| 5 — Failure lab | 11 | 42–52 | Preparation, four failures and their pass criteria, maintenance, controller failure, break preparation |
| 6 — History | 6 | 53–58 | Restart checks; 6.1–6.4; interpreting events, extrema and missing history |
| 7 — Dashboard | 6 | 59–64 | Users, displayed information vs commands, four required cards, peer usability test |
| 8 — Design | 20 | 65–84 | Scenario, communications, remote access, batteries, DC/AC power, worked energy examples, system/test plan, exchange and equipment return |

## Files and editing

- [Generation guide](../SLIDE-GENERATION-GUIDE.md): visual and writing rules, exemplar IDs, image-mask method and production workflow.
- [Activity 2–8 manifest](activity-2-8.json): final slide IDs, wording, notes, worksheet references, image paths and primary-source URLs. All content is UTF-8.
- [Slide catalog](SLIDE-CATALOG.md): slide-by-slide mapping from native ID to worksheet section and layout.
- [Request builder](../../scripts/build_workshop_slides.mjs): duplicates the native Activity 1 exemplars and produces connector batch requests; it does not contact Google or contain credentials.
- [Reference assets](../slide-reference/assets/): cover illustrations and selected frames from the repository's walkthrough recordings. Original equipment photographs and diagrams remain under `docs/images/`.

For ordinary revisions, edit the existing native deck in place and update the manifest. Do not blindly rerun duplicate requests on a deck that already has these IDs. Activity 1 itself is maintained in the native deck; this is not a standalone whole-deck reconstruction script.

To build the request files for a fresh copy containing the Activity 1 exemplars, save a full presentation read to a private JSON file, then run from the repository root:

```powershell
node scripts/build_workshop_slides.mjs .tmp/workshop-slides/expand-source.json .tmp/workshop-slides/expansion
```

The builder needs Node.js and the tracked PNG/JPEG assets, with no additional npm dependencies. It reads image dimensions directly and preserves proportions. Its generated files contain machine-specific absolute paths and belong in `.tmp/`, not Git. It emits `batches.json` (native duplicate/update requests, local image upload paths and notes) and `slide-plan.json` (exemplar mapping).

Apply each batch through the Google Slides connector, passing its local `image_uris` when present. Then read the native speaker-note IDs, write the corresponding notes, and reorder slides using the manifest order after Activity 1. Read back the presentation, run the available skill's issue checker, render and inspect before delivery. Use the guide for revision protection and native image-mask details.

## Content decisions

Current `docs/activity-2.md` through `docs/activity-8.md` controlled the scope. History is Activity 6; Dashboard is Activity 7. Actual screen labels are preserved, while explanations use natural Thai. Detailed demonstration and troubleshooting steps are in speaker notes rather than packed into the slide body.

For the communications and battery discussions, generic ranges, prices, lifespan and cycle counts were not presented as guarantees. The slides direct learners to test their site and check the selected product's specifications. Primary sources are linked in the relevant manifest entries and native speaker notes.

The energy examples explicitly use 12 V and illustrative usable fractions of 50% for lead-acid and 85% for LFP. LED: 400 Wh/day, approximately 67 Ah or 40 Ah, and 133 W of panels before losses. Pump: 2,200 Wh/day, approximately 367 Ah or 216 Ah, and 733 W before losses. These are classroom calculations; actual sizing must account for losses, reserve time and startup requirements. The 1,100 W pump is a stipulated load, not a claim that every AC load's real watts equal V × A.

Air humidity is explicitly labeled as a classroom stand-in for soil moisture. Manual mode disables automatic starts, not the stopping/protection rules. Pump vibration is supporting evidence, not proof of water flow. The failure lab requires Traces/notifications as evidence when multiple protections may stop the pump.

## Validation and known limitation

The completed native deck was read back with 84 slides in order. The structural issue checker reported zero issues. Google rendered all 84 slides for visual review; the corrected image/caption slides were rendered again. Covers, Thai text fit, worksheet circles, image proportions and actual small-corner masks were checked. No manual page counters or discarded footer/action bars were added.

Activity 1's pre-existing, intentionally labeled image placeholder remains on native slide `a1_slide_8` (currently ninth). Activities 2–8 have no new image placeholders. The live Slides document is stored in Drive; Git stores the guide, content manifest, request builder, reference assets and catalog, not the native Slides file itself.

## Approved automation illustration layout

Slide 40 matches slide 39's Auto/Manual selector, with Auto highlighted blue. Its current preview is `planning/slide-reference/slide-40-auto-selector-preview.png`.

Slide 39 distinguishes an Auto/Manual mode selector from a manually operated ON/OFF toggle. The current preview is `planning/slide-reference/slide-39-mode-selector-preview.png`, superseding its earlier contact-sheet image.

Slide 33 uses the same timeline style, with pass/fail markers inside and outside After–Before. Its current preview is `planning/slide-reference/slide-33-timeline-preview.png`. A failed time condition skips the action; it does not command the light to turn off.

Slide 35 now uses an After–Before timeline with the permitted interval highlighted in blue; `planning/slide-reference/slide-35-timeline-preview.png` supersedes its earlier contact-sheet image. Its existing instructions retain the separate light-level condition and the Time triggers at both boundaries.

Slide 31 was subsequently revised to explain hysteresis with separate ON/OFF thresholds and a band where the light keeps its current state. Its current preview is `planning/slide-reference/slide-31-hysteresis-preview.png`; this supersedes slide 31 in the earlier contact sheet. The generator omits the central flow arrow for this diagram.

Slide 24 (native ID a3_05) is the approved exemplar: modern conceptual line art with blue/yellow accents, followed by editable Thai headings and instructions. The layout also covers slides 31, 33, 35, 36, 38–40, 44 and 47–49. Images show events, conditions and observed results with generic symbols, without invented electrical connectors. Wiring, History and Dashboard screenshots remain useful references and retain their layouts.

`automation-visuals.json` records the 11 additional illustrations, exact prompts and Thai copy. `slide-24-review-example.json` records the approved exemplar. The manifest now supplies `concept` fields to the shared `scripts/concept_slide_layout.mjs` layout, used by the standard builder. Rebuilds preserve all 12 conceptual slides.

Rollout verified on 21 September 2026: all 44 new/revised text fields matched native readback, deck order and count stayed at 84 slides, and all 12 concept slides were rendered and visually inspected. The issue checker reported no errors; the two existing warnings concern intentional wiring arrows on slide 15. Review sheets are saved as `planning/slide-reference/automation-concepts-1.jpg` through `automation-concepts-3.jpg`. The 74-slide Activity 2–8 builder completed successfully with all 12 concept layouts.
