"""Lesson 08.5: sample size: how sure can we be about each door?

From this folder: uv run python sample_size.py [all]
"""
import sys

from scorecard import data
from scorecard.stats import exact_upper

DOORS = ["email_body", "chat", "help_centre_page", "tool_result"]
rows = [r for r in data.labels("08-attack-outcomes")
        if r["outcome"] != "not_arrived" and not r["repeat_of"]]
if sys.argv[1:] != ["all"]:             # "all" adds the log's emails
    rows = [r for r in rows if r["source"] == "red-team"]

def door_counts(rows, door):
    """(attacks that got through, attacks tried) on one door."""
    raise NotImplementedError(
        "TODO 08.5: return (attacks whose outcome is not 'resisted', "
        "attacks) among the rows on this door, see the lesson's "
        "'Coverage and sample size are two questions' section")

print("door               tries  failed  upper limit")
for door in DOORS:
    k, n = door_counts(rows, door)
    limit = f"{exact_upper(k, n):.3f}" if n else "never tried"
    print(f"{door:18} {n:5}  {k:6}  {limit}")
