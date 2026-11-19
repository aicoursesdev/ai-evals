"""Lesson 05.2: the same, for the checks that read the drafts.

Given: the recorded drafts, and the lines that print the results.
It uses your `seed_scores` from which_run.py.

From this folder: uv run python which_drafts.py
"""
import statistics

from plumbing import clean, drafts, emails, sample_ids, seed_runs
from which_run import seed_scores

if __name__ == "__main__":
    E, T = emails(), drafts("hd-1")
    ids, runs = sample_ids(), seed_runs("draft-seeds")
    done = [s for s in range(1, 6) if all(s in runs.get(i, {}) for i in ids)]
    print("seeds complete for all 100 emails:", done)
    at_zero = sum(clean(E[i], T[i]) for i in ids)
    print("temperature 0 (the recorded trace):", at_zero,
          "of 100 drafts with no check firing")
    scores = seed_scores(lambda i, s: clean(E[i], runs[i][s]), ids, done)
    for s, score in zip(done, scores):
        print(f"seed {s}:", score, "of 100")
    print("typical wobble:", round(statistics.stdev(scores), 1), "points")
