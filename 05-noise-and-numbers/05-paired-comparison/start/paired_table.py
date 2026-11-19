"""Lesson 05.5: the same emails as pairs, and the paired range.

Given: both versions' outcomes on the 277 emails and the lines that print.
You write `count_pairs`, `paired_range` and `mcnemar_p`.

From this folder: uv run python paired_table.py
"""
import math

from plumbing import clean, drafts, emails
from scorecard.stats import paired


def count_pairs(a, b):
    """The four kinds of pair in two 0/1 lists scored on the same cases."""
    raise NotImplementedError(
        "TODO 05.5: return the counts of both, only_a, only_b and "
        "neither, see the lesson's 'Each email is a pair' section")


def paired_range(worse, better, n):
    """The mean change, its standard error and 95% range, from the counts
    of cases that got worse and better out of n."""
    raise NotImplementedError(
        "TODO 05.5: return the mean change, its standard error and 95% "
        "range from the two counts, see the lesson's 'Each email is a "
        "pair' section")


def mcnemar_p(worse, better):
    """Chance of a split at least this lopsided if each changed case were
    a fair coin toss, counting both directions."""
    raise NotImplementedError(
        "TODO 05.5: return twice the chance of the smaller count or "
        "fewer in fair coin tosses, see the lesson's 'McNemar’s test "
        "from two counts' section")


if __name__ == "__main__":
    E, T1, T2 = emails(), drafts("hd-1"), drafts("hd-2")
    ids = sorted(T2)
    a = [clean(E[i], T1[i]) for i in ids]
    b = [clean(E[i], T2[i]) for i in ids]

    c = count_pairs(a, b)
    print("both clean:", c["both"], " only hd-1 clean:", c["only_a"],
          " only hd-2 clean:", c["only_b"], " neither:", c["neither"])

    diff, se, low, high = paired_range(c["only_a"], c["only_b"], len(ids))
    print(f"by hand: {diff:+.1%}, standard error {se:.4f}, "
          f"range {low:+.1%} to {high:+.1%}")

    r = paired(a, b)
    print(f"paired(): {r['diff']:+.1%}, range {r['low']:+.1%} to "
          f"{r['high']:+.1%}")
    print("McNemar exact p-value:",
          round(mcnemar_p(c["only_a"], c["only_b"]), 4))
