"""Lesson 09.7: the mix, the slices and the reweighting.

No model and no network: the tests read the recorded log (never the sealed
emails). From the top folder: make check 09.7
"""
import runpy
from collections import Counter
from pathlib import Path

import pytest

import plumbing
import reweight

HERE = Path(__file__).parent


def printed(name, capsys):
    """What a script in this folder prints, one string per line."""
    runpy.run_path(str(HERE / name), run_name="__main__")
    return [line.rstrip() for line in capsys.readouterr().out.splitlines()]


def test_the_same_mix_and_rates_give_the_ordinary_score():
    mix = Counter({"a": 10, "b": 30})
    assert reweight.reweighted(mix, {"a": 5, "b": 30}, mix) == pytest.approx(
        35 / 40)


def test_week_a_mix_with_week_b_rates():
    mix_a = Counter({"a": 10, "b": 30})           # shares 0.25 and 0.75
    right, seen = Counter({"a": 9, "b": 15}), Counter({"a": 10, "b": 30})
    assert reweight.reweighted(mix_a, right, seen) == pytest.approx(
        0.25 * 0.9 + 0.75 * 0.5)


def test_a_kind_missing_from_week_b_drops_out_and_the_rest_rescale():
    mix_a = Counter({"a": 10, "b": 30})
    right, seen = Counter({"a": 9}), Counter({"a": 10})
    assert reweight.reweighted(mix_a, right, seen) == pytest.approx(0.9)


def test_week_4_on_week_1_s_mix_is_87_5_percent():
    mix1 = plumbing.counts(1)[0]
    mix4, right4 = plumbing.counts(4)
    assert round(100 * reweight.reweighted(mix1, right4, mix4), 1) == 87.5


def test_mix_by_week_prints_the_table_the_lesson_shows(capsys):
    assert printed("mix_by_week.py", capsys) == [
        'emails: wk 1: 150 wk 2: 123 wk 3: 134 wk 4: 143',
        'category             wk 1   wk 2   wk 3   wk 4',
        'account                5%     2%     2%     2%',
        'complaint              7%     5%     8%    10%',
        'order_change           9%    12%    13%     4%',
        'other                  7%     8%     6%     2%',
        'payment                7%    12%    10%     6%',
        'product_question      14%    20%    13%     7%',
        'refund                13%     9%     7%    20%',
        'return                12%     9%     7%    24%',
        'shipping_delay        13%    11%    26%    15%',
        'spam                   6%     7%     5%     4%',
        'warranty               7%     3%     2%     6%',
    ]


def test_score_by_slice_prints_the_table_the_lesson_shows(capsys):
    assert printed("score_by_slice.py", capsys) == [
        'category               wk 1     wk 2     wk 3     wk 4',
        'account                 8/8      3/3      3/3      3/3',
        'complaint              6/10      5/6     6/11     6/14',
        'order_change          13/13    14/15    16/17      6/6',
        'other                 11/11     8/10      8/8      3/3',
        'payment               11/11    12/15    12/14      7/8',
        'product_question      20/21    24/25    16/18     9/10',
        'refund                19/19    10/11      8/9    26/29',
        'return                12/18    10/11      6/9    26/35',
        'shipping_delay        20/20    14/14    34/35    21/21',
        'spam                    8/9      8/9      6/7      4/6',
        'warranty               9/10      4/4      3/3      8/8',
        'week 1: 137 of 150 = 91.3%',
        'week 2: 112 of 123 = 91.1%',
        'week 3: 118 of 134 = 88.1%',
        'week 4: 119 of 143 = 83.2%',
    ]


def test_reweight_prints_the_table_and_the_two_changes(capsys):
    assert printed("reweight.py", capsys) == [
        'category           wk 1 share wk 4 rate share*rate',
        'account                 0.053     1.000      0.053',
        'complaint               0.067     0.429      0.029',
        'order_change            0.087     1.000      0.087',
        'other                   0.073     1.000      0.073',
        'payment                 0.073     0.875      0.064',
        'product_question        0.140     0.900      0.126',
        'refund                  0.127     0.897      0.114',
        'return                  0.120     0.743      0.089',
        'shipping_delay          0.133     1.000      0.133',
        'spam                    0.060     0.667      0.040',
        'warranty                0.067     1.000      0.067',
        '',
        'week 1 as it was:               91.3%',
        "week 4 on week 1's mix:         87.5%  (week 4's rates)",
        'week 4 as it was:               83.2%',
        'change within the kinds:        -3.9%',
        'change from the mix of kinds:   -4.3%',
        "resampling week 4's emails: 81.9% to 92.2%",
    ]
