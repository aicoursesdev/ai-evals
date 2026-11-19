"""Lesson 07.5: where does each failed trial first go wrong? Checks run in
the order things happen in a run; the first one that fails names the link.

From this folder: uv run python first_failure.py
"""
import json
from collections import Counter

from scorecard import agents
from trials import failed

REAL = {"get_order", "check_policy", "propose_refund"}


def named_order_only(t):
    """Every order id the agent passed on is the one the customer gave."""
    ids = [json.loads(c["arguments"] or "{}").get("order_id")
           for c in t["trajectory"]]
    return all(i in (None, t["scenario"]["order_id"]) for i in ids)


CHECKS = [
    ("1 invented an order id", named_order_only),
    ("2 called a tool that does not exist",
     lambda t: all(c["tool"] in REAL for c in t["trajectory"])),
    ("3 wrong decision (proposed, or not, or the amount)",
     lambda t: agents.state_correct(t, t["scenario"])),
    ("4 proposed the same refund again",
     lambda t: len(agents.proposals(t)) <= 1),
    ("5 never finished (step cap)", lambda t: t["stop"] == "answered"),
    ("6 final answer not the required JSON",
     lambda t: t["outcome"] is not None),
    ("7 said the wrong outcome or amount",
     lambda t: agents.outcome_correct(t, t["scenario"])),
]


def first_leak(t):
    """The name of the first check this trial fails, or None."""
    for name, check in CHECKS:
        if not check(t):
            return name
    return None


if __name__ == "__main__":
    rows = failed()
    for label, group in (
            ("temperature 0", [t for t in rows if t["temperature"] == 0]),
            ("temperature 0.7", [t for t in rows if t["temperature"] > 0])):
        counts = Counter(first_leak(t) or "none" for t in group)
        assert counts == agents.transitions(group, CHECKS)  # same counts
        print(f"\n{label}: {len(group)} trials failed the outcome")
        for name, _ in CHECKS:
            print(f"  {name:55} {counts.get(name, 0):3}")
    print()
    for t in rows:
        if t["temperature"] == 0:
            print(t["id"], t["scenario"]["expected"], "->",
                  agents.first_failure(t, CHECKS))
    print("\nwrong decisions at step 3, by what was expected (the 36 trials):")
    bad = [t for t in rows if first_leak(t).startswith("3")]
    kinds = Counter()
    for t in bad:
        left = agents.proposals(t)
        did = ("proposed" if left else "did not propose")
        expected = t["scenario"]["expected"]
        if left and expected in ("approve_proposal", "escalate_to_meera"):
            did = "proposed the wrong amount or approver"
        kinds[(expected, did)] += 1
    for (expected, did), n in sorted(kinds.items()):
        print(f"  expected {expected:18} {did:38} {n:3}")
