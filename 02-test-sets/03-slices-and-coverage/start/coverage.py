"""Lesson 02.3: who writes in, and how many of each the open part holds.

From this folder: uv run python coverage.py
"""
from plumbing import print_coverage
from scorecard import data
from slices import log, tally


def coverage(emails, opened):
    """One row per slice: (slice, in the log, share of the log, in the open
    part, how many a fair hundred would hold, whether open has under 5)."""
    raise NotImplementedError(
        "TODO 02.3: return one row per slice, (slice, in the log, "
        "share, in open, if fair, under 5), see the lesson's 'The "
        "coverage table' section")


if __name__ == "__main__":
    print_coverage(coverage(log(), data.testset("open")))
