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
    return [("triage right", 0.80, True), ("no check fires", 0.70, True),
            ("triage change", -0.02, True), ("checks change", -0.02, True)]


def scores(mail, old, new):
    """{name: (low, mid, high)} for the new version and its change, and
    the number of emails both versions answered."""
    ids = sorted(set(old) & set(new) & set(mail))
    found = {}
    for name, change, rate in (("triage right", "triage change",
                                category_right),
                               ("no check fires", "checks change", clean)):
        a = [rate(mail[i], old[i]) for i in ids]
        b = [rate(mail[i], new[i]) for i in ids]
        low, high = wilson(sum(b), len(b))
        found[name] = (low, sum(b) / len(b), high)
        p = paired(a, b)
        found[change] = (p["low"], p["diff"], p["high"])
    return found, len(ids)


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
