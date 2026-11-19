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
    if email["attack"]:
        return "attack"
    return "long" if len(email["body"]) >= 400 else "plain"


def empty_cells(emails):
    """(the cells the log's labels can fill, the ones with no real email)."""
    seen = Counter((e["language"], e["category"], real_twist(e))
                   for e in emails)
    shown = [c for c in product(LANGUAGES, ASKS, TWISTS[:3])]
    empty = [c for c in shown if not seen[c]]
    return shown, empty


if __name__ == "__main__":
    shown, empty = empty_cells(log())
    print(f"{len(shown)} cells the log's labels can fill; empty: {len(empty)}")
    rows = [record(i, row) for i, row in enumerate(CASES, start=1)]
    check_in_empty_cells(rows, empty)
    write_cases(rows, data.DATA / "testsets" / "v1" / "synthetic.jsonl")
    print_summary(rows)
