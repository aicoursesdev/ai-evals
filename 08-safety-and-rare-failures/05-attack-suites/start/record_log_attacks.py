"""Lesson 08.5: run the attack emails of log weeks 3 and 4 through hd-1.

NEEDS A MODEL (Ollama). A live recorder: no test runs it, and you do not
need it, because its recording is already in data/runs/08-attacks/.

    uv run python record_log_attacks.py

The traces for those weeks were still being recorded when this module was
written, so these 12 emails were run on their own, with hd-1's settings
(temperature 0). Appends to data/runs/08-attacks/log-weeks-3-4.jsonl and
skips emails already there.
"""
import json

from helpdesk.pipeline import handle
from scorecard import data

OUT = data.DATA / "runs" / "08-attacks" / "log-weeks-3-4.jsonl"
lines = OUT.read_text().splitlines() if OUT.exists() else []
done = {json.loads(line)["id"] for line in lines}
for week in (3, 4):
    for e in data.emails(week=week):
        if e["attack"] and e["id"] not in done:
            record = handle(e, "hd-1", 0)
            with open(OUT, "a", encoding="utf-8") as f:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
            print("recorded", e["id"], flush=True)
