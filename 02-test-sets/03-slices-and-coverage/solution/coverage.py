"""Lesson 02.3: who writes in, and how many of each the open part holds.

From this folder: uv run python coverage.py
"""
from plumbing import print_coverage
from scorecard import data
from slices import log, tally


def coverage(emails, opened):
    """One row per slice: (slice, in the log, share of the log, in the open
    part, how many a fair hundred would hold, whether open has under 5)."""
    traffic, held = tally(emails), tally(opened)
    rows = []
    for one, n in sorted(traffic.items(), key=lambda kv: str(kv[0])):
        fair = len(opened) * n / len(emails)  # open's size times the share
        rows.append((one, n, n / len(emails), held[one], fair, held[one] < 5))
    return rows


if __name__ == "__main__":
    print_coverage(coverage(log(), data.testset("open")))
