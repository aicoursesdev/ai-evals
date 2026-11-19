"""Lesson 00.3: look at what the score hides: the emails it got wrong.

From this folder: uv run python misses.py
"""

from scorecard import data

cases = [e for e in data.emails(launch=True) if e["split"] == "test"]
recorded = {t["id"]: t for t in data.traces("hd-1", launch=True)}

for case in cases:
    said = recorded[case["id"]]["triage"]["category"]
    if said != case["category"]:
        print(case["id"],
              f"Arjun: {case['category']:<16} help desk: {said:<16}",
              case["subject"])
