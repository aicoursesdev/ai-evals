"""Lesson 08.2: run the 30 harmless look-alike emails through the help desk.

NEEDS A MODEL (Ollama). A live recorder: no test runs it, and you do not
need it, because its recording is already in data/runs/08-look-alikes/.

    uv run python record_look_alikes.py [--reverse]

Uses the model in helpdesk/versions/hd-1/settings.json.
Appends one JSON line per email to data/runs/08-look-alikes/hd-1.jsonl and
skips emails already there, so it is safe to stop and restart. Run it
twice, the second time with --reverse, to use two workers.
"""
import json
import sys

from helpdesk.pipeline import handle
from scorecard.data import DATA

OUT = DATA / "runs" / "08-look-alikes" / "hd-1.jsonl"
emails = [json.loads(line) for line in
          (DATA / "attacks" / "look-alikes.jsonl").read_text().splitlines()]


def recorded():
    if not OUT.exists():
        return set()
    return {json.loads(line)["id"] for line in OUT.read_text().splitlines()}


# "--reverse" works from the end, so two copies can share the job.
if "--reverse" in sys.argv:
    emails.reverse()
for e in emails:
    if e["id"] in recorded():
        continue
    record = handle(e, "hd-1", 0)
    with open(OUT, "a", encoding="utf-8") as out:
        out.write(json.dumps(record, ensure_ascii=False) + "\n")
    print("recorded", e["id"], flush=True)
