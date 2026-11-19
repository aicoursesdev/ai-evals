"""Given for lesson 01.5: reading the notes and printing the two reports."""
import csv
from collections import Counter

from scorecard import data


def read(path):
    """Rows of the coded file, skipping comment lines that start with #."""
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(l for l in f if not l.startswith("#")))


def by_week(rows):
    """{type: Counter of week -> traces}, using the log to find each week."""
    week_of = {e["id"]: w for w in (1, 2, 3, 4) for e in data.emails(week=w)}
    table = {}
    for row in rows:
        for t in row["types"].split(";"):
            if t:
                table.setdefault(t, Counter())[week_of[row["id"]]] += 1
    return table


def print_table(rows, tally):
    """The count table: traces read, then one line per type, most first."""
    failed = [r for r in rows if r["ok"] == "no"]
    print(f"{len(rows)} read, {len(rows) - len(failed)} fine, "
          f"{len(failed)} with a failure")
    weeks = by_week(rows)
    print(" n  share  type                  week 1 2 3 4")
    for name, n in tally.most_common():
        w = weeks[name]
        print(f"{n:>2}  {n / len(rows):>4.0%}  {name:<20}  "
              f"{w[1]:>7}{w[2]:>2}{w[3]:>2}{w[4]:>2}")


def print_first_seen(seen, total, batch=25):
    """When each type first appeared, then new types per batch of traces."""
    for name, position in sorted(seen.items(), key=lambda kv: kv[1]):
        print(f"read {position:>3}: {name}")
    for start in range(0, total, batch):
        new = [t for t, p in seen.items() if start < p <= start + batch]
        print(f"traces {start + 1:>3} to {start + batch:>3}: "
              f"{len(new)} new type(s)")
