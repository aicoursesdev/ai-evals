"""Lesson 09.7: the triage score by week and by slice.

From this folder: uv run python score_by_slice.py
"""
from plumbing import WEEKS, counts

seen = {w: counts(w) for w in WEEKS}
print(f"{'category':18}" + "".join(f"{'wk ' + str(w):>9}" for w in WEEKS))
for cat in sorted(seen[1][0]):
    cells = [f"{seen[w][1][cat]}/{seen[w][0][cat]}" for w in WEEKS]
    print(f"{cat:18}" + "".join(f"{c:>9}" for c in cells))
for w in WEEKS:
    right, n = sum(seen[w][1].values()), sum(seen[w][0].values())
    print(f"week {w}: {right} of {n} = {right / n:.1%}")
