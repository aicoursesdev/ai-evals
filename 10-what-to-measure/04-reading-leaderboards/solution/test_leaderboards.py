"""Lesson 10.4: the best of many private tries, and scores near the ceiling.

Both scripts work on made-up numbers: no model, no network, and no data
file is read. From the top folder: make check 10.4
"""
import random
import runpy
from pathlib import Path

import pytest

import near_the_ceiling
import private_variants
from scorecard.stats import wilson

HERE = Path(__file__).parent


def printed(name, capsys):
    runpy.run_path(str(HERE / name), run_name="__main__")
    return [line.rstrip() for line in capsys.readouterr().out.splitlines()]


def test_one_try_is_the_share_of_votes_won():
    rng = random.Random(1)
    again = random.Random(1)
    one = private_variants.best_of(1, rng)
    assert one == sum(again.random() < 0.5 for _ in range(400)) / 400


def test_the_best_of_many_is_the_largest_of_their_scores():
    rng, again = random.Random(2), random.Random(2)
    scores = [sum(again.random() < 0.5 for _ in range(400)) / 400
              for _ in range(5)]
    assert private_variants.best_of(5, rng) == max(scores)


def test_more_private_tries_publish_a_higher_average():
    rng = random.Random(3)
    ones = private_variants.average_published(1, rng)
    many = private_variants.average_published(27, rng)
    assert ones == pytest.approx(0.5, abs=0.01) and many > ones + 0.03


def test_the_average_is_over_the_releases(monkeypatch):
    monkeypatch.setattr(private_variants, "RELEASES", 3)
    scores = iter([0.5, 0.6, 0.7])
    monkeypatch.setattr(private_variants, "best_of", lambda v, r: next(scores))
    assert private_variants.average_published(9, None) == pytest.approx(0.6)


def test_private_variants_prints_the_lessons_numbers(capsys):
    assert printed("private_variants.py", capsys) == [
        "true win rate 50%, 400 votes per variant, 2,000 simulated releases",
        "best of  1 private variants: average published score 50.0%",
        "best of  5 private variants: average published score 52.9%",
        "best of 27 private variants: average published score 55.0%",
        "one honest score of 50% on 400 votes: range 45.1% to 54.9%"]


def test_a_score_line_gives_the_wilson_range():
    low, high = wilson(490, 500)
    assert near_the_ceiling.score_line(490) == (
        f"490 of 500 right (98.0%): range {low:.1%} to {high:.1%}")


def test_near_the_ceiling_prints_three_overlapping_ranges(capsys):
    assert printed("near_the_ceiling.py", capsys) == [
        "400 of 500 right (80.0%): range 76.3% to 83.3%",
        "490 of 500 right (98.0%): range 96.4% to 98.9%",
        "495 of 500 right (99.0%): range 97.7% to 99.6%"]
