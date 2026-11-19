"""Lesson 05.6: emails that come in clumps, and resampling by clump.

Given: the log, the bootstrap from scorecard.stats and the lines that print.
You write `group_by` and `mean_of_clumps`.

From this folder: uv run python clumps.py
"""
import collections

from plumbing import clean, drafts, emails
from scorecard.stats import bootstrap, clustered_se, standard_error


def group_by(ids, key):
    """{key of an id: [the ids with that key]}, in the order first seen."""
    groups = {}
    for i in ids:
        groups.setdefault(key(i), []).append(i)
    return groups


def mean_of_clumps(clumps):
    """The mean over every case in a list of clumps (lists of 0/1)."""
    flat = [y for clump in clumps for y in clump]
    return sum(flat) / len(flat)


if __name__ == "__main__":
    E, T1 = emails(), drafts("hd-1")
    ids = sorted(E)
    by_sender = group_by(ids, lambda i: E[i]["from_email"])
    sizes = collections.Counter(len(v) for v in by_sender.values())
    print("senders by how many emails they sent:", dict(sorted(sizes.items())))
    three = next(v for v in by_sender.values() if len(v) == 3)
    for i in three:
        print(" ", i, E[i]["from_email"], "|", E[i]["subject"])

    x = [clean(E[i], T1[i]) for i in ids]
    mean = lambda v: sum(v) / len(v)
    print(f"hd-1, no check firing: {mean(x):.1%} of {len(x)}")
    plain = bootstrap(x, mean)
    clumps = [[clean(E[i], T1[i]) for i in v] for v in by_sender.values()]
    by_clump = bootstrap(clumps, mean_of_clumps)      # draw whole senders
    print(f"resample emails: {plain[0]:.1%} to {plain[1]:.1%}")
    print(f"resample senders: {by_clump[0]:.1%} to {by_clump[1]:.1%}")
    senders = [E[i]["from_email"] for i in ids]
    print("standard error, as if independent:",
          round(standard_error(mean(x), len(x)), 4),
          " by sender:", round(clustered_se(x, senders), 4))
