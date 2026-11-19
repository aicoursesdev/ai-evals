"""Lesson 07.3: the outcome checks from 07.2, finished, and two path helpers
for you to write.

The course's own versions are in scorecard/agents.py: compare yours with
them when the tests pass. Later lessons add more to this file.
Check from the repo's top folder with: make check 07.3
A trial is a dict with "trajectory": its tool calls, in order, each with a
"tool" name, its "arguments" and its "result".
"""


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
    raise NotImplementedError(
        "TODO 07.3: return True when any call c in trial['trajectory'] has "
        "c['tool'] equal to tool, see the lesson's 'Habits a check would "
        "punish' section")


def called_in_order(trial, tools):
    """The tools appear in this order (other calls may sit between).
    ['a', 'c'] is in order in the calls a, b, c; ['c', 'a'] is not."""
    raise NotImplementedError(
        "TODO 07.3: make names = iter(c['tool'] for c in "
        "trial['trajectory']) and return all(t in names for t in tools): "
        "an iterator remembers its place, so each search carries on after "
        "the last match, see the lesson's 'Six rules, counted' section")
