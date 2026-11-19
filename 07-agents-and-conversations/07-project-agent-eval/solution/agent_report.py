"""Lesson 07.7: is the refund agent reliable? The numbers for the report to
Meera, from the 180 recorded trials of hd-1.

From this folder: uv run python agent_report.py
"""
from collections import Counter

from checks import CHECKS, RULES, outcome_ok
from scorecard import agents, data, stats

scenarios = {s["id"]: s for s in data.scenarios()}
trials = [{**t, "scenario": scenarios[t["id"]]}
          for t in data.run("07-refund-trials")["hd-1"]]
cold = [t for t in trials if t["temperature"] == 0]
hot = [t for t in trials if t["temperature"] == 0.7]

won = sum(outcome_ok(t) for t in cold)
low, high = stats.wilson(won, 30)
print(f"outcome, one run at temperature 0: {won}/30 = {won / 30:.3f} "
      f"(95% {low:.2f} to {high:.2f})")

c = [sum(outcome_ok(t) for t in hot if t["id"] == sid) for sid in scenarios]
n = [5] * 30
for k in (1, 3, 5):
    at, hat = agents.pass_at_k(c, n, k), agents.pass_hat_k(c, n, k)
    print(f"temperature 0.7, 5 trials: pass@{k} {at:.3f}  pass^{k} {hat:.3f}")

print("\nby kind of case (right trials / trials, all 180):")
for kind in ("approve_proposal", "escalate_to_meera", "deny", "ask_for_info"):
    group = [t for t in trials if t["scenario"]["expected"] == kind]
    print(f"  {kind:18} {sum(map(outcome_ok, group)):3}/{len(group)}")

print("\npath rules broken (of 180 trials):")
for name, rule in RULES.items():
    print(f"  {name:26} {sum(not rule(t) for t in trials):3}")

failed = [t for t in trials if not outcome_ok(t)]
print(f"\nfirst failing link, {len(failed)} failed trials:")
links = Counter(agents.first_failure(t, CHECKS) for t in failed)
for name, n in links.most_common():
    print(f"  {name:34} {n:3}")

tokens = [t["prompt_tokens"] + t["completion_tokens"] for t in trials]
good = sum(map(outcome_ok, trials))
print(f"right trials: {good}/180")
print(f"\ntokens per trial {sum(tokens) / 180:,.0f}, "
      f"per right trial {sum(tokens) / good:,.0f}")
PRICE = 1.0  # dollars per million tokens: a round number for the example
print(f"at an assumed ${PRICE:.2f} per million tokens: "
      f"${sum(tokens) / 180 * PRICE / 1e6:.4f} per trial, "
      f"${sum(tokens) / good * PRICE / 1e6:.4f} per right trial")
