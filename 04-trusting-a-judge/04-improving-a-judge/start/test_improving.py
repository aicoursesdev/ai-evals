"""Lesson 04.4: comparing judge versions by the two rates, in your own code.

No model and no network: every verdict comes from a recorded run in the repo.
From the top folder: make check 04.4
"""
import runpy
import sys
from pathlib import Path

import pytest

import compare_versions as cv
from judge_versions import DEV, path
from plumbing import arjun, chosen, template, verdicts
from scorecard.judge import rates

HERE = Path(__file__).parent
EXAMPLES = ["E-0660", "E-0602", "E-0398"]


def printed(name, capsys, monkeypatch, *argv):
    """What a script here prints with these arguments, one string per line."""
    monkeypatch.setattr(sys, "argv", [name, *argv])
    runpy.run_path(str(HERE / name), run_name="__main__")
    return [line.rstrip() for line in capsys.readouterr().out.splitlines()]


def test_choose_takes_the_highest_sum_of_the_two_rates():
    sums = {"v1": 1.21, "v2": 1.19, "v3": 1.22, "v4": 1.40}
    assert cv.choose(sums) == "v4"


def test_a_high_rate_on_one_side_does_not_win_on_its_own():
    assert cv.choose({"a": 0.9 + 0.2, "b": 0.6 + 0.6}) == "b"


def test_score_version_counts_the_two_rates_the_counts_and_no_line_replies():
    ids = DEV[:6]
    human = dict(zip(ids, ["pass", "pass", "fail", "fail", "unsure", "pass"]))
    seen = dict(zip(ids, ["pass", "none", "pass", "fail", "pass", "unsure"]))
    tpr, tnr, c, none = cv.score_version(human, seen)
    assert (tpr, tnr, none) == (1 / 3, 1 / 2, 1)
    assert c == {"tp": 1, "fp": 1, "fn": 2, "tn": 1}


def test_score_version_leaves_out_the_skipped_drafts_and_unrecorded_ones():
    ids = DEV[:5]
    human = dict(zip(DEV, ["pass", "fail"] * 50))
    seen = dict(zip(ids, ["pass", "pass", "fail", "fail", "pass"]))
    _, _, c, _ = cv.score_version(human, seen, skip={ids[0]})
    assert sum(c.values()) == 4
    seen = {i: "pass" for i in ids}
    _, _, c, _ = cv.score_version(human, seen)
    assert sum(c.values()) == 5


@pytest.mark.parametrize("version", ["v1", "v2", "v3", "v4"])
def test_the_hand_rates_agree_with_scorecard_rates(version):
    human, seen = arjun("03-right-rule-arjun"), verdicts(path(version))
    ids = [i for i in DEV if i not in EXAMPLES and human[i] != "unsure"]
    person = [human[i] == "pass" for i in ids]
    judged = [seen[i] == "pass" for i in ids]
    tpr, tnr, _, _ = cv.score_version(human, seen, set(EXAMPLES))
    assert (tpr, tnr) == pytest.approx(rates(person, judged))


def test_the_four_versions_score_as_the_lesson_shows():
    human, got = arjun("03-right-rule-arjun"), {}
    for v in ("v1", "v2", "v3", "v4"):
        tpr, tnr, c, none = cv.score_version(
            human, verdicts(path(v)), set(EXAMPLES))
        got[v] = (c["tp"], c["tp"] + c["fn"], c["tn"], c["tn"] + c["fp"],
                  round(tpr + tnr, 2), none)
    assert got == {"v1": (37, 60, 16, 27, 1.21, 3),
                   "v2": (36, 60, 16, 27, 1.19, 3),
                   "v3": (31, 60, 19, 27, 1.22, 5),
                   "v4": (44, 60, 18, 27, 1.40, 4)}


def test_the_rule_picks_v4_from_the_recorded_versions():
    human, sums = arjun("03-right-rule-arjun"), {}
    for v in ("v1", "v2", "v3", "v4"):
        tpr, tnr, _, _ = cv.score_version(human, verdicts(path(v)),
                                          set(EXAMPLES))
        sums[v] = tpr + tnr
    assert cv.choose(sums) == "v4"


def test_the_held_out_prompt_is_the_chosen_development_prompt():
    assert chosen() == template("v4")


def test_compare_versions_prints_the_table_the_lesson_shows(capsys,
                                                            monkeypatch):
    assert printed("compare_versions.py", capsys, monkeypatch,
                   "v1,v2,v3,v4", *EXAMPLES) == [
        'version  kept  caught  tpr    tnr    tpr+tnr  no line',
        'v1       37/60  16/27   61.7%  59.3%    1.21      3',
        'v2       36/60  16/27   60.0%  59.3%    1.19      3',
        'v3       31/60  19/27   51.7%  70.4%    1.22      5',
        'v4       44/60  18/27   73.3%  66.7%    1.40      4',
        'highest tpr + tnr: v4',
    ]


def test_judge_versions_replays_the_recording_and_counts_it(capsys,
                                                            monkeypatch):
    assert printed("judge_versions.py", capsys, monkeypatch, "v2") == [
        "v2 {'pass': 54, 'fail': 28, 'unsure': 15, 'none': 3}"]
    assert printed("judge_versions.py", capsys, monkeypatch, "v4") == [
        "v4 {'pass': 58, 'fail': 23, 'unsure': 14, 'none': 5}"]


def test_judge_heldout_prints_the_two_rates_on_the_held_out_drafts(
        capsys, monkeypatch):
    assert printed("judge_heldout.py", capsys, monkeypatch) == [
        ("{'tp': 38, 'fp': 10, 'fn': 21, 'tn': 16} passes kept 64.4%, "
         "fails held back 61.5%"),
        "Arjun's unsure drafts, judge says: {'fail': 1, 'none': 1, "
        "'pass': 4, 'unsure': 9}",
        'no verdict line: 1',
    ]
