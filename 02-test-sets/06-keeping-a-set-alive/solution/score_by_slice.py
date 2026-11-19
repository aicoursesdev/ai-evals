"""Lesson 02.3: the triage score for each slice of the log.

Given in lesson 02.6: the function you wrote in 02.3.
From this folder: uv run python score_by_slice.py
"""
from held_back import usable_emails, usable_triage
from plumbing import print_scores
from slices import slices_of


def score_by_slice(emails, said):
    """{slice: [right, total]}: right means the category matches Arjun's."""
    table = {}
    for email in emails:
        right = said[email["id"]]["category"] == email["category"]
        for one in slices_of(email):
            row = table.setdefault(one, [0, 0])
            row[0] += right
            row[1] += 1
    return table


if __name__ == "__main__":
    emails, said = usable_emails(), usable_triage()
    print_scores(score_by_slice(emails, said), said, emails)
