"""Lesson 00.6: the first scorecard's numbers, and its five open questions.

The tests need no model and no network:

    make check 00.6
"""

import re
from pathlib import Path

import pytest

import scorecard_v1
from scorecard import data, run

HERE = Path(__file__).parent


def test_triage_score_gives_one_row_per_email_marked_on_the_category():
    emails = [{"id": "a", "category": "refund"},
              {"id": "b", "category": "return"}]
    traces = [{"id": "a", "triage": {"category": "refund"}},
              {"id": "b", "triage": {"category": "refund"}}]
    rows = scorecard_v1.triage_score(emails, traces)
    assert rows == [{"id": "a", "output": "refund", "category": True},
                    {"id": "b", "output": "refund", "category": False}]


def test_triage_score_on_the_test_split_is_42_of_50():
    test = [e for e in data.emails(launch=True) if e["split"] == "test"]
    rows = scorecard_v1.triage_score(test, data.traces("hd-1", launch=True))
    assert (sum(r["category"] for r in rows), len(rows)) == (42, 50)
    assert run.pass_rate(rows, "category") == pytest.approx(0.84)


def test_triage_score_on_week_1_is_137_of_150():
    rows = scorecard_v1.triage_score(
        data.emails(week=1), data.traces("hd-1", week=1))
    assert (sum(r["category"] for r in rows), len(rows)) == (137, 150)


def test_main_prints_the_scorecard_the_lesson_shows(
        capsys, monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    scorecard_v1.main()
    assert capsys.readouterr().out.splitlines() == [
        "Triage accuracy (category), help desk hd-1",
        "  Kiran's test split : 42 of 50 = 84.0%",
        "  Week 1 of the log  : 137 of 150 = 91.3%",
        "  Gap (week 1 minus test): +7.3 points",
        "  Week 1 in three slices of 50: 47, 47, 43 right",
    ]


def test_main_saves_both_sets_of_rows_for_later_lessons(
        capsys, monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    scorecard_v1.main()
    assert len(run.load("kiran-test.jsonl")) == 50
    assert len(run.load("week-1.jsonl")) == 150


def test_scorecard_md_names_both_counts_and_asks_five_questions():
    text = (HERE / "scorecard.md").read_text(encoding="utf-8")
    assert "42 of 50" in text and "137 of 150" in text
    questions = re.findall(r"^\d\.\s.*\?\s*$", text, re.M)
    assert len(questions) >= 5, (
        "scorecard.md needs five numbered questions, each ending in '?'")
