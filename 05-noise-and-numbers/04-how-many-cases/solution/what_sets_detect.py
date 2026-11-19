"""Lesson 05.4: what the course's own sets can and cannot see.

From this folder: uv run python what_sets_detect.py
"""
import math

p = 0.88                                    # the log's rate, about
print("cases  range for one score   two separate sets must differ by")
for n in (20, 50, 100, 277, 550):
    half = 1.96 * math.sqrt(p * (1 - p) / n)
    gap = 1.96 * math.sqrt(2 * p * (1 - p) / n)
    print(f"{n:>5}  +-{half:>5.1%}             about {gap:>5.1%}")
