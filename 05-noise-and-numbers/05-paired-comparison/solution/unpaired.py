"""Lesson 05.5: hd-1 and hd-2 as two separate scores (the unpaired view).

Given: both versions' outcomes on the 277 emails and the Wilson ranges.
You write `unpaired_range`.

From this folder: uv run python unpaired.py
"""
import math

from plumbing import clean, drafts, emails
from scorecard.stats import wilson


def unpaired_range(a, b):
    """Difference of two pass rates scored as separate sets, with its
    standard error and 95% range."""
    pa, pb = sum(a) / len(a), sum(b) / len(b)
    se = math.sqrt(pa * (1 - pa) / len(a) + pb * (1 - pb) / len(b))
    diff = pb - pa
    return diff, se, diff - 1.96 * se, diff + 1.96 * se


if __name__ == "__main__":
    E, T1, T2 = emails(), drafts("hd-1"), drafts("hd-2")
    ids = sorted(T2)                 # weeks 3 and 4, outside the sealed part
    a = [clean(E[i], T1[i]) for i in ids]
    b = [clean(E[i], T2[i]) for i in ids]
    n = len(ids)
    for name, x in (("hd-1", a), ("hd-2", b)):
        lo, hi = wilson(sum(x), n)
        print(f"{name}: {sum(x)} of {n} drafts with no check firing "
              f"({sum(x) / n:.1%}), range {lo:.1%} to {hi:.1%}")

    diff, se, low, high = unpaired_range(a, b)
    print(f"difference {diff:+.1%}, standard error {se:.3f}, "
          f"range {low:+.1%} to {high:+.1%}")
