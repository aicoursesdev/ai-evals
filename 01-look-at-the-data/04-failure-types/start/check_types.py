"""Check a coded notes file against the failure types you defined.

    uv run python check_types.py coded.csv failure-types.md

Every type used in the `types` column must be defined, every defined type
should be used, and every failed trace needs at least one type.
"""
import sys

from plumbing import coded_rows, defined_types, print_report


def problems(rows, defined):
    """Every way the rows and the definitions disagree, one line each."""
    raise NotImplementedError(
        "TODO 01.4: return a list of problem lines: a failed row with no "
        "type, a fine row with types, a type used but not in defined, and "
        "a defined type never used, see the lesson's 'Code every note' "
        "section")


if __name__ == "__main__":
    rows = coded_rows(sys.argv[1])
    bad = problems(rows, defined_types(sys.argv[2]))
    print_report(rows, bad)
    sys.exit(1 if bad else 0)
