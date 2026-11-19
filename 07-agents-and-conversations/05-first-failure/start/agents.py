"""Lesson 07.5: the first failing link, for you to write, on top of the
checks from 07.2 to 07.4, finished.

The course's own versions are in scorecard/agents.py: compare yours with
them when the tests pass. Check from the repo's top folder with:
make check 07.5
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
    succeeds, averaged over tasks."""
    values = [1 - comb(n - s, k) / comb(n, k)
              for s, n in zip(successes, trials)]
    return sum(values) / len(values)


def pass_hat_k(successes, trials, k):
    """Chance that all k trials drawn from the n recorded succeed,
    averaged over tasks."""
    values = [comb(s, k) / comb(n, k) for s, n in zip(successes, trials)]
    return sum(values) / len(values)


def first_failure(trial, checks):
    """Name of the first check that fails, or None if all pass.
    checks is a list of (name, function(trial) -> bool)."""
    raise NotImplementedError(
        "TODO 07.5: go through checks in order and return the name of the "
        "first (name, check) whose check(trial) is False; None when all "
        "pass, see the lesson's 'Count the first failing link' section")


def transitions(trials, checks):
    """Count, per check name, the trials whose first failure it was
    ('none' counts trials that passed everything)."""
    raise NotImplementedError(
        "TODO 07.5: make a dict, and for each trial add 1 to the count "
        "under first_failure(trial, checks) or 'none'; return the dict, "
        "see the lesson's 'Count the first failing link' section")
