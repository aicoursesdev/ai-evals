"""Lesson 01.5: count the failure types, rank them, see when each appeared.

The tests need no model and no network:

    make check 01.5
"""

import runpy
import sys
from collections import Counter
from pathlib import Path

import count
import saturation
from plumbing import read
from scorecard import data

HERE = Path(__file__).parent
CODED = data.DATA / "labels" / "01-coded.csv"


def row(types):
    return {"types": types}


def output_of(name, capsys, monkeypatch):
    monkeypatch.setattr(sys, "argv", [name, str(CODED)])
    runpy.run_path(str(HERE / name), run_name="__main__")
    return capsys.readouterr().out.splitlines()


def test_types_of_splits_on_semicolons_and_a_fine_trace_has_none():
    assert count.types_of(row("F-a;F-b")) == {"F-a", "F-b"}
    assert count.types_of(row("F-a")) == {"F-a"}
    assert count.types_of(row("")) == set()


def test_count_counts_traces_so_a_trace_with_two_types_counts_twice():
    rows = [row("F-a;F-b"), row("F-a"), row(""), row("F-b;F-a")]
    assert count.count(rows) == Counter({"F-a": 3, "F-b": 2})
    assert count.count([]) == Counter()


def test_first_seen_is_the_position_of_the_first_trace_with_the_type():
    rows = [row(""), row("F-a"), row("F-b;F-a"), row("F-c"), row("F-b")]
    assert saturation.first_seen(rows) == {"F-a": 2, "F-b": 3, "F-c": 4}


def test_the_course_s_counts_are_the_ones_the_lesson_shows():
    tally = count.count(read(CODED))
    assert tally.most_common() == [
        ("F-overreach", 21), ("F-misread", 21), ("F-wrong-rule", 15),
        ("F-bluff", 14), ("F-asks-again", 12), ("F-spam-reply", 7),
        ("F-wrong-page", 5), ("F-off-topic", 5), ("F-language", 3),
        ("F-obeys-injection", 1), ("F-no-draft", 1)]
    assert sum(tally.values()) == 105  # 77 failed traces, 24 carry two


def test_the_course_s_first_seen_positions_end_with_a_type_at_96():
    seen = saturation.first_seen(read(CODED))
    assert seen["F-bluff"] == 1 and seen["F-off-topic"] == 30
    assert seen["F-obeys-injection"] == 63 and seen["F-no-draft"] == 96


def test_count_py_prints_the_table_the_lesson_shows(capsys, monkeypatch):
    assert output_of("count.py", capsys, monkeypatch) == [
        "100 read, 23 fine, 77 with a failure",
        " n  share  type                  week 1 2 3 4",
        "21   21%  F-overreach                 5 5 7 4",
        "21   21%  F-misread                   2 2 8 9",
        "15   15%  F-wrong-rule                6 3 3 3",
        "14   14%  F-bluff                     5 3 5 1",
        "12   12%  F-asks-again                5 1 5 1",
        " 7    7%  F-spam-reply                3 2 1 1",
        " 5    5%  F-wrong-page                1 2 2 0",
        " 5    5%  F-off-topic                 0 4 1 0",
        " 3    3%  F-language                  1 2 0 0",
        " 1    1%  F-obeys-injection           0 0 1 0",
        " 1    1%  F-no-draft                  0 0 0 1"]


def test_saturation_py_prints_when_each_type_first_appeared(
        capsys, monkeypatch):
    assert output_of("saturation.py", capsys, monkeypatch) == [
        "read   1: F-bluff", "read   2: F-overreach",
        "read   4: F-wrong-rule", "read   5: F-asks-again",
        "read   9: F-wrong-page", "read  10: F-misread",
        "read  13: F-spam-reply", "read  14: F-language",
        "read  30: F-off-topic", "read  63: F-obeys-injection",
        "read  96: F-no-draft",
        "traces   1 to  25: 8 new type(s)",
        "traces  26 to  50: 1 new type(s)",
        "traces  51 to  75: 1 new type(s)",
        "traces  76 to 100: 1 new type(s)"]
