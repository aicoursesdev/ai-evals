"""Lesson 07.2: the outcome checks, on made-up trials and on the recordings.

No model and no network. From the top folder: make check 07.2
"""
import runpy
from pathlib import Path

import pytest

from agents import outcome_correct, proposals, state_correct
from trials import load, scenarios

HERE = Path(__file__).parent


def printed(name, capsys):
    """What a script in this folder prints, one string per line."""
    runpy.run_path(str(HERE / name), run_name="__main__")
    return [line.rstrip() for line in capsys.readouterr().out.splitlines()]


def proposal(amount, waiting_for="Arjun", status="proposed"):
    result = {"status": status, "amount_inr": amount,
              "waiting_for": waiting_for}
    return {"tool": "propose_refund", "result": result}


def trial(calls=(), outcome=None, amount=None):
    return {"trajectory": list(calls), "outcome": outcome,
            "refund_inr": amount}


APPROVE = {"expected": "approve_proposal", "refund_inr": 2299}
ESCALATE = {"expected": "escalate_to_meera", "refund_inr": 14499}
DENY = {"expected": "deny", "refund_inr": None}


def test_proposals_are_the_results_of_calls_that_came_back_proposed():
    calls = [{"tool": "get_order", "result": {"status": "delivered"}},
             proposal(2299), proposal(10, status="error")]
    assert proposals(trial(calls)) == [calls[1]["result"]]


def test_a_denial_that_leaves_nothing_behind_passes_the_state_check():
    assert state_correct(trial(), DENY)


def test_a_denial_that_leaves_a_proposal_fails_the_state_check():
    assert not state_correct(trial([proposal(2299)]), DENY)


def test_an_approval_needs_a_proposal_of_the_right_amount_for_arjun():
    assert state_correct(trial([proposal(2299)]), APPROVE)
    assert not state_correct(trial(), APPROVE)
    assert not state_correct(trial([proposal(2000)]), APPROVE)
    assert not state_correct(trial([proposal(2299, "Arjun and Meera")]),
                             APPROVE)


def test_an_escalation_must_wait_for_arjun_and_meera():
    assert state_correct(trial([proposal(14499, "Arjun and Meera")]),
                         ESCALATE)
    assert not state_correct(trial([proposal(14499)]), ESCALATE)


def test_one_wrong_proposal_among_right_ones_fails_the_state_check():
    calls = [proposal(8000), proposal(2299)]
    assert not state_correct(trial(calls), APPROVE)


def test_the_stated_outcome_and_amount_must_both_match():
    assert outcome_correct(trial(outcome="deny"), DENY)
    assert not outcome_correct(trial(outcome="ask_for_info"), DENY)
    assert outcome_correct(trial(outcome="approve_proposal", amount=2299),
                           APPROVE)
    assert not outcome_correct(trial(outcome="approve_proposal", amount=1),
                               APPROVE)
    assert not outcome_correct(trial(), DENY)


def test_the_agent_at_temperature_0_said_20_of_30_and_left_26_of_30(capsys):
    runs = load(0)
    said = sum(outcome_correct(r, scenarios[r["id"]]) for r in runs)
    left = sum(state_correct(r, scenarios[r["id"]]) for r in runs)
    both = sum(outcome_correct(r, scenarios[r["id"]])
               and state_correct(r, scenarios[r["id"]]) for r in runs)
    assert (len(runs), said, left, both) == (30, 20, 26, 20)


def test_outcome_by_hand_prints_20_26_and_20_and_the_six_unsaid(capsys):
    lines = printed("outcome_by_hand.py", capsys)
    assert lines[:3] == ["said the right outcome  20/30",
                         "left the right state    26/30",
                         "both                    20/30"]
    assert [x.split()[0] for x in lines[3:]] == [
        "RF-12", "RF-15", "RF-16", "RF-21", "RF-23", "RF-28"]


def test_a_do_nothing_agent_passes_16_of_30_on_the_queue_and_0_on_both(
        capsys):
    lines = printed("do_nothing.py", capsys)
    row = {line[:24].strip(): line[24:].split() for line in lines[2:]}
    assert row["does nothing"] == ["16/30", "0/30", "0/30"]


def test_the_best_fixed_answer_is_deny_with_11_of_30(capsys):
    row = {line[:24].strip(): line[24:].split()
           for line in printed("do_nothing.py", capsys)[2:]}
    assert row["always deny"] == ["16/30", "11/30", "11/30"]
    assert row["always ask for info"][2] == "5/30"
    assert row["always approve 2299"][2] == "2/30"
    assert row["always escalate 14499"][2] == "2/30"
    assert max(int(v[2].split("/")[0]) for v in row.values()) == 11
