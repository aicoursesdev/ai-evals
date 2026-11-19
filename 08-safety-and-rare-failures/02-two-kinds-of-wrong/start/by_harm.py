"""Lesson 08.2: one rate or many: each harm gets its own count.

From this folder: uv run python by_harm.py
"""
from scorecard import data

attacks = [r for r in data.labels("08-attack-outcomes")
           if r["source"] == "red-team" and r["outcome"] != "not_arrived"]

def count_by_harm(rows):
    """{harm: (attacks that got through, attacks tried)}."""
    raise NotImplementedError(
        "TODO 08.2: return {harm: (attacks that got through, attacks "
        "tried)}, counting outcome complied or partly as got through, "
        "see the lesson's 'One rate or many' section")

for harm, (failed, tries) in count_by_harm(attacks).items():
    print(f"{harm:14} {failed}/{tries}")
