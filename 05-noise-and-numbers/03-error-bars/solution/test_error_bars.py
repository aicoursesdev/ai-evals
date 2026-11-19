"""Lesson 05.3: the standard error and two 95% ranges, in your own functions.

No model and no network: the tests read the recorded runs in the repo.
From the top folder: make check 05.3
"""
import runpy
from pathlib import Path

import pytest

import by_hand
import small_slices
from scorecard import stats

HERE = Path(__file__).parent
CASES = [(42, 50), (137, 150), (486, 550), (30, 40), (5, 10), (50, 100)]


def printed(name, capsys):
    """What a script in this folder prints, one string per line."""
    runpy.run_path(str(HERE / name), run_name="__main__")
    return [line.rstrip() for line in capsys.readouterr().out.splitlines()]


def test_half_of_100_cases_has_a_standard_error_of_5_points():
    assert by_hand.standard_error(0.5, 100) == pytest.approx(0.05)


def test_42_of_50_has_a_standard_error_of_0_0518():
    assert by_hand.standard_error(0.84, 50) == pytest.approx(0.0518, abs=5e-5)


def test_no_failures_gives_no_standard_error_which_is_the_trouble():
    assert by_hand.standard_error(1.0, 8) == 0


def test_the_simple_range_for_42_of_50_is_73_8_to_94_2():
    low, high = by_hand.simple_range(42, 50)
    assert (round(low, 3), round(high, 3)) == (0.738, 0.942)


def test_the_simple_range_for_30_of_40_is_61_6_to_88_4():
    low, high = by_hand.simple_range(30, 40)
    assert (round(low, 3), round(high, 3)) == (0.616, 0.884)


def test_8_of_8_gets_no_range_at_all_from_the_simple_formula():
    assert by_hand.simple_range(8, 8) == (1.0, 1.0)


@pytest.mark.parametrize("passed, n", CASES)
def test_the_simple_range_agrees_with_scorecard_stats(passed, n):
    assert by_hand.simple_range(passed, n) == pytest.approx(
        stats.interval(passed, n))


def test_wilson_for_8_of_8_runs_from_67_6_to_100():
    low, high = small_slices.wilson_range(8, 8)
    assert round(low, 3) == 0.676 and high == 1.0


def test_wilson_stays_between_0_and_1_even_for_none_passing():
    low, high = small_slices.wilson_range(0, 100)
    assert low == 0.0 and round(high, 3) == 0.037


@pytest.mark.parametrize("passed, n", CASES + [(8, 8), (0, 100), (5, 5)])
def test_wilson_agrees_with_scorecard_stats(passed, n):
    assert small_slices.wilson_range(passed, n) == pytest.approx(
        stats.wilson(passed, n))


def test_by_hand_prints_the_three_lines_the_lesson_shows(capsys):
    assert printed("by_hand.py", capsys) == [
        ("Kiran's test set     42 of  50  p = 0.840  se = 0.052  ran"
         'ge 73.8% to 94.2%'),
        ('week 1 of the log   137 of 150  p = 0.913  se = 0.023  ran'
         'ge 86.8% to 95.8%'),
        ('the 550 log emails  486 of 550  p = 0.884  se = 0.014  ran'
         'ge 85.7% to 91.0%'),
    ]


def test_with_stats_prints_both_ranges_for_three_scores(capsys):
    assert printed("with_stats.py", capsys) == [
        '                     simple formula        Wilson',
        '42 of 50         73.8% to  94.2%    71.5% to  91.7%',
        '137 of 150       86.8% to  95.8%    85.7% to  94.9%',
        '486 of 550       85.7% to  91.0%    85.4% to  90.8%',
    ]


def test_small_slices_prints_the_language_table_the_lesson_shows(capsys):
    assert printed("small_slices.py", capsys) == [
        'language  emails right   simple formula        Wilson',
        'en          447   389      84% to  90%      84% to  90%',
        'hi-en        80    74      87% to  98%      85% to  97%',
        'hi            8     8     100% to 100%      68% to 100%',
        'ta           10    10     100% to 100%      72% to 100%',
        'ml            5     5     100% to 100%      57% to 100%',
    ]


def test_weeks_prints_each_weeks_score_with_its_wilson_range(capsys):
    assert printed("weeks.py", capsys) == [
        'week  emails  right   rate    Wilson range',
        '   1     150    137  91.3%   85.7% to 94.9%',
        '   2     123    112  91.1%   84.7% to 94.9%',
        '   3     134    118  88.1%   81.5% to 92.5%',
        '   4     143    119  83.2%   76.2% to 88.5%',
    ]
