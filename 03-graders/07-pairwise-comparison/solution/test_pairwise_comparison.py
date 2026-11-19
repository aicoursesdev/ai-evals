"""Lesson 03.7: ask each pair in both orders, count a win only if it holds.

The tests need no model and no network:

    make check 03.7
"""

import runpy
from pathlib import Path

import pairwise
from scorecard import data

HERE = Path(__file__).parent


def output_of(name, capsys):
    runpy.run_path(str(HERE / name), run_name="__main__")
    return capsys.readouterr().out.splitlines()


def test_winner_turns_a_or_b_back_into_the_version_shown_there():
    order = ("hd-2", "hd-1")
    assert pairwise.winner("They differ.\nA", order) == "hd-2"
    assert pairwise.winner("They differ.\nB", order) == "hd-1"
    assert pairwise.winner("Equal.\nTIE", order) == "tie"


def test_winner_reads_the_last_line_in_any_capitals_and_after_marks():
    order = ("hd-1", "hd-2")
    assert pairwise.winner("A is longer.\n**b**", order) == "hd-2"
    assert pairwise.winner("A\nOn reflection:\nTie", order) == "tie"


def test_winner_is_none_without_a_verdict_line():
    assert pairwise.winner("I would pick B because it is warmer", (
        "hd-1", "hd-2")) is None
    assert pairwise.winner("", ("hd-1", "hd-2")) is None


def test_both_orders_reads_each_recorded_reply_with_its_own_order():
    saved = {("E-1", "hd-1"): "Why.\nA", ("E-1", "hd-2"): "Why.\nA"}
    assert pairwise.both_orders("E-1", saved) == {
        "hd-1": "hd-1", "hd-2": "hd-2"}  # the first-shown reply won twice
    saved = {("E-2", "hd-1"): "Why.\nB", ("E-2", "hd-2"): "Why.\nA"}
    assert pairwise.both_orders("E-2", saved) == {
        "hd-1": "hd-2", "hd-2": "hd-2"}  # hd-2 won in both orders


def test_holds_in_both_keeps_a_win_only_when_the_orders_agree():
    assert pairwise.holds_in_both("hd-1", "hd-1") == "hd-1"
    assert pairwise.holds_in_both("tie", "tie") == "tie"
    assert pairwise.holds_in_both("hd-1", "hd-2") == "split"
    assert pairwise.holds_in_both("hd-1", "tie") == "split"


def test_the_pairs_and_prompts_are_the_recorded_ones():
    rows = data.read_jsonl(pairwise.OUT)
    by_id = {p["id"]: p for p in pairwise.pairs()}
    assert len(by_id) == 60 and len(rows) == 120
    assert all(pairwise.prompt_for(by_id[r["id"]], (r["a"], r["b"]))
               == r["prompt"] for r in rows)


def test_the_recording_gives_the_lessons_winners_in_both_orders():
    saved = pairwise.recorded()
    both = [pairwise.both_orders(i, saved) for i in
            sorted({i for i, _ in saved})]
    firsts = [pairwise.holds_in_both(b["hd-1"], b["hd-2"]) for b in both]
    assert [firsts.count(v) for v in ("hd-1", "hd-2", "split")] == [
        22, 10, 28]


def test_swap_report_prints_what_the_lesson_shows(capsys):
    assert output_of("swap_report.py", capsys) == [
        "120 requests; no verdict on 0",
        "who won by position: {'second': 40, 'first': 79, 'tie': 1}",
        "both orders give: {'hd-2': 10, 'split': 28, 'hd-1': 22}",
        "the longer reply won both times on 19 pairs",
        "asked with hd-1 first: {'hd-2': 14, 'hd-1': 45, 'tie': 1}",
        "asked with hd-2 first: {'hd-2': 34, 'hd-1': 26}",
        "pairs where hd-1's reply is longer: 52"]


def test_pairwise_replays_the_recording_and_calls_no_model(capsys):
    # Without --live the file prints nothing and never reaches a model.
    assert output_of("pairwise.py", capsys) == []


def test_no_script_parses_a_sealed_trace(capsys):
    # The guard in ../conftest.py fails the test; pairs() reads traces
    # only through scorecard.graders.logged.
    for name in ("pairwise.py", "swap_report.py"):
        runpy.run_path(str(HERE / name), run_name="__main__")
