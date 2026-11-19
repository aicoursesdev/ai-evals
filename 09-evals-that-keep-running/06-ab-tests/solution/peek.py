"""Lesson 09.6: SIMULATE an A/B test with no real difference, peeked at daily.

Given: the experiment's settings, `share` and the lines that print.
You write `z_score` and `first_win`.

From this folder: uv run python peek.py
Seed 7, so every reader gets the same numbers. Nothing here is recorded
from the help desk: both arms have the same true rate by construction.
"""
import math
import random
from statistics import NormalDist

from scorecard.stats import bonferroni

DAYS, PER_DAY, RATE, RUNS = 28, 100, 0.5, 10_000   # drafts per arm per day


def z_score(a, b, n):
    """How many standard errors apart two counts out of n each are."""
    pooled = (a + b) / (2 * n)
    se = math.sqrt(pooled * (1 - pooled) * 2 / n)
    return abs(a - b) / n / se


def first_win(rng, bar, looks):
    """The first day in looks where |z| reaches the bar, or None."""
    a = b = 0
    for day in range(1, DAYS + 1):
        a += sum(rng.random() < RATE for _ in range(PER_DAY))
        b += sum(rng.random() < RATE for _ in range(PER_DAY))
        if day in looks and z_score(a, b, day * PER_DAY) >= bar:
            return day
    return None


def share(bar, looks):
    """The first winning day (or None) of RUNS experiments, from seed 7."""
    rng = random.Random(7)
    return [first_win(rng, bar, looks) for _ in range(RUNS)]


if __name__ == "__main__":
    strict = NormalDist().inv_cdf(1 - bonferroni(0.05, DAYS) / 2)
    print(f"{RUNS} simulated experiments, true rate {RATE} in both arms")
    for name, bar, looks in (
            ("look once, on day 28", 1.96, {28}),
            ("look every day", 1.96, set(range(1, DAYS + 1))),
            ("look every 7 days", 1.96, {7, 14, 21, 28}),
            (f"look every day, bar {strict:.2f}", strict, set(range(1, 29)))):
        wins = share(bar, looks)
        hit = [w for w in wins if w]
        print(f"{name:32} false wins {len(hit) / RUNS:6.1%}   "
              f"by day 7: {sum(w <= 7 for w in hit) / RUNS:5.1%}")

    daily = [w for w in share(1.96, set(range(1, 29))) if w]
    print("looking every day, false wins so far:", {
        d: f"{sum(w <= d for w in daily) / RUNS:.1%}"
        for d in (1, 7, 14, 21, 28)})
