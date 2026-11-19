"""When did each failure type first appear, in the order you read?

    uv run python saturation.py coded.csv
"""
import sys

from plumbing import print_first_seen, read


def first_seen(rows):
    """{type: position (1 to 100) of the first trace that carried it}."""
    raise NotImplementedError(
        "TODO 01.5: return a dict from each type to the position (counting "
        "from 1) of the first row that carries it, see the lesson's "
        "'When to stop reading' section")


if __name__ == "__main__":
    rows = read(sys.argv[1])
    print_first_seen(first_seen(rows), len(rows))
