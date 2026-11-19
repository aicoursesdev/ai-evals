"""Lesson 02.4: lay out the grid of dimensions and write the made-up cases.

From this folder: uv run python build_synthetic.py
"""
from collections import Counter
from itertools import product

from cases import CASES
from plumbing import (ASKS, LANGUAGES, TWISTS, check_in_empty_cells,
                      print_summary, record, write_cases)
from scorecard import data
from slices import log


def real_twist(email):
    """The twist an email's own labels can show (the log has no more)."""
    raise NotImplementedError(
        "TODO 02.4: return 'attack', 'long' (400 characters or more) "
        "or 'plain' from the email's own labels, see the lesson's "
        "'Name what varies' section")


def empty_cells(emails):
    """(the cells the log's labels can fill, the ones with no real email)."""
    raise NotImplementedError(
        "TODO 02.4: return the cells the log's labels can fill and "
        "those with no real email, see the lesson's 'Name what "
        "varies' section")


if __name__ == "__main__":
    shown, empty = empty_cells(log())
    print(f"{len(shown)} cells the log's labels can fill; empty: {len(empty)}")
    rows = [record(i, row) for i, row in enumerate(CASES, start=1)]
    check_in_empty_cells(rows, empty)
    write_cases(rows, data.DATA / "testsets" / "v1" / "synthetic.jsonl")
    print_summary(rows)
