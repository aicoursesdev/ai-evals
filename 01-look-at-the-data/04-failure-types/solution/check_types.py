"""Check a coded notes file against the failure types you defined.

    uv run python check_types.py coded.csv failure-types.md

Every type used in the `types` column must be defined, every defined type
should be used, and every failed trace needs at least one type.
"""
import sys

from plumbing import coded_rows, defined_types, print_report


def problems(rows, defined):
    """Every way the rows and the definitions disagree, one line each."""
    found = []
    used = set()
    for row in rows:
        types = {t for t in row["types"].split(";") if t}
        used |= types
        if row["ok"] == "no" and not types:
            found.append(f"{row['id']}: failed but has no type")
        if row["ok"] == "yes" and types:
            found.append(f"{row['id']}: fine but has types {sorted(types)}")
        found += [f"{row['id']}: {t} is not defined" for t in types - defined]
    found += [f"{t} is defined but never used" for t in defined - used]
    return found


if __name__ == "__main__":
    rows = coded_rows(sys.argv[1])
    bad = problems(rows, defined_types(sys.argv[2]))
    print_report(rows, bad)
    sys.exit(1 if bad else 0)
