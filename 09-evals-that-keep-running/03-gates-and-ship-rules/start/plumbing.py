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


def clean(email, trace):
    """1 when none of the seven code checks fires on the draft, else 0."""
    return int(not any(check(email, trace)
                       for check, _ in CHECKS.values()))


def sample_ids():
    """The 100 week-4 emails of the recorded repeats."""
    path = data.DATA / "runs" / "05-repeats" / "sample-ids.json"
    return json.loads(path.read_text())


def repeats():
    """(baseline, triage reruns, check reruns) as lists of 0/1 over the 100
    emails: hd-1 at temperature 0 (the ordinary trace), then 20 reruns of
    triage and 5 of the whole help desk at temperature 0.7."""
    mail, base = emails(), drafts("hd-1")
    ids = [i for i in sample_ids() if i in mail]
    tri, full = {}, {}
    for r in data.run("05-repeats")["triage-seeds"]:
        tri.setdefault(r["seed"], {})[r["id"]] = r
    for r in data.run("05-repeats")["draft-seeds"]:
        full.setdefault(r["seed"], {})[r["id"]] = r
    return ([[category_right(mail[i], base[i]) for i in ids],
             [clean(mail[i], base[i]) for i in ids]],
            [[category_right(mail[i], t[i]) for i in ids]
             for t in tri.values()],
            [[clean(mail[i], t[i]) for i in ids] for t in full.values()])
