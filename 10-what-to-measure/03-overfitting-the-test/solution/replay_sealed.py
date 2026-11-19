"""Lesson 10.3: the open part and the sealed part side by side, replayed
from data/runs/10-sealed/. No model call, no sealed trace opened.

From this folder: uv run python replay_sealed.py
"""
import json

from honest_or_spent import verdict
from plumbing import RUNS, judge_pass, measures, open_part

GOOD = ("triage right", "no check fires", "judge: clear PASS (v4)")


def rule(name, open_hits, open_n, low, high):
    """The plan's rule for a measure of good outcomes. The seven checks were
    written by reading the open drafts, so they get a table and no verdict."""
    if name not in GOOD:
        return "table only"
    return verdict(open_hits, open_n, low, high)


if __name__ == "__main__":
    sealed = json.loads((RUNS / "10-sealed" / "scores.json").read_text())
    mail, seen = open_part()
    opened = measures(mail, seen)
    opened["judge: clear PASS (v4)"] = judge_pass(RUNS / "04-dev" / "v4.jsonl")
    print(f"{'measure':27}{'open':>8}{'sealed':>8}   {'sealed range':16}rule")
    for name, (h, n, low, high) in sealed["rates"].items():
        oh, on = opened[name]
        rule_said = rule(name, oh, on, low, high)
        print(f"{name:27}{oh:>5}/{on:<3}{h:>5}/{n:<3}  "
              f"{low:6.1%} to {high:5.1%}  {rule_said}")
