"""Lesson 04.6: pad each draft with filler and ask again.

Given: the recordings and the lines that print. Uses `moves` and `same_on`
from bias_counts.py.

From this folder: uv run python length_test.py
"""
from bias_counts import moves, same_on
from bias_runs import FILLER, OUT, sample
from plumbing import RUNS, arjun, cases, verdicts

before = verdicts(RUNS / "04-dev" / "v4.jsonl")  # the dev run, unpadded
after = verdicts(OUT / "length.jsonl")
ids = sample()
words = [len(c["draft"].split()) for c in cases(ids)]
print(f"{len(ids)} drafts, {sum(words) / len(words):.0f} words on average; "
      f"the filler adds {len(FILLER.split())}")

for (a, b), n in sorted(moves(before, after, ids).items()):
    print(f"  {a:>6} -> {b:<6} {n}")
print("verdict changed on", len(ids) - same_on(before, after, ids), "of",
      len(ids))
rest = [i for i in ids if i != "E-0398"]  # E-0398 is an example in the prompt
print("without E-0398, an example in the prompt: changed on",
      len(rest) - same_on(before, after, rest), "of", len(rest))

human = arjun("03-right-rule-arjun")
for call in ("pass", "fail"):
    mine = [i for i in ids if human[i] == call]
    kept, padded = (sum(v[i] == "pass" for i in mine)
                    for v in (before, after))
    print(f"Arjun {call}: judge passes {kept} of {len(mine)} unpadded, "
          f"{padded} padded")
