"""Lesson 10.2: the goal and its guard, for four ways to send drafts unread.

No model and no network: the tests read the recorded runs in the repo.
From the top folder: make check 10.2
"""
import runpy
from pathlib import Path

import gate_candidates
from gate_candidates import GATES, goal_and_guard
from plumbing import open_drafts
from scorecard import data

HERE = Path(__file__).parent

DRAFTS = [{"quiet": True, "judged": True, "fine": True},
          {"quiet": True, "judged": False, "fine": False},
          {"quiet": False, "judged": True, "fine": False},
          {"quiet": False, "judged": False, "fine": False}]


def test_the_goal_and_the_guard_count_what_the_gate_sends():
    assert goal_and_guard(DRAFTS, GATES["send everything"]) == (4, 3)
    assert goal_and_guard(DRAFTS, GATES["no check fires"]) == (2, 1)
    assert goal_and_guard(DRAFTS, GATES["judge says PASS"]) == (2, 1)
    assert goal_and_guard(DRAFTS, GATES["both"]) == (1, 0)


def test_a_gate_that_sends_nothing_has_no_wrong_replies():
    assert goal_and_guard(DRAFTS, lambda d: False) == (0, 0)


def test_the_open_drafts_are_the_100_open_emails():
    drafts = open_drafts()
    assert [d["id"] for d in drafts] == sorted(
        e["id"] for e in data.testset("open"))
    assert len(drafts) == 100


def test_gate_candidates_prints_the_table_of_the_lesson(capsys):
    runpy.run_path(str(HERE / "gate_candidates.py"), run_name="__main__")
    assert [x.rstrip() for x in capsys.readouterr().out.splitlines()] == [
        "gate             sent unread  wrong among them   95% range",
        "send everything   100 of 100    77 (77.0%)      67.8% to 84.2%",
        "no check fires     68 of 100    45 (66.2%)      54.3% to 76.3%",
        "judge says PASS    58 of 100    37 (63.8%)      50.9% to 74.9%",
        "both               40 of 100    19 (47.5%)      32.9% to 62.5%"]
