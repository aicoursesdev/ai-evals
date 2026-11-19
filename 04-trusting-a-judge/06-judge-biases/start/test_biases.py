"""Lesson 04.6: the counts behind three bias tests, in your own functions.

No model and no network: every verdict comes from a recorded run in the repo.
From the top folder: make check 04.6
"""
import json
import runpy
from pathlib import Path

import pytest

import bias_counts as bc
import bias_runs
from plumbing import RUNS, read_trials, verdicts, winner
from scorecard import data
from scorecard.judge import agreement

HERE = Path(__file__).parent
PAIRS = RUNS / "03-pairwise" / "pairs.jsonl"


def printed(name, capsys):
    """What a script in this folder prints, one string per line."""
    runpy.run_path(str(HERE / name), run_name="__main__")
    return [line.rstrip() for line in capsys.readouterr().out.splitlines()]


def row(email, first, second, reply):
    """A pairwise record: `first` was shown as Reply A."""
    return {"id": email, "a": first, "b": second, "reply": reply}


def test_winner_reads_the_last_line_and_maps_it_to_the_version_shown():
    assert winner("Reasons.\nA", ("hd-1", "hd-2")) == "hd-1"
    assert winner("Reasons.\nB", ("hd-1", "hd-2")) == "hd-2"
    assert winner("Reasons.\nTIE", ("hd-1", "hd-2")) == "tie"
    assert winner("no answer", ("hd-1", "hd-2")) is None


def test_by_place_counts_first_second_and_tie():
    rows = [row("e1", "hd-1", "hd-2", "A"), row("e1", "hd-2", "hd-1", "A"),
            row("e2", "hd-1", "hd-2", "B"), row("e2", "hd-2", "hd-1", "TIE")]
    assert bc.by_place(rows) == {"first": 2, "second": 1, "tie": 1}


def test_the_recorded_pairs_say_first_79_second_40_tie_1():
    assert bc.by_place(data.read_jsonl(PAIRS)) == {
        "first": 79, "second": 40, "tie": 1}


def test_same_both_orders_counts_pairs_where_one_version_wins_twice():
    rows = [row("e1", "hd-1", "hd-2", "A"), row("e1", "hd-2", "hd-1", "B"),
            row("e2", "hd-1", "hd-2", "A"), row("e2", "hd-2", "hd-1", "A"),
            row("e3", "hd-1", "hd-2", "TIE"), row("e3", "hd-2", "hd-1", "TIE")]
    assert bc.same_both_orders(rows) == (3, 1)


def test_the_recorded_pairs_agree_on_32_of_60_in_both_orders():
    assert bc.same_both_orders(data.read_jsonl(PAIRS)) == (60, 32)


def test_moves_counts_each_pair_of_before_and_after():
    before = {"a": "pass", "b": "pass", "c": "fail", "d": "none"}
    after = {"a": "fail", "b": "pass", "c": "fail", "d": "unsure"}
    assert bc.moves(before, after, ["a", "b", "c", "d"]) == {
        ("pass", "fail"): 1, ("pass", "pass"): 1, ("fail", "fail"): 1,
        ("none", "unsure"): 1}


def test_moves_only_looks_at_the_ids_it_is_given():
    before, after = {"a": "pass", "b": "fail"}, {"a": "fail", "b": "fail"}
    assert bc.moves(before, after, ["b"]) == {("fail", "fail"): 1}


def test_the_padded_drafts_moved_as_the_lesson_shows():
    ids = bias_runs.sample()
    before = verdicts(RUNS / "04-dev" / "v4.jsonl")
    after = verdicts(bias_runs.OUT / "length.jsonl")
    moved = bc.moves(before, after, ids)
    assert moved[("pass", "pass")] == 13 and moved[("pass", "fail")] == 3
    assert sum(n for (a, b), n in moved.items() if a != b) == 10


@pytest.mark.parametrize("first, again", [
    (["pass", "fail", "pass", "unsure"], ["pass", "fail", "fail", "unsure"]),
    (["pass"] * 5, ["pass"] * 5),
    (["pass", "fail"], ["fail", "pass"]),
])
def test_same_on_agrees_with_scorecard_agreement(first, again):
    ids = range(len(first))
    assert bc.same_on(first, again, ids) == round(
        agreement(first, again) * len(first))


def test_asked_twice_at_temperature_0_the_same_verdict_on_29_of_30():
    ids = bias_runs.sample()
    first = verdicts(RUNS / "04-dev" / "v4.jsonl")
    again = verdicts(bias_runs.OUT / "again-t0.jsonl")
    assert bc.same_on(first, again, ids) == 29


def test_kinds_per_draft_counts_how_many_verdicts_each_draft_got():
    runs = [{"a": "pass", "b": "pass", "c": "pass"},
            {"a": "pass", "b": "fail", "c": "fail"},
            {"a": "pass", "b": "pass", "c": "unsure"}]
    assert bc.kinds_per_draft(runs, ["a", "b", "c"]) == {1: 1, 2: 1, 3: 1}


def test_six_runs_give_4_17_8_1_kinds_of_verdict_per_draft():
    ids = bias_runs.sample()
    hot = read_trials(bias_runs.OUT / "again-t07.jsonl")
    runs = [verdicts(RUNS / "04-dev" / "v4.jsonl")]
    runs += [hot[k] for k in sorted(hot)]
    assert bc.kinds_per_draft(runs, ids) == {1: 4, 2: 17, 3: 8, 4: 1}


def test_the_sample_is_the_30_recorded_drafts_and_holds_a_prompt_example():
    ids = bias_runs.sample()
    recorded = json.loads((bias_runs.OUT / "sample-ids.json").read_text())
    assert ids == recorded and len(ids) == 30 and "E-0398" in ids


def test_position_test_prints_the_counts_the_lesson_shows(capsys):
    assert printed("position_test.py", capsys) == [
        "120 requests: {'second': 40, 'first': 79, 'tie': 1}",
        ('60 pairs; the same version wins in both orders on 32; the '
         'winner changes with the order on 28'),
    ]


def test_length_test_prints_the_moves_and_the_changed_count(capsys):
    assert printed("length_test.py", capsys) == [
        '30 drafts, 87 words on average; the filler adds 34',
        '    fail -> fail   6',
        '    none -> unsure 1',
        '    pass -> fail   3',
        '    pass -> none   1',
        '    pass -> pass   13',
        '    pass -> unsure 2',
        '  unsure -> pass   3',
        '  unsure -> unsure 1',
        'verdict changed on 10 of 30',
        'without E-0398, an example in the prompt: changed on 9 of 29',
        'Arjun pass: judge passes 15 of 20 unpadded, 13 padded',
        'Arjun fail: judge passes 4 of 10 unpadded, 3 padded',
    ]


def test_again_test_prints_the_runs_and_the_kinds(capsys):
    assert printed("again_test.py", capsys) == [
        'temperature 0, asked twice: same verdict on 29 of 30',
        '  temperature 0.7, run 1: judge passes 43.3%',
        '  temperature 0.7, run 2: judge passes 36.7%',
        '  temperature 0.7, run 3: judge passes 56.7%',
        '  temperature 0.7, run 4: judge passes 30.0%',
        '  temperature 0.7, run 5: judge passes 50.0%',
        'kinds of verdict per draft over six runs: {1: 4, 2: 17, 3: 8, 4: 1}',
        'all six runs agree on 4 of 30 drafts',
    ]


def test_bias_runs_counts_the_recorded_requests(capsys):
    assert printed("bias_runs.py", capsys) == [
        'length 30', 'again-t0 30', 'again-t07 150']
