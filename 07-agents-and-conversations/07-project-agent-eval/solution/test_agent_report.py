"""Lesson 07.7: your checks on made-up trials, then the report's figures on
the 180 recordings.

No model and no network. From the top folder: make check 07.7
"""
import json
import runpy
from collections import Counter
from pathlib import Path

import pytest

from checks import CHECKS, RULES, outcome_ok
from scorecard import data

HERE = Path(__file__).parent
SCENARIO = {"id": "RF-01", "expected": "approve_proposal",
            "refund_inr": 2299, "order_id": "TW-1"}


def call(tool, order_id="TW-1", result=None):
    return {"tool": tool, "arguments": json.dumps({"order_id": order_id}),
            "result": result or {}}


def propose(amount=2299, who="Arjun"):
    done = {"status": "proposed", "amount_inr": amount, "waiting_for": who}
    return call("propose_refund", result=done)


def trial(calls, outcome="approve_proposal", amount=2299, **more):
    base = {"trajectory": list(calls), "outcome": outcome,
            "refund_inr": amount, "stop": "answered", "reply": "ok",
            "final_raw": "ok", "scenario": SCENARIO}
    return base | more


@pytest.fixture(scope="module")
def trials():
    scenarios = {s["id"]: s for s in data.scenarios()}
    rows = data.run("07-refund-trials")["hd-1"]
    return [{**t, "scenario": scenarios[t["id"]]} for t in rows]


def test_a_trial_that_said_and_left_the_right_thing_passes_the_outcome():
    assert outcome_ok(trial([call("get_order"), propose()]))


def test_a_right_answer_with_no_proposal_fails_the_outcome():
    assert not outcome_ok(trial([call("get_order")]))


def test_a_right_proposal_with_the_wrong_answer_fails_the_outcome():
    assert not outcome_ok(trial([propose()], outcome="deny", amount=None))


def test_the_checks_come_in_the_order_things_happen_in_a_run():
    assert len(CHECKS) == 7
    names = [name for name, _ in CHECKS]
    assert names[0].startswith("invented") and names[2] == "wrong decision"
    assert names[-1].startswith("wrong outcome")


def test_each_path_rule_is_broken_by_the_trial_it_names():
    good = trial([call("get_order"), propose()])
    assert all(rule(good) for rule in RULES.values())
    broken = {
        "order id as given": trial([call("get_order", "ORD-9")]),
        "real tools only": trial([call("ask_for_info")]),
        "one proposal": trial([propose(), propose()]),
        "within the step cap": trial([], stop="step cap"),
        "does not say it is done": trial(
            [], reply="Your refund has been approved."),
    }
    assert list(broken) == list(RULES)
    for name, bad in broken.items():
        assert not RULES[name](bad), name


def test_20_of_30_trials_at_temperature_0_are_right(trials):
    cold = [t for t in trials if t["temperature"] == 0]
    assert (len(cold), sum(outcome_ok(t) for t in cold)) == (30, 20)


def test_106_of_the_180_trials_are_right(trials):
    assert sum(outcome_ok(t) for t in trials) == 106


def test_by_kind_the_right_trials_are_35_17_53_and_1(trials):
    def right(kind):
        group = [t for t in trials if t["scenario"]["expected"] == kind]
        return sum(map(outcome_ok, group)), len(group)
    assert [right(k) for k in ("approve_proposal", "escalate_to_meera",
                               "deny", "ask_for_info")] == [
        (35, 60), (17, 24), (53, 66), (1, 30)]


def test_the_rules_are_broken_6_14_59_29_and_51_times(trials):
    assert [sum(not rule(t) for t in trials) for rule in RULES.values()] \
        == [6, 14, 59, 29, 51]


def test_the_first_failing_links_count_36_13_13_6_5_and_1(trials):
    failed = [t for t in trials if not outcome_ok(t)]
    links = Counter(next((n for n, check in CHECKS if not check(t)), None)
                    for t in failed)
    assert len(failed) == 74
    assert sorted(links.values(), reverse=True) == [36, 13, 13, 6, 5, 1]
    assert links[CHECKS[2][0]] == 36


def test_the_report_prints_every_figure_the_lesson_asks_for(capsys):
    runpy.run_path(str(HERE / "agent_report.py"), run_name="__main__")
    out = capsys.readouterr().out.replace(",", "")
    for figure in ("20/30", "0.667", "0.49 to 0.81",
                   "pass@1 0.573", "pass^3 0.307", "pass@5 0.833",
                   "pass^5 0.167", "35/60", "17/24", "53/66", "1/30",
                   "106", "5881", "9987", "$0.0059", "$0.0100"):
        assert figure in out, f"the report never prints {figure}"
