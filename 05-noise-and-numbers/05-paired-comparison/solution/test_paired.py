"""Lesson 05.5: paired comparison, in your own functions.

No model and no network: the tests read the recorded drafts in the repo.
From the top folder: make check 05.5
"""
import runpy
from pathlib import Path

import pytest

import paired_table
import unpaired
from scorecard import stats

HERE = Path(__file__).parent


def printed(name, capsys):
    """What a script in this folder prints, one string per line."""
    runpy.run_path(str(HERE / name), run_name="__main__")
    return [line.rstrip() for line in capsys.readouterr().out.splitlines()]


def lists(both, only_a, only_b, neither):
    """Two 0/1 lists with exactly these four counts of pairs."""
    a = [1] * both + [1] * only_a + [0] * only_b + [0] * neither
    b = [1] * both + [0] * only_a + [1] * only_b + [0] * neither
    return a, b


def test_five_cases_sort_into_the_four_kinds_of_pair():
    a, b = [1, 1, 0, 0, 1], [1, 0, 1, 0, 1]
    assert paired_table.count_pairs(a, b) == {
        "both": 2, "only_a": 1, "only_b": 1, "neither": 1}


def test_count_pairs_agrees_with_scorecard_stats():
    a, b = lists(199, 12, 27, 39)
    assert paired_table.count_pairs(a, b) == stats.pair_counts(a, b)


def test_ten_cases_that_all_got_better_move_by_10_points_of_100():
    diff, se, low, high = paired_table.paired_range(0, 10, 100)
    assert diff == pytest.approx(0.1)
    assert se == pytest.approx((0.1 - 0.01) ** 0.5 / 99 ** 0.5)
    assert low < 0.1 < high


def test_no_changes_means_no_difference_and_no_wobble():
    assert paired_table.paired_range(0, 0, 50) == (0, 0, 0, 0)


def test_27_better_and_12_worse_of_277_gives_5_4_points_1_0_to_9_8():
    diff, se, low, high = paired_table.paired_range(12, 27, 277)
    assert round(diff, 4) == 0.0542 and round(se, 4) == 0.0223
    assert (round(low, 3), round(high, 3)) == (0.010, 0.098)


def test_paired_range_agrees_with_scorecard_stats():
    a, b = lists(199, 12, 27, 39)
    got = paired_table.paired_range(12, 27, len(a))
    want = stats.paired(a, b)
    assert got == pytest.approx(
        (want["diff"], want["se"], want["low"], want["high"]))


def test_no_changed_case_is_no_evidence():
    assert paired_table.mcnemar_p(0, 0) == 1.0


def test_five_changes_all_one_way_is_2_in_32_each_side_so_0_0625():
    assert paired_table.mcnemar_p(0, 5) == pytest.approx(2 / 32)
    assert paired_table.mcnemar_p(5, 0) == pytest.approx(2 / 32)


def test_an_even_split_is_certainly_luck():
    assert paired_table.mcnemar_p(3, 3) == 1.0


def test_12_against_27_has_a_p_value_of_0_0237():
    assert round(paired_table.mcnemar_p(12, 27), 4) == 0.0237


@pytest.mark.parametrize("worse, better", [(12, 27), (8, 0), (13, 21), (4, 9)])
def test_mcnemar_p_agrees_with_scorecard_stats(worse, better):
    a, b = lists(50, worse, better, 50)
    assert paired_table.mcnemar_p(worse, better) == pytest.approx(
        stats.mcnemar(a, b))


def test_half_against_60_percent_of_100_each_is_ten_points_plus_or_minus_14():
    a, b = [1] * 50 + [0] * 50, [1] * 60 + [0] * 40
    diff, se, low, high = unpaired.unpaired_range(a, b)
    assert diff == pytest.approx(0.1) and se == pytest.approx(0.07)
    assert (round(low, 3), round(high, 3)) == (-0.037, 0.237)


def test_unpaired_hd1_against_hd2_runs_from_minus_1_4_to_plus_12_2():
    a, b = lists(199, 12, 27, 39)
    diff, se, low, high = unpaired.unpaired_range(a, b)
    assert round(se, 3) == 0.035
    assert (round(low, 3), round(high, 3)) == (-0.014, 0.122)


def test_unpaired_prints_the_two_ranges_and_the_difference(capsys):
    assert printed("unpaired.py", capsys) == [
        ('hd-1: 211 of 277 drafts with no check firing (76.2%), rang'
         'e 70.8% to 80.8%'),
        ('hd-2: 226 of 277 drafts with no check firing (81.6%), rang'
         'e 76.6% to 85.7%'),
        'difference +5.4%, standard error 0.035, range -1.4% to +12.2%',
    ]


def test_paired_table_prints_the_pair_counts_and_the_ranges(capsys):
    assert printed("paired_table.py", capsys) == [
        ('both clean: 199  only hd-1 clean: 12  only hd-2 clean: 27 '
         ' neither: 39'),
        'by hand: +5.4%, standard error 0.0223, range +1.0% to +9.8%',
        'paired(): +5.4%, range +1.0% to +9.8%',
        'McNemar exact p-value: 0.0237',
    ]


def test_single_checks_prints_the_table_the_lesson_shows(capsys):
    assert printed("single_checks.py", capsys) == [
        ('check                fires on: hd-1  hd-2   only hd-1  onl'
         'y hd-2  p-value'),
        ('wrong script                   4     2          2         '
         ' 0     0.500'),
        ('missing or old page           22    18         11         '
         ' 7     0.481'),
        ('reply to spam                 10    10          0         '
         ' 0     1.000'),
        ('invented address               1     0          1         '
         ' 0     1.000'),
        ('claims an action              10     2          8         '
         ' 0     0.008'),
        ('asks for known id             24    20         11         '
         ' 7     0.481'),
        ('empty draft                    1     1          0         '
         ' 0     1.000'),
        ('without claims an action: only hd-1 clean 13  only hd-2 cl'
         'ean 21  p-value 0.229'),
    ]


def test_judge_view_prints_the_order_swap_counts(capsys):
    assert printed("judge_view.py", capsys) == [
        '60 pairs: hd-1 won both orders 22, hd-2 10, split 28',
        ('hd-1 won 22 of the 32 that held both ways; range for that '
         'share 51% to 82%'),
        'exact p-value, if each were a coin toss: 0.0501',
        'mean words, hd-1: 89  hd-2: 70',
    ]
