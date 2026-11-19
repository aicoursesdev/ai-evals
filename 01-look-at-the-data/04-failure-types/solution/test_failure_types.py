"""Lesson 01.4: check_types.py finds where notes and definitions disagree.

The tests need no model and no network:

    make check 01.4
"""

import runpy
import sys
from pathlib import Path

import pytest

import check_types
from plumbing import coded_rows, defined_types
from scorecard import data

HERE = Path(__file__).parent
LABELS = data.DATA / "labels"


def row(id, ok, types=""):
    return {"id": id, "ok": ok, "types": types}


def test_a_clean_sheet_has_no_problems():
    rows = [row("E-1", "no", "F-a"), row("E-2", "no", "F-a;F-b"),
            row("E-3", "yes")]
    assert check_types.problems(rows, {"F-a", "F-b"}) == []


def test_a_failed_trace_needs_a_type():
    rows = [row("E-1", "no"), row("E-2", "no", "F-a")]
    assert check_types.problems(rows, {"F-a"}) == [
        "E-1: failed but has no type"]


def test_a_fine_trace_has_no_types():
    rows = [row("E-1", "yes", "F-a"), row("E-2", "no", "F-a")]
    assert check_types.problems(rows, {"F-a"}) == [
        "E-1: fine but has types ['F-a']"]


def test_every_type_used_must_be_defined():
    rows = [row("E-1", "no", "F-a;F-x")]
    assert check_types.problems(rows, {"F-a"}) == [
        "E-1: F-x is not defined"]


def test_every_type_defined_must_be_used():
    rows = [row("E-1", "no", "F-a")]
    assert check_types.problems(rows, {"F-a", "F-b"}) == [
        "F-b is defined but never used"]


def test_the_course_s_notes_and_definitions_agree():
    rows = coded_rows(LABELS / "01-coded.csv")
    defined = defined_types(LABELS / "01-failure-types.md")
    assert len(rows) == 100 and len(defined) == 11
    assert check_types.problems(rows, defined) == []


def test_a_definitions_file_with_one_type_shows_the_other_ten_as_missing():
    rows = coded_rows(LABELS / "01-coded.csv")
    bad = check_types.problems(rows, {"F-bluff"})
    assert "E-0154: F-overreach is not defined" in bad
    assert not any("F-bluff" in line for line in bad)


def test_check_types_py_prints_100_rows_and_0_problems(capsys, monkeypatch):
    monkeypatch.setattr(sys, "argv", [
        "check_types.py", str(LABELS / "01-coded.csv"),
        str(LABELS / "01-failure-types.md")])
    with pytest.raises(SystemExit) as stop:
        runpy.run_path(str(HERE / "check_types.py"), run_name="__main__")
    assert stop.value.code == 0
    assert capsys.readouterr().out == "100 rows; 0 problems\n"
