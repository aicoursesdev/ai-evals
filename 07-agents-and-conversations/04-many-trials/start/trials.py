"""Lesson 07.4: the recorded trials, split by temperature (already written
for you).

`scenarios` maps a scenario id such as "RF-01" to its record. `hot` is the
150 trials recorded at temperature 0.7, five per scenario (seeds 1 to 5), and
`cold` the 30 at temperature 0, one per scenario, all from
runs/07-refund-trials/hd-1.jsonl. `passed(trial)` is True when the trial said
the right outcome and left the right state (the two checks of lesson 07.2).
"""
from scorecard import agents, data

scenarios = {s["id"]: s for s in data.scenarios()}
rows = data.run("07-refund-trials")["hd-1"]
hot = [r for r in rows if r["temperature"] == 0.7]
cold = [r for r in rows if r["temperature"] == 0]


def passed(trial):
    s = scenarios[trial["id"]]
    return agents.outcome_correct(trial, s) and agents.state_correct(trial, s)
