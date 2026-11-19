"""Lesson 05.6: the bootstrap on the paired differences, by hand.

Given: the 277 paired differences, and the lines that print the results.
You write `resample_stats`.

From this folder: uv run python bootstrap_by_hand.py
"""
import random

from plumbing import clean, drafts, emails
from scorecard.stats import bootstrap


def resample_stats(values, stat, rng, repeats=10_000):
    """stat of each of `repeats` resamples of values, drawn with
    replacement and as long as values, lowest first."""
    raise NotImplementedError(
        "TODO 05.6: return the sorted stat of each resample drawn with "
        "rng.choices, see the lesson's 'Resample your own results' "
        "section")


if __name__ == "__main__":
    E, T1, T2 = emails(), drafts("hd-1"), drafts("hd-2")
    ids = sorted(T2)
    diffs = [clean(E[i], T2[i]) - clean(E[i], T1[i]) for i in ids]  # +1, 0, -1
    mean = lambda d: sum(d) / len(d)
    print(len(diffs), "pairs; the mean difference is",
          round(mean(diffs), 4))

    rng = random.Random(7)          # seeded: your numbers match
    means = resample_stats(diffs, mean, rng)
    print(f"the 10,000 resampled means run from {means[0]:+.1%} "
          f"to {means[-1]:+.1%}")
    print(f"by hand: 2.5th to 97.5th percentile {means[250]:+.1%} "
          f"to {means[9749]:+.1%}")
    low, high = bootstrap(diffs, mean)
    print(f"bootstrap(): {low:+.1%} to {high:+.1%}")
