"""Merge the answer files teams download from the worksheet into one CSV.

    python scripts/collect_answers.py answers/            # -> answers.csv
    python scripts/collect_answers.py answers/ -o day2.csv

Each `farm-team-<n>-<zone>.json` (the "ดาวน์โหลดคำตอบ" button in the worksheet) becomes one
row; each field key becomes one column. Team and zone come first, then the keys in sorted
order, which groups them by session and activity (s1.*, s2.*, s3.*, d.* for the design
canvas). Written as UTF-8 with BOM so Excel opens the Thai text correctly.

Key conventions and the storage format: FILLABLE-WORKSHEET.md.
"""
import argparse
import csv
import json
import sys
from collections import Counter
from pathlib import Path

LEAD = ["_team", "_zone", "_file", "_exported", "team.no", "team.zone"]


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("folder", type=Path, help="folder holding the teams' .json files")
    ap.add_argument("-o", "--out", type=Path, default=Path("answers.csv"))
    args = ap.parse_args()

    rows, keys = [], set()
    for path in sorted(args.folder.glob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            print(f"skip {path.name}: {exc}", file=sys.stderr)
            continue
        fields = data.get("fields") if isinstance(data, dict) else None
        if not isinstance(fields, dict):
            print(f"skip {path.name}: no 'fields' object", file=sys.stderr)
            continue
        row = {
            "_file": path.name,
            "_exported": data.get("exported", ""),
            "_team": str(data.get("team") or fields.get("team.no", "")).strip(),
            "_zone": str(data.get("zone") or fields.get("team.zone", "")).strip(),
        }
        row.update({k: v for k, v in fields.items() if str(v).strip()})
        keys.update(row)
        rows.append(row)

    dupes = [t for t, n in Counter(r["_team"] for r in rows).items() if n > 1 and t]
    if dupes:
        print(f"note: more than one file for team(s) {', '.join(dupes)}", file=sys.stderr)

    cols = LEAD + sorted(k for k in keys if k not in LEAD)
    with args.out.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    print(f"{len(rows)} teams, {len(cols)} columns -> {args.out}")


if __name__ == "__main__":
    main()
