"""Lesson 06.5: grounded against correct, a number check and a recorded
judge, all scored against Arjun's labels.

No model and no network: the judge's replies are replayed from the repo.
From the top folder: make check 06.5
"""
import runpy
from pathlib import Path

import pytest

import judge_grounded
from scorecard import data
from scorecard.stats import wilson

HERE = Path(__file__).parent


def printed(name, capsys):
    """What a script in this folder prints, one string per line."""
    runpy.run_path(str(HERE / name), run_name="__main__")
    return [line.rstrip() for line in capsys.readouterr().out.splitlines()]


@pytest.fixture(scope="module")
def labels():
    return {r["id"]: r for r in data.labels("06-answers-arjun")}


def test_arjun_marked_44_of_60_answers_grounded_and_46_correct(labels):
    assert len(labels) == 60
    assert sum(r["grounded"] == "1" for r in labels.values()) == 44
    assert sum(r["correct"] == "1" for r in labels.values()) == 46
    low, high = wilson(44, 60)
    assert (round(low, 2), round(high, 2)) == (0.61, 0.83)


def test_grounded_and_correct_come_apart_41_5_3_and_11(labels):
    cells = {}
    for r in labels.values():
        key = (r["correct"] == "1", r["grounded"] == "1")
        cells[key] = cells.get(key, 0) + 1
    assert cells == {(True, True): 41, (True, False): 5,
                     (False, True): 3, (False, False): 11}


def test_number_check_py_passes_all_60_replies_and_catches_no_ungrounded_one(
        capsys):
    assert printed("number_check.py", capsys) == [
        "check passes: 60 of 60 | Arjun says grounded: 44",
        "{'tp': 44, 'fp': 16, 'fn': 0, 'tn': 0}",
        "catches 0% of the ungrounded answers; "
        "passes 100% of the grounded ones",
        "numbers not in the chunks: {}",
    ]


def test_citations_py_lists_the_six_replies_that_cite_a_page_not_shown_or_none(
        capsys):
    out = printed("citations.py", capsys)
    assert out == [
        "Q-03 cited ['returns-policy', 'jacket-size-guide'] "
        "not shown: ['returns-policy']",
        "Q-14 cited ['cancel-order', 'returns-policy'] "
        "not shown: ['returns-policy']",
        "Q-31 cited ['missing-item'] not shown: ['missing-item']",
        "Q-32 cited [] not shown: []",
        "Q-47 cited ['jacket-size-guide', 'returns-policy'] "
        "not shown: ['returns-policy']",
        "Q-56 cited [] not shown: []",
    ]


def test_the_recorded_judge_prompts_are_the_prompt_in_judge_grounded_py():
    saved = {r["id"]: r for r in data.read_jsonl(judge_grounded.OUT)}
    assert len(saved) == 60
    for case in judge_grounded.cases():
        assert judge_grounded.PROMPT.format(**case) == saved[case["id"]][
            "prompt"]


def test_the_replayed_judge_passes_31_of_60_and_four_replies_have_no_verdict(
        capsys):
    judge_grounded.report()
    assert capsys.readouterr().out.splitlines() == [
        "judge says grounded: 31 of 60 | Arjun: 44",
        "replies with no verdict line (counted as FAIL): "
        "['Q-41', 'Q-52', 'Q-53', 'Q-55']",
        "of Arjun's grounded answers the judge passes 64%; "
        "of his ungrounded it fails 81%",
        "only the 56 replies with a verdict: passes 70% of grounded, "
        "fails 81% of ungrounded",
    ]
