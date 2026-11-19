"""Lesson 02.2: draw a sample of the log, at random or by slice.

Given: the log, the slices an email belongs to and the count of them.
You write `random_sample` and `slice_sample`.
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
    raise NotImplementedError(
        "TODO 02.2: return n emails chosen by chance, "
        "random.Random(seed).sample(pool, n), see the lesson's 'A "
        "random sample' section")


def slice_sample(pool, n, seed, have=(), floor=10):
    """n emails. Each pick is the email whose least-covered slice holds the
    fewest emails so far, counting no slice past `floor`; once every slice
    has `floor`, the rest is random (a seeded shuffle breaks ties)."""
    raise NotImplementedError(
        "TODO 02.2: pick n emails, each time the one whose least- "
        "covered slice holds the fewest so far, see the lesson's 'A "
        "sample by slice' section")
