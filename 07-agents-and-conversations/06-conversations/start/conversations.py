"""Lesson 07.6: the recorded conversations, ready to use (already written
for you).

`convs` is the list of the eight conversations in
runs/07-conversations/conversations.jsonl, and `scenarios` maps a scenario
id such as "RF-10" to its record in scenarios/refunds.jsonl.
"""
from scorecard import data

FILE = data.DATA / "runs" / "07-conversations" / "conversations.jsonl"
convs = data.read_jsonl(FILE)
scenarios = {s["id"]: s for s in data.scenarios()}
