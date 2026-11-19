"""Lesson 02.5: look for copies and near-copies among the 750 emails.

Given: it calls your `shingles` through `near_pairs` (near.py).
From this folder: uv run python duplicates.py
"""
from near import near_pairs
from scorecard import data
from slices import log


def main():
    launch = data.emails(launch=True)
    everything = launch + log()
    print(len(everything), "emails:", len(launch), "launch,", len(log()),
          "log")
    bodies = [e["body"].strip().lower() for e in everything]
    print("exact copies of a body:", len(bodies) - len(set(bodies)))
    runs = near_pairs(everything, floor=0.5, n=3)
    print("pairs sharing half their 3-word runs:", len(runs))
    words = near_pairs(everything, floor=0.4, n=1)
    print("pairs sharing 40% of their words:", len(words), "(closest first)")
    for a, b, share in words[:6]:
        print("  ", a, b, share)


if __name__ == "__main__":
    main()
