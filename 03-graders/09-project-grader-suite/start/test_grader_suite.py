"""Lesson 03.9: the grader suite and the cases that prove it.

The tests need no model and no network:

    make check 03.9
"""

import re
import runpy
from pathlib import Path

import pytest

import judge_rule
import run_suite
import suite
from scorecard.graders import CHECKS
from suite_cases import CASES, JUDGE_REPLIES

HERE = Path(__file__).parent


def output_of(name, capsys):
    runpy.run_path(str(HERE / name), run_name="__main__")
    return capsys.readouterr().out.splitlines()


def test_checks_for_lists_every_check_that_targets_a_failure_type():
    assert suite.checks_for("F-bluff") == [
        "missing or old page", "invented address"]
    assert suite.checks_for("F-no-draft") == ["empty draft"]
    assert suite.checks_for("F-misread") == []


def test_marker_names_checks_then_the_rule_and_judge_then_the_gap():
    assert suite.marker("F-spam-reply") == "code: reply to spam"
    assert suite.marker("F-bluff") == (
        "code: missing or old page + invented address")
    assert suite.marker("F-wrong-rule") == (
        "right rule: Arjun's rule + judge_rule")
    assert suite.marker("F-misread").startswith("needs its own rule")


def test_own_cases_counts_the_right_ones_and_leaves_out_the_gaps():
    fires_on_hi = lambda email, trace: trace == "hi"
    cases = [("fires", {}, "hi", True), ("quiet", {}, "yo", False),
             ("wrong", {}, "hi", False), ("GAP: missed", {}, "yo", True)]
    assert run_suite.own_cases(fires_on_hi, cases) == (2, 3)
    assert run_suite.own_cases(fires_on_hi, []) == (0, 0)


@pytest.mark.parametrize("name", list(CHECKS))
def test_your_cases_for_each_check_hold_both_kinds_and_all_agree(name):
    right, total = run_suite.own_cases(CHECKS[name][0], CASES[name])
    wants = {c[3] for c in CASES[name] if not c[0].startswith("GAP")}
    assert total >= 3 and wants == {True, False}, (
        f"TODO 03.9: give {name!r} at least three cases, some that fire "
        f"and some that do not, see the lesson's 'Steps' section")
    assert right == total


def test_your_verdict_reader_cases_cover_all_four_readings_and_are_right():
    readings = {want for _, want in JUDGE_REPLIES}
    assert readings == {"pass", "fail", "unsure", "none"}, (
        "TODO 03.9: give read_verdict replies for pass, fail, unsure and "
        "none, see the lesson's 'Steps' section")
    assert all(judge_rule.read_verdict(r) == want
               for r, want in JUDGE_REPLIES)


def test_the_suite_report_says_every_check_right_on_its_own_cases(capsys):
    lines = output_of("run_suite.py", capsys)
    first = lines[1:lines.index("")]
    assert len(first) == 8 and first[-1].lstrip().startswith("verdict reader")
    assert all(re.search(r"(\d+) of \1 right$", x) for x in first)


def test_the_suite_report_gives_the_lessons_numbers_by_type_and_judge(capsys):
    lines = output_of("run_suite.py", capsys)
    by_type = [re.sub(r"\s{2,}", " ", x.strip()) for x in lines[11:22]]
    assert by_type == [
        "F-overreach 21 in the map 10 caught code: claims an action",
        "F-misread 21 in the map needs its own rule and judge "
        "(not built here)",
        "F-wrong-rule 15 in the map right rule: Arjun's rule + judge_rule",
        "F-bluff 14 in the map 6 caught code: missing or old page + "
        "invented address",
        "F-asks-again 12 in the map 6 caught code: asks for known id",
        "F-spam-reply 7 in the map 6 caught code: reply to spam",
        "F-wrong-page 5 in the map 3 caught code: missing or old page",
        "F-off-topic 5 in the map needs its own rule and judge "
        "(not built here)",
        "F-language 3 in the map 2 caught code: wrong script",
        "F-obeys-injection 1 in the map attack set and outcome check "
        "(Module 08)",
        "F-no-draft 1 in the map 1 caught code: empty draft"]
    assert lines[-2] == "   both gave pass or fail on 77 drafts; agree on 52"
    assert lines[-1] == "   replies with no verdict line: 3"


def test_the_report_names_every_failure_type_and_the_judge_numbers():
    report = (HERE / "suite.md").read_text(encoding="utf-8")
    missing = [t for t in suite.TYPES if t not in report]
    assert not missing and "77" in report and "52" in report, (
        "TODO 03.9: write suite.md with a row for each of the eleven "
        "failure types and the judge numbers, see the lesson's 'Steps' "
        "section")


def test_no_script_parses_a_sealed_trace(capsys):
    # The guard in ../conftest.py fails the test; the suite reads traces
    # only through scorecard.graders.logged.
    output_of("run_suite.py", capsys)
