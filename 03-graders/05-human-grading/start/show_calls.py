"""Lesson 03.5: Arjun's "right rule" calls, counted and shown.

From this folder: uv run python show_calls.py
"""
from collections import Counter

import plumbing
from scorecard import data

calls = data.labels("03-right-rule-arjun")
print(dict(Counter(c["call"] for c in calls)))

emails = plumbing.emails_by_id()
notes = {r["id"]: r["note"] for r in data.labels("01-coded")}
verdicts = {c["id"]: c["call"] for c in calls}
for id_ in ("E-0158", "E-0151", "E-0156", "E-0185"):
    print(f"\n{verdicts[id_]}: {id_} {emails[id_]['subject']!r}")
    print("  Arjun's note:", notes[id_])
