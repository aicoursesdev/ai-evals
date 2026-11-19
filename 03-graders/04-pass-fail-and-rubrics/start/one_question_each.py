"""Lesson 03.4: the failure map read as eleven yes-or-no questions.

From this folder: uv run python one_question_each.py
"""
from collections import Counter

import plumbing


def yes_counts(coded):
    """How many drafts answer yes to each failure type's question."""
    raise NotImplementedError(
        "TODO 03.4: return a Counter that adds 1 for each failure type "
        "each draft's set holds, see the lesson's 'One question per "
        "check' section")


def yes_per_draft(coded):
    """{number of yes answers: how many drafts gave that many}."""
    raise NotImplementedError(
        "TODO 03.4: return a Counter of how many drafts hold 0, 1, 2 "
        "... failure types, see the lesson's 'One question per check' "
        "section")


if __name__ == "__main__":
    coded = plumbing.coded()
    print("question: does the draft have this failure?")
    for failure, n in yes_counts(coded).most_common():
        print(f"  {failure:<18} yes on {n:>2} of {len(coded)}")
    counts = yes_per_draft(coded)
    print(f"no on all eleven: {counts[0]} of {len(coded)} drafts")
    print("drafts by number of yes answers:", sorted(counts.items()))
