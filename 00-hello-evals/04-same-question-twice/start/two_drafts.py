"""Lesson 00.4: one email, two runs: the labels agree, the wording does not.

From this folder: uv run python two_drafts.py
"""

from scorecard import data

runs = data.run("00-ask-twice")
for name in ("temp-0.7-seed-1", "temp-0.7-seed-2"):
    row = next(r for r in runs[name] if r["id"] == "E-0211")
    print(name, row["triage"])
    print("   ", row["draft"][:230].replace("\n", " "), "...\n")
