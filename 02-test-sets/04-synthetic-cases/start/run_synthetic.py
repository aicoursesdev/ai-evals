"""Lesson 02.4: run the made-up cases through the help desk, live.

NEEDS A MODEL (Ollama, qwen3.5:4b). From this folder:
    uv run python run_synthetic.py            # all cases not yet recorded
    uv run python run_synthetic.py S-01       # just that one
One request at a time and no retries. A case whose reply never ends is
recorded with an `error`, not dropped. Appends to data/runs/02-synthetic/.
"""
import json
import sys
import time

import openai

from helpdesk import llm
from helpdesk.pipeline import handle
from scorecard import data

llm.ATTEMPTS = 1  # a connection error is recorded, not retried
OUT = data.DATA / "runs" / "02-synthetic" / "hd-1.jsonl"


def run_one(case):
    """The help desk's trace for one case, or a record of why none."""
    began = time.time()
    try:
        return handle(case)
    except openai.OpenAIError as err:  # includes the 300-second timeout
        return {"id": case["id"], "version": "hd-1", "draft": "",
                "error": f"{type(err).__name__} after "
                         f"{round(time.time() - began)} seconds"}


if __name__ == "__main__":
    wanted = set(sys.argv[1:])
    done = {r["id"] for r in data.read_jsonl(OUT)} if OUT.exists() else set()
    for case in data.testset("synthetic"):
        if case["id"] in done or (wanted and case["id"] not in wanted):
            continue
        trace = run_one(case)
        with open(OUT, "a", encoding="utf-8") as f:
            f.write(json.dumps(trace, ensure_ascii=False) + "\n")
        result = trace.get("error",
                           "draft of %d characters" % len(trace["draft"]))
        print(case["id"], trace.get("seconds", "-"), "s", result, flush=True)
