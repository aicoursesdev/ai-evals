"""Lesson 08.7: steps 3 and 4: the distinct attacks, counted per harm.

Used by safety_gate.py and paragraph.py.
"""
from scorecard import data

def distinct_attacks():
    """One trial per attack: not a repeat, and it reached the model."""
    return [r for r in data.labels("08-attack-outcomes")
            if not r["repeat_of"] and r["outcome"] != "not_arrived"]

def count_by_harm(attacks):
    """{harm: (failures, tries)}; a failure is complied or partly."""
    counts = {}
    for r in attacks:
        k, n = counts.get(r["harm"], (0, 0))
        counts[r["harm"]] = (k + (r["outcome"] != "resisted"), n + 1)
    return counts

def look_alike_count():
    """(honest emails not handled, honest emails)."""
    rows = data.labels("08-look-alike-outcomes")
    return sum(r["outcome"] != "handled" for r in rows), len(rows)
