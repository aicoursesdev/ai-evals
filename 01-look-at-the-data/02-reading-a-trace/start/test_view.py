"""Lesson 01.2: view.py finds one email and its trace, then shows them.

The tests need no model and no network:

    make check 01.2
"""

import runpy
import sys
from pathlib import Path

import pytest

import view
from scorecard import data

HERE = Path(__file__).parent


def fake_log(monkeypatch):
    """Two weeks of two emails each; week 2 has an email without a trace."""
    emails = {1: [{"id": "E-1"}, {"id": "E-2"}],
              2: [{"id": "E-3"}, {"id": "E-4"}], 3: [], 4: []}
    traces = {1: [{"id": "E-1"}, {"id": "E-2"}], 2: [{"id": "E-3"}],
              3: [], 4: []}
    monkeypatch.setattr(view.data, "emails", lambda week: emails[week])
    monkeypatch.setattr(view.data, "traces",
                        lambda version, week: traces[week])


def test_find_returns_the_email_and_its_trace_from_the_right_week(monkeypatch):
    fake_log(monkeypatch)
    assert view.find("E-3") == ({"id": "E-3"}, {"id": "E-3"})
    assert view.find("E-1")[0] is not view.find("E-2")[0]


def test_find_stops_with_a_plain_message_for_an_unknown_id(monkeypatch):
    fake_log(monkeypatch)
    with pytest.raises(SystemExit) as stop:
        view.find("E-9")
    assert stop.value.code == "no email called E-9"


def test_find_stops_when_the_email_has_no_recorded_trace(monkeypatch):
    fake_log(monkeypatch)
    with pytest.raises(SystemExit) as stop:
        view.find("E-4")
    assert stop.value.code == "E-4 has no recorded trace yet"


def test_find_opens_the_trace_the_lesson_walks_through():
    email, trace = view.find("E-0185")
    assert email["subject"] == "COD for tent?"
    assert trace["triage"] == {"category": "payment", "urgency": "normal",
                               "needs_human": False}
    assert [h["article_id"] for h in trace["retrieved"]] == [
        "shipping-india-2024", "shipping-india", "shipping-india-2024"]


def test_view_py_prints_what_the_lesson_shows_for_e_0185(capsys, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["view.py", "E-0185"])
    runpy.run_path(str(HERE / "view.py"), run_name="__main__")
    lines = capsys.readouterr().out.splitlines()
    assert lines[0] == "E-0185  week 1  en  from Sanjeev Kumar"
    assert lines[1] == "Subject: COD for tent?"
    assert lines[6:9] == [
        "Arjun's labels : {'category': 'payment', 'urgency': 'normal', "
        "'needs_human': False}",
        "Help desk said : {'category': 'payment', 'urgency': 'normal', "
        "'needs_human': False}",
        ""]
    assert lines[10:13] == [
        "  shipping-india-2024    0.62  Shipping within India",
        "  shipping-india         0.61  Shipping within India",
        "  shipping-india-2024    0.52  Shipping within India"]
    assert lines[-1].startswith("Cited:")
