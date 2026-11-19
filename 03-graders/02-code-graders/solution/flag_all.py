"""Lesson 03.2: all seven code checks on the 550 logged traces.

From this folder: uv run python flag_all.py
"""
from collections import Counter

import plumbing
from scorecard.graders import CHECKS

emails, traces = plumbing.emails_by_id(), plumbing.traces_by_id()

print(f"{'check':<21} wk1  wk2  wk3  wk4  total")
for name, (check, types) in CHECKS.items():
    by_week = Counter(emails[i]["week"] for i in emails
                      if check(emails[i], traces[i]))
    cells = "  ".join(f"{by_week[w]:>3}" for w in plumbing.WEEKS)
    print(f"{name:<21} {cells}  {sum(by_week.values()):>5}")
