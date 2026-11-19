"""Lesson 05.7: twenty "variants" of one unchanged prompt, one winner.

Given: the twenty recorded runs, the small set and the lines that print.
You write `score` and `best_seed`.

From this folder: uv run python twenty_variants.py
"""
import random
import statistics

from plumbing import emails, sample_ids, seed_runs


def score(good, seed, subset):
    """How many of the emails in subset this seed got right (good is
    {(email id, seed): 1 or 0})."""
    return sum(good[i, seed] for i in subset)


def best_seed(scores):
    """The seed with the highest score; a tie goes to the lowest seed."""
    return max(scores, key=lambda s: (scores[s], -s))


if __name__ == "__main__":
    E, runs, ids = emails(), seed_runs("triage-seeds"), sample_ids()
    good = {(i, s): int(all(runs[i][s]["triage"][k] == E[i][k] for k in
                            ("category", "urgency", "needs_human")))
            for i in ids for s in range(1, 21)}
    rng = random.Random(7)          # seeded: your numbers match
    small = rng.sample(ids, 20)     # the small test set
    fresh = [i for i in ids if i not in small]
    small_scores = {s: score(good, s, small) for s in range(1, 21)}
    print("on 20 emails:", list(small_scores.values()))
    best = best_seed(small_scores)
    print(f"winner: seed {best}, {small_scores[best]} of 20 "
          f"({small_scores[best] / 20:.0%})")
    on_fresh = [score(good, s, fresh) for s in range(1, 21)]
    print(f"winner on the other 80: {on_fresh[best - 1]} of 80 "
          f"({on_fresh[best - 1] / 80:.0%}); the 20 variants on average "
          f"{statistics.mean(on_fresh):.1f} of 80 "
          f"({statistics.mean(on_fresh) / 80:.0%})")
