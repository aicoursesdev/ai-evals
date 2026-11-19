"""Lesson 05.3: a 95% range for a pass rate, by hand.

Given: the three scores, and the loop that prints a line for each.
You write `standard_error` and `simple_range`.

From this folder: uv run python by_hand.py
"""
import math


def standard_error(p, n):
    """How far a pass rate p from n cases typically lands from the truth."""
    return math.sqrt(p * (1 - p) / n)


def simple_range(passed, n):
    """The 95% range: 1.96 standard errors either side of the pass rate."""
    p = passed / n
    half = 1.96 * standard_error(p, n)
    return p - half, p + half


if __name__ == "__main__":
    for name, passed, n in [("Kiran's test set", 42, 50),
                            ("week 1 of the log", 137, 150),
                            ("the 550 log emails", 486, 550)]:
        p = passed / n
        se = standard_error(p, n)
        low, high = simple_range(passed, n)
        print(f"{name:<19} {passed:>3} of {n:>3}  p = {p:.3f}  "
              f"se = {se:.3f}  range {low:.1%} to {high:.1%}")
