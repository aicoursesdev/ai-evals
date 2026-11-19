"""Project 01.7: failure_map.py turns coded notes into the failure map.

The tests need no model and no network:

    make check 01.7
"""

import runpy
import sys
from pathlib import Path

import failure_map
from plumbing import definitions, read
from scorecard import data

HERE = Path(__file__).parent
LABELS = data.DATA / "labels"


def small_case():
    rows = [{"id": "E-1", "ok": "no", "types": "F-a;F-b"},
            {"id": "E-2", "ok": "no", "types": "F-b"},
            {"id": "E-3", "ok": "yes", "types": ""}]
    defs = {"F-a": ("A is wrong.", "E-1"), "F-b": ("B is wrong.", "E-2")}
    return rows, defs, {"F-a": "fix", "F-b": "judge"}


def test_the_map_has_a_heading_with_the_counts_and_a_table_header():
    lines = failure_map.map_lines(*small_case())
    assert lines[0] == ("# Failure map: 3 traces read, 1 fine, "
                        "2 with at least one failure")
    assert lines[1] == ""
    assert lines[2] == ("| rank | type | traces | example | what it is | "
                        "what it needs |")
    assert lines[3] == "| --- | --- | --- | --- | --- | --- |"


def test_the_map_ranks_types_by_count_with_definition_and_decision():
    lines = failure_map.map_lines(*small_case())
    assert lines[4:] == ["| 1 | F-b | 2 | E-2 | B is wrong. | judge |",
                         "| 2 | F-a | 1 | E-1 | A is wrong. | fix |"]


def test_the_course_s_map_starts_with_the_three_biggest_types(
        capsys, monkeypatch):
    monkeypatch.setattr(sys, "argv", [
        "failure_map.py", str(LABELS / "01-coded.csv"),
        str(LABELS / "01-failure-types.md")])
    runpy.run_path(str(HERE / "failure_map.py"), run_name="__main__")
    lines = capsys.readouterr().out.splitlines()
    assert lines[0] == ("# Failure map: 100 traces read, 23 fine, "
                        "77 with at least one failure")
    assert len(lines) == 4 + 11
    cells = [[c.strip() for c in l.strip("|").split("|")][:4]
             for l in lines[4:]]
    assert cells[:3] == [["1", "F-overreach", "21", "E-0498"],
                         ["2", "F-misread", "21", "E-0473"],
                         ["3", "F-wrong-rule", "15", "E-0158"]]
    assert cells[-1] == ["11", "F-no-draft", "1", "E-0722"]


def test_every_type_in_the_course_s_notes_has_a_decision():
    types = set(definitions(LABELS / "01-failure-types.md"))
    assert types <= set(failure_map.DECISION)
    rows = read(LABELS / "01-coded.csv")
    lines = failure_map.map_lines(
        rows, definitions(LABELS / "01-failure-types.md"),
        failure_map.DECISION)
    assert not any("decide: fix, check or judge" in l for l in lines)
