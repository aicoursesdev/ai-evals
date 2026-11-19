"""Lesson 00.4: same help desk, same recordings: how much does the score
move when only the emails change?

From this folder: uv run python slices.py
"""

import random

from scorecard import data

launch = data.emails(launch=True)
week1 = data.emails(week=1)
rec = {t["id"]: t for t in data.traces("hd-1", launch=True)}
rec |= {t["id"]: t for t in data.traces("hd-1", week=1)}


def right(email):
    return rec[email["id"]]["triage"]["category"] == email["category"]


def score(emails):
    return sum(right(e) for e in emails)


dev = [e for e in launch if e["split"] == "dev"]
test = [e for e in launch if e["split"] == "test"]
print("launch dev :", score(dev), "of 100")
print("launch test:", score(test), "of 50")
for start in (0, 50, 100):                 # three slices of week 1
    print(f"week 1, emails {start + 1}-{start + 50}:",
          score(week1[start:start + 50]), "of 50")

raise NotImplementedError(
    "TODO 00.4: make rng = random.Random(7), then draws = a list of 1000 "
    "scores, each of score(rng.sample(week1, 50)), see the lesson's "
    "'Which emails you pick' section")
print("1000 random draws of 50 from week 1:", min(draws), "to", max(draws),
      "of 50")
