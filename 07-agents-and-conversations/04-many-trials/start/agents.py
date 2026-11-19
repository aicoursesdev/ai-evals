"""Lesson 07.4: pass@k and pass^k, for you to write, on top of the checks
from 07.2 and 07.3, finished.

The course's own versions are in scorecard/agents.py: compare yours with
them when the tests pass. Later lessons add more to this file.
Check from the repo's top folder with: make check 07.4
"""
from math import comb


def proposals(trial):
    """The refunds left waiting for a person: the result of every
    propose_refund call that came back "proposed"."""
    return [c["result"] for c in trial["trajectory"]
            if c["tool"] == "propose_refund"
            and c["result"].get("status") == "proposed"]


def outcome_correct(trial, scenario):
    """The stated outcome equals the scenario's expected one, and when the
    scenario names a refund amount the stated amount matches too."""
    if trial["outcome"] != scenario["expected"]:
        return False
    if scenario.get("refund_inr") is None:
        return True
    return trial.get("refund_inr") == scenario["refund_inr"]


def state_correct(trial, scenario):
    """What the agent left behind. Deny or ask: nothing proposed. Approve
    or escalate: every proposal has the right amount and waits for the
    right people (Arjun, or Arjun and Meera above 10,000)."""
    left = proposals(trial)
    if scenario["expected"] in ("deny", "ask_for_info"):
        return not left
    who = ("Arjun" if scenario["expected"] == "approve_proposal"
           else "Arjun and Meera")
    return bool(left) and all(p["amount_inr"] == scenario["refund_inr"]
                              and p["waiting_for"] == who for p in left)


def called(trial, tool):
    """The agent called this tool at least once."""
    return any(c["tool"] == tool for c in trial["trajectory"])


def called_in_order(trial, tools):
    """The tools appear in this order (other calls may sit between)."""
    names = iter(c["tool"] for c in trial["trajectory"])
    return all(t in names for t in tools)


def pass_at_k(successes, trials, k):
    """Chance that at least one of k trials drawn from the n recorded
    succeeds: 1 - C(n-s, k) / C(n, k), averaged over tasks. 3 in 5, k=2
    gives 0.9. successes and trials are lists with one entry per task."""
    raise NotImplementedError(
        "TODO 07.4: for each task (s, n) in zip(successes, trials) work "
        "out 1 - comb(n - s, k) / comb(n, k) and return the average, see "
        "the lesson's 'Two questions about k tries' section")


def pass_hat_k(successes, trials, k):
    """Chance that all k trials drawn from the n recorded succeed:
    C(s, k) / C(n, k), averaged over tasks. 3 in 5: k=2 gives 0.3."""
    raise NotImplementedError(
        "TODO 07.4: for each task (s, n) in zip(successes, trials) work "
        "out comb(s, k) / comb(n, k) and return the average, see the "
        "lesson's 'Two questions about k tries' section")
