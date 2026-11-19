"""Lesson 00.3: a yardstick for the score: always give the same answer.

From this folder: uv run python baseline.py
"""

from collections import Counter

from scorecard import data

cases = [e for e in data.emails(launch=True) if e["split"] == "test"]
counts = Counter(case["category"] for case in cases)
for category, n in counts.most_common(3):
    share = f"{n / len(cases):.0%}"
    print(f"always '{category}': {n} of {len(cases)} right ({share})")
