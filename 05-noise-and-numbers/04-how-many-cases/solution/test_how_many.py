"""Lesson 05.4: how many cases a width needs, in your own function.

No model and no network. From the top folder: make check 05.4
"""
import runpy
from pathlib import Path

import pytest

import how_many
from scorecard.stats import sample_size

HERE = Path(__file__).parent


def printed(name, capsys):
    """What a script in this folder prints, one string per line."""
    runpy.run_path(str(HERE / name), run_name="__main__")
    return [line.rstrip() for line in capsys.readouterr().out.splitlines()]


def test_plus_or_minus_5_points_in_the_worst_case_needs_385_cases():
    assert how_many.cases_needed(0.05, 0.5) == 385


def test_half_the_margin_needs_four_times_the_cases_1537():
    assert how_many.cases_needed(0.025, 0.5) == 1537


def test_a_rate_near_90_needs_far_fewer_cases_139():
    assert how_many.cases_needed(0.05, 0.9) == 139


def test_meeras_3_points_at_93_percent_needs_278_emails():
    assert how_many.cases_needed(0.03, 0.93) == 278


def test_it_rounds_up_96_04_cases_is_97():
    assert how_many.cases_needed(0.10, 0.5) == 97


@pytest.mark.parametrize("margin", [0.10, 0.05, 0.025, 0.02, 0.01])
@pytest.mark.parametrize("p", [0.5, 0.9, 0.95])
def test_it_agrees_with_scorecard_stats(margin, p):
    assert how_many.cases_needed(margin, p) == sample_size(margin, p)


def test_how_many_prints_the_two_lines_the_lesson_shows(capsys):
    assert printed("how_many.py", capsys) == [
        'by hand: 385  sample_size: 385',
        'margin   p = 0.5   p = 0.9   p = 0.95',
        '+-10.0%       97        35         19',
        '+- 5.0%      385       139         73',
        '+- 2.5%     1537       554        292',
        '+- 2.0%     2401       865        457',
        '+- 1.0%     9604      3458       1825',
    ]


def test_what_sets_detect_prints_the_range_each_set_can_see(capsys):
    assert printed("what_sets_detect.py", capsys) == [
        'cases  range for one score   two separate sets must differ by',
        '   20  +-14.2%             about 20.1%',
        '   50  +- 9.0%             about 12.7%',
        '  100  +- 6.4%             about  9.0%',
        '  277  +- 3.8%             about  5.4%',
        '  550  +- 2.7%             about  3.8%',
    ]
