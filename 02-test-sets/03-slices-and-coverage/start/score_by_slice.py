"""Lesson 02.3: the triage score for each slice of the log.

From this folder: uv run python score_by_slice.py
"""
from held_back import usable_emails, usable_triage
from plumbing import print_scores
from slices import slices_of


def score_by_slice(emails, said):
    """{slice: [right, total]}: right means the category matches Arjun's."""
    raise NotImplementedError(
        "TODO 02.3: return {slice: [right, total]} over all the "
        "slices of each email, see the lesson's 'A score per slice' "
        "section")


if __name__ == "__main__":
    emails, said = usable_emails(), usable_triage()
    print_scores(score_by_slice(emails, said), said, emails)
