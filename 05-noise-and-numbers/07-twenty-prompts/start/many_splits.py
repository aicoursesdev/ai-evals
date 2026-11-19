"""Lesson 05.7: how often is the winner luck? 1,000 splits (a SIMULATION
of choosing the small set; the 20 runs are the recorded ones).

Given: the recorded runs, the count of splits and the lines that print.
You write `one_split`; it uses your `score` and `best_seed`.

From this folder: uv run python many_splits.py
"""
import random
import statistics

from plumbing import emails, sample_ids, seed_runs
from scorecard.stats import mcnemar
from twenty_variants import best_seed, score


def one_split(good, ids, rng):
    """Draw 20 emails, pick the best of the 20 seeds on them, and score
    it on the other 80. Returns the winner's score and seed 1's on the
    20, and their outcomes on the 80 (seed 1 stands for "today")."""
    raise NotImplementedError(
        "TODO 05.7: draw 20 emails, find the best seed on them and "
        "score it on the other 80, see the lesson's 'How often is the "
        "winner luck?' section")


if __name__ == "__main__":
    E, runs, ids = emails(), seed_runs("triage-seeds"), sample_ids()
    good = {(i, s): int(all(runs[i][s]["triage"][k] == E[i][k] for k in
                            ("category", "urgency", "needs_human")))
            for i in ids for s in range(1, 21)}
    rng = random.Random(7)          # seeded: your numbers match
    gaps, naive, confirmed, strict = [], 0, 0, 0
    for _ in range(1000):
        top, today, old, new = one_split(good, ids, rng)
        gaps.append(top / 20 - sum(new) / 80)
        looks_better = top > today              # a "win" on 20 emails
        held_up = looks_better and sum(new) > sum(old)
        naive += looks_better
        confirmed += held_up
        strict += held_up and mcnemar(old, new) < 0.05
    print("winner's score on the small set minus on fresh emails, on "
          "average:", f"{statistics.mean(gaps) * 100:.1f} points")
    print("declared better than today on the 20 emails:", naive, "of 1000")
    print("... and also ahead on the 80 fresh emails:  ", confirmed,
          "of 1000")
    print("... and ahead by a margin McNemar accepts:  ", strict, "of 1000")
