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

RULES = {
    "uses only real tools": lambda t, s: all(
        c["tool"] in REAL for c in t["trajectory"]),
    "asks about the named order": lambda t, s: all(
        o == s["order_id"] for o in order_ids(t)),
    "looks up before proposing": lambda t, s: not agents.proposals(t)
        or agents.called_in_order(t, ["get_order", "propose_refund"]),
    "proposes at most once": lambda t, s: len(agents.proposals(t)) <= 1,
    "finishes within the step cap": lambda t, s: t["stop"] == "answered",
    "does not say it is done": lambda t, s: not DONE.search(reply_text(t)),
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
