"""Lesson 00.3: the same eval, written with your own run.py.

From this folder: uv run python score_launch.py
"""

import run
from scorecard import data

cases = [e for e in data.emails(launch=True) if e["split"] == "test"]
recorded = {t["id"]: t for t in data.traces("hd-1", launch=True)}

rows = run.run(
    cases,
    system=lambda case: recorded[case["id"]]["triage"]["category"],
    graders={"category": lambda output, case: output == case["category"]},
)
run.save(rows, "launch-test.jsonl")
again = run.load("launch-test.jsonl")
print(len(again), "rows saved and read back")
print("first row:", again[0])
print("pass rate:", run.pass_rate(again, "category"))
