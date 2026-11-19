"""Lesson 09.5: the simulated team and the precision of "sent unchanged".

No model and no network: the tests read the repo's recorded files. Nothing
here is recorded from a help desk: the actions are simulated.
From the top folder: make check 09.5
"""
import json
import runpy
from pathlib import Path

import pytest

import how_good_is_sent
import make_actions
import plumbing
from scorecard import graders

HERE = Path(__file__).parent


def printed(name, capsys):
    """What a script in this folder prints, one string per line."""
    runpy.run_path(str(HERE / name), run_name="__main__")
    return [line.rstrip() for line in capsys.readouterr().out.splitlines()]


def test_simulate_gives_one_row_per_draft_in_id_order():
    rows = make_actions.simulate({"E-2": (1, True), "E-1": (2, False)})
    assert [r["id"] for r in rows] == ["E-1", "E-2"]
    assert [r["week"] for r in rows] == [2, 1]
    assert all(r["simulated"] is True for r in rows)
    assert {r["action"] for r in rows} <= {"sent", "edited", "rewritten"}


def test_simulate_is_the_same_every_time_and_the_seed_changes_it():
    drafts = plumbing.coded()
    assert make_actions.simulate(drafts) == make_actions.simulate(drafts)
    assert make_actions.simulate(drafts, seed=8) != make_actions.simulate(
        drafts)


def test_simulate_sends_most_fine_drafts_and_fewer_failing_ones():
    fine = {f"E-{i}": (1, True) for i in range(1000)}
    bad = {f"E-{i}": (1, False) for i in range(1000)}
    share = lambda d: sum(r["action"] == "sent"
                          for r in make_actions.simulate(d)) / 1000
    assert share(fine) == pytest.approx(0.85, abs=0.04)
    assert share(bad) == pytest.approx(0.35, abs=0.04)


def test_the_sale_weeks_send_more_failing_drafts_unread():
    bad = {f"E-{i}": (w, False) for i, w in enumerate([2] * 1000)}
    sent = sum(r["action"] == "sent" for r in make_actions.simulate(bad))
    assert sent / 1000 == pytest.approx(0.55, abs=0.04)


def test_simulate_reproduces_the_recorded_file():
    recorded = [json.loads(line) for line in
                plumbing.ACTIONS.read_text().splitlines()]
    assert make_actions.simulate(plumbing.coded()) == recorded


def test_make_actions_writes_the_file_and_says_so(
        capsys, tmp_path, monkeypatch):
    out, recorded = tmp_path / "actions.jsonl", plumbing.ACTIONS
    monkeypatch.setattr(plumbing, "ACTIONS", out)
    assert printed("make_actions.py", capsys) == [
        'wrote 100 simulated actions to actions.jsonl']
    assert out.read_bytes() == recorded.read_bytes()


def test_precision_and_recall_of_a_small_flag():
    assert how_good_is_sent.precision_recall({1, 2, 3, 4}, {1, 2, 5}) == (
        0.5, 2 / 3)
    assert how_good_is_sent.precision_recall(set(), {1}) == (None, 0.0)
    assert how_good_is_sent.precision_recall({1}, set()) == (0.0, None)


@pytest.mark.parametrize("flagged, actual", [
    ({1, 2, 3}, {2, 3, 4, 5}), ({1}, {1}), (set(), set()), ({7, 8}, {1})])
def test_precision_recall_agrees_with_scorecard(flagged, actual):
    assert how_good_is_sent.precision_recall(flagged, actual) == (
        graders.precision_recall(flagged, actual))


def test_how_good_is_sent_prints_what_the_lesson_shows(capsys):
    assert printed("how_good_is_sent.py", capsys) == [
        "actions: {'sent': 62, 'edited': 26, 'rewritten': 12}",
        'sent unchanged: 62 drafts; 18 are fine',
        ('precision 0.29 (of sent, share fine); recall 0.78 (of fine, '
         'share sent)'),
        'weeks 1 and 4: 30 sent, 11 fine, precision 0.37',
        'sale weeks 2, 3: 32 sent, 7 fine, precision 0.22',
        ("edited or rewritten: 38 drafts; precision 0.87 for 'has a "
         "failure', recall 0.43"),
    ]
