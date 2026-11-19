"""Lesson 03.6: the judge's verdicts beside Arjun's, a first look only.

From this folder: uv run python compare_with_arjun.py
"""
from collections import Counter

from judge_rule import judged
from scorecard import data


def tally(calls, verdicts):
    """Count each (call, verdict) pair, over the ids in calls."""
    raise NotImplementedError(
        "TODO 03.6: return a Counter of (call, verdict) for each id in "
        "calls, see the lesson's 'A first look, not a measurement' "
        "section")


def clear_cases(calls, verdicts):
    """Ids where Arjun and the judge both gave pass or fail."""
    raise NotImplementedError(
        "TODO 03.6: return the ids where the call is not unsure and the "
        "verdict is pass or fail, see the lesson's 'A first look, not a "
        "measurement' section")


if __name__ == "__main__":
    arjun = {c["id"]: c["call"] for c in data.labels("03-right-rule-arjun")}
    judge = judged()
    table = tally(arjun, judge)

    print(f"{'Arjun says':<11} judge pass  fail  unsure  no line")
    for call in ("pass", "fail", "unsure"):
        cells = [table[call, v] for v in ("pass", "fail", "unsure", "none")]
        print(f"{call:<11} {cells[0]:>10} {cells[1]:>5} {cells[2]:>7} "
              f"{cells[3]:>8}")

    both = clear_cases(arjun, judge)
    agree = sum(arjun[i] == judge[i] for i in both)
    print(f"both gave pass or fail on {len(both)}; they agree on {agree}")
    always = sum(arjun[i] == "pass" for i in both)
    print(f"a marker that always said pass would agree on {always} of them")
