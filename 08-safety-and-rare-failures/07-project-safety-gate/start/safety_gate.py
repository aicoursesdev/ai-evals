"""Lesson 08.7: the safety gate, with a verdict that can say "not proven".

From this folder: uv run python safety_gate.py
"""
from counts import count_by_harm, distinct_attacks, look_alike_count
from scorecard.report import gate
from scorecard.stats import exact_upper
from verdict import LIMITS, LOOK_ALIKE_LIMIT, tries_needed, verdict

counts = count_by_harm(distinct_attacks())
counts["look-alikes"] = look_alike_count()
limits = LIMITS | {"look-alikes": LOOK_ALIKE_LIMIT}
scores = {}
print(f"{'category':14} fail/tries  upper  limit  {'verdict':15}  clean tries")
for harm, limit in limits.items():
    k, n = counts[harm]
    upper = exact_upper(k, n)
    scores[harm] = (1 - upper, 1 - k / n, 1)        # safe rate: low, mid, high
    print(f"{harm:14} {k:3}/{n:<3}     {upper:.3f}  {limit:.2f}   "
          f"{verdict(k, n, limit):15}  {tries_needed(limit)}")
# The course's gate: the low end of the safe rate must be at least 1 - limit.
passed, reasons = gate(scores, [(h, 1 - x, True) for h, x in limits.items()])
print("\ngate passed:", passed)
for reason in reasons:
    print(" ", reason)
