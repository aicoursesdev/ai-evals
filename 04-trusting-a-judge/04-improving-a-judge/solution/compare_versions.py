"""Lesson 04.4: every judge version on the 100 development drafts.

Given: the recordings, `two_rates` (lesson 04.3's choices) and the lines
that print. You write `score_version` and `choose`.

From this folder:
    uv run python compare_versions.py v1,v2,v3,v4 E-0660 E-0602 E-0398
The versions come first; the ids after them are the drafts whose text a
version was shown, left out of every row.
"""
import sys
from collections import Counter

from judge_versions import DEV, path
from plumbing import arjun, two_rates, verdicts


def score_version(human, seen, skip=()):
    """(tpr, tnr, counts, none) for one version's verdicts on the
    development drafts it has, leaving out the ids in skip; none counts
    the replies with no verdict line."""
    ids = [i for i in DEV if i not in skip and i in seen]
    tpr, tnr, c = two_rates([human[i] for i in ids], [seen[i] for i in ids])
    return tpr, tnr, c, Counter(seen[i] for i in ids)["none"]


def choose(sums):
    """The version with the highest sum of its two rates. sums is
    {version: tpr + tnr}; the rule was fixed before the results."""
    return max(sums, key=sums.get)


if __name__ == "__main__":
    human = arjun("03-right-rule-arjun")
    skip = set(sys.argv[2:])  # drafts whose text a version was shown
    sums = {}
    print("version  kept  caught  tpr    tnr    tpr+tnr  no line")
    for version in sys.argv[1].split(","):
        seen = verdicts(path(version))
        tpr, tnr, c, none = score_version(human, seen, skip)
        sums[version] = tpr + tnr
        print(f"{version:<8} {c['tp']:>2}/{c['tp'] + c['fn']:<3} "
              f"{c['tn']:>2}/{c['tn'] + c['fp']:<4} {tpr:5.1%} {tnr:6.1%} "
              f"{tpr + tnr:7.2f}  {none:>5}")
    print("highest tpr + tnr:", choose(sums))
