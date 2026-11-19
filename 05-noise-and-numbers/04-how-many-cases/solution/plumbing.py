"""Given: the log, both versions' drafts and the recorded repeats, loaded
without the 50 sealed emails of the test set (scorecard.graders.logged
never parses a sealed line)."""
import json

from scorecard import data
from scorecard.graders import CHECKS, logged


def emails():
    """{id: email} for the 550 log emails outside the sealed part."""
    return {e["id"]: e for w in (1, 2, 3, 4) for e in logged("emails", w)}


def drafts(version):
    """{id: trace} for one version: hd-1 on weeks 1-4, hd-2 on 3-4."""
    weeks = (1, 2, 3, 4) if version == "hd-1" else (3, 4)
    return {t["id"]: t for w in weeks for t in logged("traces", w, version)}


def category_right(email, trace):
    """1 when the triage category is the one Arjun labelled, else 0."""
    return int(trace["triage"]["category"] == email["category"])


def fires(email, trace):
    """The names of the Module 03 checks that fire on this draft."""
    return [name for name, (check, _) in CHECKS.items()
            if check(email, trace)]


def clean(email, trace):
    """1 when no code check fires on the draft, else 0."""
    return int(not fires(email, trace))


def sample_ids():
    """The 100 week-4 emails of the recorded repeats."""
    path = data.DATA / "runs" / "05-repeats" / "sample-ids.json"
    return json.loads(path.read_text())


def seed_runs(name):
    """{id: {seed: record}} from runs/05-repeats/<name>.jsonl."""
    found = {}
    for r in data.run("05-repeats")[name]:
        found.setdefault(r["id"], {})[r["seed"]] = r
    return found
