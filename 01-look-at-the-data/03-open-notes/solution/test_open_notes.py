"""Lesson 01.3: draw the same 100 emails, and keep a notes sheet in shape.

The tests need no model and no network. They check the shape of a notes
sheet (its columns, its ids, that ok is yes or no), never the wording of a
note:

    make check 01.3
"""

import csv
import runpy
from pathlib import Path

import pytest

import plumbing
import sample
from scorecard import data

HERE = Path(__file__).parent


def read_sheet(path):
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(line for line in f
                                   if not line.startswith("#")))


def test_draw_ids_takes_25_from_each_week_in_id_order(monkeypatch):
    log = {w: [{"id": f"E-{w}{n:03d}"} for n in range(40)]
           for w in (1, 2, 3, 4)}
    monkeypatch.setattr(sample.data, "emails", lambda week: log[week])
    ids = sample.draw_ids()
    assert len(ids) == 100 and len(set(ids)) == 100
    for w in (1, 2, 3, 4):
        part = ids[(w - 1) * 25:w * 25]
        assert part == sorted(part)
        assert all(i in {e["id"] for e in log[w]} for i in part)


def test_draw_ids_gives_the_same_ids_every_time():
    assert sample.draw_ids() == sample.draw_ids()


def test_the_course_ids_start_and_end_as_the_lesson_shows(capsys):
    ids = sample.draw_ids()
    assert ids[:3] == ["E-0151", "E-0154", "E-0156"]
    assert ids[-3:] == ["E-0732", "E-0739", "E-0745"]
    assert "E-0722" in ids  # the one trace with no draft
    plumbing.print_ids(ids)
    lines = capsys.readouterr().out.splitlines()
    assert lines[0] == "100 ids drawn" and len(lines) == 11
    assert lines[1] == ("E-0151 E-0154 E-0156 E-0158 E-0167 E-0175 E-0177 "
                        "E-0181 E-0185 E-0204")


def test_sample_py_starts_a_sheet_and_leaves_an_existing_one_alone(
        capsys, monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr("sys.argv", ["sample.py", "--sheet"])
    runpy.run_path(str(HERE / "sample.py"), run_name="__main__")
    assert "wrote my-notes.csv" in capsys.readouterr().out
    rows = read_sheet(tmp_path / "my-notes.csv")
    assert list(rows[0]) == ["id", "week", "ok", "note"]
    assert [r["id"] for r in rows] == sample.draw_ids()
    assert {r["ok"] for r in rows} == {""}
    with pytest.raises(SystemExit):
        runpy.run_path(str(HERE / "sample.py"), run_name="__main__")


def check_notes(path, need_filled):
    """The shape of a notes sheet: columns, the 100 ids, ok is yes or no."""
    rows = read_sheet(path)
    assert list(rows[0])[:4] == ["id", "week", "ok", "note"]
    assert [r["id"] for r in rows] == sample.draw_ids()
    weeks = {e["id"]: w for w in (1, 2, 3, 4)
             for e in data.emails(week=w)}
    assert all(int(r["week"]) == weeks[r["id"]] for r in rows)
    for r in rows[:need_filled]:
        assert r["ok"] in ("yes", "no"), f"{r['id']}: ok is yes or no"
        assert r["note"].strip(), f"{r['id']} has no note"
    assert all(r["ok"] in ("", "yes", "no") for r in rows)


def test_the_course_s_own_notes_have_the_shape_of_a_sheet():
    check_notes(data.DATA / "labels" / "01-open-notes.csv", need_filled=100)


def test_your_notes_sheet_if_you_have_started_one():
    sheet = HERE / "my-notes.csv"
    if not sheet.exists():
        pytest.skip("no my-notes.csv yet: run sample.py --sheet")
    check_notes(sheet, need_filled=25)  # the first 25 are the lesson's goal
