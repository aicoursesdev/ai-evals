"""Lesson 05.2: how far does the score move when the model is asked again?

Given: the recorded repeats, and the lines that print the results.
You write `one_label`, `all_three` and `seed_scores`.

From this folder: uv run python which_run.py
"""
import statistics

from plumbing import emails, sample_ids, seed_runs


def one_label(email, triage):
    """1 when the triage category is the one Arjun labelled, else 0."""
    raise NotImplementedError(
        "TODO 05.2: return 1 when the triage category is Arjun's, else "
        "0, see the lesson's 'What the model said this run' section")


def all_three(email, triage):
    """1 when category, urgency and needs_human are all Arjun's."""
    raise NotImplementedError(
        "TODO 05.2: return 1 when all three labels are Arjun's, see the "
        "lesson's 'What the model said this run' section")


def seed_scores(good, ids, seeds):
    """One score per seed: how many of the emails have good(id, seed) = 1."""
    raise NotImplementedError(
        "TODO 05.2: return one score per seed, see the lesson's 'What "
        "the model said this run' section")


if __name__ == "__main__":
    E = emails()
    ids, runs = sample_ids(), seed_runs("triage-seeds")
    seeds = range(1, 21)
    cat = seed_scores(lambda i, s: one_label(E[i], runs[i][s]["triage"]),
                      ids, seeds)
    three = seed_scores(lambda i, s: all_three(E[i], runs[i][s]["triage"]),
                        ids, seeds)
    print("category right, 20 seeds:", min(cat), "to", max(cat),
          "of 100, spread", round(statistics.stdev(cat), 1))
    print("all three labels right:  ", min(three), "to", max(three),
          "of 100, spread", round(statistics.stdev(three), 1))
    moved = [i for i in ids if len({runs[i][s]["triage"]["category"]
                                    for s in seeds}) > 1]
    print("emails whose category changed across the 20 seeds:", len(moved))
    mixed = [i for i in ids
             if 0 < sum(one_label(E[i], runs[i][s]["triage"])
                        for s in seeds) < 20]
    print("emails right in some seeds and wrong in others:", len(mixed))
