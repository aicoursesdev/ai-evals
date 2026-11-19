"""Project 09: the gate. Exit code 0 means the change may ship.

Given: the recorded drafts, `scorecard.report.gate` and the lines that
print. You write `RULES` (your ship rule) and `scores`.

From this folder: uv run python gate.py hd-2     (or: gate.py swap)
"""
import sys

from plumbing import clean, drafts, emails, right, swap
from scorecard.report import gate
from scorecard.stats import paired, wilson

# The ship rule: (score name, the minimum its lower end must reach, True).
RULES = [("triage right", 0.80, True), ("no check fires", 0.70, True),
         ("triage change", -0.02, True), ("checks change", -0.02, True)]


def scores(mail, old, new):
    """{name: (low, mid, high)} for the new version and its change, and
    the number of emails both versions answered."""
    ids = sorted(set(old) & set(new) & set(mail))
    found = {}
    for name, change, rate in (("triage right", "triage change", right),
                               ("no check fires", "checks change", clean)):
        a = [rate(mail[i], old[i]) for i in ids]
        b = [rate(mail[i], new[i]) for i in ids]
        low, high = wilson(sum(b), len(b))
        found[name] = (low, sum(b) / len(b), high)
        p = paired(a, b)
        found[change] = (p["low"], p["diff"], p["high"])
    return found, len(ids)


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
