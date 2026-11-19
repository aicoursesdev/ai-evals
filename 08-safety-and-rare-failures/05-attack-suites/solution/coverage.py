"""Lesson 08.5: coverage: which doors and harms did the attacks try?

From this folder: uv run python coverage.py
"""
from collections import Counter

from scorecard import data

DOORS = ["email_body", "chat", "help_centre_page", "tool_result"]
HARMS = ["money", "personal_data", "account", "internal_info", "false_policy"]
rows = [r for r in data.labels("08-attack-outcomes")
        if r["source"] == "red-team" and r["outcome"] != "not_arrived"]

def grid(rows):
    """How many attacks tried each (door, harm) pair: a Counter."""
    return Counter((r["door"], r["harm"]) for r in rows)

cells = grid(rows)
print(f"{'door':17}" + "".join(f"{h:>14}" for h in HARMS))
for door in DOORS:
    print(f"{door:17}" + "".join(f"{cells[door,h] or '.':>14}" for h in HARMS))
