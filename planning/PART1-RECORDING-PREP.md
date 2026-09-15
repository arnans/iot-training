# Part 1 (Online Course) — Recording Preparation Note

> **Status 2026-09-01: NOT ready to record.** Course design is done ([COURSE-DESIGN.md](COURSE-DESIGN.md)); the v3 self-recording flow still needs the outline, outcomes, demo captures, media, and tooling listed below. Resume from "Shortest path" at the bottom.

## Methodology: v3 outline-driven hybrid (from book-cs1 Module 5)

Reference docs (on origin/main of book-cs1, in `promo-video/`): `MODULE5-HANDOFF.md` (process record), `module5-outline.md` (as-built example), `MODULE4-HANDOFF.md` (day-one checklist), `m5-keypoints.html` (key-point prompter). KSM: `skills/video-editing-pipeline.md` § v3. Pipeline repo: `github.com/arnans/video-pipeline` (private), `WORKFLOW.md` § v3.

The flow:
1. **Outline** — sections + key points only; each segment tagged `[TALK]` or `[DEMO]`; per-segment time budget; segment IDs (`p1-01`…).
2. **Capture `[DEMO]` clips first** (screen recordings of the real system).
3. **Record** — `[TALK]`: speak naturally from the key-point prompter, one file per segment; flub protocol = pause, re-read the whole sentence. `[DEMO]`: Premiere Voice-Over Record over the clip (clip on V1/A1, VO on A2, export per segment). VO setup: Default Input = mic, Windows mic privacy on, "Mute input during timeline recording" ON, headphones.
4. **ASR** — `asr_pass.py` default settings (no `--fast`, no VAD) with key points as `initial_prompt`, then **always** `repair_gaps.py`; a "no words > 6 s" warning means check the frames before cutting.
5. **Claude transcript review** → as-built outline → placement table (have / need media).
6. Cards drafted by `make_cards_*.py` → manual Codex beautify → `CARDS-EXTERNAL.md` sentinel → `build_narration_xml.py` → Premiere import (always a new sequence; fixes go as patches).
7. **Validate one `[TALK]` + one `[DEMO]` through the whole loop before recording the rest.**

Every `[DEMO]` is its own segment ID, never embedded inside a `[TALK]`.

## Readiness by item

| Item | Status | Gap |
|---|---|---|
| Outline | Not ready | COURSE-DESIGN.md has syllabus bullets, not speaking key points; no segment IDs, no TALK/DEMO split, no per-segment budgets |
| Outcomes | Partial | Goals mapped to sections; no per-section outcome statements; self-check quiz items not written |
| DEMO captures | Not ready | Section 5 needs a working HASS + both boards (sensor graph, pump toggle, automation firing); Section 6 needs the install screencast → blessed install path + HASS version decided. Prerequisite: firmware for both boards (COURSE-DESIGN production task #2) |
| V2 media | Not ready | Sensor/actuator photos, spec-sheet excerpts, marketplace price listings, relay rating plate, pump control box photo (Auto/Off/Manual selector), comms-comparison diagram, Input/Logic/Output card. No asset inventory (`analysis/asset-sources.json` pattern). Cards are generated after recording — not needed now |
| ASR term glossary | Not written | Thai/English mixed terms for Whisper `initial_prompt`: Home Assistant, ESPHome, relay, MQTT, LoRa, hysteresis, capacitive, actuator… |
| Tooling on this machine | Missing | Local book-cs1 clone is 5 commits behind origin (`promo-video/` only on origin); `video-pipeline` not cloned here (searched C: and E:); Whisper env needed |

## Design decision to settle first

COURSE-DESIGN.md says "narrated slide decks"; v3 is **on-camera presenter + cards on V2**. They reconcile (slides become cards), but Sections 1–4 are visual-heavy and will carry more V2 media than Module 5 did; Sections 5–6 are mostly screen-share `[DEMO]` with VO. Recommendation: use v3 as-is — confirm before writing the outline.

## Shortest path to ready

1. Confirm on-camera + cards.
2. Claude writes `part1-outline.md` (v3 format: segments, key points, budgets), per-section outcomes + quiz items, ASR glossary, and clones `m5-keypoints.html` → `p1-keypoints.html`.
3. Roger: firmware + working HASS → capture Section 5 and 6 demos; `git pull` book-cs1 and clone `video-pipeline` on this machine.
4. Validate one `[TALK]` + one `[DEMO]` end-to-end, then record the rest.
