"""Count the failure types in a coded notes file, most common first.

    uv run python count.py coded.csv
"""
import sys
from collections import Counter

from plumbing import print_table, read


def types_of(row):
    """The set of types on one row (empty for a fine trace)."""
    raise NotImplementedError(
        "TODO 01.5: return the set of types in row['types'], which are "
        "separated by semicolons, with no empty one, see the lesson's "
        "'Count the traces per type' section")


def count(rows):
    """How many traces carry each type (a trace can carry several)."""
    raise NotImplementedError(
        "TODO 01.5: return a Counter that adds 1 for each type each row "
        "carries (use types_of), see the lesson's 'Count the traces per "
        "type' section")


if __name__ == "__main__":
    rows = read(sys.argv[1])
    print_table(rows, count(rows))
