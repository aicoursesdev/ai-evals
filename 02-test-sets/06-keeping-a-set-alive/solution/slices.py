"""Lesson 02.2: draw a sample of the log, at random or by slice.

Given in lesson 02.6: the log, the slices an email belongs to, and the
two samplers you wrote in 02.2.
"""
import random
from collections import Counter

from scorecard import data


def log():
    """All 600 logged emails, weeks 1 to 4, as one list."""
    return [e for week in (1, 2, 3, 4) for e in data.emails(week=week)]


def slices_of(email):
    """The slices an email sits in: category, language, week, and the odd
    ones: an attack, or a body of 400 characters or more."""
    out = [("category", email["category"]), ("language", email["language"]),
           ("week", email["week"])]
    if email["attack"]:
        out.append(("attack", True))
    if len(email["body"]) >= 400:
        out.append(("long", True))
    return out


def tally(emails):
    """How many emails sit in each slice: {(field, value): count}."""
    return Counter(s for e in emails for s in slices_of(e))


def random_sample(pool, n, seed):
    """n emails chosen by chance, every email equally likely."""
    return random.Random(seed).sample(pool, n)


def slice_sample(pool, n, seed, have=(), floor=10):
    """n emails. Each pick is the email whose least-covered slice holds the
    fewest emails so far, counting no slice past `floor`; once every slice
    has `floor`, the rest is random (a seeded shuffle breaks ties)."""
    rng = random.Random(seed)
    left = list(pool)
    rng.shuffle(left)
    seen = tally(have)

    def need(e):
        return sorted(min(seen[s], floor) for s in slices_of(e))

    picked = []
    for _ in range(n):
        best = min(left, key=need)
        left.remove(best)
        picked.append(best)
        seen.update(slices_of(best))
    return picked
