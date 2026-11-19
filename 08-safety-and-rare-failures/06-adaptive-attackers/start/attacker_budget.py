"""Lesson 08.6: a clean fixed suite against an attacker with a budget.

From this folder: uv run python attacker_budget.py
"""
import random

from scorecard.stats import exact_upper

q = 0.02                    # chance that one try gets through

def chance_of_a_break(q, budget):
    """Chance that at least one of `budget` tries gets through."""
    raise NotImplementedError(
        "TODO 08.6: return 1 - (1 - q) ** budget, see the lesson's "
        "'The attacker has a budget' section")

print("limit the clean 100-try suite supports:", round(exact_upper(0, 100), 4))
print("chance a 100-try suite sees nothing:", round((1 - q) ** 100, 3))
rng = random.Random(7)      # seeded: your numbers match mine
print("tries   formula   simulated (10,000 attackers)")
for budget in (1, 10, 50, 100, 300):
    broke = sum(any(rng.random() < q for _ in range(budget))
                for _ in range(10_000))
    print(f"{budget:5}   {chance_of_a_break(q, budget):.3f}     "
          f"{broke / 10_000:.3f}")
