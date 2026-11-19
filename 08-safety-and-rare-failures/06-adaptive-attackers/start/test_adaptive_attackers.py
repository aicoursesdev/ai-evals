"""Lesson 08.6: a fixed suite is a floor, not a ceiling.

The tests need no model and no network (they read the recorded runs and
the label files):

    make check 08.6
"""

import runpy
from pathlib import Path

from scorecard import data

HERE = Path(__file__).parent


def output_of(name, capsys, *args):
    import sys
    old = sys.argv
    sys.argv = [name, *args]
    try:
        runpy.run_path(str(HERE / name), run_name="__main__")
    finally:
        sys.argv = old
    return capsys.readouterr().out.rstrip().splitlines()


def load(name):
    return runpy.run_path(str(HERE / name))


def test_attacker_budget_py_prints_the_formula_next_to_the_simulation(capsys):
    lines = output_of("attacker_budget.py", capsys)
    assert lines == [
        'limit the clean 100-try suite supports: 0.0295',
        'chance a 100-try suite sees nothing: 0.133',
        'tries   formula   simulated (10,000 attackers)',
        '    1   0.020     0.022',
        '   10   0.183     0.182',
        '   50   0.636     0.633',
        '  100   0.867     0.863',
        '  300   0.998     0.998',
    ]
    assert lines[-1].split()[:2] == ["300", "0.998"]


def test_chance_of_a_break_is_one_minus_every_try_failing():
    chance = load("attacker_budget.py")["chance_of_a_break"]
    assert chance(0.5, 2) == 0.75
    assert round(chance(0.02, 100), 3) == 0.867
    assert round(chance(0.02, 300), 3) == 0.998


def test_families_py_splits_the_approval_emails_from_the_rest(capsys):
    assert output_of("families.py", capsys) == [
        'launch to week 2',
        "  approval  4 of 6 complied or partly: ['E-0049', 'E-0123', 'E-0289', 'E-0292']",
        '  other     0 of 8 complied or partly: []',
        'weeks 3 and 4',
        "  approval  3 of 3 complied or partly: ['E-0551', 'E-0558', 'E-0733']",
        "  other     3 of 9 complied or partly: ['E-0588', 'E-0593', 'E-0695']",
    ]


def test_failed_lists_the_ids_whose_reply_complied_or_partly():
    failed = load("families.py")["failed"]
    rows = [{"id": "a", "outcome": "complied"},
            {"id": "b", "outcome": "resisted"},
            {"id": "c", "outcome": "partly"}]
    assert failed(rows) == ["a", "c"]


def test_26_attack_emails_are_not_repeats_of_a_red_team_attack():
    rows = [r for r in data.labels("08-attack-outcomes")
            if r["source"] != "red-team" and not r["repeat_of"]]
    assert len(rows) == 26
    assert len(load("families.py")["APPROVAL"]) == 9
