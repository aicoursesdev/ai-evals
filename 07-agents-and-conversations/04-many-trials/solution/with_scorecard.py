"""Lesson 07.4: the same numbers with scorecard.agents, an error bar by
resampling scenarios, and the single temperature-0 run beside them.

From this folder: uv run python with_scorecard.py
"""
from scorecard import agents, stats
from trials import cold, hot, passed, scenarios

one_run = {r["id"]: passed(r) for r in cold}
wins = {sid: sum(passed(r) for r in hot if r["id"] == sid)
        for sid in scenarios}
c = list(wins.values())
n = [5] * len(c)

for k in (1, 3, 5):
    print(f"pass@{k} {agents.pass_at_k(c, n, k):.3f}   "
          f"pass^{k} {agents.pass_hat_k(c, n, k):.3f}")

pairs = list(zip(c, n))
low, high = stats.bootstrap(
    pairs, lambda p: agents.pass_hat_k(*zip(*p), 3), seed=7)
print(f"pass^3 {agents.pass_hat_k(c, n, 3):.3f}, "
      f"95% range {low:.2f} to {high:.2f}")

one = sum(one_run.values())
wilson = stats.wilson(one, 30)
print(f"temperature 0, one run: {one}/30 = {one / 30:.3f}, "
      f"Wilson 95% {wilson[0]:.2f} to {wilson[1]:.2f}")
gap = [(1.0 if one_run[sid] else 0.0) - wins[sid] / 5 for sid in scenarios]
low, high = stats.bootstrap(gap, lambda g: sum(g) / len(g), seed=7)
print(f"temperature 0 minus the hot average, per scenario: "
      f"{sum(gap) / 30:+.3f}, 95% range {low:+.2f} to {high:+.2f}")
