"""Lesson 05.2: how far does the score move with the cases you draw?

Given: the log, and the loop that prints the table.
You write `draw_scores`.

From this folder: uv run python which_cases.py
"""
import random
import statistics

from plumbing import category_right, drafts, emails


def draw_scores(right, n, rng):
    """1,000 scores, lowest first, each from n emails drawn at random."""
    raise NotImplementedError(
        "TODO 05.2: return the 1,000 sorted scores, each from n emails "
        "drawn with rng.sample, see the lesson's 'Which emails you "
        "drew' section")


if __name__ == "__main__":
    E, T = emails(), drafts("hd-1")
    right = {i: category_right(E[i], T[i]) for i in sorted(E)}
    print(f"the log: {sum(right.values())} of {len(right)} categories right")

    rng = random.Random(7)      # seeded: your numbers match
    print("cases  lowest  2.5th  97.5th  highest  typical")
    for n in (50, 100, 150, 275):
        draws = draw_scores(right, n, rng)
        print(f"{n:>5}  {draws[0]:>6.0%}  {draws[25]:>5.0%}  "
              f"{draws[974]:>6.0%}  {draws[-1]:>7.0%}  "
              f"{statistics.pstdev(draws) * 100:>5.1f}")
