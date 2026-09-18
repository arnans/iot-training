#!/usr/bin/env python3
"""Cut the activity banner PNGs down to the web-sized .webp the pages actually load.

The source PNGs come out of image generation at 2172x724 and about 2 MB each -- far
more than a banner strip needs, and slow on the workshop's WiFi. extra.css shows them
at `aspect-ratio: 6/1` with `object-fit: cover`, so the browser already throws the top
and bottom away: this script makes that same centre crop up front, scales it to 1600px
wide (the content column is 76rem) and encodes WebP. About 80-110 KB each, with no
visible change on the page.

The repo keeps only the .webp. The PNGs were removed to save space, so before re-running
this, put the sources back in docs/images/activity-banners/ -- either the last commit
that carried them:

    git checkout 724a788 -- docs/images/activity-banners      # then delete the PNGs again

or a freshly generated banner, using the prompts in that folder's PROMPTS.md. A new
banner only needs to be 6:1 or taller and at least 1600px wide.

    python scripts/build-banners.py

Requires Pillow. Re-run after adding or regenerating a banner, and commit the .webp.
"""

from pathlib import Path

from PIL import Image

BANNERS = Path(__file__).resolve().parent.parent / "docs" / "images" / "activity-banners"
WIDTH, HEIGHT = 1600, 267          # 6:1, matching .activity-banner in extra.css
QUALITY = 65


def main() -> None:
    total_png = total_webp = 0
    for png in sorted(BANNERS.glob("*.png")):
        src = Image.open(png).convert("RGB")
        band = round(src.width / 6)
        top = (src.height - band) // 2
        out = src.crop((0, top, src.width, top + band)).resize((WIDTH, HEIGHT), Image.LANCZOS)
        webp = png.with_suffix(".webp")
        out.save(webp, "WEBP", quality=QUALITY, method=6)
        total_png += png.stat().st_size
        total_webp += webp.stat().st_size
        print(f"{png.name:30} {png.stat().st_size / 1e6:5.2f} MB -> "
              f"{webp.name:31} {webp.stat().st_size / 1024:6.1f} KB")
    if total_png:
        print(f"{'total':30} {total_png / 1e6:5.2f} MB -> {'':31} {total_webp / 1024:6.1f} KB")


if __name__ == "__main__":
    main()
