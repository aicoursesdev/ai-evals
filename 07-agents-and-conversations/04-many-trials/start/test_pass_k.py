"""Lesson 07.4: pass@k and pass^k, on worked examples and on the 150 hot
trials.

No model and no network. From the top folder: make check 07.4
"""
import runpy
from pathlib import Path

import pytest

from agents import pass_at_k, pass_hat_k
from trials import hot, passed, scenarios

HERE = Path(__file__).parent


def printed(name, capsys):
    """What a script in this folder prints, one string per line."""
    runpy.run_path(str(HERE / name), run_name="__main__")
    return [line.rstrip() for line in capsys.readouterr().out.splitlines()]


def test_four_right_in_five_gives_pass_hat_3_of_0_4_and_pass_hat_2_of_0_6():
    assert pass_hat_k([4], [5], 3) == pytest.approx(0.4)
    assert pass_hat_k([4], [5], 2) == pytest.approx(0.6)


def test_four_right_in_five_gives_pass_at_2_of_1():
    assert pass_at_k([4], [5], 2) == pytest.approx(1.0)


def test_three_right_in_five_gives_pass_hat_2_of_0_3_and_pass_at_2_of_0_9():
    assert pass_hat_k([3], [5], 2) == pytest.approx(0.3)
    assert pass_at_k([3], [5], 2) == pytest.approx(0.9)


def test_at_k_1_both_measures_are_the_plain_success_rate():
    c = [0, 1, 4, 5]
    assert pass_at_k(c, [5] * 4, 1) == pytest.approx(0.5)
    assert pass_hat_k(c, [5] * 4, 1) == pytest.approx(0.5)


def test_the_whole_agent_number_is_the_average_over_tasks():
    assert pass_hat_k([5, 0], [5, 5], 3) == pytest.approx(0.5)
    assert pass_at_k([5, 0], [5, 5], 3) == pytest.approx(0.5)


def test_pass_at_k_never_falls_and_pass_hat_k_never_rises_as_k_grows():
    c = [0, 1, 2, 3, 4, 5]
    at = [pass_at_k(c, [5] * 6, k) for k in range(1, 6)]
    hat = [pass_hat_k(c, [5] * 6, k) for k in range(1, 6)]
    assert at == sorted(at) and hat == sorted(hat, reverse=True)


def test_the_hot_trials_are_150_five_per_scenario():
    assert len(hot) == 150
    assert {sid: sum(t["id"] == sid for t in hot)
            for sid in scenarios} == {sid: 5 for sid in scenarios}


def test_the_hot_agent_has_pass_at_k_and_pass_hat_k_at_k_1_3_and_5():
    c = [sum(passed(t) for t in hot if t["id"] == sid) for sid in scenarios]
    n = [5] * 30
    got = [(pass_at_k(c, n, k), pass_hat_k(c, n, k)) for k in (1, 3, 5)]
    assert got == [(pytest.approx(0.573, abs=5e-4),) * 2,
                   (pytest.approx(0.787, abs=5e-4),
                    pytest.approx(0.307, abs=5e-4)),
                   (pytest.approx(0.833, abs=5e-4),
                    pytest.approx(0.167, abs=5e-4))]


def test_by_hand_counts_5_3_2_6_9_5_scenarios_and_the_same_numbers(capsys):
    lines = printed("by_hand.py", capsys)
    assert lines[1] == "[(0, 5), (1, 3), (2, 2), (3, 6), (4, 9), (5, 5)]"
    assert lines[2:] == [
        "k=1  pass@1 0.573   pass^1 0.573",
        "k=2  pass@2 0.733   pass^2 0.413",
        "k=3  pass@3 0.787   pass^3 0.307",
        "k=5  pass@5 0.833   pass^5 0.167"]


def test_with_the_harness_pass_hat_3_has_a_95_percent_range_0_19_to_0_44(
        capsys):
    lines = printed("with_scorecard.py", capsys)
    assert lines[:3] == ["pass@1 0.573   pass^1 0.573",
                         "pass@3 0.787   pass^3 0.307",
                         "pass@5 0.833   pass^5 0.167"]
    assert lines[3] == "pass^3 0.307, 95% range 0.19 to 0.44"


def test_one_run_at_temperature_0_passed_20_of_30_with_range_0_49_to_0_81(
        capsys):
    lines = printed("with_scorecard.py", capsys)
    assert lines[4] == ("temperature 0, one run: 20/30 = 0.667, "
                        "Wilson 95% 0.49 to 0.81")
    assert "+0.093" in lines[5] and "-0.01 to +0.20" in lines[5]
