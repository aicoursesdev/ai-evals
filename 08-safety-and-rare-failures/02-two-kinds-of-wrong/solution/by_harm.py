"""Lesson 08.2: one rate or many: each harm gets its own count.

From this folder: uv run python by_harm.py
"""
from scorecard import data

attacks = [r for r in data.labels("08-attack-outcomes")
           if r["source"] == "red-team" and r["outcome"] != "not_arrived"]

def count_by_harm(rows):
    """{harm: (attacks that got through, attacks tried)}."""
    counts = {}
    for r in rows:
        k, n = counts.get(r["harm"], (0, 0))
        got_through = r["outcome"] in ("complied", "partly")
        counts[r["harm"]] = (k + got_through, n + 1)
    return counts

for harm, (failed, tries) in count_by_harm(attacks).items():
    print(f"{harm:14} {failed}/{tries}")
