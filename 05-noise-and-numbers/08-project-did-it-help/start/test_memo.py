"""Lesson 05.8: did the change help? The memo's numbers and the memo.

No model and no network: the tests read the recorded drafts in the repo.
From the top folder: make check 05.8
"""
import re
import runpy
from pathlib import Path

import pytest

import memo
from scorecard import stats

HERE = Path(__file__).parent


def printed(name, capsys):
    """What a script in this folder prints, one string per line."""
    runpy.run_path(str(HERE / name), run_name="__main__")
    return [line.rstrip() for line in capsys.readouterr().out.splitlines()]


def test_a_reported_rate_gives_the_share_the_count_and_the_range():
    assert memo.line("hd-1, no check firing", 211, 277) == (
        "hd-1, no check firing: 76.2% (211 of 277), "
        "95% range 70.8% to 80.8%")


def test_a_rate_of_100_percent_still_gets_a_range_below_it():
    assert memo.line("all", 100, 100) == (
        "all: 100.0% (100 of 100), 95% range 96.3% to 100.0%")


def test_five_changes_all_one_way_are_not_quite_enough_for_p_under_0_05():
    a, b = [0] * 5 + [1] * 3, [1] * 5 + [1] * 3
    out = memo.compare(a, b)
    assert out["pairs"] == {"both": 3, "only_a": 0, "only_b": 5, "neither": 0}
    assert out["paired"]["diff"] == pytest.approx(5 / 8)
    assert out["p"] == pytest.approx(2 / 32)


def test_compare_agrees_with_scorecard_stats_on_the_277_pairs():
    a = [1] * 199 + [1] * 12 + [0] * 27 + [0] * 39
    b = [1] * 199 + [0] * 12 + [1] * 27 + [0] * 39
    out = memo.compare(a, b)
    assert out["pairs"] == stats.pair_counts(a, b)
    assert out["p"] == stats.mcnemar(a, b)
    assert round(out["paired"]["diff"], 3) == 0.054


def test_memo_prints_the_six_lines_the_lesson_shows(capsys):
    assert printed("memo.py", capsys) == [
        'hd-1, no check firing: 76.2% (211 of 277), 95% range 70.8% to 80.8%',
        'hd-2, no check firing: 81.6% (226 of 277), 95% range 76.6% to 85.7%',
        "pairs: {'both': 199, 'only_a': 12, 'only_b': 27, 'neither': 39}",
        'paired difference +5.4%, range +1.0% to +9.8%',
        'bootstrap range +1.1% to +9.7%',
        'McNemar exact p-value: 0.0237',
    ]


def test_length_check_prints_the_checks_by_draft_length(capsys):
    assert printed("length_check.py", capsys) == [
        'hd-1 drafts by length   drafts  with a check firing',
        '   0 to 60   words       21       7 (33%)',
        '  60 to 80   words      161      50 (31%)',
        '  80 to 100  words      246      58 (24%)',
        ' 100 to 1000 words      121      18 (15%)',
    ]


def test_the_memo_is_one_page_with_the_numbers_and_the_sections():
    text = (HERE / "memo.md").read_text(encoding="utf-8")
    heads = " ".join(re.findall(r"^#+ (.*)$", text, re.M)).lower()
    numbers = ["211", "226", "277", "199", "12", "27", "39", "+1.0", "+9.8"]
    todo = ("TODO 05.8: write memo.md: the answer, what was held fixed, "
            "the result with the numbers from memo.py, what it does not "
            "cover and a recommendation, see the lesson's 'The memo' "
            "section")
    assert "TODO" not in text, todo
    assert all(n in text for n in numbers), todo
    assert all(w in heads for w in (
        "answer", "held fixed", "result", "does not cover",
        "recommendation")), todo
    assert len(text.split()) <= 700, "the memo is one page: 700 words at most"
