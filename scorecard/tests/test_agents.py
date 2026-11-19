import pytest
from scorecard import agents as a


def trial(tools, outcome="deny", refund=0):
    return {"calls": [{"tool": t} for t in tools], "outcome": outcome,
            "refund_inr": refund}


def test_outcome_and_calls():
    deny = {"expected": "deny"}
    ok = {"expected": "approve_proposal", "refund_inr": 2299}
    assert a.outcome_correct(trial([]), deny)
    assert a.outcome_correct(trial([], "approve_proposal", 2299), ok)
    assert not a.outcome_correct(trial([], "approve_proposal", 100), ok)
    t = trial(["lookup_order", "check_policy", "propose_refund"])
    assert a.called(t, "check_policy") and not a.called(t, "email")
    assert a.called_in_order(t, ["lookup_order", "propose_refund"])
    assert not a.called_in_order(t, ["propose_refund", "lookup_order"])


def test_pass_k():
    # one task, 3 successes in 5 trials
    assert a.pass_hat_k([3], [5], 1) == pytest.approx(0.6)
    assert a.pass_hat_k([3], [5], 2) == pytest.approx(0.3)
    assert a.pass_hat_k([3], [5], 3) == pytest.approx(0.1)
    assert a.pass_at_k([3], [5], 2) == pytest.approx(0.9)
    assert a.pass_at_k([3], [5], 1) == pytest.approx(0.6)
    # averaged over tasks: an always-right and an always-wrong task
    assert a.pass_hat_k([5, 0], [5, 5], 3) == pytest.approx(0.5)


def test_first_failure_and_transitions():
    checks = [("looked up", lambda t: a.called(t, "lookup_order")),
              ("right outcome", lambda t: t["outcome"] == "deny")]
    good = trial(["lookup_order"])
    skipped = trial([])
    wrong = trial(["lookup_order"], "approve_proposal")
    assert a.first_failure(good, checks) is None
    assert a.first_failure(skipped, checks) == "looked up"
    got = a.transitions([good, skipped, wrong, wrong], checks)
    assert got == {"none": 1, "looked up": 1, "right outcome": 2}


def test_recorded_trial_state():
    """A recorded trial keeps "trajectory" with results; check the state."""
    done = {"status": "proposed", "amount_inr": 2299, "waiting_for": "Arjun"}
    rec = {"trajectory": [{"tool": "get_order", "result": {}},
                          {"tool": "propose_refund", "result": done}],
           "outcome": "approve_proposal", "refund_inr": 2299}
    ok = {"expected": "approve_proposal", "refund_inr": 2299}
    big = {"expected": "escalate_to_meera", "refund_inr": 14499}
    assert a.called_in_order(rec, ["get_order", "propose_refund"])
    assert a.state_correct(rec, ok) and a.outcome_correct(rec, ok)
    assert not a.state_correct(rec, big)          # waits for Arjun only
    assert not a.outcome_correct(rec, big)
    assert not a.state_correct(rec, {"expected": "deny"})
    assert a.state_correct({"trajectory": [], "outcome": None},
                           {"expected": "ask_for_info"})
