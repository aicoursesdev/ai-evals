"""Lesson 05.2: where the wobble comes from, in your own functions.

No model and no network: the tests read the recorded runs in the repo.
From the top folder: make check 05.2
(The guard in ../../conftest.py fails any test that parses a sealed trace;
every script below runs under it.)
"""
import random
import runpy
from pathlib import Path

import which_cases
import which_key
import which_run

HERE = Path(__file__).parent


def printed(name, capsys):
    """What a script in this folder prints, one string per line."""
    runpy.run_path(str(HERE / name), run_name="__main__")
    return [line.rstrip() for line in capsys.readouterr().out.splitlines()]


def test_drawing_every_email_gives_the_same_score_each_time():
    right = {i: int(i < 42) for i in range(50)}  # 42 of 50 right
    scores = which_cases.draw_scores(right, 50, random.Random(1))
    assert len(scores) == 1000 and set(scores) == {0.84}


def test_draws_of_half_the_emails_come_back_sorted_and_move():
    right = {i: i % 2 for i in range(100)}
    scores = which_cases.draw_scores(right, 10, random.Random(1))
    assert scores == sorted(scores) and scores[0] < 0.5 < scores[-1]
    assert all(0 <= s <= 1 for s in scores)


def test_one_label_checks_only_the_category():
    email = {"category": "return"}
    assert which_run.one_label(email, {"category": "return"}) == 1
    assert which_run.one_label(email, {"category": "warranty"}) == 0


def test_all_three_needs_category_urgency_and_needs_human():
    email = {"category": "a", "urgency": "high", "needs_human": True}
    assert which_run.all_three(email, dict(email)) == 1
    assert which_run.all_three(email, dict(email, urgency="low")) == 0
    assert which_run.all_three(email, dict(email, needs_human=False)) == 0


def test_seed_scores_counts_the_good_emails_of_each_seed():
    good = lambda i, s: int(i <= s)  # seed s gets emails 1..s right
    assert which_run.seed_scores(good, [1, 2, 3], [1, 2, 3]) == [1, 2, 3]
    assert which_run.seed_scores(good, [], [1, 2]) == [0, 0]


def test_no_wrong_keys_leaves_the_score_and_all_wrong_keys_zeroes_it():
    ids = list(range(20))
    E = {i: {"category": "a"} for i in ids}
    T = {i: {"triage": {"category": "a"}} for i in ids}
    rng = random.Random(7)
    assert which_key.score_with_wrong_keys(E, T, ids, ["a", "b"], 0, rng) == 1
    assert which_key.score_with_wrong_keys(E, T, ids, ["a", "b"], 1, rng) == 0


def test_a_tenth_wrong_keys_costs_about_a_tenth_of_the_score():
    ids = list(range(100))
    E = {i: {"category": "a"} for i in ids}
    T = {i: {"triage": {"category": "a"}} for i in ids}
    score = which_key.score_with_wrong_keys(
        E, T, ids, ["a", "b", "c"], 0.10, random.Random(7))
    assert score == 0.9


def test_which_cases_prints_the_table_the_lesson_shows(capsys):
    assert printed("which_cases.py", capsys) == [
        'the log: 486 of 550 categories right',
        'cases  lowest  2.5th  97.5th  highest  typical',
        '   50     74%    80%     96%     100%    4.2',
        '  100     78%    82%     94%      97%    2.9',
        '  150     81%    84%     93%      95%    2.2',
        '  275     84%    86%     91%      92%    1.3',
    ]


def test_which_run_prints_the_four_lines_the_lesson_shows(capsys):
    assert printed("which_run.py", capsys) == [
        'category right, 20 seeds: 76 to 85 of 100, spread 2.0',
        'all three labels right:   22 to 35 of 100, spread 4.1',
        'emails whose category changed across the 20 seeds: 31',
        'emails right in some seeds and wrong in others: 28',
    ]


def test_which_drafts_uses_all_five_seeds_and_counts_the_empty_draft(capsys):
    assert printed("which_drafts.py", capsys) == [
        'seeds complete for all 100 emails: [1, 2, 3, 4, 5]',
        ('temperature 0 (the recorded trace): 78 of 100 drafts with '
         'no check firing'),
        'seed 1: 76 of 100',
        'seed 2: 78 of 100',
        'seed 3: 73 of 100',
        'seed 4: 73 of 100',
        'seed 5: 77 of 100',
        'typical wobble: 2.3 points',
    ]


def test_which_key_prints_the_simulated_scores_the_lesson_shows(capsys):
    assert printed("which_key.py", capsys) == [
        'wrong keys  score',
        '       0%  88.4%',
        '       2%  86.5%',
        '       5%  83.6%',
        '      10%  79.5%',
    ]
