"""Lesson 09.8: triage with the usual model and a smaller one, same 149
emails, and a paired comparison.

Given: the recorded runs, the paired range of 05.5 and the lines that
print. You write `changes_by_category`.

From this folder: uv run python swap_triage.py
Reads data/runs/09-model-swap/ and the ordinary traces; no model is called.
"""
from collections import Counter

from plumbing import right, swap
from scorecard.stats import mcnemar, pair_counts, paired


def changes_by_category(mail, ids, a, b):
    """(emails, got worse, got better) per category, as three Counters;
    a and b are the two models' 0/1 lists over ids."""
    seen = Counter(mail[i]["category"] for i in ids)
    lost = Counter(mail[i]["category"] for i, x, y in zip(ids, a, b) if x > y)
    won = Counter(mail[i]["category"] for i, x, y in zip(ids, a, b) if y > x)
    return seen, lost, won


if __name__ == "__main__":
    mail, old, new = swap()
    ids = sorted(new)
    a, b = [[right(mail[i], t[i]) for i in ids] for t in (old, new)]
    print(f"usual {sum(a)} of {len(a)} right, smaller {sum(b)} of {len(b)}")
    print(pair_counts(a, b))
    p = paired(a, b)
    print(f"change {p['diff']:+.1%}, range {p['low']:+.1%} to "
          f"{p['high']:+.1%}, McNemar p {mcnemar(a, b):.4f}")

    seen, lost, won = changes_by_category(mail, ids, a, b)
    print(f"{'category':18}{'emails':>7}{'worse':>7}{'better':>8}")
    for cat, n in seen.most_common():
        print(f"{cat:18}{n:>7}{lost[cat]:>7}{won[cat]:>8}")
