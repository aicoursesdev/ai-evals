"""Lesson 02.7: the first score on the open part, and only the open part.

From this folder: uv run python first_score.py
A trace line whose id is not in the open part is skipped before it is
parsed, so the sealed part is not touched.
"""
import json

from plumbing import print_first_score, trace_lines
from scorecard import data


def open_categories(lines, opened):
    """{id: the help desk's category} for the open emails only. `lines` are
    raw trace lines and `opened` holds the open ids."""
    said = {}
    for line in lines:
        if line[8:14] in opened:  # every line starts {"id": "E-0152"
            trace = json.loads(line)
            said[trace["id"]] = trace["triage"]["category"]
    return said


if __name__ == "__main__":
    opened = {e["id"]: e for e in data.testset("open")}
    print_first_score(opened, open_categories(trace_lines(), opened))
