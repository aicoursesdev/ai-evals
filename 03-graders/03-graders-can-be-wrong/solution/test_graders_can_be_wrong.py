"""Lesson 03.3: test the graders themselves, with cases you already know.

The tests need no model and no network:

    make check 03.3
"""

import runpy
from pathlib import Path

import pytest

import check_cases
import old_limit
from grader_cases import CASES
from scorecard.graders import CHECKS

HERE = Path(__file__).parent
SCRIPTS = ("number_graders.py", "measure.py", "check_cases.py",
           "old_limit.py", "before_the_fix.py")


def output_of(name, capsys):
    runpy.run_path(str(HERE / name), run_name="__main__")
    return capsys.readouterr().out.splitlines()


def draft(text):
    return {"draft": text}


def test_naive_fires_whenever_the_old_limit_is_written():
    assert old_limit.naive(draft("free over ₹1,500"))
    assert not old_limit.naive(draft("free over ₹2,000"))


def test_fixed_fires_on_the_old_limit_unless_the_new_one_is_there_too():
    assert old_limit.fixed(draft("free over ₹1,500"))
    assert old_limit.fixed(draft("free over ₹ 1500 today"))
    assert not old_limit.fixed(draft("free over ₹2,000, not ₹1,500"))
    assert not old_limit.fixed(draft("free over ₹2,000"))
    assert not old_limit.fixed(draft("a ₹15,000 order"))


def test_run_cases_lists_the_wrong_ones_and_the_gaps_apart():
    fires_on_hi = lambda email, trace: trace["draft"] == "hi"
    cases = [("fires", {}, draft("hi"), True),
             ("quiet", {}, draft("yo"), False),
             ("wrong", {}, draft("hi"), False),
             ("GAP: misses", {}, draft("yo"), True)]
    wrong, gaps = check_cases.run_cases(fires_on_hi, cases)
    assert wrong == [("wrong", False)]
    assert gaps == ["GAP: misses"]


def test_run_cases_treats_a_closed_gap_as_an_ordinary_right_case():
    fires = lambda email, trace: True
    wrong, gaps = check_cases.run_cases(
        fires, [("GAP: now caught", {}, draft("x"), True)])
    assert wrong == [] and gaps == []


@pytest.mark.parametrize("name", ["reply to spam", "empty draft"])
def test_your_cases_hold_one_that_fires_one_that_does_not_and_all_agree(name):
    cases = CASES[name]
    wants = {want for *_, want in cases}
    assert wants == {True, False}, (
        f"TODO 03.3: write at least one case that should fire and one "
        f"that should not for {name!r}, see the lesson's 'Test the "
        f"grader itself' section")
    wrong, gaps = check_cases.run_cases(CHECKS[name][0], cases)
    assert wrong == [] and gaps == []


def test_number_graders_prints_the_table_the_lesson_shows(capsys):
    assert output_of("number_graders.py", capsys) == [
        "answer       exact  close_to  contains",
        "96.124991    True   True       True",
        "96.12        False  True       True",
        "96.1         False  False      False",
        "96.20        False  False      False",
        "not 96.12    False  False      True"]


def test_old_limit_prints_the_two_drafts_the_lesson_names(capsys):
    assert output_of("old_limit.py", capsys) == [
        "naive  fires on 2: E-0185, E-0505",
        "fixed  fires on 1: E-0185"]


def test_check_cases_prints_the_lines_the_lesson_shows(capsys):
    assert output_of("check_cases.py", capsys) == [
        "wrong script         4 of 4 right",
        "missing or old page  4 of 4 right",
        "reply to spam        3 of 3 right",
        "invented address     4 of 4 right",
        "claims an action     3 of 3 right "
        "(known gap: GAP: promises in other words)",
        "asks for known id    4 of 4 right",
        "empty draft          3 of 3 right"]


def test_before_the_fix_shows_the_two_bugs_the_cases_found(capsys):
    assert output_of("before_the_fix.py", capsys) == [
        "wrong script: wrong on 'Tamil email, no draft (E-0722)': "
        "fired True",
        "asks for known id: wrong on 'asks only guests (E-0745)': "
        "fired True"]


def test_measure_prints_precision_and_recall_for_the_seven_checks(capsys):
    assert output_of("measure.py", capsys) == [
        "check                flags right real caught  precision  recall",
        "wrong script             2     2    3      2       100%     67%",
        "missing or old page     10     8   19      8        80%     42%",
        "reply to spam            6     6    7      6       100%     86%",
        "invented address         2     2   14      2       100%     14%",
        "claims an action        10    10   21     10       100%     48%",
        "asks for known id        6     6   12      6       100%     50%",
        "empty draft              1     1    1      1       100%    100%"]


def test_no_script_parses_a_sealed_trace(capsys):
    for name in SCRIPTS:  # the guard in ../conftest.py fails the test
        runpy.run_path(str(HERE / name), run_name="__main__")
