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
    pairs = list(zip(a, b))
    return {"both": pairs.count((1, 1)), "only_a": pairs.count((1, 0)),
            "only_b": pairs.count((0, 1)), "neither": pairs.count((0, 0))}


def paired_range(worse, better, n):
    """The mean change, its standard error and 95% range, from the counts
    of cases that got worse and better out of n."""
    diff = (better - worse) / n
    spread = (better + worse) / n - diff**2     # how much the +-1 vary
    se = math.sqrt(spread / (n - 1))
    return diff, se, diff - 1.96 * se, diff + 1.96 * se


def mcnemar_p(worse, better):
    """Chance of a split at least this lopsided if each changed case were
    a fair coin toss, counting both directions."""
    changed = worse + better
    if changed == 0:
        return 1.0
    few = sum(math.comb(changed, k) for k in range(min(worse, better) + 1))
    return min(1.0, 2 * few / 2**changed)


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
