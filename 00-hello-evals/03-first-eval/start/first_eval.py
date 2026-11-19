"""Lesson 00.3: the smallest eval: cases, a grader and a score.

From this folder: uv run python first_eval.py
"""

from scorecard import data

cases = [e for e in data.emails(launch=True) if e["split"] == "test"]
recorded = {t["id"]: t for t in data.traces("hd-1", launch=True)}


def system(case):
    """What the help desk said the category was (from the recording)."""
    raise NotImplementedError(
        "TODO 00.3: return the category the help desk recorded for this "
        "case: recorded[case['id']]['triage']['category'], see the "
        "lesson's 'Cases, a grader and a score' section")


def grader(output, case):
    """Right or wrong: does it match Arjun's label?"""
    raise NotImplementedError(
        "TODO 00.3: return True when output equals Arjun's label, "
        "case['category'], see the lesson's 'Cases, a grader and a "
        "score' section")


results = [grader(system(case), case) for case in cases]

print(sum(results), "of", len(results), "right")
print(f"accuracy {sum(results) / len(results):.1%}")
