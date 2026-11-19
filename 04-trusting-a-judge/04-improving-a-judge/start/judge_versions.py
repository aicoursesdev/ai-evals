"""Lesson 04.4: record one judge version on the 100 development drafts.

From this folder:
    uv run python judge_versions.py v2 --live   asks the local model,
        one request at a time, and skips ids already recorded (NEEDS A MODEL)
Without --live nothing is asked: the recording is read and counted.
"""
import sys
from collections import Counter

from plumbing import RUNS, SETTINGS, arjun, cases, template, verdicts
from scorecard.judge import record

DEV = list(arjun("03-right-rule-arjun"))  # the 100 development ids


def path(version):
    """v1 is the recording from lesson 03.6; later versions are new."""
    if version == "v1":
        return RUNS / "03-judge" / "right-rule.jsonl"
    return RUNS / "04-dev" / f"{version}.jsonl"


def record_version(version):
    """Ask the local model about each development draft (NEEDS A MODEL)."""
    rows = [{"id": c["id"], "prompt": template(version).format(**c)}
            for c in cases(DEV)]
    record(path(version), rows, SETTINGS)


if __name__ == "__main__":
    version = sys.argv[1]
    if "--live" in sys.argv:
        record_version(version)
    print(version, dict(Counter(verdicts(path(version)).values())))
