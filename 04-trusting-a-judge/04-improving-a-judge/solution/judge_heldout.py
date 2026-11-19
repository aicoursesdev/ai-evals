"""Lesson 04.4: the chosen judge, run once on the 100 held-out drafts.

From this folder:
    uv run python judge_heldout.py v4 --live   asks the local model, once
        per draft, and saves the prompt (NEEDS A MODEL)
Without --live the recording is read and the two rates printed.
"""
import sys

from plumbing import (RUNS, SETTINGS, arjun, cases, held_out, template,
                      two_rates, verdicts)
from scorecard.judge import record

OUT = RUNS / "04-heldout" / "judge.jsonl"

if __name__ == "__main__":
    if "--live" in sys.argv:
        OUT.parent.mkdir(exist_ok=True)
        (OUT.parent / "prompt.txt").write_text(template(sys.argv[1]))
        rows = [{"id": c["id"],
                 "prompt": template(sys.argv[1]).format(**c)}
                for c in cases(held_out())]
        record(OUT, rows, SETTINGS)
    human, seen = arjun("04-right-rule-arjun"), verdicts(OUT)
    ids = held_out()
    tpr, tnr, c = two_rates([human[i] for i in ids], [seen[i] for i in ids])
    print(c, f"passes kept {tpr:.1%}, fails held back {tnr:.1%}")
    unsure = [seen[i] for i in ids if human[i] == "unsure"]
    print("Arjun's unsure drafts, judge says:", dict(
        (v, unsure.count(v)) for v in sorted(set(unsure))))
    print("no verdict line:", sum(v == "none" for v in seen.values()))
