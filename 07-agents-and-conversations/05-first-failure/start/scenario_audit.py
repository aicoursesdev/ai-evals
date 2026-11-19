"""Lesson 07.5: is any task unwinnable or any expected answer wrong? Count
the right trials per scenario (six trials each) and list the weakest.

From this folder: uv run python scenario_audit.py
"""
from collections import defaultdict

from scorecard import agents
from trials import load, scenarios

right = defaultdict(int)
for t in load():
    s = scenarios[t["id"]]
    raise NotImplementedError(
        "TODO 07.5: add 1 to right[t['id']] when the trial passes both "
        "agents.outcome_correct(t, s) and agents.state_correct(t, s), see "
        "the lesson's 'Is it the agent, the task or the grader?' section")

print("scenarios with 0 or 1 right trial out of 6:")
for sid, n in sorted(right.items(), key=lambda x: x[1]):
    if n <= 1:
        s = scenarios[sid]
        print(f"  {sid} {n}/6 expected {s['expected']:18} "
              f"{s['message'][:48]!r}")
