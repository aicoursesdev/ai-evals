"""Lesson 02.2: what a random 100 holds, and what a sample by slice holds.

Given: it calls your `random_sample` and `slice_sample`.
From this folder: uv run python random_vs_slice.py
"""
import statistics

from slices import log, random_sample, slice_sample, tally

RARE = [("language", "ml"), ("language", "hi"), ("language", "ta"),
        ("attack", True), ("long", True), ("category", "account"),
        ("category", "warranty")]


def name(one):
    return f"{one[0]}={one[1]}"


def main():
    emails = log()
    traffic = tally(emails)
    plain = tally(random_sample(emails, 100, seed=1))
    by_slice = tally(slice_sample(emails, 100, seed=1))
    print(f"{'slice':<20}{'log':>5}{'random 100':>12}{'by slice':>10}")
    for one in RARE:
        print(f"{name(one):<20}{traffic[one]:>5}"
              f"{plain[one]:>12}{by_slice[one]:>10}")
    counts = {one: [] for one in RARE}
    for seed in range(1000):  # a thousand different random hundreds
        drawn = tally(random_sample(emails, 100, seed))
        for one in RARE:
            counts[one].append(drawn[one])
    print("\n1000 random hundreds: fewest, median, most; draws with none")
    for one in RARE:
        n = counts[one]
        print(f"{name(one):<20}{min(n):>3}{statistics.median(n):>6}"
              f"{max(n):>5}{sum(c == 0 for c in n):>8}")


if __name__ == "__main__":
    main()
