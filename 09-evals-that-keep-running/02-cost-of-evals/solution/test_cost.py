"""Lesson 09.2: timing a check and the schedule's arithmetic.

No model and no network: the tests read the recorded runs in the repo.
From the top folder: make check 09.2
"""
import re
import runpy
from pathlib import Path

import pytest

import cost_table

HERE = Path(__file__).parent


def printed(name, capsys):
    """What a script in this folder prints, one string per line."""
    runpy.run_path(str(HERE / name), run_name="__main__")
    return [line.rstrip() for line in capsys.readouterr().out.splitlines()]


def test_time_suite_runs_every_check_on_every_pair(monkeypatch):
    seen = []
    monkeypatch.setattr(cost_table, "CHECKS", {
        "a": (lambda e, t: seen.append(("a", e, t)), ""),
        "b": (lambda e, t: seen.append(("b", e, t)), "")})
    seconds = cost_table.time_suite([(1, 2), (3, 4), (5, 6)])
    assert len(seen) == 6 and ("b", 5, 6) in seen
    assert 0 <= seconds < 1


def test_time_suite_counts_the_time_the_checks_take(monkeypatch):
    def slow(email, trace):
        for _ in range(200_000):
            pass
    monkeypatch.setattr(cost_table, "CHECKS", {"slow": (slow, "")})
    assert cost_table.time_suite([(0, 0)]) > 0.001


def test_means_and_totals_read_the_named_fields():
    calls = [{"seconds": 2.0, "tokens": 10}, {"seconds": 4.0, "tokens": 30}]
    assert cost_table.means(calls, "seconds", "tokens") == [3.0, 20.0]
    assert cost_table.totals(calls, "seconds", "tokens") == [6.0, 40]


def test_25_drafts_at_60_seconds_is_25_minutes():
    assert cost_table.minutes_to_read(25, 60) == 25
    assert cost_table.minutes_to_read(10, 90) == 15


def test_the_judges_recorded_cost_is_2_2_seconds_and_91_tokens():
    calls = cost_table.judge_calls("04-heldout")
    seconds, tokens = cost_table.means(calls, "seconds", "completion_tokens")
    assert (round(seconds, 1), round(tokens)) == (2.2, 91)


def test_cost_table_prints_the_table_the_lesson_shows(capsys):
    lines = printed("cost_table.py", capsys)
    # the first line is the one that is timed on your machine
    assert re.fullmatch(
        r"code suite, 550 drafts: \d+\.\d\d s \(\d+\.\d\d ms a draft, "
        r"no tokens\)", lines[0])
    assert lines[1:] == [
        'judge qwen3.5:4b: 2.2 s and 91 reply tokens a verdict (100 calls)',
        'judge qwen3.5:2b: 0.6 s and 71 reply tokens a verdict (100 calls)',
        'person (assumed pace): 60 s a draft',
        '',
        ('writing the 100 drafts of the open part: 159,193 prompt + 13,918 '
         'reply tokens, 4,035 s summed over emails (several ran at once)'),
        'judging 100 drafts: 215 s, 9,113 reply tokens',
        'a person reading 25 drafts: 25 minutes',
    ]
