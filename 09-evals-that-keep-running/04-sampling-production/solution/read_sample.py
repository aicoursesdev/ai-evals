"""Lesson 09.4: what the reading of the sample found.

From this folder: uv run python read_sample.py
Reads the label file the reading was saved in.
"""
from collections import Counter

from scorecard import data
from scorecard.stats import wilson

rows = data.labels("09-weekly-sample")
for how in ("random", "flagged"):
    calls = Counter(r["call"] for r in rows if r["selected"] == how)
    print(f"{how:8}", dict(calls))
clear = [r["call"] for r in rows
         if r["selected"] == "random" and r["call"] != "unsure"]
low, high = wilson(clear.count("fail"), len(clear))
print(f"random drafts failing: {clear.count('fail')} of {len(clear)}, "
      f"range {low:.0%} to {high:.0%}")
types = Counter(r["types"] for r in rows if r["types"])
print("failure types:", dict(types.most_common()))
known = {line[3:].strip() for line in open(data.DATA / "labels" /
         "01-failure-types.md") if line.startswith("## F-")}
print("not in Module 01's map:", set(types) - known or "none")
