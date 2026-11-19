"""Lesson 09.7: the mix of email kinds by week.

From this folder: uv run python mix_by_week.py
"""
from plumbing import WEEKS, counts

seen = {w: counts(w)[0] for w in WEEKS}
print("emails:", *(f"wk {w}: {sum(seen[w].values())}" for w in WEEKS))
print(f"{'category':18}" + "".join(f"{'wk ' + str(w):>7}" for w in WEEKS))
for cat in sorted(seen[1]):
    shares = [seen[w][cat] / sum(seen[w].values()) for w in WEEKS]
    print(f"{cat:18}" + "".join(f"{s:>7.0%}" for s in shares))
