# Slide asset provenance

These assets support the native Google Slides deck and `planning/slides/activity-2-8.json`.

- `a5_05-vibration-sensor-v2.png` replaces slide 47's timer with a round blue vibration sensor attached to the left pump. Built-in image_gen edit; prompt in `planning/slides/automation-visuals.json`.

- `a4_12-auto-selector-v2.png` uses slide 39's Auto/Manual selector with Auto selected, retaining slide 40's flowing pump. Built-in image_gen edit with both images as references; prompt in `planning/slides/automation-visuals.json`.

- `a4_11-mode-selector-v2.png` revises slide 39: Auto/Manual selector on the left; automatic pump symbol and hand operating an ON/OFF toggle on the right. Built-in image_gen edit; prompt in `planning/slides/automation-visuals.json`.

- `a4_05-timeline-v2.png` replaces slide 33's clock/bulb scenes with an After–Before timeline showing a passed condition inside the interval and failed conditions outside. Built-in image_gen; prompt in `planning/slides/automation-visuals.json`.

- `a4_07-timeline-v2.png` replaces slide 35's separate clock/bulb scenes with a timeline: After starts the permitted interval and Before ends it. Generated with built-in image_gen; full prompt in `planning/slides/automation-visuals.json`.

- `a4_03-hysteresis-v2.png` replaces the initial slide 31 illustration with separate lower ON and higher OFF thresholds and a blue keep-state band. Built-in image_gen; full prompt in `planning/slides/automation-visuals.json`. Its horizontal axis is light level, not time.

- `a3-05-trigger-action-symbolic-v5.png` is the user-approved conceptual illustration exemplar. Earlier `a3-05-trigger-action*` variants document the design review, and are not the current slide image.
- `a4_03-concept.png`, `a4_05-concept.png`, `a4_07-concept.png`, `a4_08-concept.png`, `a4_10-concept.png`, `a4_11-concept.png`, `a4_12-concept.png`, `a5_02-concept.png`, `a5_05-concept.png`, `a5_06-concept.png`, and `a5_07-concept.png` were generated with built-in image_gen using the approved exemplar as a style reference. Exact prompts and slide mappings are in `planning/slides/automation-visuals.json`. They illustrate concepts, not actual equipment, wiring or app interfaces.

- `activity-02-led.jpg`, `activity-03-rules.jpg`, `activity-04-irrigation.jpg`, `activity-05-protection.jpg`, `activity-07-dashboard.jpg`, `activity-08-design.jpg`: JPEG copies of the existing full original illustrations used to create the corresponding worksheet banners. They are illustrations, not photographs of actual farms. The cover uses a native center crop without stretching.
- `activity-06-history.jpg`: JPEG conversion of the current `docs/images/activity-banners/activity-06-history.webp`, showing farmers reading a historical graph. It replaces the older landscape-only artwork.
- The `a4-*.png`, `a5-*.png`, `a6-3-build-dashboard.png` and `hist-1-history-graph.png` assets are actual frames from the repository's Home Assistant demonstration recordings under `docs/images/walkthroughs/`. Their original recording IDs predate the renumbering of History and Dashboard. Names, dates, values and entity identifiers in screenshots are examples, not values learners should copy.
- `a5-3-sensor-unavailable.png` is a frame at 55% of the matching 25.25-second MP4, showing the state-change trigger configuration. The other selected frames were taken from the recordings' original frame sequences, either the final useful screen or just before the Save dialog.

Do not use video poster title cards as substitutes for interface screenshots. Preserve the full relevant screenshot content and use native small-radius image masks. Keep edge-to-edge cover banners square.
