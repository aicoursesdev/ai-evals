"""Lesson 08.3: zero failures and the limit they allow.

The tests need no model and no network (they read the recorded runs and
the label files):

    make check 08.3
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


def test_clean_chances_py_prints_the_chance_of_a_clean_run_of_100(capsys):
    assert output_of("clean_chances.py", capsys) == [
        'true rate 1%: chance of 0 failures in 100 = 0.366',
        'true rate 3%: chance of 0 failures in 100 = 0.048',
        'true rate 5%: chance of 0 failures in 100 = 0.006',
    ]


def test_chance_clean_multiplies_one_clean_try_by_itself():
    chance = load("clean_chances.py")["chance_clean"]
    assert chance(0.5, 3) == 0.125
    assert round(chance(0.03, 100), 3) == 0.048


def test_by_hand_py_prints_the_limit_and_the_rule_of_three(capsys):
    lines = output_of("by_hand.py", capsys)
    assert lines == [
        '   10 clean trials: exact 0.2589   3/n = 0.3000',
        '   30 clean trials: exact 0.0950   3/n = 0.1000',
        '   59 clean trials: exact 0.0495   3/n = 0.0508',
        '  100 clean trials: exact 0.0295   3/n = 0.0300',
        '  300 clean trials: exact 0.0099   3/n = 0.0100',
        ' 1000 clean trials: exact 0.0030   3/n = 0.0030',
        'smallest n with limit under 5%: 59',
    ]


def test_the_exact_limit_after_zero_failures_in_100_is_0_0295():
    upper = load("by_hand.py")["upper_limit"]
    assert round(upper(100), 4) == 0.0295
    assert abs(upper(1000) - 3 / 1000) < 0.0001
    assert upper(59) < 0.05 <= upper(58)


def test_with_scorecard_py_prints_0_0295_for_zero_failures_in_100(capsys):
    lines = output_of("with_scorecard.py", capsys)
    assert lines == [
        '0 failures in 100',
        '  rule of three       0.03',
        '  exact upper limit   0.0295',
        '  two-sided interval  [0.0, 0.0362]',
        '  Wilson interval     [0.0, 0.037]',
        'failures in 100 -> one-sided upper limit, two-sided interval',
        '  0: upper 0.0295   interval 0.0000 to 0.0362',
        '  1: upper 0.0466   interval 0.0003 to 0.0545',
        '  2: upper 0.0616   interval 0.0024 to 0.0704',
        '  3: upper 0.0757   interval 0.0062 to 0.0852',
        '298 clean trials: limit 0.01000',
        '299 clean trials: limit 0.00997',
    ]
    assert "0.0295" in lines[2]


def test_limits_returns_the_one_sided_limit_and_the_interval():
    limits = load("with_scorecard.py")["limits"]
    upper, (low, high) = limits(2, 100)
    assert round(upper, 4) == 0.0616
    assert (round(low, 4), round(high, 4)) == (0.0024, 0.0704)


def test_our_counts_py_puts_a_limit_on_each_harm(capsys):
    assert output_of("our_counts.py", capsys) == [
        'harm           fail/trials   upper limit   95% interval',
        'money            2/6          0.729         0.043 to 0.777',
        'personal_data    1/4          0.751         0.006 to 0.806',
        'account          0/1          0.950         0.000 to 0.975',
        'internal_info    0/2          0.776         0.000 to 0.842',
        'false_policy     1/1          1.000         0.025 to 1.000',
        'all harms        4/14         0.540         0.084 to 0.581',
    ]


def test_count_by_harm_counts_the_outcomes_it_is_given():
    count = load("our_counts.py")["count_by_harm"]
    rows = [{"harm": "money", "outcome": "partly"},
            {"harm": "money", "outcome": "complied"},
            {"harm": "account", "outcome": "resisted"}]
    assert count(rows, {"complied", "partly"}) == {
        "money": (2, 2), "account": (0, 1)}
    assert count(rows, {"complied"})["money"] == (1, 2)
