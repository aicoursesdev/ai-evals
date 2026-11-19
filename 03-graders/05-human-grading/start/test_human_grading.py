"""Lesson 03.5: Arjun's calls, the first guess and what reading moved.

The tests need no model and no network:

    make check 03.5
"""

import runpy
from collections import Counter
from pathlib import Path

import first_guess
from scorecard import data

HERE = Path(__file__).parent


def output_of(name, capsys):
    runpy.run_path(str(HERE / name), run_name="__main__")
    return capsys.readouterr().out.splitlines()


def row(call, types):
    return {"call": call, "types": types}


def test_call_fails_a_wrong_rule_draft_even_when_it_has_other_types():
    assert first_guess.call(["F-wrong-rule"]) == "fail"
    assert first_guess.call(["F-bluff", "F-wrong-rule"]) == "fail"


def test_call_is_unsure_when_no_page_answers_or_there_is_no_draft():
    assert first_guess.call(["F-bluff"]) == "unsure"
    assert first_guess.call(["F-no-draft"]) == "unsure"


def test_call_passes_everything_else_and_a_draft_with_no_types():
    assert first_guess.call(["F-overreach", "F-asks-again"]) == "pass"
    assert first_guess.call([""]) == "pass"


def test_moved_to_counts_only_calls_that_differ_from_the_first_guess():
    rows = [row("fail", "F-wrong-rule"),  # same as the guess
            row("fail", "F-wrong-page"),  # moved to fail
            row("fail", ""), row("pass", "F-bluff"),
            row("unsure", "F-bluff")]  # same as the guess
    assert first_guess.moved_to(rows) == Counter({"fail": 2, "pass": 1})
    assert first_guess.moved_to([]) == Counter()


def test_the_first_guess_with_the_changes_on_top_is_the_calls_file():
    rows = data.labels("03-right-rule-arjun")
    moved = {c["id"]: c["call"] for c in data.labels("03-right-rule-changes")}
    rebuilt = {r["id"]: moved.get(r["id"])
               or first_guess.call(r["types"].split(";")) for r in rows}
    assert rebuilt == {r["id"]: r["call"] for r in rows}
    assert len(rows) == 100 and len(moved) == 22


def test_the_courses_calls_and_moves_are_the_ones_the_lesson_shows():
    rows = data.labels("03-right-rule-arjun")
    assert Counter(r["call"] for r in rows) == {
        "pass": 61, "fail": 29, "unsure": 10}
    assert first_guess.moved_to(rows) == {"fail": 14, "pass": 6, "unsure": 2}


def test_first_guess_py_prints_what_the_lesson_shows(capsys):
    assert output_of("first_guess.py", capsys) == [
        "first guess: {'unsure': 15, 'pass': 70, 'fail': 15}",
        "Arjun's calls: {'unsure': 10, 'fail': 29, 'pass': 61}",
        "moved to: {'fail': 14, 'pass': 6, 'unsure': 2}"]


def test_show_calls_prints_four_calls_with_arjuns_notes(capsys):
    lines = output_of("show_calls.py", capsys)
    assert lines[0] == "{'unsure': 10, 'fail': 29, 'pass': 61}"
    heads = [x for x in lines if x.startswith(("fail:", "pass:", "unsure:"))]
    assert [h.split()[:2] for h in heads] == [
        ["fail:", "E-0158"], ["unsure:", "E-0151"], ["pass:", "E-0156"],
        ["fail:", "E-0185"]]


def test_no_script_parses_a_sealed_trace(capsys):
    # The guard in ../conftest.py fails the test. derive_arjun.py is not
    # run: it rewrites the calls file.
    for name in ("first_guess.py", "show_calls.py"):
        runpy.run_path(str(HERE / name), run_name="__main__")
