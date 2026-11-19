"""Lesson 03.4: the failure map as eleven yes-or-no questions.

The tests need no model and no network:

    make check 03.4
"""

import runpy
from collections import Counter
from pathlib import Path

import one_question_each as q

HERE = Path(__file__).parent


def output_of(name, capsys):
    runpy.run_path(str(HERE / name), run_name="__main__")
    return capsys.readouterr().out.splitlines()


def test_yes_counts_adds_one_for_each_type_a_draft_holds():
    coded = {"a": {"F-x", "F-y"}, "b": {"F-x"}, "c": set()}
    assert q.yes_counts(coded) == Counter({"F-x": 2, "F-y": 1})
    assert q.yes_counts({}) == Counter()


def test_yes_per_draft_counts_drafts_by_their_number_of_yes_answers():
    coded = {"a": {"F-x", "F-y"}, "b": {"F-x"}, "c": set(), "d": {"F-z"}}
    assert q.yes_per_draft(coded) == Counter({0: 1, 1: 2, 2: 1})


def test_the_maps_counts_are_the_ones_the_lesson_shows():
    coded = q.plumbing.coded()
    assert q.yes_counts(coded).most_common(3) == [
        ("F-overreach", 21), ("F-misread", 21), ("F-wrong-rule", 15)]
    assert sorted(q.yes_per_draft(coded).items()) == [
        (0, 23), (1, 53), (2, 20), (3, 4)]


def test_one_question_each_prints_what_the_lesson_shows(capsys):
    assert output_of("one_question_each.py", capsys) == [
        "question: does the draft have this failure?",
        "  F-overreach        yes on 21 of 100",
        "  F-misread          yes on 21 of 100",
        "  F-wrong-rule       yes on 15 of 100",
        "  F-bluff            yes on 14 of 100",
        "  F-asks-again       yes on 12 of 100",
        "  F-spam-reply       yes on  7 of 100",
        "  F-wrong-page       yes on  5 of 100",
        "  F-off-topic        yes on  5 of 100",
        "  F-language         yes on  3 of 100",
        "  F-obeys-injection  yes on  1 of 100",
        "  F-no-draft         yes on  1 of 100",
        "no on all eleven: 23 of 100 drafts",
        "drafts by number of yes answers: [(0, 23), (1, 53), (2, 20), (3, 4)]"]


def test_no_script_parses_a_sealed_trace(capsys):
    # The guard in ../conftest.py fails the test; this script reads only
    # the failure map, never a trace.
    output_of("one_question_each.py", capsys)
