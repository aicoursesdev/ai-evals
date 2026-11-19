"""Lesson 09.5: SIMULATE what a team does with each draft.

Given: the rule's chances, the 100 coded drafts and the file it writes.
You write `simulate`.

From this folder: uv run python make_actions.py
There is no real team in the repo. This writes data/feedback/actions.jsonl
from a rule you can read below, with seed 7, so everyone gets the same file.
"""
import json
import random

from plumbing import ACTIONS, coded

# chance a draft is sent unchanged, then the rest is split edited : rewritten
SENT_FINE = 0.85                    # a fine draft is mostly sent as it is
SENT_BAD = {1: 0.35, 2: 0.55, 3: 0.55, 4: 0.35}   # sale weeks: busy readers
EDITED_SHARE = {True: 0.8, False: 2 / 3}          # of the rest, by fine or not


def simulate(drafts, seed=7):
    """One simulated action per draft in {id: (week, fine)}, as the rows of
    the file, in id order. The same seed gives the same rows."""
    raise NotImplementedError(
        "TODO 09.5: return one simulated action per draft from a seeded "
        "Random, see the lesson's 'A simulated team' section")


if __name__ == "__main__":
    rows = simulate(coded())
    ACTIONS.parent.mkdir(exist_ok=True)
    ACTIONS.write_text("".join(json.dumps(r) + "\n" for r in rows))
    print("wrote", len(rows), "simulated actions to", ACTIONS.name)
