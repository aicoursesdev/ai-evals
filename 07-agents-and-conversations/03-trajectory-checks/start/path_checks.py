"""Lesson 07.3: path rules over the 180 recorded trials. Each rule is a
function of one trial and its scenario that returns True when the rule is
kept.

From this folder: uv run python path_checks.py
"""
import re
from collections import Counter

from scorecard import agents
from trials import order_ids, reply_text, scenarios, trials

REAL = {"get_order", "check_policy", "propose_refund"}
# Said as done: "has been approved", "is approved", "has been processed".
DONE = re.compile(r"\b(has|have) been (successfully )?(approved|processed|"
                  r"paid|issued|refunded)|\bis approved\b", re.I)


def todo(message):
    """A rule that is not written yet: it raises `message` when it runs."""
    def rule(t, s):
        raise NotImplementedError(message)
    return rule


# Replace each todo(...) with `lambda t, s: ...`, True when the rule is kept.
RULES = {
    "uses only real tools": todo(
        "TODO 07.3: True when every call c in t['trajectory'] has c['tool'] "
        "in REAL, see the lesson's 'Six rules, counted' section"),
    "asks about the named order": todo(
        "TODO 07.3: True when every id in order_ids(t) equals "
        "s['order_id'], see the lesson's 'Six rules, counted' section"),
    "looks up before proposing": todo(
        "TODO 07.3: True when agents.proposals(t) is empty, or "
        "agents.called_in_order(t, ['get_order', 'propose_refund']), see "
        "the lesson's 'Six rules, counted' section"),
    "proposes at most once": todo(
        "TODO 07.3: True when len(agents.proposals(t)) is at most 1, see "
        "the lesson's 'Six rules, counted' section"),
    "finishes within the step cap": todo(
        "TODO 07.3: True when t['stop'] equals 'answered', see the "
        "lesson's 'Six rules, counted' section"),
    "does not say it is done": todo(
        "TODO 07.3: True when DONE.search(reply_text(t)) finds nothing, "
        "see the lesson's 'Six rules, counted' section"),
}

if __name__ == "__main__":
    broken = Counter()
    for t in trials:
        for name, rule in RULES.items():
            broken[name] += not rule(t, scenarios[t["id"]])
    for name in RULES:
        print(f"{name:30} broken in {broken[name]:3} of {len(trials)} trials")
    clean = [t for t in trials if all(r(t, scenarios[t["id"]])
                                      for r in RULES.values())]
    print("trials that keep every rule:", len(clean))
