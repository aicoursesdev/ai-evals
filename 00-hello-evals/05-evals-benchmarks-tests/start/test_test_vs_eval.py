"""Lesson 00.5: a test of the parser, and an eval of the help desk.

The tests need no model and no network:

    make check 00.5
"""

import runpy
from pathlib import Path

from helpdesk.pipeline import parse_triage

HERE = Path(__file__).parent


def test_the_script_prints_both_lines_the_lesson_shows(capsys):
    runpy.run_path(str(HERE / "a_test_and_an_eval.py"), run_name="__main__")
    assert capsys.readouterr().out.splitlines() == [
        "tests pass: the parser reads good JSON and spots a chatty reply",
        "eval: 137 of 150 week-1 emails sorted as Arjun did",
    ]


def test_the_parser_reads_good_json():
    labels, error = parse_triage(
        '{"category": "refund", "urgency": "high", "needs_human": true}')
    assert error is None
    assert labels == {"category": "refund", "urgency": "high",
                      "needs_human": True}


def test_the_parser_spots_a_chatty_reply_that_is_not_json():
    _, error = parse_triage("Sure! This looks like a refund request.")
    assert error == "reply is not JSON"


def test_the_parser_names_a_category_that_is_not_one_of_the_eleven():
    _, error = parse_triage(
        '{"category": "greeting", "urgency": "low", "needs_human": false}')
    assert error == "unknown category 'greeting'"


def test_137_of_150_is_91_percent_not_a_pass_or_a_fail_yet():
    assert round(137 / 150 * 100, 1) == 91.3
