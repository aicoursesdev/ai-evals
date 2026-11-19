"""Lesson 04.5: how wide is the range? Resample by hand, seed 7.

Given: the held-out pairs, the unlabelled verdicts and the lines that print.
You write `rates_of` and `one_repeat`.

From this folder: uv run python resample.py
"""
import random

from plumbing import heldout_pairs, heldout_rates, raw_passes
from scorecard.stats import corrected_interval, corrected_rate


def rates_of(pairs):
    """(pass-keeping rate, catch rate) from [(Arjun passes, judge passes)]."""
    good = [j for h, j in pairs if h]
    bad = [j for h, j in pairs if not h]
    return sum(good) / len(good), 1 - sum(bad) / len(bad)


def one_repeat(pairs, verdicts, rng, vary_labels, vary_sample):
    """One corrected rate from a resampled set of labels and/or drafts."""
    if vary_labels:
        pairs = rng.choices(pairs, k=len(pairs))
    if vary_sample:
        verdicts = rng.choices(verdicts, k=len(verdicts))
    tpr, tnr = rates_of(pairs)
    if tpr + tnr <= 1:
        return None  # the judge no better than a coin: no estimate
    return corrected_rate(sum(verdicts) / len(verdicts), tpr, tnr)


if __name__ == "__main__":
    pairs, verdicts = heldout_pairs(), raw_passes()
    rng = random.Random(7)
    for name, labels, sample in (("only the 250 drafts vary", False, True),
                                 ("only the 85 labels vary", True, False),
                                 ("both vary", True, True)):
        runs = [one_repeat(pairs, verdicts, rng, labels, sample)
                for _ in range(2000)]
        kept = sorted(r for r in runs if r is not None)
        low, high = kept[int(0.025 * len(kept))], kept[int(0.975 * len(kept))]
        print(f"{name:<26} {low:.3f} to {high:.3f}  "
              f"({2000 - len(kept)} skipped)")

    tpr, tnr, m1, m0 = heldout_rates()
    raw, n = sum(verdicts) / len(verdicts), len(verdicts)
    low, high = corrected_interval(raw, n, tpr, tnr, m1, m0)
    print(f"{'closed form (scorecard)':<26} {low:.3f} to {high:.3f}")
