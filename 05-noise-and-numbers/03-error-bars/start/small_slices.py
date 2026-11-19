"""Lesson 05.3: where the simple formula breaks, on the log's languages.

Given: the log, the simple range from scorecard.stats and the table.
You write `wilson_range`.

From this folder: uv run python small_slices.py
"""
import math

from plumbing import category_right, drafts, emails
from scorecard.stats import interval


def wilson_range(passed, n):
    """Wilson's 95% range for passed of n, held between 0 and 1."""
    raise NotImplementedError(
        "TODO 05.3: return Wilson's range from its centre and half- "
        "width, held between 0 and 1, see the lesson's 'Where the "
        "simple formula breaks' section")


if __name__ == "__main__":
    E, T = emails(), drafts("hd-1")
    print("language  emails right   simple formula        Wilson")
    for lang in ("en", "hi-en", "hi", "ta", "ml"):
        ids = [i for i in E if E[i]["language"] == lang]
        right = sum(category_right(E[i], T[i]) for i in ids)
        a, b = interval(right, len(ids)), wilson_range(right, len(ids))
        print(f"{lang:<8} {len(ids):>6} {right:>5}   "
              f"{a[0]:>6.0%} to {a[1]:>4.0%}   {b[0]:>6.0%} to {b[1]:>4.0%}")
