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
    out = []
    for part, rows in held.items():
        if email["id"] in {r["id"] for r in rows}:
            out.append(f"already in {part}")
        near = [r["id"] for r in rows if similar(email, r, n=1) >= 0.5]
        if near and email["id"] not in near:
            out.append(f"near copy of {near} in {part}")
    if not found.strip():
        out.append("no note on where it was found and what went wrong")
    return out


def next_version(version):
    """Adding cases bumps the minor number: 1.0 becomes 1.1."""
    major, minor = version.split(".")
    return f"{major}.{int(minor) + 1}"


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
