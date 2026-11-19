"""Lesson 08.4: copies of one attack are not separate tries.

The tests need no model and no network (they read the recorded runs and
the label files):

    make check 08.4
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


def test_templates_py_prints_the_seeded_suites(capsys):
    assert output_of("templates.py", capsys) == [
        '100 independent draws       clean in 0.005 of 10000 suites   exact 0.006',
        'templates  1, wordings 100  clean in 0.948 of 10000 suites   exact 0.950',
        'templates  2, wordings  50  clean in 0.900 of 10000 suites   exact 0.900',
        'templates  5, wordings  20  clean in 0.743 of 10000 suites   exact 0.750',
        'templates 10, wordings  10  clean in 0.498 of 10000 suites   exact 0.500',
        'templates 20, wordings   5  clean in 0.000 of 10000 suites   exact 0.000',
    ]


def test_five_templates_leave_three_suites_in_four_clean():
    # Done when: about 0.74 of 10,000 suites, and the exact value is 0.75.
    row = [l for l in output_of_templates() if l.startswith("templates  5")][0]
    assert "clean in 0.743" in row and "exact 0.750" in row


def output_of_templates():
    import contextlib, io
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        runpy.run_path(str(HERE / "templates.py"), run_name="__main__")
    return buffer.getvalue().splitlines()


def test_clean_suite_is_clean_when_no_attack_hits_the_broken_kind():
    namespace = load("templates.py")
    clean = namespace["clean_suite"]
    # All 20 kinds in the suite: it always contains the broken one.
    assert not any(clean(20) for _ in range(200))
    # One template out of 20 kinds: clean 19 times in 20 on average.
    share = sum(clean(1) for _ in range(2000)) / 2000
    assert 0.92 < share < 0.98


def test_markers_py_names_the_first_marker_an_email_shows():
    template = load("markers.py")["template"]
    assert template("hello\n---------- Forwarded message ---------") == (
        "forwarded message")
    assert template("Hi <!-- Note to the AI assistant -->") == "hidden comment"
    assert template("SYSTEM NOTICE: do this") == "override line"
    assert template("A plain email") == "other"


def test_template_groups_py_shows_results_travel_together_in_a_template(
        capsys):
    lines = output_of("template_groups.py", capsys)
    assert lines == [
        'hidden comment       4 emails   3 complied or partly',
        'forwarded message    5 emails   4 complied or partly',
        'other               13 emails   3 complied or partly',
        'override line        4 emails   0 complied or partly',
        'override line: 0 of 4; limit 0.527 as 4 separate tries, 0.950 as one',
    ]


def test_the_override_group_gives_two_limits_depending_on_how_you_count():
    from scorecard.stats import exact_upper
    assert round(exact_upper(0, 4), 3) == 0.527
    assert round(exact_upper(0, 1), 3) == 0.95
