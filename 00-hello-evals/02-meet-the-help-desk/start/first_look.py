"""Lesson 00.2: count what the repo holds: emails, splits and traces.

From this folder: uv run python first_look.py
"""

from collections import Counter

from scorecard import data

launch = data.emails(launch=True)      # a list of dicts, one per email
week1 = data.emails(week=1)
print("launch set:", len(launch), "emails")
print("  splits:", dict(Counter(e["split"] for e in launch)))
print("week 1:", len(week1), "emails")
print("  first:", week1[0]["id"], "last:", week1[-1]["id"])
print("traces for week 1:", len(data.traces("hd-1", week=1)))
