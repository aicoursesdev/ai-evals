"""Lesson 09.8: the chosen judge prompt, run by a smaller model on the same
100 held-out drafts.

From this folder:
    uv run python judge_swap.py --live   asks the local model, one request
        at a time, and saves the replies (NEEDS Ollama and qwen3.5:2b)
Without --live the recording in data/runs/09-judge-swap/ is read.
"""
import os
import sys

if "--live" in sys.argv:             # must be set before helpdesk loads
    os.environ["LLM_MODEL"] = "qwen3.5:2b"

from plumbing import RUNS, SETTINGS, cases, held_out, verdicts
from scorecard.judge import record

PROMPT = (RUNS / "04-heldout" / "prompt.txt").read_text()
OUT = RUNS / "09-judge-swap" / "judge.jsonl"

if "--live" in sys.argv:
    rows = [{"id": c["id"], "prompt": PROMPT.format(**c)}
            for c in cases(held_out())]
    record(OUT, rows, SETTINGS)
print({v: list(verdicts(OUT).values()).count(v)
       for v in ("pass", "fail", "unsure", "none")})
