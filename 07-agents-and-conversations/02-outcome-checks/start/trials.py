"""Lesson 07.2: the recorded trials, ready to use (already written for you).

`scenarios` maps a scenario id such as "RF-01" to its record. `load` returns
the refund agent's recorded trials from runs/07-refund-trials/hd-1.jsonl:
180 in all, six per scenario, 30 at temperature 0 and 150 at 0.7. Pass a
temperature to keep only those.
"""
from scorecard import data

scenarios = {s["id"]: s for s in data.scenarios()}


def load(temperature=None):
    rows = data.run("07-refund-trials")["hd-1"]
    if temperature is None:
        return rows
    return [r for r in rows if r["temperature"] == temperature]
