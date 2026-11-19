"""Lesson 08.7: step 8: the numbers for your paragraph.

From this folder: uv run python paragraph.py
"""
from collections import Counter

from counts import distinct_attacks
from scorecard.stats import exact_upper

attacks = distinct_attacks()
doors = Counter(r["door"] for r in attacks)
bad = [r for r in attacks if r["outcome"] != "resisted"]
whole = sum(r["outcome"] == "complied" for r in bad)
k, n = len(bad), len(attacks)
print(f"{n} distinct attacks through {len(doors)} doors:", dict(doors))
print(f"{whole} did what the attacker asked and {k - whole} did part of it.")
print(f"All harms together: {k} of {n}, upper limit {exact_upper(k, n):.3f}.")
print("Not tried: tool results, attackers who adapt, any other attack.")
