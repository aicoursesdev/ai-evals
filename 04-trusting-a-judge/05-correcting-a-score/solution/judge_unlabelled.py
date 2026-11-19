"""Lesson 04.5: the chosen judge on logged drafts nobody has labelled.

From this folder:
    uv run python judge_unlabelled.py --live   asks the local model, one
        request at a time, and skips drafts already recorded (NEEDS A MODEL)
Without --live the recording is read and counted.
"""
import json
import random
import sys
from collections import Counter

from plumbing import RUNS, SETTINGS, WEEKS, cases, chosen, held_out, verdicts
from scorecard import data
from scorecard.graders import logged
from scorecard.judge import record

OUT = RUNS / "04-unlabelled" / "judge.jsonl"


def sample(n=250):
    """n logged ids in none of the open, held-out or sealed parts
    (logged() already leaves the sealed part out), drawn with seed 5."""
    skip = {e["id"] for e in data.testset("open")} | set(held_out())
    log = sorted(e["id"] for w in WEEKS for e in logged("emails", w))
    return sorted(random.Random(5).sample(
        [i for i in log if i not in skip], n))


if __name__ == "__main__":
    ids = sample()
    if "--live" in sys.argv:
        OUT.parent.mkdir(exist_ok=True)
        (OUT.parent / "sample-ids.json").write_text(json.dumps(ids))
        record(OUT, [{"id": c["id"], "prompt": chosen().format(**c)}
                     for c in cases(ids)], SETTINGS)
    print(len(ids), "drafts;", dict(Counter(verdicts(OUT).values())))
