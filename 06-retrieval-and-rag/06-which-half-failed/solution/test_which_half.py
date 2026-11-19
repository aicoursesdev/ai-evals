"""Lesson 06.6: the two-by-two of page fetched against answer right, and the
half that failed for each of the 14 wrong answers.

No model and no network: the tests read the recorded run and Arjun's labels.
From the top folder: make check 06.6
"""
import runpy
from pathlib import Path

HERE = Path(__file__).parent


def run(name, capsys):
    """A script's globals and what it printed, one string per line."""
    names = runpy.run_path(str(HERE / name), run_name="__main__")
    return names, [x.rstrip() for x in capsys.readouterr().out.splitlines()]


def test_the_two_by_two_counts_44_8_1_and_2(capsys):
    _, out = run("two_by_two.py", capsys)
    assert out[:3] == [
        "                     answer right   answer wrong",
        "right page fetched        44              8",
        "right page missing         1              2",
    ]


def test_the_two_by_two_names_the_questions_in_the_three_cells_that_matter(
        capsys):
    _, out = run("two_by_two.py", capsys)
    assert out[3:] == [
        "(True, False) ['Q-02', 'Q-17', 'Q-18', 'Q-23', 'Q-24', 'Q-26', "
        "'Q-47', 'Q-55']",
        "(False, False) ['Q-03', 'Q-31']",
        "(False, True) ['Q-32']",
    ]


def test_the_rule_names_retrieval_when_page_missing_or_archived_cited(
        capsys):
    names, _ = run("sort_failures.py", capsys)
    questions = {q["id"]: q for q in names["data"].questions()}
    half = names["half_that_failed"]
    assert half(questions["Q-03"]).startswith("retrieval")      # not in top 3
    assert half(questions["Q-17"]).startswith("retrieval")     # archived
    assert half(questions["Q-24"]).startswith("generation")     # not cited
    assert half(questions["Q-56"]).startswith("no page")        # no answer


def test_sort_failures_py_sorts_14_wrong_answers_into_4_6_and_4(capsys):
    _, out = run("sort_failures.py", capsys)
    assert out == [
        "Q-02 | generation: the right page was there",
        "Q-03 | retrieval: the right page was not in the top 3",
        "Q-17 | retrieval: the archived page was fetched and cited",
        "Q-18 | retrieval: the archived page was fetched and cited",
        "Q-23 | generation: the right page was there",
        "Q-24 | generation: the right page was there",
        "Q-26 | generation: the right page was there",
        "Q-31 | retrieval: the right page was not in the top 3",
        "Q-47 | generation: the right page was there",
        "Q-55 | generation: the right page was there",
        "Q-56 | no page can help: the reply should say it does not know",
        "Q-58 | no page can help: the reply should say it does not know",
        "Q-59 | no page can help: the reply should say it does not know",
        "Q-60 | no page can help: the reply should say it does not know",
        "14 wrong answers; 4 retrieval, 6 generation, 4 with nothing to find",
    ]
