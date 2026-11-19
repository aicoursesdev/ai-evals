"""Given: hd-1's triage on the log, week by week, without the sealed
emails (scorecard.graders.logged never parses a sealed line)."""
from collections import Counter

from scorecard.graders import logged

WEEKS = (1, 2, 3, 4)


def rows(week):
    """[(category Arjun labelled, 1 if the help desk's triage matched)]
    for the week's emails outside the sealed part."""
    traces = {t["id"]: t for t in logged("traces", week)}
    return [(e["category"],
             int(traces[e["id"]]["triage"]["category"] == e["category"]))
            for e in logged("emails", week)]


def counts(week):
    """({category: emails}, {category: emails the triage got right})."""
    got = rows(week)
    return (Counter(c for c, _ in got),
            Counter(c for c, hit in got if hit))
