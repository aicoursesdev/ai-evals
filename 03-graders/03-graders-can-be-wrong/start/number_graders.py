"""Lesson 03.3: one answer, three graders, three verdicts.

The expected value begins with the digits the CORE-Bench story gives.

From this folder: uv run python number_graders.py
"""
from scorecard.graders import close_to, contains, exact

EXPECTED = 96.124991
answers = ["96.124991", "96.12", "96.1", "96.20", "not 96.12"]

print(f"{'answer':<12} exact  close_to  contains")
for answer in answers:
    case = {"expected": str(EXPECTED), "tolerance": 0.005}
    strict = exact(answer, case)
    right_size = close_to(answer, {"expected": EXPECTED, "tolerance": 0.005})
    loose = contains(answer, {"expected": "96.12"})
    print(f"{answer:<12} {strict!s:<6} {right_size!s:<9}  {loose}")
