"""Lesson 02.7: test set v1: eligible, checks, table and open_categories.

The tests need no model and no network:

    make check 02.7
"""

import json
import runpy
import sys
from collections import Counter
from pathlib import Path

import pytest

from build_testset import FLOOR, SEED, eligible
from check_testset import checks
from coverage_table import table
from first_score import open_categories
from plumbing import OUT, PARTS, prompt_files, tagged, used_ids, write
from scorecard import data
from slices import log, slice_sample

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


def mail(id, week=2, attack=False):
    return {"id": id, "week": week, "attack": attack}


def real_inputs():
    parts = {p: data.testset(p) for p in PARTS}
    launch = {e["id"] for e in data.emails(launch=True)}
    return parts, launch, prompt_files(), used_ids()


def result(parts, launch, prompts, used):
    return dict(checks(parts, launch, prompts, used))


# ---- eligible ----------------------------------------------------------

def test_eligible_keeps_weeks_2_to_4_that_nothing_else_opens():
    emails = [mail("E-1", week=1), mail("E-2"), mail("E-3", week=4)]
    assert [e["id"] for e in eligible(emails, set(), set())] == ["E-2", "E-3"]


def test_eligible_drops_attacks_read_emails_and_emails_in_a_run():
    emails = [mail("E-1", attack=True), mail("E-2"), mail("E-3"),
              mail("E-4"), mail("E-5", week=4)]
    got = eligible(emails, coded={"E-2"}, used={"E-3"})
    assert [e["id"] for e in got] == ["E-4", "E-5"]


def test_the_course_pool_holds_243_emails():
    emails = log()
    coded = {r["id"] for r in data.labels("01-coded")}
    pool = eligible(emails, coded, used_ids())
    assert len(pool) == 243
    assert Counter(e["week"] for e in pool) == {2: 120, 3: 93, 4: 30}


def test_the_seeded_draw_is_the_sealed_part_on_file(tmp_path):
    emails = log()
    coded = {r["id"] for r in data.labels("01-coded")}
    opened = [e for e in emails if e["id"] in coded]
    pool = eligible(emails, coded, used_ids())
    sealed = slice_sample(pool, 50, SEED, have=opened, floor=FLOOR)
    sealed.sort(key=lambda e: e["id"])
    write([tagged(e, "sealed") for e in sealed], tmp_path / "sealed.jsonl")
    on_file = (OUT / "sealed.jsonl").read_bytes()
    assert (tmp_path / "sealed.jsonl").read_bytes() == on_file
    write([tagged(e, "open") for e in opened], tmp_path / "open.jsonl")
    assert (tmp_path / "open.jsonl").read_bytes() == (
        OUT / "open.jsonl").read_bytes()


# ---- checks ------------------------------------------------------------

def test_every_check_holds_on_the_course_set():
    got = result(*real_inputs())
    assert len(got) == 7 and all(got.values()), got


def test_a_set_of_99_open_emails_fails_the_first_check():
    parts, launch, prompts, used = real_inputs()
    parts["open"] = parts["open"][:99]
    assert not result(parts, launch, prompts, used)["100 open, 50 sealed"]


def test_a_repeated_id_fails_the_second_check():
    parts, launch, prompts, used = real_inputs()
    parts["synthetic"] = parts["synthetic"] + [parts["synthetic"][0]]
    assert not result(parts, launch, prompts, used)["every id appears once"]


def test_a_sealed_email_in_the_launch_set_fails_the_third_check():
    parts, launch, prompts, used = real_inputs()
    launch = launch | {parts["sealed"][0]["id"]}
    got = result(parts, launch, prompts, used)
    assert not got["no sealed email is in the launch set"]


@pytest.mark.parametrize("change", [{"week": 1}, {"attack": True}])
def test_a_sealed_week_1_email_or_attack_fails_the_fourth_check(change):
    parts, launch, prompts, used = real_inputs()
    parts["sealed"] = [parts["sealed"][0] | change] + parts["sealed"][1:]
    name = "sealed: not week 1, not open, not an attack, in no run"
    assert not result(parts, launch, prompts, used)[name]


def test_a_sealed_email_in_a_recorded_run_fails_the_fourth_check():
    parts, launch, prompts, used = real_inputs()
    used = used | {parts["sealed"][0]["id"]}
    name = "sealed: not week 1, not open, not an attack, in no run"
    assert not result(parts, launch, prompts, used)[name]


