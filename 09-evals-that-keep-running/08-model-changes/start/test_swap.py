"""Lesson 09.8: the swap, paired, and the judge under two models.

No model and no network: every verdict and every draft is read from the
recorded runs, and the live branch of judge_swap.py is never taken.
From the top folder: make check 09.8
"""
import random
import runpy
import sys
from collections import Counter
from pathlib import Path

import pytest

import compare_judges
import swap_triage
from scorecard import judge

HERE = Path(__file__).parent


def printed(name, capsys):
    """What a script in this folder prints, one string per line."""
    runpy.run_path(str(HERE / name), run_name="__main__")
    return [line.rstrip() for line in capsys.readouterr().out.splitlines()]


def test_changes_by_category_counts_worse_and_better_emails():
    mail = {1: {"category": "refund"}, 2: {"category": "refund"},
            3: {"category": "spam"}, 4: {"category": "spam"}}
    seen, lost, won = swap_triage.changes_by_category(
        mail, [1, 2, 3, 4], [1, 1, 0, 1], [0, 1, 1, 1])
    assert seen == Counter(refund=2, spam=2)
    assert lost == Counter(refund=1) and won == Counter(spam=1)


def test_the_hundred_and_forty_nine_emails_lose_24_and_win_5():
    from plumbing import right, swap
    mail, old, new = swap()
    ids = sorted(new)
    a, b = [[right(mail[i], t[i]) for i in ids] for t in (old, new)]
    seen, lost, won = swap_triage.changes_by_category(mail, ids, a, b)
    assert sum(seen.values()) == 149
    assert (sum(lost.values()), sum(won.values())) == (24, 5)
    assert max(lost.values()) == 5


def test_judge_counts_treat_only_a_clear_pass_as_a_pass():
    human = {1: "pass", 2: "pass", 3: "fail", 4: "fail", 5: "pass"}
    said = {1: "pass", 2: "none", 3: "pass", 4: "unsure", 5: "fail"}
    assert compare_judges.judge_counts(human, said, [1, 2, 3, 4, 5]) == {
        "tp": 1, "fn": 2, "fp": 1, "tn": 1}


def test_judge_counts_leave_out_the_ids_not_asked_for():
    human, said = {1: "pass", 2: "fail"}, {1: "pass", 2: "fail"}
    assert compare_judges.judge_counts(human, said, [1]) == {
        "tp": 1, "fn": 0, "fp": 0, "tn": 0}


@pytest.mark.parametrize("seed", range(5))
def test_judge_counts_agree_with_scorecard_confusion(seed):
    rng = random.Random(seed)
    ids = list(range(40))
    human = {i: rng.choice(["pass", "fail"]) for i in ids}
    said = {i: rng.choice(["pass", "fail", "unsure", "none"]) for i in ids}
    want = judge.confusion([human[i] == "pass" for i in ids],
                           [said[i] == "pass" for i in ids])
    assert compare_judges.judge_counts(human, said, ids) == want


def test_judge_rates_are_passes_kept_and_fails_held_back():
    c = {"tp": 38, "fn": 21, "tn": 16, "fp": 10}
    kept, held = compare_judges.judge_rates(c)
    assert (round(kept, 3), round(held, 3)) == (0.644, 0.615)
    assert round(kept + held - 1, 2) == 0.26


def test_the_smaller_judge_is_no_better_than_a_coin():
    c = {"tp": 9, "fn": 50, "tn": 21, "fp": 5}
    kept, held = compare_judges.judge_rates(c)
    assert round(kept + held - 1, 2) == -0.04


def test_swap_triage_prints_the_pairs_the_range_and_the_categories(capsys):
    assert printed("swap_triage.py", capsys) == [
        'usual 128 of 149 right, smaller 109 of 149',
        "{'both': 104, 'only_a': 24, 'only_b': 5, 'neither': 16}",
        'change -12.8%, range -19.6% to -5.9%, McNemar p 0.0005',
        'category           emails  worse  better',
        'shipping_delay         28      3       0',
        'product_question       18      0       1',
        'order_change           18      5       0',
        'refund                 16      3       0',
        'payment                15      3       1',
        'return                 13      2       2',
        'complaint              12      3       0',
        'other                  10      1       1',
        'spam                    9      3       0',
        'warranty                5      0       0',
        'account                 5      1       0',
    ]


def test_swap_checks_prints_the_table_the_lesson_shows(capsys):
    assert printed("swap_checks.py", capsys) == [
        'check                   usual  smaller',
        'wrong script                3        5',
        'missing or old page        18       18',
        'reply to spam              10        9',
        'invented address            2        3',
        'claims an action           10        3',
        'asks for known id          10       14',
        'empty draft                 0        0',
        'no check fires: usual 101, smaller 102 of 149',
        ("{'both': 79, 'only_a': 22, 'only_b': 23, 'neither': 25} "
         "McNemar p 1.00"),
    ]


def test_compare_judges_prints_both_models_rates(capsys):
    assert printed("compare_judges.py", capsys) == [
        "usual: verdicts {'fail': 18, 'pass': 52, 'unsure': 29, 'none': 1}",
        '  no verdict line: 1, of them on drafts Arjun passed: 0',
        '  passes kept 38 of 59 = 64.4% (range 52% to 75%)',
        '  fails held back 16 of 26 = 61.5% (range 43% to 78%)',
        "smaller: verdicts {'none': 29, 'pass': 16, 'fail': 45, 'unsure': 10}",
        '  no verdict line: 29, of them on drafts Arjun passed: 15',
        '  passes kept 9 of 59 = 15.3% (range 8% to 27%)',
        '  fails held back 21 of 26 = 80.8% (range 62% to 91%)',
    ]


def test_judge_swap_reads_the_recording_and_never_asks_a_model(
        capsys, monkeypatch):
    def refuse(*args, **kwargs):
        raise AssertionError("the live branch was taken")
    monkeypatch.setattr(sys, "argv", ["judge_swap.py"])
    monkeypatch.setattr(judge, "record", refuse)
    assert printed("judge_swap.py", capsys) == [
        "{'pass': 16, 'fail': 45, 'unsure': 10, 'none': 29}"]
