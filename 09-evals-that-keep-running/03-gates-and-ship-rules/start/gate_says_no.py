"""Lesson 09.3: the same gate on a change that should not ship.

Given: everything it reads and prints; it uses your `scores` and
`ship_rule` from gate.py.

From this folder: uv run python gate_says_no.py
The change is hd-1 with a smaller model (recorded in data/runs/09-model-swap/,
the subject of lesson 09.8), on 149 emails of the open part of the test set
and the launch set's test split. No sealed email is read.
"""
from gate import scores, ship_rule
from plumbing import drafts, emails
from scorecard import data
from scorecard.report import gate

swap = {r["id"]: r for r in data.run("09-model-swap")["hd-1-qwen3.5-2b"]}
mail = emails() | {e["id"]: e for e in data.emails(launch=True)}
old = drafts("hd-1") | {t["id"]: t for t in data.traces(launch=True)}
found, n = scores(mail, old, swap)
print(f"smaller model against hd-1 on {n} emails")
for name, (low, mid, high) in found.items():
    print(f"{name:15} {mid:+.3f}  range {low:+.3f} to {high:+.3f}")
passed, reasons = gate(found, ship_rule())
print("gate passed:", passed)
for reason in reasons:
    print(" ", reason)
