"""Lesson 04.3: the judge against Arjun on the 100 development drafts.

Given: the two recordings, the twelve-cell table and the lines that print.
You write `settle`, `count_cells` and `rates_from_counts`.

From this folder: uv run python two_by_two.py
"""
from collections import Counter

from plumbing import arjun_dev, judge_v1
from scorecard.judge import confusion, rates


def print_table(arjun, judge):
    """Every pair of Arjun's call and the judge's verdict, counted."""
    table = Counter((arjun[i], judge[i]) for i in arjun)
    print(f"{'Arjun says':<11} judge pass  fail  unsure  no line")
    for call in ("pass", "fail", "unsure"):
        cells = [table[call, v] for v in ("pass", "fail", "unsure", "none")]
        print(f"{call:<11} {cells[0]:>10} {cells[1]:>5} {cells[2]:>7} "
              f"{cells[3]:>8}")


def settle(arjun, judge):
    """(ids, person, judged): the drafts Arjun called pass or fail, and
    for each whether Arjun and the judge passed it. The judge passes
    only on a clear PASS."""
    raise NotImplementedError(
        "TODO 04.3: return the ids Arjun called pass or fail, and "
        "for each whether he passed it and whether the judge did, "
        "on a clear PASS only, see the lesson's 'What to do with "
        "unsure' section")


def count_cells(person, judged):
    """The four counts of the table; True means pass."""
    raise NotImplementedError(
        "TODO 04.3: return the four counts tp, fp, fn and tn, see "
        "the lesson's 'What to do with unsure' section")


def rates_from_counts(c):
    """(passes kept, fails held back) from the four counts."""
    raise NotImplementedError(
        "TODO 04.3: return the pass-keeping rate and the catch "
        "rate from the four counts, see the lesson's 'Two rates "
        "in plain words' section")


if __name__ == "__main__":
    arjun, judge = arjun_dev(), judge_v1()
    print_table(arjun, judge)

    ids, person, judged = settle(arjun, judge)
    c = count_cells(person, judged)
    print(c, "on", len(ids), "drafts")
    print("scorecard:", confusion(person, judged))

    tpr, tnr = rates_from_counts(c)
    print(f"passes kept {tpr:.1%}, fails held back {tnr:.1%}")
    print("scorecard rates:", [round(r, 3) for r in rates(person, judged)])

    accuracy = (c["tp"] + c["tn"]) / len(ids)
    print(f"accuracy {accuracy:.1%}; always saying pass: "
          f"{sum(person) / len(ids):.1%}")
    fails = [i for i in ids if arjun[i] == "fail"]
    print("fails judged FAIL:", sum(judge[i] == "fail" for i in fails),
          "of", len(fails))
