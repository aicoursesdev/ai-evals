"""Project 09: the gate. Exit code 0 means the change may ship.

Given: the recorded drafts, `scorecard.report.gate` and the lines that
print. You write `RULES` (your ship rule) and `scores`.

From this folder: uv run python gate.py hd-2     (or: gate.py swap)
"""
import sys

from plumbing import clean, drafts, emails, right, swap
from scorecard.report import gate
from scorecard.stats import paired, wilson

# TODO 09.9: write your ship rule here as a list of rules, each
# (score name, the minimum its lower end must reach, True), see the lesson's
# 'Step 1: write the ship rule and run the gate' section. The scores are
# "triage right", "no check fires", "triage change" and "checks change".
RULES = []


def scores(mail, old, new):
    """{name: (low, mid, high)} for the new version and its change, and
    the number of emails both versions answered."""
    raise NotImplementedError(
        "TODO 09.9: build the four scores with wilson and paired, see the "
        "lesson's 'Step 1: write the ship rule and run the gate' section")


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "hd-2"
    args = swap() if which == "swap" else (
        emails(), drafts("hd-1"), drafts(which))
    found, n = scores(*args)
    print(f"{which} against hd-1 on {n} emails")
    for name, (low, mid, high) in found.items():
        print(f"{name:15} {mid:+.3f}  range {low:+.3f} to {high:+.3f}")
    passed, reasons = gate(found, RULES)
    print("gate passed:", passed)
    for reason in reasons:
        print(" ", reason)
    sys.exit(0 if passed else 1)
