"""Lesson 04.6: ask the same question again, and five times warmer.

Given: the recordings and the lines that print. Uses `same_on` and
`kinds_per_draft` from bias_counts.py.

From this folder: uv run python again_test.py
"""
from bias_counts import kinds_per_draft, same_on
from bias_runs import OUT, sample
from plumbing import RUNS, read_trials, verdicts

ids = sample()
first = verdicts(RUNS / "04-dev" / "v4.jsonl")
again = verdicts(OUT / "again-t0.jsonl")
print("temperature 0, asked twice: same verdict on "
      f"{same_on(first, again, ids)} of {len(ids)}")

hot = read_trials(OUT / "again-t07.jsonl")  # {trial: {id: verdict}}
for k, seen in sorted(hot.items()):
    share = sum(v == "pass" for v in seen.values()) / len(seen)
    print(f"  temperature 0.7, run {k}: judge passes {share:.1%}")
runs = [first] + [hot[k] for k in sorted(hot)]
kinds = kinds_per_draft(runs, ids)
print("kinds of verdict per draft over six runs:",
      dict(sorted(kinds.items())))
print(f"all six runs agree on {kinds[1]} of {len(ids)} drafts")
