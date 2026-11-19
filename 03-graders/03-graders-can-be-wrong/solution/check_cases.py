"""Lesson 03.3: run every check on its own known cases.

From this folder: uv run python check_cases.py
"""
from grader_cases import CASES
from scorecard.graders import CHECKS


def run_cases(check, cases):
    """What a check gets wrong on its known cases, and its known gaps.

    A case is (what it is, email, trace, should it fire). Returns
    (wrong, gaps): the (what, want) of each case it gets wrong, and the
    name of each case marked GAP that it still misses.
    """
    wrong = [(what, want) for what, e, t, want in cases
             if check(e, t) != want and not what.startswith("GAP")]
    gaps = [what for what, e, t, want in cases
            if what.startswith("GAP") and check(e, t) != want]
    return wrong, gaps


if __name__ == "__main__":
    for name, cases in CASES.items():
        wrong, gaps = run_cases(CHECKS[name][0], cases)
        total = len(cases) - len(gaps)
        print(f"{name:<20} {total - len(wrong)} of {total} right",
              *(f"WRONG: {w}" for w, _ in wrong),
              *(f"(known gap: {g})" for g in gaps))
