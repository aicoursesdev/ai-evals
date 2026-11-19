"""Lesson 05.4: how many cases a given width needs.

Given: the table of margins and pass rates, built on scorecard.stats.
You write `cases_needed`.

From this folder: uv run python how_many.py
"""
import math

from scorecard.stats import sample_size


def cases_needed(margin, p):
    """Cases for a 95% range of plus or minus margin, rounded up."""
    raise NotImplementedError(
        "TODO 05.4: return 1.96 squared times p * (1 - p) over the "
        "margin squared, rounded up, see the lesson's 'The formula' "
        "section")


if __name__ == "__main__":
    # plus or minus 5 points, worst case
    by_hand = cases_needed(0.05, 0.5)
    print("by hand:", by_hand, " sample_size:", sample_size(0.05, 0.5))

    print("margin   p = 0.5   p = 0.9   p = 0.95")
    for margin in (0.10, 0.05, 0.025, 0.02, 0.01):
        row = [sample_size(margin, p) for p in (0.5, 0.9, 0.95)]
        print(f"+-{margin:>5.1%} {row[0]:>8} {row[1]:>9} {row[2]:>10}")
