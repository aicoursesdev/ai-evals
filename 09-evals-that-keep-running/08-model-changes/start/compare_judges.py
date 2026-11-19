"""Lesson 09.8: the chosen judge prompt under two models, against Arjun.

Given: the two recordings of the 100 held-out drafts and the lines that
print. You write `judge_counts` and `judge_rates`.

From this folder: uv run python compare_judges.py
Reads the recordings; no model is called.
"""
from collections import Counter

from plumbing import RUNS, held_out, verdicts
from scorecard import data
from scorecard.stats import wilson


def judge_counts(human, said, ids):
    """Four counts of a judge against Arjun's calls on ids: tp (judge and
    Arjun passed), fn (Arjun passed, judge did not), tn (neither passed)
    and fp. Only a clear "pass" counts as a pass."""
    raise NotImplementedError(
        "TODO 09.8: count the judge's passes kept, passes lost, fails "
        "held back and fails passed, see the lesson's 'The judge is a "
        "model too' section")


def judge_rates(c):
    """(passes kept, fails held back) as shares, from the four counts."""
    raise NotImplementedError(
        "TODO 09.8: return the share of passes kept and the share of "
        "fails held back, see the lesson's 'The judge is a model too' "
        "section")


if __name__ == "__main__":
    human = {r["id"]: r["call"] for r in data.labels("04-right-rule-arjun")}
    ids = [i for i in held_out() if human[i] != "unsure"]
    for name, folder in (("usual", "04-heldout"),
                         ("smaller", "09-judge-swap")):
        seen = verdicts(RUNS / folder / "judge.jsonl")
        said = Counter(seen[i] for i in held_out())
        c = judge_counts(human, seen, ids)
        kept, held = c["tp"] + c["fn"], c["tn"] + c["fp"]
        keep_rate, hold_rate = judge_rates(c)
        lo, hi = wilson(c["tp"], kept)
        lo2, hi2 = wilson(c["tn"], held)
        print(f"{name}: verdicts {dict(said)}")
        lost = sum(seen[i] == "none" and human[i] == "pass" for i in ids)
        print(f"  no verdict line: {said['none']}, of them on drafts "
              f"Arjun passed: {lost}")
        print(f"  passes kept {c['tp']} of {kept} = {keep_rate:.1%} "
              f"(range {lo:.0%} to {hi:.0%})")
        print(f"  fails held back {c['tn']} of {held} = {hold_rate:.1%} "
              f"(range {lo2:.0%} to {hi2:.0%})")
