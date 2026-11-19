"""Count the failure types in a coded notes file, most common first.

    uv run python count.py coded.csv
"""
import sys
from collections import Counter

from plumbing import print_table, read


def types_of(row):
    """The set of types on one row (empty for a fine trace)."""
    return {t for t in row["types"].split(";") if t}


def count(rows):
    """How many traces carry each type (a trace can carry several)."""
    tally = Counter()
    for row in rows:
        tally.update(types_of(row))
    return tally


if __name__ == "__main__":
    rows = read(sys.argv[1])
    print_table(rows, count(rows))
