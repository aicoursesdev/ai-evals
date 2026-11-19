"""Lesson 07.2: the outcome checks, as functions of one trial.

You write these three. The course's own versions are in scorecard/agents.py:
compare yours with them when the tests pass. Later lessons add more to this
file. Check from the repo's top folder with: make check 07.2
A trial is a dict with "trajectory" (its tool calls, each with a "result"),
"outcome" and "refund_inr"; a scenario has "expected" and "refund_inr".
"""


def proposals(trial):
    """The refunds left waiting for a person: the result of every
    propose_refund call that came back "proposed"."""
    raise NotImplementedError(
        "TODO 07.2: return the c['result'] of each call c in "
        "trial['trajectory'] whose tool is 'propose_refund' and whose "
        "result status is 'proposed', see the lesson's 'What the agent "
        "leaves behind' section")


def outcome_correct(trial, scenario):
    """The stated outcome equals the scenario's expected one, and when the
    scenario names a refund amount the stated amount matches too."""
    raise NotImplementedError(
        "TODO 07.2: False unless trial['outcome'] equals "
        "scenario['expected']; then True when scenario['refund_inr'] is "
        "None, else compare it with trial['refund_inr'], see the lesson's "
        "'What the agent leaves behind' section")


def state_correct(trial, scenario):
    """What the agent left behind. Deny or ask: nothing proposed. Approve
    or escalate: every proposal has the right amount and waits for the
    right people (Arjun, or Arjun and Meera above 10,000)."""
    raise NotImplementedError(
        "TODO 07.2: for deny and ask_for_info return not proposals(trial); "
        "otherwise return True only when there is a proposal and every one "
        "has amount_inr equal to scenario['refund_inr'] and waiting_for "
        "'Arjun' (approve) or 'Arjun and Meera' (escalate), see the "
        "lesson's 'What the agent leaves behind' section")
