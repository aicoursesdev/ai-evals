"""Lesson 00.2: follow one email through the help desk, as recorded.

From this folder: uv run python one_trace.py
"""

from scorecard import data

email_id = "E-0156"
email = next(e for e in data.emails(week=1) if e["id"] == email_id)
trace = next(t for t in data.traces("hd-1", week=1) if t["id"] == email_id)

print("EMAIL     ", email["subject"], "|", email["body"])
print("ARJUN SAID", email["category"], email["urgency"], email["needs_human"])
print("TRIAGE    ", trace["triage"])
for hit in trace["retrieved"]:
    print("RETRIEVED ", hit["article_id"], hit["score"])
print("DRAFT     ", trace["draft"])
print("CITED     ", trace["citations"])
