"""Lesson 04.6: does the first reply shown win? Replays lesson 03.7's run.

Given: the recording and the lines that print. Uses `by_place` and
`same_both_orders` from bias_counts.py.

From this folder: uv run python position_test.py
"""
from bias_counts import by_place, same_both_orders
from plumbing import RUNS
from scorecard import data

rows = data.read_jsonl(RUNS / "03-pairwise" / "pairs.jsonl")
print(len(rows), "requests:", dict(by_place(rows)))
pairs, same = same_both_orders(rows)
print(f"{pairs} pairs; the same version wins in both orders on {same}; "
      f"the winner changes with the order on {pairs - same}")
