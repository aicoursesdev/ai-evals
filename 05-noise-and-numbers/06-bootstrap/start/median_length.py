"""Lesson 05.6: an error bar for a number with no formula.

Given: both versions' draft lengths, and `bootstrap` from scorecard.stats.
You write `median_gap`.

From this folder: uv run python median_length.py
"""
import statistics

from plumbing import drafts
from scorecard.stats import bootstrap


def median_gap(rows):
    """Median words of hd-2's drafts minus median of hd-1's."""
    raise NotImplementedError(
        "TODO 05.6: return the median of hd-2's words minus the median "
        "of hd-1's, see the lesson's 'A number with no formula' section")


if __name__ == "__main__":
    T1, T2 = drafts("hd-1"), drafts("hd-2")
    pairs = [(len(T1[i]["draft"].split()), len(T2[i]["draft"].split()))
             for i in sorted(T2)]          # words in hd-1's and hd-2's draft
    print("median words: hd-1", statistics.median(a for a, _ in pairs),
          " hd-2", statistics.median(b for _, b in pairs))
    print("median gap:", median_gap(pairs))
    low, high = bootstrap(pairs, median_gap)   # each email's pair stays whole
    print(f"bootstrap range for the gap: {low} to {high} words")
