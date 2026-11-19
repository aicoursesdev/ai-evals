"""Lesson 09.3: the gate, run on hd-2 against hd-1. Exit code 0 when the
change may ship, 1 when it may not (so CI can stop on it).

Given: the recorded drafts, `scorecard.report.gate` and the lines that
print. You write `ship_rule` and `scores`.

From this folder: uv run python gate.py
"""
import sys

from plumbing import category_right, clean, drafts, emails
from scorecard.report import gate
from scorecard.stats import paired, wilson


def ship_rule():
    """The ship rule as data: (score name, the minimum its lower end must
    reach, True to compare the lower end)."""
    raise NotImplementedError(
        "TODO 09.3: return the four rules of the ship rule as data, see "
        "the lesson's 'A rule written down' section")


def scores(mail, old, new):
    """{name: (low, mid, high)} for the new version and its change, and
    the number of emails both versions answered."""
    raise NotImplementedError(
        "TODO 09.3: build the four scores with wilson and paired, see the "
        "lesson's 'The gate in code' section")


if __name__ == "__main__":
    found, n = scores(emails(), drafts("hd-1"), drafts("hd-2"))
    print(f"hd-2 against hd-1 on {n} emails")
    for name, (low, mid, high) in found.items():
        print(f"{name:15} {mid:+.3f}  range {low:+.3f} to {high:+.3f}")
    passed, reasons = gate(found, ship_rule())
    print("gate passed:", passed)
    for reason in reasons:
        print(" ", reason)
    sys.exit(0 if passed else 1)
