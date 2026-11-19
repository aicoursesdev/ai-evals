"""Lesson 07.3: a rule and a taste, on the trials whose outcome was right.
The rule: look the order up before proposing. The tastes: always call
check_policy, and follow the exact path get_order, check_policy, propose.

From this folder: uv run python rules_vs_style.py
"""
from scorecard import agents
from trials import scenarios, trials

right = [t for t in trials
         if agents.outcome_correct(t, scenarios[t["id"]])
         and agents.state_correct(t, scenarios[t["id"]])]
print("trials with the right outcome:", len(right), "of", len(trials))

checks = {
    "rule: order looked up before any proposal":
        lambda t: not agents.proposals(t)
        or agents.called_in_order(t, ["get_order", "propose_refund"]),
    "taste: calls check_policy": lambda t: agents.called(t, "check_policy"),
    "taste: exactly get_order, check_policy, propose_refund": lambda t: [
        c["tool"] for c in t["trajectory"]]
    == ["get_order", "check_policy", "propose_refund"],
}
for name, check in checks.items():
    failed = [t for t in right if not check(t)]
    print(f"{name}\n    fails {len(failed)} of {len(right)} right trials")

skipped = [t for t in right if not agents.called(t, "check_policy")]
for t in skipped:
    s = scenarios[t["id"]]
    print(t["id"], "trial", t["trial"], "expected", s["expected"],
          "| tools:", [c["tool"] for c in t["trajectory"]])
