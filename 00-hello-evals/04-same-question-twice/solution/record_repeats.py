"""Lesson 00.4: record the 'ask twice' run: 10 week-1 emails, five times at
temperature 0.7 (seeds 1 to 5) and once at temperature 0.

From this folder: uv run python record_repeats.py

NEEDS A LIVE MODEL (Ollama with qwen3.5:4b). You never need to run it: its
result is already in the repo, and the tests never call it. Resumable: a
finished file is skipped.
"""

import json

from helpdesk.pipeline import handle
from scorecard import data

OUT = data.DATA / "runs" / "00-ask-twice"
EMAILS = data.emails(week=1)[::15]  # every 15th email: E-0151, E-0166, ...


def record(name, temperature, seed):
    """Run the emails once and write one file; skip it if it exists."""
    path = OUT / f"{name}.jsonl"
    if path.exists():
        return
    rows = [handle(e, temperature=temperature, seed=seed) for e in EMAILS]
    with open(path, "w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    print("wrote", path, flush=True)


if __name__ == "__main__":
    record("temp-0", 0, None)
    for seed in range(1, 6):
        record(f"temp-0.7-seed-{seed}", 0.7, seed)
