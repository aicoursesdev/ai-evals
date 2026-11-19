"""Lesson 07.7: the refund agent's checks in one place: the outcome check,
the path rules, and the ordered list that names where a failed trial first
went wrong. A trial here carries its scenario under "scenario".

You write the checks and the report. Your own versions from lessons 07.2 to
07.5 are the way in; the finished ones are in solution/. agent_report.py
imports from this file.
"""
import json
import re

from scorecard import agents

REAL = {"get_order", "check_policy", "propose_refund"}
DONE = re.compile(r"\b(has|have) been (successfully )?(approved|processed|"
                  r"paid|issued|refunded)|\bis approved\b", re.I)


def todo(message):
    """A check that is not written yet: it raises `message` when it runs."""
    def check(t):
        raise NotImplementedError(message)
    return check


def outcome_ok(t):
    """Said the right outcome and left the right state."""
    raise NotImplementedError(
        "TODO 07.7: True when agents.outcome_correct(t, t['scenario']) and "
        "agents.state_correct(t, t['scenario']) both hold, see the "
        "lesson's 'What to build' section")


def named_order_only(t):
    """Every order id the agent passed to a tool is the customer's."""
    raise NotImplementedError(
        "TODO 07.7: read order_id from json.loads(c['arguments'] or '{}') "
        "for each call c in t['trajectory'] and return True when every id "
        "found is t['scenario']['order_id'], see the lesson's 'What to "
        "build' section")


def says_done(t):
    """The agent tells the customer the refund is done."""
    raise NotImplementedError(
        "TODO 07.7: take the text t['reply'] when t['outcome'] is set, "
        "else t['final_raw'] or '', and return True when DONE.search "
        "finds something in it, see the lesson's 'What to build' section")


# In the order things happen in a run. The first that fails is the link.
# Replace each todo(...) with `lambda t: ...` (or one of the functions).
CHECKS = [
    ("invented an order id", todo(
        "TODO 07.7: True when named_order_only(t), see the lesson's "
        "'What to build' section")),
    ("called a tool that does not exist", todo(
        "TODO 07.7: True when every call's tool in t['trajectory'] is in "
        "REAL, see the lesson's 'What to build' section")),
    ("wrong decision", todo(
        "TODO 07.7: True when agents.state_correct(t, t['scenario']), see "
        "the lesson's 'What to build' section")),
    ("proposed the same refund again", todo(
        "TODO 07.7: True when len(agents.proposals(t)) is at most 1, see "
        "the lesson's 'What to build' section")),
    ("never finished", todo(
        "TODO 07.7: True when t['stop'] equals 'answered', see the "
        "lesson's 'What to build' section")),
    ("answer not the required JSON", todo(
        "TODO 07.7: True when t['outcome'] is not None, see the lesson's "
        "'What to build' section")),
    ("wrong outcome or amount", todo(
        "TODO 07.7: True when agents.outcome_correct(t, t['scenario']), "
        "see the lesson's 'What to build' section")),
]
# Rules about the path that hold whether or not the outcome was right:
# True when the rule is kept.
RULES = {
    "order id as given": todo(
        "TODO 07.7: the same check as the first link, see the lesson's "
        "'What to build' section"),
    "real tools only": todo(
        "TODO 07.7: the same check as the second link, see the lesson's "
        "'What to build' section"),
    "one proposal": todo(
        "TODO 07.7: the same check as the fourth link, see the lesson's "
        "'What to build' section"),
    "within the step cap": todo(
        "TODO 07.7: the same check as the fifth link, see the lesson's "
        "'What to build' section"),
    "does not say it is done": todo(
        "TODO 07.7: not says_done(t), see the lesson's 'What to build' "
        "section"),
}
