"""Lesson 03.6: a model judge for "right rule", replayed from its recording.

The tests need no model and no network:

    make check 03.6
"""

import runpy
from collections import Counter
from pathlib import Path

import compare_with_arjun as compare
import judge_rule
from scorecard import data

HERE = Path(__file__).parent


def output_of(name, capsys):
    runpy.run_path(str(HERE / name), run_name="__main__")
    return capsys.readouterr().out.splitlines()


def test_read_verdict_takes_the_last_line_in_any_capitals():
    reply = "The page says 30 days.\nPASS"
    assert judge_rule.read_verdict(reply) == "pass"
    assert judge_rule.read_verdict("Reasons.\nfail") == "fail"
    assert judge_rule.read_verdict("It is unclear.\nUNSURE") == "unsure"


def test_read_verdict_skips_marks_before_the_word_and_keeps_the_last():
    assert judge_rule.read_verdict("Why.\n**FAIL**") == "fail"
    assert judge_rule.read_verdict("PASS\nOn reflection:\n- FAIL") == "fail"


def test_read_verdict_says_none_when_the_word_ends_a_sentence():
    assert judge_rule.read_verdict("The reply is fine, so PASS") == "none"
    assert judge_rule.read_verdict("") == "none"


def test_tally_counts_each_pair_of_call_and_verdict():
    calls = {"a": "pass", "b": "pass", "c": "fail", "d": "unsure"}
    verdicts = {"a": "pass", "b": "fail", "c": "fail", "d": "none"}
    assert compare.tally(calls, verdicts) == Counter({
        ("pass", "pass"): 1, ("pass", "fail"): 1, ("fail", "fail"): 1,
        ("unsure", "none"): 1})


def test_clear_cases_leaves_out_unsure_calls_and_unsure_or_missing_verdicts():
    calls = {"a": "pass", "b": "fail", "c": "unsure", "d": "pass",
             "e": "fail"}
    verdicts = {"a": "pass", "b": "unsure", "c": "pass", "d": "none",
                "e": "pass"}
    assert compare.clear_cases(calls, verdicts) == ["a", "e"]


def test_the_prompt_filled_in_is_the_recorded_prompt_character_for_character():
    recorded = {r["id"]: r["prompt"]
                for r in data.read_jsonl(judge_rule.OUT)}
    cases = list(judge_rule.cases())
    assert len(cases) == len(recorded) == 100
    assert all(judge_rule.PROMPT.format(**c) == recorded[c["id"]]
               for c in cases)


def test_the_recorded_replies_read_as_the_lesson_says():
    judged = judge_rule.judged()
    assert Counter(judged.values()) == {
        "pass": 53, "fail": 28, "unsure": 16, "none": 3}
    none = sorted(i for i, v in judged.items() if v == "none")
    assert none == ["E-0261", "E-0580", "E-0739"]


def test_compare_with_arjun_prints_the_table_the_lesson_shows(capsys):
    assert output_of("compare_with_arjun.py", capsys) == [
        "Arjun says  judge pass  fail  unsure  no line",
        "pass                38    12       8        3",
        "fail                13    14       2        0",
        "unsure               2     2       6        0",
        "both gave pass or fail on 77; they agree on 52",
        "a marker that always said pass would agree on 50 of them"]


def test_judge_rule_replays_the_recording_and_calls_no_model(capsys):
    # Without --live the file prints nothing and never reaches a model.
    assert output_of("judge_rule.py", capsys) == []


def test_no_script_parses_a_sealed_trace(capsys):
    # The guard in ../conftest.py fails the test; the judge's cases come
    # from scorecard.graders.logged, which skips sealed lines unread.
    for name in ("judge_rule.py", "compare_with_arjun.py"):
        runpy.run_path(str(HERE / name), run_name="__main__")
