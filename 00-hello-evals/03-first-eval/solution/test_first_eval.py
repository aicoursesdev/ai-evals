"""Lesson 00.3: your first eval, and the run.py you write for it.

The tests need no model and no network:

    make check 00.3
"""

import runpy
from pathlib import Path

import pytest

import run
from scorecard import run as course_run

HERE = Path(__file__).parent


def output_of(name, capsys):
    runpy.run_path(str(HERE / name), run_name="__main__")
    return capsys.readouterr().out


def test_first_eval_py_scores_42_of_50_which_is_84_percent(capsys):
    assert output_of("first_eval.py", capsys).splitlines() == [
        "42 of 50 right", "accuracy 84.0%"]


def test_the_grader_says_right_only_when_the_category_matches_arjuns():
    grader = runpy.run_path(str(HERE / "first_eval.py"))["grader"]
    assert grader("refund", {"category": "refund"}) is True
    assert grader("return", {"category": "refund"}) is False


def test_always_answering_product_question_would_get_7_of_50(capsys):
    first = output_of("baseline.py", capsys).splitlines()[0]
    assert first == "always 'product_question': 7 of 50 right (14%)"


def test_misses_py_lists_the_8_emails_the_help_desk_got_wrong(capsys):
    lines = output_of("misses.py", capsys).splitlines()
    assert [line.split()[0] for line in lines] == [
        "E-0047", "E-0054", "E-0098", "E-0122",
        "E-0123", "E-0125", "E-0138", "E-0142"]


def test_run_gives_one_row_per_case_with_a_true_or_false_per_grader():
    rows = run.run(
        [{"id": "a", "x": 1}, {"id": "b", "x": 2}],
        system=lambda case: case["x"],
        graders={"odd": lambda out, case: out % 2, "big": lambda o, c: o > 1},
    )
    assert rows == [{"id": "a", "output": 1, "odd": True, "big": False},
                    {"id": "b", "output": 2, "odd": False, "big": True}]


def test_save_then_load_gives_back_the_same_rows(tmp_path):
    rows = [{"id": "E-0001", "output": "कहाँ", "ok": True},
            {"id": "E-0002", "output": "refund", "ok": False}]
    path = tmp_path / "rows.jsonl"
    run.save(rows, path)
    assert len(path.read_text(encoding="utf-8").splitlines()) == 2
    assert "कहाँ" in path.read_text(encoding="utf-8")
    assert run.load(path) == rows


def test_pass_rate_is_the_share_of_rows_the_named_grader_passed():
    assert run.pass_rate([{"g": True}, {"g": False}], "g") == 0.5
    assert run.pass_rate([{"g": True}] * 4, "g") == 1.0


def test_your_run_py_agrees_with_the_course_s_scorecard_run_py(tmp_path):
    cases = [{"id": i, "n": i} for i in range(6)]
    args = (cases, lambda c: c["n"] * 2, {"big": lambda o, c: o > 5})
    assert run.run(*args) == course_run.run(*args)
    assert run.pass_rate(run.run(*args), "big") == pytest.approx(
        course_run.pass_rate(course_run.run(*args), "big"))


def test_score_launch_py_saves_50_rows_and_reads_back_a_pass_rate_of_0_84(
        capsys, monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    lines = output_of("score_launch.py", capsys).splitlines()
    assert lines[0] == "50 rows saved and read back"
    assert lines[1] == ("first row: {'id': 'E-0004', 'output': "
                        "'product_question', 'category': True}")
    assert lines[2] == "pass rate: 0.84"
    assert len(run.load(tmp_path / "launch-test.jsonl")) == 50
