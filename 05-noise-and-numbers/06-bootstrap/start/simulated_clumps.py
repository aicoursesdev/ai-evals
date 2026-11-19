"""Lesson 05.6: a SIMULATION of clumps big enough to matter. 100 customers
write 5 emails each; a customer's emails pass together more than chance.

From this folder: uv run python simulated_clumps.py
"""
import random

from scorecard.stats import bootstrap, clustered_se, standard_error

rng = random.Random(7)          # seeded: your numbers match
customers = []
for _ in range(100):
    chance = rng.choice([0.55, 0.95])   # each customer's own pass chance
    customers.append([int(rng.random() < chance) for _ in range(5)])
flat = [y for c in customers for y in c]
mean = lambda v: sum(v) / len(v)
print(f"{len(flat)} emails, {mean(flat):.1%} pass")
print("standard error as if independent:",
      round(standard_error(mean(flat), 500), 4))
ids = [k for k, c in enumerate(customers) for _ in c]
print("standard error by customer:      ", round(clustered_se(flat, ids), 4))
low, high = bootstrap(flat, mean)
print(f"resample emails:    {low:.1%} to {high:.1%}")
low, high = bootstrap(customers, lambda cs: mean([y for c in cs for y in c]))
print(f"resample customers: {low:.1%} to {high:.1%}")
