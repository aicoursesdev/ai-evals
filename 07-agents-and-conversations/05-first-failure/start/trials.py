"""Lesson 07.5: the recorded trials that failed, ready to use (already
written for you).

`scenarios` maps a scenario id such as "RF-01" to its record. `load()`
returns all 180 trials of runs/07-refund-trials/hd-1.jsonl, each with its
scenario added under "scenario". `failed()` keeps the 74 that did not both
say and leave the right outcome (the two checks of lesson 07.2).
"""
from scorecard import agents, data

scenarios = {s["id"]: s for s in data.scenarios()}


def load():
    rows = data.run("07-refund-trials")["hd-1"]
    return [{**t, "scenario": scenarios[t["id"]]} for t in rows]


def failed():
    return [t for t in load()
            if not (agents.outcome_correct(t, t["scenario"])
                    and agents.state_correct(t, t["scenario"]))]
