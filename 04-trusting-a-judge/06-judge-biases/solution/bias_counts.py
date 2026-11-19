"""Lesson 04.6: the counts behind three tests of a judge.

Given: the recordings and the lines that print.
You write `by_place`, `same_both_orders`, `moves`, `same_on` and
`kinds_per_draft`.

Used by position_test.py, length_test.py and again_test.py.
"""
from collections import Counter

from plumbing import winner


def by_place(rows):
    """How often the reply shown first, the one shown second or a tie
    won, over pairwise records with a, b (the versions shown first and
    second) and reply."""
    shown = Counter()
    for r in rows:
        who = winner(r["reply"], (r["a"], r["b"]))
        if who == "tie":
            shown["tie"] += 1
        elif who == r["a"]:
            shown["first"] += 1
        else:
            shown["second"] += 1
    return shown


def same_both_orders(rows):
    """(pairs, same): how many email ids the records cover, and on how
    many of them the same version wins in both orders."""
    by_pair = {}  # email id -> {version shown first: who won}
    for r in rows:
        who = winner(r["reply"], (r["a"], r["b"]))
        by_pair.setdefault(r["id"], {})[r["a"]] = who
    same = sum(w["hd-1"] == w["hd-2"] != "tie" for w in by_pair.values())
    return len(by_pair), same


def moves(before, after, ids):
    """Counter of (verdict before, verdict after) over the ids."""
    return Counter((before[i], after[i]) for i in ids)


def same_on(first, again, ids):
    """On how many of the ids two runs gave the same verdict."""
    return sum(first[i] == again[i] for i in ids)


def kinds_per_draft(runs, ids):
    """Counter of how many different verdicts a draft got over the runs
    (a list of {id: verdict}): {1: drafts with one kind, 2: ...}."""
    return Counter(len({r[i] for r in runs}) for i in ids)
