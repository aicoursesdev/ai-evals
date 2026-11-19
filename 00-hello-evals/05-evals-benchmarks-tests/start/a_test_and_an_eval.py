"""Lesson 00.5: a test guards one behaviour of the code; an eval scores the
product.

From this folder: uv run python a_test_and_an_eval.py
"""

from helpdesk.pipeline import parse_triage
from scorecard import data

# A test: one input, one expected answer, pass or fail. No model involved.
labels, error = parse_triage(
    '{"category": "refund", "urgency": "high", "needs_human": true}')
assert error is None and labels["category"] == "refund"

labels, error = parse_triage("Sure! This looks like a refund request.")
assert error == "reply is not JSON"
print("tests pass: the parser reads good JSON and spots a chatty reply")

# An eval: many real emails, a score, and no promise that it is 100%.
week1 = data.emails(week=1)
raise NotImplementedError(
    "TODO 00.5: build said = {email id: the help desk's triage category} "
    "from data.traces('hd-1', week=1), then right = how many week-1 "
    "emails have said[e['id']] equal to Arjun's e['category'], see the "
    "lesson's 'An eval answers your question' section")
print(f"eval: {right} of {len(week1)} week-1 emails sorted as Arjun did")
