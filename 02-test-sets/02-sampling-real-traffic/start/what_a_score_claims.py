"""Lesson 02.2: what each kind of sample lets its score claim.

Given: it calls your two samplers and your `weighted_rate`.
From this folder: uv run python what_a_score_claims.py
"""
import statistics
from collections import Counter

from held_back import usable_emails, usable_triage
from slices import random_sample, slice_sample
from weighting import weighted_rate

emails, said = usable_emails(), usable_triage()


def plain_score(sample):
    """Share of the sample the help desk sorted as Arjun did."""
    right = [said[e["id"]]["category"] == e["category"] for e in sample]
    return sum(right) / len(right)


def weighted_score(sample, field):
    """The sample's rate inside each value of `field` (each language, say),
    weighted by that value's share of the whole log."""
    rates, weights = {}, {}
    for value, n in Counter(e[field] for e in emails).items():
        part = [e for e in sample if e[field] == value]
        if part:  # a value the sample missed adds nothing
            rates[value] = plain_score(part)
            weights[value] = n / len(emails)
    return weighted_rate(rates, weights)


def main():
    print(f"the whole log, {len(emails)} emails: {plain_score(emails):.1%}")
    rows = {name: [] for name in (
        "random 100", "by slice 100", "by slice, weighted by category",
        "by slice, weighted by language")}
    for seed in range(200):  # two hundred draws of each kind
        rows["random 100"].append(
            plain_score(random_sample(emails, 100, seed)))
        sliced = slice_sample(emails, 100, seed)
        rows["by slice 100"].append(plain_score(sliced))
        rows["by slice, weighted by category"].append(
            weighted_score(sliced, "category"))
        rows["by slice, weighted by language"].append(
            weighted_score(sliced, "language"))
    for name, scores in rows.items():
        print(f"{name:<32}mean {statistics.mean(scores):.1%}"
              f"  lowest {min(scores):.1%}  highest {max(scores):.1%}")


if __name__ == "__main__":
    main()
