"""Lesson 05.5: the same comparison on single checks.

From this folder: uv run python single_checks.py
"""
from plumbing import drafts, emails
from scorecard.graders import CHECKS
from scorecard.stats import mcnemar, pair_counts

E, T1, T2 = emails(), drafts("hd-1"), drafts("hd-2")
ids = sorted(T2)
print(f"{'check':<20} fires on: hd-1  hd-2   only hd-1  only hd-2  p-value")
for name, (check, _) in CHECKS.items():
    a = [int(not check(E[i], T1[i])) for i in ids]     # 1 means no firing
    b = [int(not check(E[i], T2[i])) for i in ids]
    c = pair_counts(a, b)        # "only_b": clean in hd-2, firing in hd-1
    print(f"{name:<20} {len(ids) - sum(a):>11} {len(ids) - sum(b):>5} "
          f"{c['only_b']:>10} {c['only_a']:>10} {mcnemar(a, b):>9.3f}")
rest = [name for name in CHECKS if name != "claims an action"]
a = [int(not any(CHECKS[k][0](E[i], T1[i]) for k in rest)) for i in ids]
b = [int(not any(CHECKS[k][0](E[i], T2[i]) for k in rest)) for i in ids]
c = pair_counts(a, b)            # the same pair table, without that check
print("without claims an action: only hd-1 clean", c["only_a"],
      " only hd-2 clean", c["only_b"], " p-value", round(mcnemar(a, b), 3))
