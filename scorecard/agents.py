"""Check a refund agent's trials. A trial is a dict: {"calls": [{"tool":
name, "args": {...}}, ...], "outcome": "deny", "refund_inr": 0}. A recorded
trial keeps its calls under "trajectory" instead, each with a "result"."""
from math import comb


def _calls(trial):
    return trial.get("calls") or trial.get("trajectory") or []


def outcome_correct(trial, scenario):
    """The stated outcome equals the scenario's expected one, and when the
    scenario names a refund amount the stated amount matches too."""
    if trial["outcome"] != scenario["expected"]:
        return False
    if scenario.get("refund_inr") is None:
        return True
    return trial.get("refund_inr") == scenario["refund_inr"]


def proposals(trial):
    """The refunds the agent left waiting for a person: the result of
    every propose_refund call that came back "proposed"."""
    return [c["result"] for c in _calls(trial)
            if c["tool"] == "propose_refund"
            and c.get("result", {}).get("status") == "proposed"]


def state_correct(trial, scenario):
    """What the agent left behind. Deny or ask: nothing proposed. Approve
    or escalate: every proposal has the right amount and waits for the
    right people (Arjun, or Arjun and Meera above 10,000)."""
    left = proposals(trial)
    if scenario["expected"] in ("deny", "ask_for_info"):
        return not left
    who = "Arjun" if scenario["expected"] == "approve_proposal" else "Arjun and Meera"
    return bool(left) and all(p["amount_inr"] == scenario["refund_inr"]
                              and p["waiting_for"] == who for p in left)


def called(trial, tool):
    """The agent called this tool at least once."""
    return any(c["tool"] == tool for c in _calls(trial))


def called_in_order(trial, tools):
    """The tools appear in this order (other calls may sit between)."""
    names = iter(c["tool"] for c in _calls(trial))
    return all(t in names for t in tools)  # each search resumes in place


def pass_at_k(successes, trials, k):
    """Chance that at least one of k trials drawn from the n recorded
    succeeds: 1 - C(n-s, k) / C(n, k). 3 in 5, k=2 gives 0.9.
    successes and trials are lists with one entry per task."""
    return _mean(1 - comb(n - s, k) / comb(n, k)
                 for s, n in zip(successes, trials))


def pass_hat_k(successes, trials, k):
    """Chance that all k trials drawn from the n recorded succeed:
    C(s, k) / C(n, k), averaged over tasks. 3 in 5: k=2 gives 0.3."""
    return _mean(comb(s, k) / comb(n, k)
                 for s, n in zip(successes, trials))


def _mean(values):
    values = list(values)
    return sum(values) / len(values)


def first_failure(trial, checks):
    """Name of the first check that fails, or None if all pass.
    checks is a list of (name, function(trial) -> bool)."""
    for name, check in checks:
        if not check(trial):
            return name
    return None


def transitions(trials, checks):
    """Count, per check name, the trials whose first failure it was
    ('none' counts trials that passed everything)."""
    counts = {}
    for trial in trials:
        name = first_failure(trial, checks) or "none"
        counts[name] = counts.get(name, 0) + 1
    return counts
