"""Lesson 03.2: the four hand-written checks and the two help desk checks.

The tests need no model and no network:

    make check 03.2
"""

import json
import runpy
from pathlib import Path

import pytest

import hand_checks
import own_checks
from scorecard import data

HERE = Path(__file__).parent
SCRIPTS = ("four_cases.py", "own_checks.py", "flag_all.py")


def output_of(name, capsys):
    runpy.run_path(str(HERE / name), run_name="__main__")
    return capsys.readouterr().out.splitlines()


def test_exact_ignores_spaces_at_the_ends_and_nothing_else():
    assert hand_checks.exact(" refund \n", "refund")
    assert not hand_checks.exact("Refund", "refund")


def test_pattern_finds_the_shape_anywhere_in_the_text():
    regex = r"TW-\d{5}"
    assert hand_checks.pattern("your order TW-10279 is on its way", regex)
    assert not hand_checks.pattern("your order TW-1028 is on its way", regex)


def test_schema_needs_every_key_and_an_allowed_value():
    allowed = {"urgency": {"low", "high"}, "needs_human": {True, False}}
    assert hand_checks.schema({"urgency": "low", "needs_human": True},
                              allowed)
    assert not hand_checks.schema({"urgency": "urgent",
                                   "needs_human": True}, allowed)
    assert not hand_checks.schema({"urgency": "low"}, allowed)


def test_within_accepts_a_gap_no_bigger_than_the_tolerance():
    assert hand_checks.within(10.04, 10, tolerance=0.05)
    assert not hand_checks.within(10.06, 10, tolerance=0.05)
    assert not hand_checks.within(171, 2000 - 1839, tolerance=0)


def test_no_draft_fires_on_an_empty_or_blank_draft_only():
    assert own_checks.no_draft({"draft": ""})
    assert own_checks.no_draft({"draft": "  \n"})
    assert not own_checks.no_draft({"draft": "Hello"})


def test_writes_to_spam_needs_the_spam_label_and_a_reply():
    spam = {"category": "spam"}
    assert own_checks.writes_to_spam({"triage": spam, "draft": "Hi"})
    assert not own_checks.writes_to_spam({"triage": spam, "draft": ""})
    refund = {"category": "refund"}
    assert not own_checks.writes_to_spam({"triage": refund, "draft": "Hi"})


def test_four_cases_prints_what_the_lesson_shows(capsys):
    assert output_of("four_cases.py", capsys) == [
        "exact   : True", "schema  : True", "pattern : False",
        "within  : False (says 171 )"]


def test_own_checks_prints_the_counts_the_lesson_shows(capsys):
    assert output_of("own_checks.py", capsys) == [
        "no_draft        fires on 1 of 550",
        "writes_to_spam  fires on 27 of 550"]


def test_flag_all_prints_the_table_the_lesson_shows(capsys):
    assert output_of("flag_all.py", capsys) == [
        "check                 wk1  wk2  wk3  wk4  total",
        "wrong script            4    1    2    2      9",
        "missing or old page    13   17   16    6     52",
        "reply to spam           8    9    6    4     27",
        "invented address        2    1    1    0      4",
        "claims an action        1    4    6    4     15",
        "asks for known id      12    3    9   15     39",
        "empty draft             0    0    0    1      1"]


def test_the_guard_stops_a_parse_of_a_sealed_trace():
    # A made-up line: no real sealed trace is opened to test the guard.
    sealed = data.testset("sealed")[0]["id"]
    line = json.dumps({"id": sealed, "triage": {}, "draft": ""})
    with pytest.raises(pytest.fail.Exception):
        json.loads(line)


def test_no_script_parses_a_sealed_trace(capsys):
    for name in SCRIPTS:  # the guard in ../conftest.py fails the test
        runpy.run_path(str(HERE / name), run_name="__main__")
