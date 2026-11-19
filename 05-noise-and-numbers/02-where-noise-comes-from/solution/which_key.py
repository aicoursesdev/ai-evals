"""Lesson 05.2: what a wrong answer key does to a score (a simulation).

Given: the log, and the loop over the four shares of wrong keys.
You write `score_with_wrong_keys`.

From this folder: uv run python which_key.py
"""
import random

from plumbing import drafts, emails


def score_with_wrong_keys(E, T, ids, cats, wrong, rng):
    """The category score when a share `wrong` of the keys are wrong."""
    flipped = set(rng.sample(ids, round(wrong * len(ids))))
    right = 0
    for i in ids:
        key = E[i]["category"]
        if i in flipped:    # the key holds some other category
            key = rng.choice([c for c in cats if c != key])
        right += T[i]["triage"]["category"] == key
    return right / len(ids)


if __name__ == "__main__":
    E, T = emails(), drafts("hd-1")
    ids = sorted(E)
    cats = sorted({e["category"] for e in E.values()})
    rng = random.Random(7)      # seeded: your numbers match

    print("wrong keys  score")
    for wrong in (0, 0.02, 0.05, 0.10):
        score = score_with_wrong_keys(E, T, ids, cats, wrong, rng)
        print(f"{wrong:>9.0%}  {score:.1%}")
