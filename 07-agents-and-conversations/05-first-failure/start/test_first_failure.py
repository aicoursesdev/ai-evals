"""Lesson 07.5: the first failing link, on made-up checks and on the 74
failed trials.

No model and no network. From the top folder: make check 07.5
"""
import runpy
from pathlib import Path

from agents import first_failure, transitions
from first_failure import CHECKS, first_leak
from trials import failed, load

HERE = Path(__file__).parent
ALWAYS = ("always ok", lambda t: True)
NEVER = ("never ok", lambda t: False)
BIG = ("big enough", lambda t: t["n"] > 5)


def printed(name, capsys):
    """What a script in this folder prints, one string per line."""
    runpy.run_path(str(HERE / name), run_name="__main__")
    return [line.rstrip() for line in capsys.readouterr().out.splitlines()]


def test_the_first_check_that_fails_names_the_link():
    assert first_failure({"n": 1}, [ALWAYS, BIG, NEVER]) == "big enough"


def test_a_trial_that_passes_every_check_has_no_failing_link():
    assert first_failure({"n": 9}, [ALWAYS, BIG]) is None


def test_the_order_of_the_checks_decides_which_link_is_first():
    assert first_failure({"n": 1}, [NEVER, BIG]) == "never ok"
    assert first_failure({"n": 1}, [BIG, NEVER]) == "big enough"


def test_transitions_count_each_trials_first_failure_and_none_for_passes():
    trials = [{"n": 1}, {"n": 2}, {"n": 9}]
    assert transitions(trials, [BIG, NEVER]) == {"big enough": 2,
                                                 "never ok": 1}
    assert transitions([{"n": 9}], [BIG]) == {"none": 1}


def test_there_are_74_failed_trials_10_at_temperature_0_and_64_at_0_7():
    rows = failed()
    assert len(rows) == 74
    assert sum(t["temperature"] == 0 for t in rows) == 10
    assert len(load()) == 180


def test_your_first_leak_agrees_with_first_failure_on_every_failed_trial():
    assert [first_leak(t) for t in failed()] == [
        first_failure(t, CHECKS) for t in failed()]


def test_the_first_failing_links_count_6_5_36_13_0_13_and_1_of_the_74():
    counts = transitions(failed(), CHECKS)
    assert [counts.get(name, 0) for name, _ in CHECKS] == [
        6, 5, 36, 13, 0, 13, 1]


def test_at_temperature_0_the_links_count_1_1_4_3_0_1_and_0(capsys):
    lines = printed("first_failure.py", capsys)
    cold = [int(line.split()[-1]) for line in lines[2:9]]
    assert lines[1] == "temperature 0: 10 trials failed the outcome"
    assert cold == [1, 1, 4, 3, 0, 1, 0]


def test_at_temperature_0_7_the_links_count_5_4_32_10_0_12_and_1(capsys):
    lines = printed("first_failure.py", capsys)
    hot = [int(line.split()[-1]) for line in lines[11:18]]
    assert lines[10] == "temperature 0.7: 64 trials failed the outcome"
    assert hot == [5, 4, 32, 10, 0, 12, 1]


def test_the_invented_order_number_in_rf_23_is_its_first_failing_link(
        capsys):
    lines = printed("first_failure.py", capsys)
    assert "RF-23 ask_for_info -> 1 invented an order id" in lines


def test_the_36_wrong_decisions_split_into_18_5_7_and_6(capsys):
    lines = printed("first_failure.py", capsys)
    split = {tuple(line.split()[1:-1]): int(line.split()[-1])
             for line in lines[-5:]}
    assert sum(split.values()) == 36
    assert sorted(split.values()) == [2, 4, 5, 7, 18]


def test_the_weakest_scenarios_are_five_asks_one_approval_and_one_denial(
        capsys):
    lines = printed("scenario_audit.py", capsys)
    assert lines[0] == "scenarios with 0 or 1 right trial out of 6:"
    assert [line.split()[0] for line in lines[1:]] == [
        "RF-12", "RF-17", "RF-23", "RF-24", "RF-27", "RF-10", "RF-28"]
    assert [line.split()[1] for line in lines[1:]] == [
        "0/6", "0/6", "0/6", "0/6", "0/6", "1/6", "1/6"]
