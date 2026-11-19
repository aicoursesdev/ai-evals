"""Lesson 04.2: agreement and kappa from four counts, then 100 drafts.

Given: loading the calls, and the lines that print.
You write `four_counts`, `seen_and_chance` and `kappa_from`.

From this folder: uv run python by_hand.py
"""
from collections import Counter

from plumbing import settled, two_columns
from scorecard.judge import agreement, kappa


def four_counts(a, d):
    """(both pass, both fail, only a passes, only d passes) for two lists
    of "pass" and "fail" calls on the same drafts."""
    count = Counter(zip(a, d))
    return (count["pass", "pass"], count["fail", "fail"],
            count["pass", "fail"], count["fail", "pass"])


def seen_and_chance(both_pass, both_fail, a_only, d_only):
    """The agreement seen, and the agreement chance alone would give
    two people who pass as often as these two do."""
    n = both_pass + both_fail + a_only + d_only
    seen = (both_pass + both_fail) / n
    a_pass = (both_pass + a_only) / n  # share the first passes
    d_pass = (both_pass + d_only) / n  # share the second passes
    return seen, a_pass * d_pass + (1 - a_pass) * (1 - d_pass)


def kappa_from(seen, chance):
    """The share of the room above chance that the two filled."""
    return (seen - chance) / (1 - chance)


if __name__ == "__main__":
    ids, arjun, divya = two_columns()
    a80, d80 = settled(arjun, divya)
    counts = four_counts(a80, d80)
    print(f"{sum(counts)} drafts where both said pass or fail")
    print("both pass", counts[0], "| both fail", counts[1],
          "| only Arjun passes", counts[2], "| only Divya passes", counts[3])

    seen, chance = seen_and_chance(*counts)
    print(f"agreement seen {seen:.3f}, expected by chance {chance:.3f}")
    print(f"kappa = {kappa_from(seen, chance):.3f}")

    print("scorecard on the 80:", f"{agreement(a80, d80):.3f}",
          f"{kappa(a80, d80):.3f}")
    print("scorecard on all 100:", f"{agreement(arjun, divya):.2f}",
          f"{kappa(arjun, divya):.3f}")
