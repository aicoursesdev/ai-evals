"""Lesson 07.7: the refund agent's checks in one place: the outcome check,
the path rules, and the ordered list that names where a failed trial first
went wrong. A trial here carries its scenario under "scenario".

agent_report.py imports from this file. It prints nothing by itself.
"""
import json
import re

from scorecard import agents

REAL = {"get_order", "check_policy", "propose_refund"}
DONE = re.compile(r"\b(has|have) been (successfully )?(approved|processed|"
                  r"paid|issued|refunded)|\bis approved\b", re.I)


def outcome_ok(t):
    """Said the right outcome and left the right state."""
    return (agents.outcome_correct(t, t["scenario"])
            and agents.state_correct(t, t["scenario"]))


def named_order_only(t):
    ids = [json.loads(c["arguments"] or "{}").get("order_id")
           for c in t["trajectory"]]
    return all(i in (None, t["scenario"]["order_id"]) for i in ids)


def says_done(t):
    text = t["reply"] if t["outcome"] else t["final_raw"] or ""
    return bool(DONE.search(text))


# In the order things happen in a run. The first that fails is the link.
CHECKS = [
    ("invented an order id", named_order_only),
    ("called a tool that does not exist",
     lambda t: all(c["tool"] in REAL for c in t["trajectory"])),
    ("wrong decision", lambda t: agents.state_correct(t, t["scenario"])),
    ("proposed the same refund again",
     lambda t: len(agents.proposals(t)) <= 1),
    ("never finished", lambda t: t["stop"] == "answered"),
    ("answer not the required JSON", lambda t: t["outcome"] is not None),
    ("wrong outcome or amount",
     lambda t: agents.outcome_correct(t, t["scenario"])),
]
# Rules about the path that hold whether or not the outcome was right.
RULES = {
    "order id as given": named_order_only,
    "real tools only": CHECKS[1][1],
    "one proposal": CHECKS[3][1],
    "within the step cap": CHECKS[4][1],
    "does not say it is done": lambda t: not says_done(t),
}
