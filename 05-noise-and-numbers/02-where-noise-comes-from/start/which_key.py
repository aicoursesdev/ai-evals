"""Lesson 05.2: what a wrong answer key does to a score (a simulation).

Given: the log, and the loop over the four shares of wrong keys.
You write `score_with_wrong_keys`.

From this folder: uv run python which_key.py
"""
import random

from plumbing import drafts, emails


def score_with_wrong_keys(E, T, ids, cats, wrong, rng):
    """The category score when a share `wrong` of the keys are wrong."""
    raise NotImplementedError(
        "TODO 05.2: return the category score when a share of the keys "
        "are wrong, see the lesson's 'The machine, and mistakes in the "
        "answer key' section")


if __name__ == "__main__":
    E, T = emails(), drafts("hd-1")
    ids = sorted(E)
    cats = sorted({e["category"] for e in E.values()})
    rng = random.Random(7)      # seeded: your numbers match

    print("wrong keys  score")
    for wrong in (0, 0.02, 0.05, 0.10):
        score = score_with_wrong_keys(E, T, ids, cats, wrong, rng)
        print(f"{wrong:>9.0%}  {score:.1%}")
