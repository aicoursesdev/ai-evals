"""Lesson 02.6: has the traffic moved since the set was drawn?

From this folder: uv run python drift.py
Given. Reads labels only: share of each category in each week of the log.
"""
from collections import Counter

from slices import log


def main():
    emails = log()
    weeks = {w: Counter(e["category"] for e in emails if e["week"] == w)
             for w in (1, 2, 3, 4)}
    print(f"{'category':<18}{'wk 1':>6}{'wk 2':>6}{'wk 3':>6}{'wk 4':>6}"
          "   change")
    for cat in sorted(weeks[1] | weeks[4]):
        share = [weeks[w][cat] / 150 for w in (1, 2, 3, 4)]
        print(f"{cat:<18}" + "".join(f"{s:>6.0%}" for s in share)
              + f"   {100 * (share[3] - share[0]):+.0f} points")


if __name__ == "__main__":
    main()
