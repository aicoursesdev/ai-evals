"""Lesson 00.3: the smallest eval: cases, a grader and a score.

From this folder: uv run python first_eval.py
"""

from scorecard import data

cases = [e for e in data.emails(launch=True) if e["split"] == "test"]
recorded = {t["id"]: t for t in data.traces("hd-1", launch=True)}


def system(case):
    """What the help desk said the category was (from the recording)."""
    return recorded[case["id"]]["triage"]["category"]


def grader(output, case):
    """Right or wrong: does it match Arjun's label?"""
    return output == case["category"]


results = [grader(system(case), case) for case in cases]

print(sum(results), "of", len(results), "right")
print(f"accuracy {sum(results) / len(results):.1%}")
