"""Lesson 09.7: separate "the traffic changed" from "the system changed".

Given: the weeks' counts, the bootstrap and the lines that print.
You write `reweighted`.

From this folder: uv run python reweight.py
Week 4's score, as if week 4 had week 1's mix of email kinds.
"""
from collections import Counter

from plumbing import counts, rows
from scorecard.stats import bootstrap


def reweighted(mix_a, right_b, seen_b):
    """Week B's rates on week A's mix: the sum over kinds k of
    share_A(k) * rate_B(k). mix_a is {kind: emails in week A}; right_b and
    seen_b are {kind: right} and {kind: emails} for week B."""
    raise NotImplementedError(
        "TODO 09.7: return week B's rates weighted by week A's mix of "
        "kinds, see the lesson's 'Same system, other mix' section")


if __name__ == "__main__":
    mix1, right1 = counts(1)
    mix4, right4 = counts(4)
    n1, n4 = sum(mix1.values()), sum(mix4.values())
    print(f"{'category':18}{'wk 1 share':>11}{'wk 4 rate':>10}"
          f"{'share*rate':>11}")
    for cat in sorted(mix1):
        share, rate = mix1[cat] / n1, right4[cat] / mix4[cat]
        print(f"{cat:18}{share:>11.3f}{rate:>10.3f}{share * rate:>11.3f}")
    total = reweighted(mix1, right4, mix4)
    week1, week4 = sum(right1.values()) / n1, sum(right4.values()) / n4
    print(f"\nweek 1 as it was:               {week1:.1%}")
    print(f"week 4 on week 1's mix:         {total:.1%}  (week 4's rates)")
    print(f"week 4 as it was:               {week4:.1%}")
    print(f"change within the kinds:        {total - week1:+.1%}")
    print(f"change from the mix of kinds:   {week4 - total:+.1%}")

    def on_week_1_mix(sample):
        """Week 4's score on week 1's mix for a list of (kind, hit) rows."""
        seen = Counter(kind for kind, _ in sample)
        hit = Counter(kind for kind, ok in sample if ok)
        return reweighted(mix1, hit, seen)

    low, high = bootstrap(rows(4), on_week_1_mix)
    print(f"resampling week 4's emails: {low:.1%} to {high:.1%}")
