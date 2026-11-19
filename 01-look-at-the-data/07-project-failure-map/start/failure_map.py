"""Build the failure map: types ranked, with counts, examples and decisions.

    uv run python failure_map.py coded.csv failure-types.md > failure-map.md
"""
import sys

from count import count, read
from plumbing import definitions

# What each type needs (lesson 01.6): fix, check or judge, in your words.
# Write one line for each of your types, like
#   "F-overreach": "fix: no promises in the prompt; check: phrase list",
DECISION = {}


def map_lines(rows, defs, decision):
    """The failure map as lines of Markdown: a heading and a ranked table."""
    raise NotImplementedError(
        "TODO 01.7: return the map as a list of Markdown lines: the "
        "heading with the counts, a blank line, the table header, then one "
        "row per type, most traces first, see the lesson's 'The steps' "
        "section")


if __name__ == "__main__":
    rows = read(sys.argv[1])
    print("\n".join(map_lines(rows, definitions(sys.argv[2]), DECISION)))
