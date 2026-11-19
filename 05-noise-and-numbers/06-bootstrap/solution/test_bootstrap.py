"""Lesson 05.6: the bootstrap, in your own functions.

No model and no network: the tests read the recorded drafts in the repo.
From the top folder: make check 05.6
"""
import random
import runpy
from pathlib import Path

import pytest

import bootstrap_by_hand
import clumps
import median_length
from scorecard import stats

HERE = Path(__file__).parent
mean = lambda v: sum(v) / len(v)


def printed(name, capsys):
    """What a script in this folder prints, one string per line."""
    runpy.run_path(str(HERE / name), run_name="__main__")
    return [line.rstrip() for line in capsys.readouterr().out.splitlines()]


def test_resampling_identical_slips_always_gives_that_slip():
    got = bootstrap_by_hand.resample_stats(
        [1] * 10, mean, random.Random(1), 50)
    assert got == [1.0] * 50


def test_resampled_means_come_back_sorted_one_per_repeat_and_in_range():
    got = bootstrap_by_hand.resample_stats(
        [0, 1, 1, 0, 1], mean, random.Random(1), 200)
    assert len(got) == 200 and got == sorted(got)
    assert 0 <= got[0] < 0.6 < got[-1] <= 1


def test_each_resample_is_as_long_as_the_original():
    sizes = []
    bootstrap_by_hand.resample_stats(
        list(range(7)), lambda d: sizes.append(len(d)) or 0,
        random.Random(1), 5)
    assert sizes == [7] * 5


def test_the_middle_95_of_10000_resamples_matches_scorecard_stats():
    diffs = [1] * 27 + [-1] * 12 + [0] * 238     # the 277 paired changes
    got = bootstrap_by_hand.resample_stats(diffs, mean, random.Random(7))
    assert (got[250], got[9749]) == stats.bootstrap(diffs, mean, seed=7)


def test_the_median_gap_is_hd_2s_median_minus_hd_1s():
    rows = [(10, 20), (20, 30), (30, 70)]    # (hd-1 words, hd-2 words)
    assert median_length.median_gap(rows) == 30 - 20


def test_a_longer_hd_2_gives_a_positive_gap():
    assert median_length.median_gap([(5, 9), (6, 9), (7, 9)]) == 3


def test_group_by_collects_the_ids_for_each_key_in_order_seen():
    assert clumps.group_by([1, 2, 3, 4, 5], lambda i: i % 2) == {
        1: [1, 3, 5], 0: [2, 4]}


def test_the_mean_of_clumps_pools_the_cases_not_the_clump_means():
    # one clump of two passes and one of a single fail: 2 of 3, not 1/2
    assert clumps.mean_of_clumps([[1, 1], [0]]) == pytest.approx(2 / 3)


def test_bootstrap_by_hand_prints_the_four_lines_the_lesson_shows(capsys):
    assert printed("bootstrap_by_hand.py", capsys) == [
        '277 pairs; the mean difference is 0.0542',
        'the 10,000 resampled means run from -2.5% to +13.7%',
        'by hand: 2.5th to 97.5th percentile +1.1% to +9.7%',
        'bootstrap(): +1.1% to +9.7%',
    ]


def test_median_length_prints_the_gap_and_its_range(capsys):
    assert printed("median_length.py", capsys) == [
        'median words: hd-1 89  hd-2 70',
        'median gap: -19',
        'bootstrap range for the gap: -22 to -16 words',
    ]


def test_clumps_prints_the_senders_and_both_ranges(capsys):
    assert printed("clumps.py", capsys) == [
        'senders by how many emails they sent: {1: 493, 2: 21, 3: 5}',
        '  E-0154 revathi.gupta@example.in | Storm Pro still not here',
        '  E-0511 revathi.gupta@example.in | Storm Pro - parcel stuck',
        ('  E-0622 revathi.gupta@example.in | Storm Pro parcel decla'
         'red lost - refund please'),
        'hd-1, no check firing: 75.6% of 550',
        'resample emails: 72.0% to 79.1%',
        'resample senders: 72.1% to 79.2%',
        'standard error, as if independent: 0.0183  by sender: 0.0183',
    ]


def test_simulated_clumps_prints_the_seeded_simulation(capsys):
    assert printed("simulated_clumps.py", capsys) == [
        '500 emails, 74.8% pass',
        'standard error as if independent: 0.0194',
        'standard error by customer:       0.0257',
        'resample emails:    71.0% to 78.6%',
        'resample customers: 69.6% to 79.8%',
    ]
