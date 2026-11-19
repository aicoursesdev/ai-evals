"""When did each failure type first appear, in the order you read?

    uv run python saturation.py coded.csv
"""
import sys

from plumbing import print_first_seen, read


def first_seen(rows):
    """{type: position (1 to 100) of the first trace that carried it}."""
    seen = {}
    for position, row in enumerate(rows, start=1):
        for t in row["types"].split(";"):
            if t and t not in seen:
                seen[t] = position
    return seen


if __name__ == "__main__":
    rows = read(sys.argv[1])
    print_first_seen(first_seen(rows), len(rows))
