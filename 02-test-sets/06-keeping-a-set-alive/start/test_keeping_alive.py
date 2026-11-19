"""Lesson 02.6: problems and next_version, with drift and too_easy.

The tests need no model and no network:

    make check 02.6
"""

import json
import runpy
import sys
from pathlib import Path

import pytest

import held_back
from add_case import PARTS, next_version, problems
from scorecard import data

HERE = Path(__file__).parent


@pytest.fixture
def no_sealed_parse(monkeypatch):
    """Fail if anything parses a trace line whose id is in the sealed part."""
    sealed = {e["id"] for e in data.testset("sealed")}
    real = json.loads

    def guard(text, *args, **kwargs):
        if isinstance(text, str) and '"triage":' in text \
                and text[8:14] in sealed:
            raise AssertionError("a sealed trace line was parsed")
        return real(text, *args, **kwargs)

    monkeypatch.setattr(json, "loads", guard)


def mail(id, subject="where is my parcel", body="it has not come"):
    return {"id": id, "subject": subject, "body": body}


def held(open_=(), sealed=(), synthetic=()):
    return {"open": list(open_), "sealed": list(sealed),
            "synthetic": list(synthetic)}


def run_add_case(monkeypatch, capsys, *args):
    monkeypatch.setattr(sys, "argv", ["add_case.py", *args])
    runpy.run_path(str(HERE / "add_case.py"), run_name="__main__")
    return capsys.readouterr().out


def test_a_new_email_with_a_note_may_be_added():
    assert problems(mail("E-9", "refund please"), "found in week 4",
                    held([mail("E-1")])) == []


def test_an_email_already_in_a_part_is_refused_and_the_part_is_named():
    got = problems(mail("E-1"), "a note", held(sealed=[mail("E-1")]))
    assert got == ["already in sealed"]


def test_a_near_copy_of_a_case_is_refused_and_names_the_case():
    twin = mail("E-2", "where is my parcel", "it has not come yet")
    got = problems(mail("E-9"), "a note", held(open_=[twin]))
    assert got == ["near copy of ['E-2'] in open"]


def test_a_different_email_is_not_a_near_copy():
    other = mail("E-2", "invoice", "please send the gst invoice")
    assert problems(mail("E-9"), "a note", held(open_=[other])) == []


def test_an_email_without_a_note_is_refused():
    msg = "no note on where it was found and what went wrong"
    assert problems(mail("E-9", "x y z"), "", held()) == [msg]
    assert problems(mail("E-9", "x y z"), "   ", held()) == [msg]


def test_every_reason_is_listed():
    got = problems(mail("E-1"), "", held(open_=[mail("E-1")]))
    assert len(got) == 2 and got[0] == "already in open"


def test_adding_cases_bumps_the_minor_number():
    assert next_version("1.0") == "1.1"
    assert next_version("1.9") == "1.10"
    assert next_version("2.3") == "2.4"


def test_the_three_parts_are_open_sealed_and_synthetic():
    assert PARTS == ("open", "sealed", "synthetic")


def test_add_case_py_prints_each_branch_of_the_lesson(monkeypatch, capsys):
    out = run_add_case(monkeypatch, capsys, "E-0722", "the reply never ended")
    assert out == "E-0722 refused: already in open\n"
    out = run_add_case(monkeypatch, capsys, "E-0628",
                       "a second investment pitch")
    assert out == "E-0628 refused: near copy of ['E-0348'] in open\n"
    out = run_add_case(monkeypatch, capsys, "E-0597", "")
    assert out == ("E-0597 refused: no note on where it was found and what "
                   "went wrong\n")
    out = run_add_case(monkeypatch, capsys, "E-0597",
                       "an example, not a finding")
    assert out == ("E-0597 may be added to the open part (never the sealed "
                   "part,\nyou have read it) as version 1.1\n"
                   "note: an example, not a finding\n")


def test_drift_py_shows_returns_doubling_and_refunds_rising(capsys):
    runpy.run_path(str(HERE / "drift.py"), run_name="__main__")
    rows = {line.split()[0]: line.split()
            for line in capsys.readouterr().out.splitlines()[1:]}
    assert rows["return"][1:5] == ["12%", "8%", "7%", "24%"]
    assert rows["refund"][1:5] == ["13%", "8%", "6%", "20%"]
    assert rows["return"][5:] == ["+12", "points"]
    assert rows["product_question"][5:] == ["-7", "points"]


def test_too_easy_py_lists_the_four_slices_with_no_room_left(
        capsys, no_sealed_parse):
    runpy.run_path(str(HERE / "too_easy.py"), run_name="__main__")
    lines = capsys.readouterr().out.splitlines()
    assert lines[1:] == [
        "category=account          17/17      0",
        "category=order_change     49/51      2",
        "category=shipping_delay   89/90      1",
        "category=warranty         24/25      1"]


def test_score_by_slice_py_still_prints_88_4(capsys, no_sealed_parse):
    runpy.run_path(str(HERE / "score_by_slice.py"), run_name="__main__")
    assert capsys.readouterr().out.startswith(
        "all 550 emails: 486 right = 88.4%\n")


def test_held_back_skips_a_sealed_trace_before_parsing_it(no_sealed_parse):
    assert len(held_back.sealed_ids()) == 50
    said = held_back.usable_triage()
    assert len(said) == 550 and not held_back.sealed_ids() & set(said)


def test_no_script_opens_a_trace_file_except_through_held_back():
    for path in HERE.glob("*.py"):
        if path.name not in ("held_back.py", "test_keeping_alive.py"):
            text = path.read_text(encoding="utf-8")
            assert "data.traces" not in text and '"traces"' not in text, path
