"""Lesson 04.6: three small experiments on the chosen judge.

From this folder:
    uv run python bias_runs.py --live   records the padded drafts (30),
        a second run at temperature 0 (30) and five runs at temperature
        0.7 (150), one request at a time (NEEDS A MODEL)
Without --live the recordings are read and counted.
"""
import json
import random
import sys

from plumbing import RUNS, SETTINGS, arjun, cases, chosen
from scorecard import data
from scorecard.judge import record

OUT = RUNS / "04-bias"
FILLER = ("Thank you for choosing Tidewater Goods. We value every customer "
          "and are always happy to help, so please do not hesitate to write "
          "again if there is anything else you would like to know.")


def sample(n=30):
    """n development drafts Arjun passed or failed, drawn with seed 6."""
    human = arjun("03-right-rule-arjun")
    pool = sorted(i for i, call in human.items() if call != "unsure")
    return sorted(random.Random(6).sample(pool, n))


def rows(pad=False, trial=None):
    """Prompt rows for the sample; pad adds the filler to each draft."""
    for c in cases(sample()):
        if pad:
            c["draft"] += "\n\n" + FILLER
        row = {"id": c["id"], "prompt": chosen().format(**c)}
        yield row if trial is None else row | {"trial": trial}


if __name__ == "__main__":
    if "--live" in sys.argv:
        OUT.mkdir(exist_ok=True)
        (OUT / "sample-ids.json").write_text(json.dumps(sample()))
        record(OUT / "length.jsonl", rows(pad=True), SETTINGS)
        record(OUT / "again-t0.jsonl", rows(), SETTINGS)
        for k in range(1, 6):
            hot = SETTINGS | {"temperature": 0.7, "seed": k}
            record(OUT / "again-t07.jsonl", rows(trial=k), hot)
    for name in ("length", "again-t0", "again-t07"):
        file = OUT / f"{name}.jsonl"
        print(name, len(data.read_jsonl(file)) if file.exists() else 0)
