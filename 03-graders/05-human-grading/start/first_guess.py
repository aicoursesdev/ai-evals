"""Lesson 03.5: the first guess at Arjun's calls, and where reading moved it.

The course ships Arjun's calls (labels/03-right-rule-arjun.csv). This file
rebuilds the first guess from the failure map and counts the calls that
reading each draft against the rule changed.

From this folder: uv run python first_guess.py
"""
from collections import Counter

from scorecard import data


def call(types):
    """The first-guess call on one draft, from its failure types."""
    raise NotImplementedError(
        "TODO 03.5: return fail for F-wrong-rule, unsure for F-bluff or "
        "F-no-draft without it, and pass for the rest, see the lesson's "
        "'From the map to Arjun’s calls' section")


def moved_to(rows):
    """Count the calls that reading changed, by the call they moved to.

    Each row has "call" (Arjun's) and "types" (the map's, joined by ;).
    """
    raise NotImplementedError(
        "TODO 03.5: return a Counter of Arjun's call for each row where "
        "it differs from call(types), see the lesson's 'From the map to "
        "Arjun’s calls' section")


if __name__ == "__main__":
    rows = data.labels("03-right-rule-arjun")
    guess = Counter(call(r["types"].split(";")) for r in rows)
    print("first guess:", dict(guess))
    print("Arjun's calls:", dict(Counter(r["call"] for r in rows)))
    print("moved to:", dict(moved_to(rows)))
