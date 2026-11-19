"""Lesson 06.7, project: the scorecard's numbers, its page and its fault
list.

No model and no network: everything comes from the recorded runs and
Arjun's labels. From the top folder: make check 06.7
"""
import runpy
from pathlib import Path

import pytest

HERE = Path(__file__).parent


@pytest.fixture(scope="module")
def card():
    """rag_scorecard.py's functions, loaded without writing the page."""
    return runpy.run_path(str(HERE / "rag_scorecard.py"),
                          run_name="not_main")


@pytest.fixture
def page(tmp_path, monkeypatch, capsys):
    """Run the script in an empty folder; return the page it wrote."""
    monkeypatch.chdir(tmp_path)
    runpy.run_path(str(HERE / "rag_scorecard.py"), run_name="__main__")
    capsys.readouterr()
    return (tmp_path / "rag_scorecard.md").read_text(encoding="utf-8")


def test_a_rate_comes_with_its_95_percent_range(card):
    assert card["rng"](52, 55) == "52/55 = 95% (95% range 85% to 98%)"
    assert card["rng"](46, 60) == "46/60 = 77% (95% range 65% to 86%)"


def test_the_finding_half_is_52_of_55_with_a_mean_reciprocal_rank_of_0_91(
        card):
    assert card["finding_lines"]() == [
        "## Finding the page (55 questions with an answer)",
        "- right page in the top 3: 52/55 = 95% (95% range 85% to 98%)",
        "- mean reciprocal rank: 0.910",
        "- archived page in the top 3: 4 questions "
        "(Q-17, Q-18, Q-19, Q-24); cited in 2, wrong because of it in 2",
    ]


def test_the_using_half_is_46_correct_and_44_grounded_of_60_and_1_of_5_handled(
        card):
    assert card["using_lines"]() == [
        "## Using the page (all 60, Arjun's labels)",
        "- answer correct: 46/60 = 77% (95% range 65% to 86%)",
        "- answer grounded in the chunks shown: "
        "44/60 = 73% (95% range 61% to 83%)",
        "- questions with no answer handled correctly: 1/5",
    ]


def test_the_archived_page_alone_does_not_make_a_failure_retrieval(card):
    questions = {q["id"]: q for q in card["qs"]}
    half = card["faulty_half"]
    assert half(questions["Q-17"]) == "retrieval"    # archived and cited
    assert half(questions["Q-24"]) == "generation"   # archived, not cited
    assert half(questions["Q-03"]) == "retrieval"    # right page missing
    assert half(questions["Q-56"]) == "nothing to find"


def test_the_14_wrong_answers_split_4_retrieval_6_generation_4_nothing(card):
    lines = card["wrong_answer_lines"]()
    assert lines[0] == "## Wrong answers and the half that failed"
    halves = [line.split("(")[1].split(")")[0] for line in lines[1:]]
    assert [halves.count(h) for h in
            ("retrieval", "generation", "nothing to find")] == [4, 6, 4]


def test_each_wrong_answer_carries_arjuns_note(card):
    lines = card["wrong_answer_lines"]()
    assert lines[1].startswith("- Q-02 (generation): Free pickup is right")
    assert all(": " in line and len(line) > 40 for line in lines[1:])


def test_the_page_has_the_three_parts_in_order_and_ends_with_a_newline(page):
    heads = [line for line in page.splitlines() if line.startswith("#")]
    assert heads == ["# RAG scorecard, hd-1, 60 questions",
                     "## Finding the page (55 questions with an answer)",
                     "## Using the page (all 60, Arjun's labels)",
                     "## Wrong answers and the half that failed"]
    assert page.endswith("\n")


def test_running_the_script_twice_writes_the_same_page(
        page, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    runpy.run_path(str(HERE / "rag_scorecard.py"), run_name="__main__")
    assert (tmp_path / "rag_scorecard.md").read_text(
        encoding="utf-8") == page
