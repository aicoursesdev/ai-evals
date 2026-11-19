"""Lesson 00.4: the score moves with the emails, and the wording with the run.

The tests need no model and no network (they read the recorded runs):

    make check 00.4
"""

import runpy
from pathlib import Path

from scorecard import data

HERE = Path(__file__).parent


def output_of(name, capsys):
    runpy.run_path(str(HERE / name), run_name="__main__")
    return capsys.readouterr().out


def test_slices_py_scores_the_launch_sets_and_three_slices_of_week_1(capsys):
    assert output_of("slices.py", capsys).splitlines()[:5] == [
        "launch dev : 88 of 100",
        "launch test: 42 of 50",
        "week 1, emails 1-50: 47 of 50",
        "week 1, emails 51-100: 47 of 50",
        "week 1, emails 101-150: 43 of 50",
    ]


def test_slices_py_1000_seeded_draws_of_50_range_from_41_to_50(capsys):
    last = output_of("slices.py", capsys).splitlines()[5]
    assert last == "1000 random draws of 50 from week 1: 41 to 50 of 50"


def test_the_three_week_1_slices_add_up_to_137_of_150_which_is_91_percent():
    assert 47 + 47 + 43 == 137
    assert round(137 / 150, 3) == 0.913


def test_repeats_py_scores_every_run_9_of_10_on_the_category(capsys):
    lines = output_of("repeats.py", capsys).splitlines()
    assert lines[0] == "run                category   all three labels"
    assert lines[1:7] == [
        "temp-0.7-seed-1    9 of 10    5 of 10",
        "temp-0.7-seed-2    9 of 10    6 of 10",
        "temp-0.7-seed-3    9 of 10    5 of 10",
        "temp-0.7-seed-4    9 of 10    5 of 10",
        "temp-0.7-seed-5    9 of 10    5 of 10",
        "temp-0             9 of 10    6 of 10",
    ]


def test_at_temperature_0_all_10_answers_match_the_original_trace(capsys):
    out = output_of("repeats.py", capsys)
    assert ("temperature 0 vs the original week-1 trace: "
            "10 of 10 identical") in out


def test_repeats_py_counts_label_sets_and_drafts_per_email(capsys):
    rows = output_of("repeats.py", capsys).splitlines()[-10:]
    counts = [tuple(map(int, line.split()[1:])) for line in rows]
    assert counts == [(1, 5), (1, 5), (1, 5), (1, 5), (2, 5),
                      (2, 5), (2, 5), (1, 5), (1, 5), (2, 5)]
    assert rows[0].split()[0] == "E-0151"


def test_two_drafts_py_shows_e_0211_worded_differently_with_the_same_facts(
        capsys):
    out = output_of("two_drafts.py", capsys)
    assert "temp-0.7-seed-1" in out and "temp-0.7-seed-2" in out
    assert "You don't send items back directly" in out
    assert "Unfortunately, we do not offer direct exchanges" in out


def test_the_recorded_runs_are_6_files_of_the_same_10_emails():
    runs = data.run("00-ask-twice")
    assert len(runs) == 6
    ids = [[row["id"] for row in rows] for rows in runs.values()]
    assert all(i == ids[0] for i in ids) and len(ids[0]) == 10
