"""Lesson 02.7: the coverage table of test set v1, as Markdown.

From this folder: uv run python coverage_table.py
Reads emails and the set's parts only. It never opens a trace.
"""
from plumbing import PARTS
from scorecard import data
from slices import log, tally


def table(traffic, parts):
    """Markdown: one row per slice with its count in the log, in each part,
    in open + sealed together (" (under 10)" when fewer than 10) and made
    up. `traffic` and each part in `parts` come from `tally`."""
    raise NotImplementedError(
        "TODO 02.7: return the Markdown coverage table, one row per "
        "slice, see the lesson's 'Steps' section")


if __name__ == "__main__":
    parts = {p: tally(data.testset(p)) for p in PARTS}
    print(table(tally(log()), parts))
