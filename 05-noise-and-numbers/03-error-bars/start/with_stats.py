"""Lesson 05.3: the same ranges from scorecard.stats, and Wilson's.

From this folder: uv run python with_stats.py
"""
from scorecard.stats import interval, wilson

print("                     simple formula        Wilson")
for name, passed, n in [("42 of 50", 42, 50), ("137 of 150", 137, 150),
                        ("486 of 550", 486, 550)]:
    a, b = interval(passed, n), wilson(passed, n)
    print(f"{name:<12} {a[0]:>9.1%} to {a[1]:>6.1%}   "
          f"{b[0]:>6.1%} to {b[1]:>6.1%}")
