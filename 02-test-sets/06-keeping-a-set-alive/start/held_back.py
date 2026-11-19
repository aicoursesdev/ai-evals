"""Lesson 02.6: load what a score may use, and nothing sealed.

Given in lesson 02.6. The sealed part of the test set is scored once, in
a later module, so no score here may look at its answers.
"""
import json

from scorecard import data
from slices import log


def sealed_ids():
    return {e["id"] for e in data.testset("sealed")}


def usable_emails():
    """The 550 logged emails that are not in the sealed part."""
    sealed = sealed_ids()
    return [e for e in log() if e["id"] not in sealed]


def usable_triage():
    """{id: the help desk's three labels} for those 550 emails. A line of
    the trace file whose id is sealed is skipped before it is parsed."""
    sealed, said = sealed_ids(), {}
    for week in (1, 2, 3, 4):
        path = data.DATA / "traces" / "hd-1" / f"week-{week}.jsonl"
        for line in path.read_text(encoding="utf-8").splitlines():
            if line[8:14] not in sealed:  # every line starts {"id": "E-0152"
                trace = json.loads(line)
                said[trace["id"]] = trace["triage"]
    return said
