"""Lesson 04.5: the correction and the resample, in your own functions.

No model and no network: every verdict comes from a recorded run in the repo.
From the top folder: make check 04.5
"""
import json
import random
import runpy
from pathlib import Path

import pytest

import correct_by_hand as cbh
import judge_unlabelled
import resample
from plumbing import heldout_pairs, heldout_rates, raw_passes
from scorecard import data
from scorecard.stats import corrected_rate

HERE = Path(__file__).parent
CASES = [(0.70, 0.90, 0.80), (0.532, 0.644, 0.615), (0.50, 0.80, 0.90),
         (0.60, 0.95, 0.70), (0.45, 0.85, 0.85)]


def printed(name, capsys):
    """What a script in this folder prints, one string per line."""
    runpy.run_path(str(HERE / name), run_name="__main__")
    return [line.rstrip() for line in capsys.readouterr().out.splitlines()]


def test_the_made_up_judge_corrects_70_to_71_4():
    assert cbh.corrected(0.70, 0.90, 0.80) == pytest.approx(0.714, abs=5e-4)


def test_the_chosen_judge_corrects_53_2_to_56_8():
    tpr, tnr, _, _ = heldout_rates()
    raw = sum(raw_passes()) / len(raw_passes())
    assert cbh.corrected(raw, tpr, tnr) == pytest.approx(0.568, abs=5e-4)


@pytest.mark.parametrize("raw, tpr, tnr", CASES)
def test_the_hand_correction_agrees_with_scorecard_stats(raw, tpr, tnr):
    assert cbh.corrected(raw, tpr, tnr) == pytest.approx(
        corrected_rate(raw, tpr, tnr))


@pytest.mark.parametrize("raw, tpr, tnr", CASES)
def test_putting_the_true_rate_back_gives_the_raw_rate(raw, tpr, tnr):
    true = cbh.corrected(raw, tpr, tnr)
    assert cbh.expected_raw(true, tpr, tnr) == pytest.approx(raw)


def test_expected_raw_adds_the_good_kept_and_the_bad_let_through():
    assert cbh.expected_raw(0.5, 0.9, 0.8) == pytest.approx(0.55)
    assert cbh.expected_raw(0.0, 0.9, 0.8) == pytest.approx(0.2)


def test_rates_of_counts_passes_kept_and_fails_held_back():
    pairs = [(True, True), (True, False), (True, True), (False, False),
             (False, True), (False, False), (False, False), (False, False)]
    assert resample.rates_of(pairs) == (2 / 3, 4 / 5)


def test_rates_of_the_held_out_pairs_are_the_chosen_judges_rates():
    tpr, tnr, _, _ = heldout_rates()
    assert resample.rates_of(heldout_pairs()) == pytest.approx((tpr, tnr))


def test_one_repeat_without_resampling_is_the_corrected_rate():
    pairs, verdicts = heldout_pairs(), raw_passes()
    got = resample.one_repeat(pairs, verdicts, random.Random(7), False, False)
    assert got == pytest.approx(0.568, abs=5e-4)


def test_one_repeat_gives_no_estimate_when_the_rates_add_up_to_one():
    pairs = [(True, True)] * 3 + [(False, True)] * 3
    assert resample.one_repeat(pairs, [True, False], random.Random(7),
                               False, False) is None


def test_resampling_the_drafts_moves_the_answer_and_the_seed_repeats_it():
    pairs, verdicts = heldout_pairs(), raw_passes()
    first = [resample.one_repeat(pairs, verdicts, random.Random(7),
                                 False, True) for _ in range(2)]
    assert first[0] == first[1] != pytest.approx(0.568, abs=1e-6)


def test_correct_by_hand_prints_what_the_lesson_shows(capsys):
    assert printed("correct_by_hand.py", capsys) == [
        'made up: corrected 0.714',
        'check: 0.700 should be 0.7',
        '250 drafts, judge passes 133: raw 0.532',
        'tpr 0.644 on 59 passes, tnr 0.615 on 26 fails',
        'corrected 0.568 (scorecard: 0.568)',
    ]


def test_resample_prints_the_three_ranges_and_the_closed_form(capsys):
    assert printed("resample.py", capsys) == [
        'only the 250 drafts vary   0.352 to 0.799  (0 skipped)',
        'only the 85 labels vary    0.000 to 1.000  (29 skipped)',
        'both vary                  0.000 to 1.000  (31 skipped)',
        'closed form (scorecard)    0.060 to 1.000',
    ]


def test_barely_above_one_prints_the_table_the_lesson_shows(capsys):
    assert printed("barely_above_one.py", capsys) == [
        'raw pass rate 0.532 on 250 drafts; calibration 59 + 26',
        'rates are made up except the third row',
        '  tpr   tnr   sum  corrected  95% range',
        '0.900 0.900  1.80     0.540   0.399 to 0.648',
        '0.800 0.800  1.60     0.553   0.344 to 0.726',
        '0.644 0.615  1.26     0.568   0.060 to 1.000',
        '0.600 0.500  1.10     0.320   0.000 to 1.000',
        '0.550 0.500  1.05     0.640   0.000 to 1.000',
    ]


def test_the_sample_is_the_recorded_250_unlabelled_drafts():
    recorded = json.loads(
        (data.DATA / "runs" / "04-unlabelled" / "sample-ids.json").read_text())
    assert judge_unlabelled.sample() == recorded and len(recorded) == 250


def test_judge_unlabelled_counts_the_recorded_verdicts(capsys):
    assert printed("judge_unlabelled.py", capsys) == [
        "250 drafts; {'pass': 133, 'unsure': 57, 'fail': 51, 'none': 9}"]
