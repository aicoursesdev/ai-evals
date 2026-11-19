"""Lesson 08.3: the same limits from scorecard.stats, and a few failures.

From this folder: uv run python with_scorecard.py
"""
from scorecard.stats import exact_interval, exact_upper, rule_of_three, wilson

def limits(failures, tries):
    """The one-sided upper limit and the two-sided interval."""
    return exact_upper(failures, tries), exact_interval(failures, tries)

upper, (low, high) = limits(0, 100)
print("0 failures in 100")
print("  rule of three      ", round(rule_of_three(100), 4))
print("  exact upper limit  ", round(upper, 4))
print("  two-sided interval ", [round(low, 4), round(high, 4)])
print("  Wilson interval    ", [round(x, 4) for x in wilson(0, 100)])
print("failures in 100 -> one-sided upper limit, two-sided interval")
for k in range(4):
    upper, (low, high) = limits(k, 100)
    print(f"  {k}: upper {upper:.4f}   interval {low:.4f} to {high:.4f}")
for n in (298, 299):
    print(f"{n} clean trials: limit {exact_upper(0, n):.5f}")
