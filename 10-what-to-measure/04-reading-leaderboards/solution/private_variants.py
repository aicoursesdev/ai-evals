"""Lesson 10.4: why publishing only the best of many private tries flatters
a ranking. SIMULATED: every variant is exactly as good as the others.

From this folder: uv run python private_variants.py
"""
import random

from scorecard.stats import wilson

TRUE_RATE = 0.50   # every variant truly wins half of its head-to-head votes
VOTES = 400        # votes behind each variant's score
RELEASES = 2000    # simulated releases averaged


def best_of(variants, rng):
    """The best score among `variants` private tries, each scored on its
    own VOTES votes. Only this one would be published."""
    return max(sum(rng.random() < TRUE_RATE for _ in range(VOTES))
               for _ in range(variants)) / VOTES


def average_published(variants, rng):
    """The average published score over RELEASES simulated releases, each
    one the best of `variants` private tries."""
    runs = [best_of(variants, rng) for _ in range(RELEASES)]
    return sum(runs) / len(runs)


if __name__ == "__main__":
    rng = random.Random(7)
    print(f"true win rate {TRUE_RATE:.0%}, {VOTES} votes per variant, "
          "2,000 simulated releases")
    for variants in (1, 5, 27):
        print(f"best of {variants:2} private variants: average "
              f"published score {average_published(variants, rng):.1%}")
    low, high = wilson(round(0.5 * VOTES), VOTES)
    print(f"one honest score of 50% on {VOTES} votes: range "
          f"{low:.1%} to {high:.1%}")
