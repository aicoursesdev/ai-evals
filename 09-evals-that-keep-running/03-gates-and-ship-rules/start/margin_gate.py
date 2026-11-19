"""Lesson 09.3: a margin taken from the spread of repeats.

Given: the recorded reruns and the lines that print. You write `margin`
and `margin_fails`.

From this folder: uv run python margin_gate.py
"""
from statistics import stdev

from plumbing import repeats
from scorecard.stats import paired


def margin(scores):
    """Two standard deviations of the reruns' scores, in emails."""
    raise NotImplementedError(
        "TODO 09.3: return two standard deviations of the scores, see the "
        "lesson's 'A margin from the repeats' section")


def margin_fails(baseline, scores):
    """How many reruns score below the baseline less the margin."""
    raise NotImplementedError(
        "TODO 09.3: return how many reruns fall below the baseline less "
        "the margin, see the lesson's 'A margin from the repeats' section")


if __name__ == "__main__":
    (base_triage, base_clean), triage_runs, check_runs = repeats()
    for name, base, runs in (("triage right", base_triage, triage_runs),
                             ("no check fires", base_clean, check_runs)):
        scores = [sum(r) for r in runs]
        fails = margin_fails(sum(base), scores)
        print(f"{name}: spread (std dev) {stdev(scores):.1f} emails of 100, "
              f"margin {margin(scores):.1f}; gate fails {fails} of "
              f"{len(runs)}")
        mean = sum(scores) / len(scores)
        print(f"  mean of the reruns {mean:.1f} against baseline "
              f"{sum(base)}")

    # Can 100 emails prove "no more than 2 points worse"? Ask the paired
    # range of each unchanged check rerun against the baseline.
    lows = [paired(base_clean, r)["low"] for r in check_runs]
    print(f"paired low ends, 5 unchanged check reruns: {min(lows):+.3f} to "
          f"{max(lows):+.3f}")
