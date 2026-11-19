"""Lesson 07.3: the 180 recorded trials and two small readers (already
written for you).

`scenarios` maps a scenario id such as "RF-01" to its record and `trials` is
every recorded trial in runs/07-refund-trials/hd-1.jsonl. `order_ids` lists
the order ids a trial's tool calls asked about; `reply_text` is what the
agent wrote to the customer: its reply when the answer was readable as
JSON, otherwise the raw text.
"""
import json

from scorecard import data

scenarios = {s["id"]: s for s in data.scenarios()}
trials = data.run("07-refund-trials")["hd-1"]


def order_ids(trial):
    """The order ids the agent passed to its tools."""
    out = []
    for c in trial["trajectory"]:
        args = json.loads(c["arguments"] or "{}")
        if "order_id" in args:
            out.append(args["order_id"])
    return out


def reply_text(trial):
    return trial["reply"] if trial["outcome"] else trial["final_raw"] or ""
