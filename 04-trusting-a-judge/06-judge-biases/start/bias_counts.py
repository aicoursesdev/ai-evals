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
    raise NotImplementedError(
        "TODO 04.6: count how often the reply shown first, the "
        "one shown second and a tie won, see the lesson's 'Order' "
        "section")


def same_both_orders(rows):
    """(pairs, same): how many email ids the records cover, and on how
    many of them the same version wins in both orders."""
    raise NotImplementedError(
        "TODO 04.6: return the number of pairs and on how many "
        "the same version wins in both orders, see the lesson's "
        "'Order' section")


def moves(before, after, ids):
    """Counter of (verdict before, verdict after) over the ids."""
    raise NotImplementedError(
        "TODO 04.6: count each pair of verdict before and verdict "
        "after, see the lesson's 'Length' section")


def same_on(first, again, ids):
    """On how many of the ids two runs gave the same verdict."""
    raise NotImplementedError(
        "TODO 04.6: count the drafts on which two runs gave the "
        "same verdict, see the lesson's 'Asking twice' section")


def kinds_per_draft(runs, ids):
    """Counter of how many different verdicts a draft got over the runs
    (a list of {id: verdict}): {1: drafts with one kind, 2: ...}."""
    raise NotImplementedError(
        "TODO 04.6: count how many drafts got one, two, three or "
        "four kinds of verdict over the runs, see the lesson's "
        "'Asking twice' section")
