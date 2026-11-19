"""Given for lesson 01.3: printing the ids and writing your notes sheet."""
import csv
import sys
from pathlib import Path

from scorecard import data


def print_ids(ids):
    """The count, then the ids ten to a line."""
    print(len(ids), "ids drawn")
    for i in range(0, len(ids), 10):
        print(" ".join(ids[i:i + 10]))


def write_sheet(ids, sheet=Path("my-notes.csv")):
    """Start the sheet: id and week filled in, ok and note left empty."""
    if sheet.exists():  # never overwrite notes you have written
        sys.exit(f"{sheet} exists, left alone")
    week_of = {e["id"]: w for w in (1, 2, 3, 4)
               for e in data.emails(week=w)}
    with open(sheet, "w", encoding="utf-8", newline="") as f:
        out = csv.writer(f)
        out.writerow(["id", "week", "ok", "note"])
        out.writerows([i, week_of[i], "", ""] for i in ids)
    print("wrote", sheet)
