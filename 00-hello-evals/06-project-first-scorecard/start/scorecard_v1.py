"""Lesson 00.6, project: a first scorecard for the help desk: triage accuracy
on Kiran's test emails and on week 1, the gap, and the spread in week 1.

From this folder: uv run python scorecard_v1.py
"""

from scorecard import data, run


def triage_score(emails, traces):
    """Run the recorded help desk over the emails; return the rows."""
    raise NotImplementedError(
        "TODO 00.6: map each trace id to its triage category, then return "
        "run.run(emails, system=..., graders={'category': ...}) where the "
        "grader is True when the output equals the email's category, see "
        "the lesson's 'The steps' section, step 2")


def main():
    """Score the test split and week 1, save both, print the scorecard."""
    raise NotImplementedError(
        "TODO 00.6: score the test split (with the launch traces) and week "
        "1 with triage_score, run.save each to kiran-test.jsonl and "
        "week-1.jsonl, print the counts, sizes and percentages, the gap "
        "with its sign, and the right answers in three slices of 50 of "
        "week 1, see the lesson's 'The steps' section, steps 3 to 5")


if __name__ == "__main__":
    main()
