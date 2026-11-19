"""Lesson 02.3: coverage and score_by_slice.

The tests need no model and no network:

    make check 02.3
"""

import json
import runpy
from pathlib import Path

import pytest

import held_back
from coverage import coverage
from failing_by_slice import failing_by_slice
from scorecard import data
from score_by_slice import score_by_slice
from slices import log

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


def mail(id, language="en", category="refund", week=1, attack=False):
    return {"id": id, "language": language, "category": category,
            "week": week, "attack": attack, "body": "short"}


def by_slice(rows):
    return {row[0]: row[1:] for row in rows}


def test_coverage_counts_each_slice_in_the_log_and_in_the_open_part():
    emails = [mail("E-1"), mail("E-2"), mail("E-3", "ta"), mail("E-4")]
    rows = by_slice(coverage(emails, [emails[0], emails[2]]))
    assert rows[("language", "en")][0] == 3
    assert rows[("language", "en")][2] == 1
    assert rows[("language", "ta")][0] == 1
    assert rows[("language", "ta")][2] == 1


def test_coverage_gives_each_share_and_what_a_fair_open_part_would_hold():
    emails = [mail("E-1"), mail("E-2"), mail("E-3", "ta"), mail("E-4")]
    n, share, held, fair, thin = by_slice(
        coverage(emails, emails[:2]))[("language", "ta")]
    assert (n, share, held, fair) == (1, 0.25, 0, 0.5)


def test_a_slice_the_open_part_holds_fewer_than_5_of_is_thin():
    emails = [mail(f"E-{i}") for i in range(10)]
    rows = by_slice(coverage(emails, emails[:5]))
    assert rows[("language", "en")][-1] is False
    assert by_slice(coverage(emails, emails[:4]))[("language", "en")][-1]


def test_coverage_is_in_slice_name_order():
    rows = coverage([mail("E-1", "ta"), mail("E-2")], [])
    names = [str(r[0]) for r in rows]
    assert names == sorted(names)


def test_the_course_coverage_has_6_thin_slices_and_the_lessons_counts():
    rows = by_slice(coverage(log(), data.testset("open")))
    assert [k for k, v in rows.items() if v[-1]] == [
        ("attack", True), ("category", "account"), ("category", "warranty"),
        ("language", "hi"), ("language", "ml"), ("language", "ta")]
    assert rows[("language", "ml")][:3] == (8, 8 / 600, 1)
    assert rows[("category", "shipping_delay")][0::2][:2] == (98, 21)
    assert [rows[("week", w)][2] for w in (1, 2, 3, 4)] == [25] * 4


def test_score_by_slice_counts_right_and_total_in_every_slice():
    emails = [mail("E-1"), mail("E-2"), mail("E-3", "ta", "refund", 2)]
    said = {"E-1": {"category": "refund"}, "E-2": {"category": "return"},
            "E-3": {"category": "refund"}}
    table = score_by_slice(emails, said)
    assert table[("language", "en")] == [1, 2]
    assert table[("language", "ta")] == [1, 1]
    assert table[("category", "refund")] == [2, 3]
    assert table[("week", 2)] == [1, 1]


def test_an_email_counts_in_every_slice_it_sits_in():
    email = mail("E-1", attack=True)
    email["body"] = "x" * 400
    table = score_by_slice([email], {"E-1": {"category": "refund"}})
    assert table[("attack", True)] == [1, 1] and table[("long", True)] == [1, 1]


def test_the_course_scores_486_of_550_and_the_slices_the_lesson_names(
        no_sealed_parse):
    emails, said = held_back.usable_emails(), held_back.usable_triage()
    table = score_by_slice(emails, said)
    assert len(emails) == 550
    assert sum(said[e["id"]]["category"] == e["category"]
               for e in emails) == 486
    assert table[("category", "complaint")] == [23, 41]
    assert table[("category", "return")] == [54, 73]
    assert table[("language", "ml")] == [5, 5]
    assert [table[("week", w)][0] for w in (1, 2, 3, 4)] == [
        137, 112, 118, 119]


def test_score_by_slice_py_prints_the_lessons_first_lines(
        capsys, no_sealed_parse):
    runpy.run_path(str(HERE / "score_by_slice.py"), run_name="__main__")
    lines = capsys.readouterr().out.splitlines()
    assert lines[0] == "all 550 emails: 486 right = 88.4%"
    assert lines[3] == "category=complaint          23 of 41    56.1%"


def test_coverage_py_prints_the_flag_on_malayalam(capsys):
    runpy.run_path(str(HERE / "coverage.py"), run_name="__main__")
    out = capsys.readouterr().out
    assert "language=ml                   8   1.3%     1      1.3" \
           "  <- under 5\n" in out


def test_failing_by_slice_gives_77_failing_of_the_100_read():
    table = failing_by_slice(data.testset("open"), data.labels("01-coded"))
    assert table[("language", "en")] == [61, 82]
    assert table[("category", "shipping_delay")] == [19, 21]
    assert table[("week", 4)] == [14, 25]
    assert sum(v[0] for k, v in table.items() if k[0] == "week") == 77


def test_the_sealed_part_is_never_parsed_by_the_scripts(no_sealed_parse):
    for name in ("score_by_slice.py", "failing_by_slice.py", "coverage.py"):
        runpy.run_path(str(HERE / name), run_name="__main__")


def test_no_script_opens_a_trace_file_except_through_held_back():
    for path in HERE.glob("*.py"):
        if path.name not in ("held_back.py", "test_slices.py"):
            assert "traces" not in path.read_text(encoding="utf-8"), path
