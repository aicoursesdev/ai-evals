"""Lesson 03.9: run the suite: its own cases, then its numbers.

From this folder: uv run python run_suite.py
"""
import plumbing
from judge_rule import judged, read_verdict
from scorecard import data
from scorecard.graders import CHECKS
from suite import TYPES, checks_for, marker
from suite_cases import CASES, JUDGE_REPLIES

emails, traces = plumbing.emails_by_id(), plumbing.traces_by_id()
coded = plumbing.coded()


def own_cases(check, cases):
    """(right, total) of a check on its known cases, leaving out GAP ones."""
    raise NotImplementedError(
        "TODO 03.9: return (right, total) for a check on its known "
        "cases, leaving out the cases whose name starts with GAP, see "
        "the lesson's 'Steps' section")


def report_checks():
    print("1. each check on its own known cases")
    for name, (check, _) in CHECKS.items():
        right, total = own_cases(check, CASES[name])
        print(f"   {name:<20} {right} of {total} right")
    right = sum(read_verdict(r) == want for r, want in JUDGE_REPLIES)
    print(f"   {'verdict reader':<20} {right} of {len(JUDGE_REPLIES)} right")


def report_types():
    print("\n2. each failure type: how many the map has, how many its "
          "checks flag")
    for failure in TYPES:
        names = checks_for(failure)
        flagged = {i for i in coded
                   if any(CHECKS[n][0](emails[i], traces[i]) for n in names)}
        real = {i for i, types in coded.items() if failure in types}
        caught = f"{len(flagged & real):>2} caught" if names else "        "
        print(f"   {failure:<18} {len(real):>2} in the map  {caught}  "
              f"{marker(failure)}")


def report_judge():
    arjun = {c["id"]: c["call"] for c in data.labels("03-right-rule-arjun")}
    judge = judged()
    both = [i for i in arjun if "unsure" not in (arjun[i], judge[i])
            and judge[i] != "none"]
    agree = sum(arjun[i] == judge[i] for i in both)
    print("\n3. right-rule judge against Arjun (replayed from the recording)")
    print(f"   both gave pass or fail on {len(both)} drafts; agree on {agree}")
    print("   replies with no verdict line:",
          sum(v == "none" for v in judge.values()))


if __name__ == "__main__":
    report_checks()
    report_types()
    report_judge()
