"""Lesson 09.3: a gate that does not cry wolf, in your own functions.

No model and no network: the tests read the recorded runs in the repo.
From the top folder: make check 09.3
"""
import runpy
from pathlib import Path

import pytest

import gate
import margin_gate
import naive_gate
from scorecard import report, stats

HERE = Path(__file__).parent


def printed(name, capsys, code=0):
    """What a script in this folder prints, one string per line; the exit
    code a script ends with must be `code` (0 when it does not exit)."""
    try:
        runpy.run_path(str(HERE / name), run_name="__main__")
        ended = 0
    except SystemExit as stop:
        ended = stop.code
    assert ended == code
    return [line.rstrip() for line in capsys.readouterr().out.splitlines()]


def test_the_naive_gate_fails_every_rerun_below_the_baseline():
    assert naive_gate.naive_fails(82, [76, 82, 83, 81, 85]) == 2
    assert naive_gate.naive_fails(82, []) == 0


def test_the_margin_is_two_standard_deviations():
    assert margin_gate.margin([10, 12, 14]) == pytest.approx(4.0)
    assert margin_gate.margin([5, 5, 5]) == 0


def test_a_rerun_passes_if_it_is_within_the_margin():
    scores = [10, 12, 14]                     # the margin is 4
    assert margin_gate.margin_fails(14, scores) == 0      # floor 10
    assert margin_gate.margin_fails(15, scores) == 1      # floor 11
    assert margin_gate.margin_fails(20, scores) == 3      # floor 16


def test_the_ship_rule_has_the_four_floors_of_the_lesson():
    assert gate.ship_rule() == [
        ("triage right", 0.80, True), ("no check fires", 0.70, True),
        ("triage change", -0.02, True), ("checks change", -0.02, True)]


def test_the_ship_rule_passes_and_fails_through_scorecard_gate():
    good = {"triage right": (0.81, 0.85, 0.9),
            "no check fires": (0.7, 0.8, 0.9),
            "triage change": (-0.02, 0, 0.02),
            "checks change": (0, 0.05, 0.1)}
    assert report.gate(good, gate.ship_rule()) == (True, [])
    bad = dict(good, **{"no check fires": (0.69, 0.8, 0.9)})
    passed, reasons = report.gate(bad, gate.ship_rule())
    assert not passed and len(reasons) == 1


def fake(n, right_old, right_new):
    """n emails whose triage (and a draft check) are right as listed."""
    mail = {i: {"category": "refund"} for i in range(n)}
    pick = lambda hits: {i: {"triage": {"category": "refund" if i in hits
                                        else "other"}} for i in range(n)}
    return mail, pick(right_old), pick(right_new)


def test_scores_measure_the_new_version_and_its_change(monkeypatch):
    monkeypatch.setattr(gate, "clean", lambda e, t: 1)
    mail, old, new = fake(10, set(range(5)), set(range(8)))
    found, n = gate.scores(mail, old, new)
    assert n == 10
    assert found["triage right"][1] == 0.8
    assert found["triage right"][::2] == pytest.approx(stats.wilson(8, 10))
    a, b = [1] * 5 + [0] * 5, [1] * 8 + [0] * 2
    p = stats.paired(a, b)
    assert found["triage change"] == pytest.approx(
        (p["low"], p["diff"], p["high"]))
    assert found["no check fires"][1] == 1 and found["checks change"][1] == 0


def test_scores_use_only_emails_both_versions_answered(monkeypatch):
    monkeypatch.setattr(gate, "clean", lambda e, t: 1)
    mail, old, new = fake(10, set(range(10)), set(range(10)))
    del new[9]
    assert gate.scores(mail, old, new)[1] == 9


def test_naive_gate_prints_what_the_lesson_shows(capsys):
    assert printed("naive_gate.py", capsys) == [
        ('triage right: baseline 82, 20 unchanged reruns scored 76 to 85; '
         'the naive gate failed 2'),
        ('no check fires: baseline 78, 5 unchanged reruns scored 73 to 78; '
         'the naive gate failed 4'),
    ]


def test_margin_gate_prints_what_the_lesson_shows(capsys):
    assert printed("margin_gate.py", capsys) == [
        ('triage right: spread (std dev) 2.0 emails of 100, margin 4.0; '
         'gate fails 1 of 20'),
        '  mean of the reruns 82.3 against baseline 82',
        ('no check fires: spread (std dev) 2.3 emails of 100, margin 4.6; '
         'gate fails 2 of 5'),
        '  mean of the reruns 75.4 against baseline 78',
        ('paired low ends, 5 unchanged check reruns: -0.135 to -0.074'),
    ]


def test_gate_passes_hd_2_and_exits_with_0(capsys):
    assert printed("gate.py", capsys, code=0) == [
        'hd-2 against hd-1 on 277 emails',
        'triage right    +0.856  range +0.809 to +0.892',
        'triage change   +0.000  range +0.000 to +0.000',
        'no check fires  +0.816  range +0.766 to +0.857',
        'checks change   +0.054  range +0.010 to +0.098',
        'gate passed: True',
    ]


def test_gate_says_no_to_the_smaller_model(capsys):
    assert printed("gate_says_no.py", capsys) == [
        'smaller model against hd-1 on 149 emails',
        'triage right    +0.732  range +0.655 to +0.796',
        'triage change   -0.128  range -0.196 to -0.059',
        'no check fires  +0.685  range +0.606 to +0.754',
        'checks change   +0.007  range -0.082 to +0.095',
        'gate passed: False',
        '  triage right: lower end 0.655 below 0.8',
        '  no check fires: lower end 0.606 below 0.7',
        '  triage change: lower end -0.196 below -0.02',
        '  checks change: lower end -0.082 below -0.02',
    ]
