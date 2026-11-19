"""Lesson 05.7: twenty variants of one prompt, in your own functions.

No model and no network: the tests read the recorded runs in the repo.
From the top folder: make check 05.7
"""
import random
import runpy
from pathlib import Path

import many_splits
import twenty_variants

HERE = Path(__file__).parent


def printed(name, capsys):
    """What a script in this folder prints, one string per line."""
    runpy.run_path(str(HERE / name), run_name="__main__")
    return [line.rstrip() for line in capsys.readouterr().out.splitlines()]


def test_score_counts_the_subset_emails_this_seed_got_right():
    good = {(1, 1): 1, (2, 1): 0, (1, 2): 1, (2, 2): 1}
    assert twenty_variants.score(good, 1, [1, 2]) == 1
    assert twenty_variants.score(good, 2, [1, 2]) == 2
    assert twenty_variants.score(good, 2, []) == 0


def test_the_best_seed_has_the_highest_score():
    assert twenty_variants.best_seed({1: 10, 2: 11, 3: 9}) == 2


def test_a_tie_goes_to_the_lowest_seed():
    assert twenty_variants.best_seed({4: 11, 2: 11, 7: 11, 3: 10}) == 2


def test_a_perfect_seed_wins_on_the_small_set_and_the_fresh_emails():
    ids = list(range(100))
    good = {(i, s): int(s == 3) for i in ids for s in range(1, 21)}
    top, today, old, new = many_splits.one_split(good, ids, random.Random(7))
    assert (top, today) == (20, 0)
    assert old == [0] * 80 and new == [1] * 80


def test_identical_seeds_make_the_first_the_winner_and_fresh_emails_match():
    ids = list(range(100))
    good = {(i, s): int(i % 2 == 0) for i in ids for s in range(1, 21)}
    top, today, old, new = many_splits.one_split(good, ids, random.Random(7))
    assert top == today and old == new and len(new) == 80


def test_twenty_variants_prints_the_winner_and_the_fresh_score(capsys):
    assert printed("twenty_variants.py", capsys) == [
        ('on 20 emails: [10, 10, 8, 11, 10, 11, 9, 10, 8, 10, 7, 9, '
         '8, 8, 10, 11, 10, 10, 11, 10]'),
        'winner: seed 4, 11 of 20 (55%)',
        ('winner on the other 80: 24 of 80 (30%); the 20 variants on'
         ' average 20.4 of 80 (26%)'),
    ]


def test_many_splits_prints_the_simulated_counts_the_lesson_shows(capsys):
    assert printed("many_splits.py", capsys) == [
        ("winner's score on the small set minus on fresh emails, on "
         'average: 11.2 points'),
        'declared better than today on the 20 emails: 870 of 1000',
        '... and also ahead on the 80 fresh emails:   371 of 1000',
        '... and ahead by a margin McNemar accepts:   0 of 1000',
    ]


def test_bar_cost_prints_the_lead_mcnemar_needs(capsys):
    assert printed("bar_cost.py", capsys) == [
        ('emails where a seed disagrees with seed 1, of 80: mean 11.'
         '3 range 3 to 25'),
        'disagreeing emails  lead needed  as points of 80',
        '                10            8            10.0',
        '                20           10            12.5',
        '                30           12            15.0',
        '                40           14            17.5',
    ]