def test_an_email_written_into_a_prompt_fails_the_fifth_check():
    parts, launch, prompts, used = real_inputs()
    first = parts["open"][0]
    prompts = prompts | {"x.md": first["subject"] + " " + first["body"]}
    got = result(parts, launch, prompts, used)
    assert not got["no real email appears in a prompt"]


def test_a_near_copy_of_an_open_email_in_sealed_fails_the_sixth_check():
    parts, launch, prompts, used = real_inputs()
    twin = parts["sealed"][0] | {
        "subject": parts["open"][0]["subject"],
        "body": parts["open"][0]["body"]}
    parts["sealed"] = [twin] + parts["sealed"][1:]
    got = result(parts, launch, prompts, used)
    assert not got["no copy or near copy across parts"]


def test_a_made_up_case_without_the_flag_fails_the_seventh_check():
    parts, launch, prompts, used = real_inputs()
    parts["synthetic"] = [parts["synthetic"][0] | {"made_up": False}]
    got = result(parts, launch, prompts, used)
    assert not got["made-up cases are all marked"]


def test_check_testset_py_prints_seven_ok_lines_and_exits_0(capsys):
    sys.argv = ["check_testset.py"]
    with pytest.raises(SystemExit) as stop:
        runpy.run_path(str(HERE / "check_testset.py"), run_name="__main__")
    assert stop.value.code == 0
    out = capsys.readouterr().out.splitlines()
    assert len(out) == 7 and all(line.startswith("ok   ") for line in out)


# ---- table -------------------------------------------------------------

def test_table_has_a_header_then_a_row_per_slice_in_order():
    traffic = Counter({("language", "ta"): 12, ("category", "spam"): 31})
    parts = {"open": Counter({("language", "ta"): 4}),
             "sealed": Counter({("language", "ta"): 2}),
             "synthetic": Counter({("language", "ta"): 7})}
    assert table(traffic, parts).splitlines() == [
        "| Slice | In the log | Open | Sealed | Real (open + sealed) | "
        "Made up |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
        "| category=spam | 31 | 0 | 0 | 0 (under 10) | 0 |",
        "| language=ta | 12 | 4 | 2 | 6 (under 10) | 7 |"]


def test_ten_real_cases_are_not_under_ten():
    traffic = Counter({("week", 2): 150})
    parts = {"open": Counter({("week", 2): 6}),
             "sealed": Counter({("week", 2): 4}),
             "synthetic": Counter()}
    assert table(traffic, parts).splitlines()[-1] == (
        "| week=2 | 150 | 6 | 4 | 10 | 0 |")


def test_coverage_table_py_shows_eight_slices_under_ten(capsys):
    runpy.run_path(str(HERE / "coverage_table.py"), run_name="__main__")
    out = capsys.readouterr().out
    assert out.count("(under 10)") == 8
    assert "| language=ml | 8 | 1 | 3 | 4 (under 10) | 5 |" in out


# ---- open_categories ---------------------------------------------------

def line(id, category):
    return json.dumps({"id": id, "triage": {"category": category}})


def test_open_categories_keeps_only_the_open_ids():
    lines = [line("E-0001", "refund"), line("E-0002", "return")]
    assert open_categories(lines, {"E-0001": {}}) == {"E-0001": "refund"}


def test_a_line_that_is_not_open_is_never_parsed():
    poison = '{"id": "E-0002", this is not json'
    lines = [line("E-0001", "refund"), poison]
    assert open_categories(lines, {"E-0001": {}}) == {"E-0001": "refund"}


def test_first_score_py_scores_87_of_100_and_parses_no_sealed_line(
        capsys, no_sealed_parse):
    runpy.run_path(str(HERE / "first_score.py"), run_name="__main__")
    assert capsys.readouterr().out == (
        "open part, triage category: 87 of 100\n"
        "by week: {1: '25 of 25', 2: '22 of 25', 3: '21 of 25', "
        "4: '19 of 25'}\n"
        "sealed part: not scored (0 times so far)\n")


def test_only_first_score_reads_a_trace_and_it_tests_the_id_first():
    for path in HERE.glob("*.py"):
        text = path.read_text(encoding="utf-8")
        if path.name in ("test_testset.py", "plumbing.py"):
            continue
        assert "data.traces" not in text and '"traces"' not in text, path
    first = (HERE / "first_score.py").read_text(encoding="utf-8")
    if "json.loads" in first:  # once you have written open_categories
        assert "in opened" in first.split("json.loads")[0].split(
            "def open_categories")[-1]
