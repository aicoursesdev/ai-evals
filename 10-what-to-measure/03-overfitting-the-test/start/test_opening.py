"""Lesson 10.3: the plan's rule, the replay of the one opening and the
width of a range. The sealed part is spent: no test scores anything, calls
a model or parses a sealed trace; they read data/runs/10-sealed/ only.
From the top folder: make check 10.3
"""
import runpy
from pathlib import Path

import pytest

import range_by_n
import replay_sealed
from honest_or_spent import verdict
from scorecard.stats import wilson

HERE = Path(__file__).parent


def printed(name, capsys, code=0):
    """What a script in this folder prints, one string per line, and the
    exit code it ends with, which must be `code`."""
    try:
        runpy.run_path(str(HERE / name), run_name="__main__")
        ended = 0
    except SystemExit as stop:
        ended = stop.code
    assert ended == code
    return [line.rstrip() for line in capsys.readouterr().out.splitlines()]


def test_the_open_share_inside_the_range_is_honest():
    assert verdict(87, 100, 0.786, 0.957) == "honest"
    assert verdict(87, 100, 0.87, 0.95) == "honest"      # on the bottom end


def test_the_open_share_above_the_range_is_spent():
    assert verdict(87, 100, 0.60, 0.85) == "spent"


def test_the_open_share_below_the_range_says_the_sealed_part_is_higher():
    assert verdict(60, 100, 0.786, 0.957) == "sealed is higher"


def test_fifty_emails_notice_a_gap_of_eleven_points_and_not_nine():
    assert verdict(87, 100, *wilson(39, 50)) == "honest"   # 78%, top 87.2%
    assert verdict(87, 100, *wilson(38, 50)) == "spent"    # 76%


def test_the_checks_get_no_verdict_and_the_good_measures_get_the_rule():
    assert replay_sealed.rule("fires: empty draft", 1, 100, 0.0, 0.07) == \
        "table only"
    assert replay_sealed.rule("triage right", 87, 100, 0.0, 0.5) == "spent"
    assert replay_sealed.rule("no check fires", 68, 100, 0.583, 0.825) == \
        "honest"


def test_a_range_row_is_the_wilson_range_and_its_width():
    low, high, width = range_by_n.range_row(50)
    assert (low, high) == pytest.approx(wilson(45, 50))
    assert width == pytest.approx((high - low) * 100)
    assert range_by_n.range_row(100, 0.5)[:2] == pytest.approx(wilson(50, 100))


def test_range_by_n_prints_the_table_of_the_lesson(capsys):
    assert printed("range_by_n.py", capsys) == [
        "a score of 90%, by the emails behind it",
        "  20 emails: 69.9% to 97.2%  (27 points wide)",
        "  50 emails: 78.6% to 95.7%  (17 points wide)",
        " 100 emails: 82.6% to 94.5%  (12 points wide)",
        " 400 emails: 86.7% to 92.6%  (6 points wide)",
        "emails for a range of plus or minus 5 points: 385"]


def test_replay_prints_the_open_and_the_sealed_part_side_by_side(capsys):
    assert printed("replay_sealed.py", capsys) == [
        "measure                        open  sealed   sealed range    rule",
        "triage right                  87/100   45/50    78.6% to 95.7%  honest",
        "fires: wrong script            2/100    2/50     1.1% to 13.5%  table only",
        "fires: missing or old page    10/100    5/50     4.3% to 21.4%  table only",
        "fires: reply to spam           6/100    0/50     0.0% to  7.1%  table only",
        "fires: invented address        2/100    1/50     0.4% to 10.5%  table only",
        "fires: claims an action       10/100    1/50     0.4% to 10.5%  table only",
        "fires: asks for known id       6/100    5/50     4.3% to 21.4%  table only",
        "fires: empty draft             1/100    0/50     0.0% to  7.1%  table only",
        "no check fires                68/100   36/50    58.3% to 82.5%  honest",
        "judge: clear PASS (v4)        58/100   30/50    46.2% to 72.4%  honest"]


def test_open_scores_prints_the_planned_measures_on_the_open_part(capsys):
    lines = printed("open_scores.py", capsys)
    assert lines[0].startswith("triage right") and "87 of 100" in lines[0]
    assert lines[-2].startswith("no check fires") and "68 of 100" in lines[-2]
    assert lines[-1].startswith("judge: clear PASS (v4)")
    assert "58 of 100" in lines[-1] and len(lines) == 10


def test_the_sealed_part_is_spent_and_the_scoring_script_refuses(capsys):
    """Never run again: scores.json exists, so the script must exit at once,
    before it opens a trace or calls a model."""
    assert (replay_sealed.RUNS / "10-sealed" / "scores.json").exists()
    with pytest.raises(SystemExit) as stop:
        runpy.run_path(str(HERE / "score_sealed.py"), run_name="__main__")
    assert "spent" in str(stop.value)
