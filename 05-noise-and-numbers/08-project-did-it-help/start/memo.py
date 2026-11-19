"""Lesson 05.8: the numbers for the memo "is hd-2 really better than hd-1?"

Given: both versions' outcomes on the 277 emails, and the lines that print.
You write `line` and `compare`, from the functions in scorecard.stats.

From this folder: uv run python memo.py
"""
from plumbing import clean, drafts, emails
from scorecard.stats import bootstrap, mcnemar, pair_counts, paired, wilson


def line(name, passed, n):
    """One reported rate: the share, the count it rests on, the range."""
    raise NotImplementedError(
        "TODO 05.8: return the share, the count it rests on and the "
        "Wilson range as one line, see the lesson's 'The memo' section")


def compare(a, b):
    """Two 0/1 lists scored on the same emails: the four pair counts, the
    paired difference and its range, the bootstrap range of the
    difference and McNemar's exact p-value."""
    raise NotImplementedError(
        "TODO 05.8: return the pair counts, the paired difference, the "
        "bootstrap range and McNemar's p-value, see the lesson's 'The "
        "memo' section")


if __name__ == "__main__":
    E, T1, T2 = emails(), drafts("hd-1"), drafts("hd-2")
    ids = sorted(T2)
    a = [clean(E[i], T1[i]) for i in ids]
    b = [clean(E[i], T2[i]) for i in ids]
    print(line("hd-1, no check firing", sum(a), len(ids)))
    print(line("hd-2, no check firing", sum(b), len(ids)))
    out = compare(a, b)
    r = out["paired"]
    print("pairs:", out["pairs"])
    print(f"paired difference {r['diff']:+.1%}, range {r['low']:+.1%} to "
          f"{r['high']:+.1%}")
    low, high = out["bootstrap"]
    print(f"bootstrap range {low:+.1%} to {high:+.1%}")
    print("McNemar exact p-value:", round(out["p"], 4))
