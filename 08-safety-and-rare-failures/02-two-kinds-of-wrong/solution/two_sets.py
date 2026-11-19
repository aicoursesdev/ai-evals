"""Lesson 08.2: the help desk's two error rates, side by side.

From this folder: uv run python two_sets.py
"""
from scorecard import data
from scorecard.stats import exact_interval

attacks = [r for r in data.labels("08-attack-outcomes")
           if r["source"] == "red-team" and r["outcome"] != "not_arrived"]
look = data.labels("08-look-alike-outcomes")

def count(rows, outcomes):
    """How many rows have an outcome in the set `outcomes`."""
    return sum(r["outcome"] in outcomes for r in rows)

def show(name, failed, tries):
    low, high = exact_interval(failed, tries)
    print(f"{name:32} {failed:3} of {tries:<3} = {failed / tries:5.1%}"
          f"   95% interval {low:.3f} to {high:.3f}")

loose = count(attacks, {"complied", "partly"})   # what the attacker asked
strict = len(look) - count(look, {"handled"})    # honest, not handled
show("hd-1: attacks through", loose, len(attacks))
show("hd-1: look-alikes mishandled", strict, len(look))
