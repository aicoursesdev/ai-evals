"""Lesson 07.4: pass@k and pass^k from five recorded trials per scenario,
with plain loops and math.comb. A trial passes when the agent said the right
outcome and left the right state.

From this folder: uv run python by_hand.py
"""
from collections import Counter
from math import comb

from trials import hot, passed, scenarios

wins = {sid: 0 for sid in scenarios}
for trial in hot:
    wins[trial["id"]] += passed(trial)
print("scenarios by number of right trials out of 5:")
print(sorted(Counter(wins.values()).items()))

n = 5
for k in (1, 2, 3, 5):
    all_k = sum(comb(c, k) / comb(n, k) for c in wins.values()) / len(wins)
    any_k = sum(1 - comb(n - c, k) / comb(n, k)
                for c in wins.values()) / len(wins)
    print(f"k={k}  pass@{k} {any_k:.3f}   pass^{k} {all_k:.3f}")
