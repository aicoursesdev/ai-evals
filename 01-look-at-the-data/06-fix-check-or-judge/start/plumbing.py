"""Given for lesson 01.6: reading your notes and scoring each check on them."""
import csv

from scorecard import data


def read(path):
    """Rows of the coded file, skipping comment lines that start with #."""
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(l for l in f if not l.startswith("#")))


def print_scores(checks, rows):
    """Run every check on every row; compare with the types you gave."""
    emails = {e["id"]: e for w in (1, 2, 3, 4) for e in data.emails(week=w)}
    traces = {t["id"]: t for w in (1, 2, 3, 4)
              for t in data.traces("hd-1", week=w)}
    print(f"{'check':<20} {'type':<14} fires  right  type total  caught")
    for name, (check, wanted) in checks.items():
        fired = {r["id"] for r in rows if check(emails[r["id"]],
                                                traces[r["id"]])}
        has = {r["id"] for r in rows if wanted in r["types"].split(";")}
        print(f"{name:<20} {wanted:<14} {len(fired):>5}  {len(fired & has):>5}"
              f"  {len(has):>10}  {len(fired & has):>6}")
