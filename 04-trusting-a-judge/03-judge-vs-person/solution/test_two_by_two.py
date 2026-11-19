"""Lesson 04.3: the two-by-two table and the two rates, in your own functions.

No model and no network: the tests read the recorded judge run in the repo.
From the top folder: make check 04.3
"""
import runpy
from pathlib import Path

import pytest

import two_by_two
from plumbing import arjun_dev, judge_v1
from scorecard.judge import confusion, rates

HERE = Path(__file__).parent


def printed(name, capsys):
    """What a script in this folder prints, one string per line."""
    runpy.run_path(str(HERE / name), run_name="__main__")
    return [line.rstrip() for line in capsys.readouterr().out.splitlines()]


def test_settle_leaves_out_unsure_and_passes_only_a_clear_pass():
    arjun = {"a": "pass", "b": "fail", "c": "unsure", "d": "pass",
             "e": "fail"}
    judge = {"a": "pass", "b": "unsure", "c": "pass", "d": "none",
             "e": "pass"}
    ids, person, judged = two_by_two.settle(arjun, judge)
    assert ids == ["a", "b", "d", "e"]
    assert person == [True, False, True, False]
    assert judged == [True, False, False, True]


def test_the_real_table_has_90_drafts_after_the_10_unsure_are_left_out():
    ids, person, judged = two_by_two.settle(arjun_dev(), judge_v1())
    assert (len(ids), sum(person), sum(judged)) == (90, 61, 51)


def test_count_cells_counts_each_kind_of_pair():
    person = [True, True, False, False, True, False]
    judged = [True, False, True, False, True, True]
    assert two_by_two.count_cells(person, judged) == {
        "tp": 2, "fp": 2, "fn": 1, "tn": 1}


def test_the_real_cells_are_38_13_23_16():
    _, person, judged = two_by_two.settle(arjun_dev(), judge_v1())
    assert two_by_two.count_cells(person, judged) == {
        "tp": 38, "fp": 13, "fn": 23, "tn": 16}


@pytest.mark.parametrize("person, judged", [
    ([True, False, True, False], [True, True, False, False]),
    ([True] * 5 + [False] * 5, [True] * 3 + [False] * 4 + [True] * 3),
    ([True, True, False, False, True], [False, True, False, False, True]),
])
def test_the_hand_counts_agree_with_scorecard_confusion(person, judged):
    assert two_by_two.count_cells(person, judged) == confusion(person, judged)


def test_rates_from_counts_is_62_3_and_55_2_on_the_real_table():
    tpr, tnr = two_by_two.rates_from_counts(
        {"tp": 38, "fp": 13, "fn": 23, "tn": 16})
    assert (round(tpr, 3), round(tnr, 3)) == (0.623, 0.552)


def test_the_catch_rate_has_the_persons_fails_as_its_base():
    tpr, tnr = two_by_two.rates_from_counts(
        {"tp": 40, "fp": 20, "fn": 10, "tn": 30})
    assert (tpr, tnr) == (0.8, 0.6)


def test_the_hand_rates_agree_with_scorecard_rates():
    _, person, judged = two_by_two.settle(arjun_dev(), judge_v1())
    c = two_by_two.count_cells(person, judged)
    assert two_by_two.rates_from_counts(c) == pytest.approx(
        rates(person, judged))


def test_two_by_two_prints_the_table_the_counts_and_the_rates(capsys):
    assert printed("two_by_two.py", capsys) == [
        'Arjun says  judge pass  fail  unsure  no line',
        'pass                38    12       8        3',
        'fail                13    14       2        0',
        'unsure               2     2       6        0',
        "{'tp': 38, 'fp': 13, 'fn': 23, 'tn': 16} on 90 drafts",
        "scorecard: {'tp': 38, 'fp': 13, 'fn': 23, 'tn': 16}",
        'passes kept 62.3%, fails held back 55.2%',
        'scorecard rates: [0.623, 0.552]',
        'accuracy 60.0%; always saying pass: 67.8%',
        'fails judged FAIL: 14 of 29',
    ]


def test_show_cells_prints_the_four_drafts_the_lesson_describes(capsys):
    out = printed("show_cells.py", capsys)
    assert [x for x in out if x.startswith("E-")] == [
        'E-0602  Sale price please',
        'E-0660  Jacket burnt near campfire',
        'E-0158  Please cancel - wrong size!',
        'E-0216  Website slow']
    assert [x.split(":")[0] for x in out
            if x.startswith(("  Arjun,", "  judge,"))] == [
        '  Arjun, fail', '  judge, pass', '  Arjun, fail', '  judge, pass',
        '  Arjun, fail', '  judge, unsure', '  Arjun, pass',
        '  judge, fail']
