"""Lesson 08.2: two systems that need no model, as controls.

From this folder: uv run python controls.py
"""
from scorecard import data
from scorecard.stats import exact_interval

attacks = [r for r in data.labels("08-attack-outcomes")
           if r["source"] == "red-team" and r["outcome"] != "not_arrived"]
look = data.labels("08-look-alike-outcomes")


def line(name, failed, tries):
    low, high = exact_interval(failed, tries)
    print(f"{name:36} {failed:3} of {tries:<3} = {failed / tries:6.1%}"
          f"   95% interval {low:.3f} to {high:.3f}")


# Refuse everything: no attack gets through, no honest email is helped.
line("always-refuse: attacks through", 0, len(attacks))
line("always-refuse: look-alikes failed", len(look), len(look))
# Do whatever the email says: every attack works, no honest email fails.
line("always-comply: attacks through", len(attacks), len(attacks))
line("always-comply: look-alikes failed", 0, len(look))
