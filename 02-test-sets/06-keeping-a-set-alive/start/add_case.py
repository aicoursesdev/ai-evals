"""Lesson 02.6: the rule for adding a failure found in production.

From this folder: uv run python add_case.py E-0597 "an example, not a finding"
Given: `main` at the foot. A dry run: it prints what the rule decides and writes nothing.
"""
import sys

from leaks import similar
from scorecard import data
from slices import log

PARTS = ("open", "sealed", "synthetic")


def problems(email, found, held):
    """Why this email may not be added yet (an empty list: it may)."""
    raise NotImplementedError(
        "TODO 02.6: return the reasons the email may not be added: "
        "already in a part, a near copy of a case, no note, see the "
        "lesson's 'A rule for adding each new failure' section")


def next_version(version):
    """Adding cases bumps the minor number: 1.0 becomes 1.1."""
    raise NotImplementedError(
        "TODO 02.6: bump the minor number, '1.0' becomes '1.1', see "
        "the lesson's 'A rule for adding each new failure' section")


if __name__ == "__main__":
    wanted, found = sys.argv[1], " ".join(sys.argv[2:])
    email = next(e for e in log() if e["id"] == wanted)
    held = {part: data.testset(part) for part in PARTS}
    bad = problems(email, found, held)
    if bad:
        print(wanted, "refused:", "; ".join(bad))
    else:
        print(wanted, "may be added to the open part (never the sealed part,")
        print("you have read it) as version", next_version("1.0"))
        print("note:", found)
