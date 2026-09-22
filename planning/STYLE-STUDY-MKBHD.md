# Style study — MKBHD, applied to the overview videos

Reference: *Google Pixel 11/Pro/Fold Impressions: It Is What It Is* (MKBHD, 12 Aug 2026, 11:13),
downloaded 22 Sep 2026 for local frame analysis only, not republished. Working files and scripts
in `user-import/style-study/` (gitignored).

Everything below is **measured**, not eyeballed: ffmpeg scene detection for cuts, OpenCV feature
matching against a fixed wide reference frame for zoom scale, frame-by-frame at every scale change.

## What he does

**His talking head is set up like ours.** One locked camera, seated, window behind — 15 of his
78 shots. Everything else is handheld product B-roll. So his A-roll grammar transfers directly.

| Finding | Evidence |
|---|---|
| **Punches are mostly instant cuts** | 12 of 14 scale changes happen between one frame and the next, in and out |
| **A fast smooth push is reserved for the signature line** | the only two eased moves (10–13 frames ≈ 0.4 s, to 1.34–1.36×) are both on the title line *"It is what it is"* (0:36 and the close at 10:12) |
| **Normal punch size 1.15–1.26×** | 9 punch-ins; the two signature pushes go further, to ~1.35× |
| **Punch on a reveal, a punchline, a number, disbelief, or an aside** | "that's it?? … a glowing LED", "Just phone calls. I can't remember the last time I made a phone call", "starts at thirteen hundred dollars", "glass is glass. But you know…" |
| **Punch back *out* when a new topic or a list starts** | out at "Not even text messages…" (a list), "Now Google also did mention…" (new topic) |
| **Two tiers** | from an already-punched 1.12×, "But then get this…" punches again to 1.31× |
| **Every talking-head return starts wide** | every A-roll shot after B-roll opens at 1.00×; the punch comes inside the shot |
| **Punched-in can hold** | 1.15× held 12 s (92.6–104.4 s); not just a few seconds |
| **Numbers get a small callout beside him** | "256 GB", "$1099 · 12 GB RAM" as a small card in the empty side of the frame — a label, not a slide |
| **Much more cutaway, much denser punches** | 38% of runtime on camera; one punch every 29 s of on-camera time |

## How ours compares

| | On camera | Zooms | One zoom per … on camera |
|---|---|---|---|
| MKBHD | 38% | 9 | 29 s |
| V1 | 78% | 3 | 233 s |
| V2 | 79% | 4 | 90 s |
| V3 | 83% | 1 | 226 s |

Our 115% base with eased zooms to 130% is the right *look*; there is far too little of it, and
all our zooms move the same way.

## Proposal (not applied — needs Roger's decision)

1. **Density: ~1 punch per 45–60 s of on-camera time** — about 13 in V1, 6 in V2, 4 in V3
   (≈23, up from 8). Chosen by his criteria from our transcript: reveals, numbers, warnings,
   jokes/asides, disbelief, and Roger's own callbacks ("แยกคนที่เป็นมือใหม่…").
2. **Mixed motion, his way:** instant cut for the ordinary punches (in to ~125%), a **fast eased
   push (~0.4 s) to ~135%** for each video's single signature line (Z1, Z4, Z7/Z8-type thesis
   lines). This contradicts the "smooth, not a cut" rule from 21 Sep, so it is Roger's call.
   Alternative that keeps the rule: all eased, but faster (0.3–0.4 s instead of 0.6 s).
3. **Punch out on a topic change or a list**, not only at the end of a sentence.
4. **Two tiers for build-ups:** 115 → 125 → 135 where Roger escalates a point.
5. **Number callouts (optional):** a small label card beside Roger for the few hard numbers he
   says — "80–90%", "220 V", "~3,000 บาท", "2–3 ชม." — label, not a text slide.
6. **More cutaway (later):** we are at ~80% on camera. Not reachable without more art; worth it
   for V1's long stretches between 7:51 and 9:08, and 11:48 to 12:17.

Constraint: our source is 1080p, so 135% is about the ceiling before softness shows; his is shot
at a higher resolution. Horizontal reframing (moving Roger off-centre for callouts) needs the
Premiere Center units verified first.
