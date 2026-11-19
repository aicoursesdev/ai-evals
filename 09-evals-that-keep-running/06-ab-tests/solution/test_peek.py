"""Lesson 09.6: the z score and the peeking loop, in your own functions.

Nothing here is recorded from the help desk: the experiments are simulated
(seed 7). No model and no network.
From the top folder: make check 09.6
"""
import math
import random
import runpy
from itertools import chain, repeat
from pathlib import Path

import pytest

import peek

HERE = Path(__file__).parent


def printed(name, capsys):
    """What a script in this folder prints, one string per line."""
    runpy.run_path(str(HERE / name), run_name="__main__")
    return [line.rstrip() for line in capsys.readouterr().out.splitlines()]


class Rigged:
    """A stand-in for random.Random: arm A always sends, arm B never."""

    def __init__(self):
        day = [0.1] * peek.PER_DAY + [0.9] * peek.PER_DAY
        self.values = chain.from_iterable(repeat(day))

    def random(self):
        return next(self.values)


def test_520_against_480_of_1000_is_1_79_standard_errors():
    assert peek.z_score(520, 480, 1000) == pytest.approx(1.79, abs=0.005)


def test_z_is_the_same_whichever_arm_is_ahead_and_zero_when_level():
    assert peek.z_score(480, 520, 1000) == peek.z_score(520, 480, 1000)
    assert peek.z_score(500, 500, 1000) == 0


def test_z_is_the_gap_over_what_luck_alone_moves_it():
    a, b, n = 530, 470, 900
    p = (a + b) / (2 * n)
    assert peek.z_score(a, b, n) == pytest.approx(
        (a / n - b / n) / math.sqrt(p * (1 - p) * 2 / n))


def test_a_lopsided_experiment_wins_on_the_first_look():
    assert peek.first_win(Rigged(), 1.96, {1}) == 1
    assert peek.first_win(Rigged(), 1.96, {5, 6}) == 5


def test_no_look_means_no_win_and_a_high_bar_means_no_win():
    assert peek.first_win(Rigged(), 1.96, set()) is None
    assert peek.first_win(Rigged(), 50, {1, 2, 3}) is None


def test_the_first_win_is_the_first_look_over_the_bar():
    rng = random.Random(7)
    wins = [peek.first_win(rng, 1.96, set(range(1, 29))) for _ in range(300)]
    assert all(w is None or 1 <= w <= 28 for w in wins)
    assert 0.1 < sum(w is not None for w in wins) / 300 < 0.45


def test_share_is_the_same_every_time():
    assert peek.share(1.96, {28}) == peek.share(1.96, {28})


def test_peek_prints_the_false_win_rates_the_lesson_shows(capsys):
    assert printed("peek.py", capsys) == [
        '10000 simulated experiments, true rate 0.5 in both arms',
        'look once, on day 28             false wins   5.0%   by day 7:  0.0%',
        'look every day                   false wins  27.8%   by day 7: 17.2%',
        'look every 7 days                false wins  13.0%   by day 7:  5.2%',
        'look every day, bar 3.12         false wins   1.6%   by day 7:  0.7%',
        ("looking every day, false wins so far: {1: '5.6%', 7: '17.2%', "
         "14: '22.5%', 21: '25.5%', 28: '27.8%'}"),
    ]
