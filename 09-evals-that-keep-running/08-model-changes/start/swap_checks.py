"""Lesson 09.8: the Module 03 code checks on both sets of drafts.

Given: everything it reads and prints.

From this folder: uv run python swap_checks.py
"""
from plumbing import clean, swap
from scorecard.graders import CHECKS
from scorecard.stats import mcnemar, pair_counts

mail, old, new = swap()
ids = sorted(new)
print(f"{'check':22}{'usual':>7}{'smaller':>9}")
for name, (check, _) in CHECKS.items():
    fired = [sum(bool(check(mail[i], t[i])) for i in ids) for t in (old, new)]
    print(f"{name:22}{fired[0]:>7}{fired[1]:>9}")
a, b = [[clean(mail[i], t[i]) for i in ids] for t in (old, new)]
print(f"no check fires: usual {sum(a)}, smaller {sum(b)} of {len(ids)}")
print(pair_counts(a, b), f"McNemar p {mcnemar(a, b):.2f}")
