"""Given: everything the three project files read. Sealed emails are never
read: scorecard.graders.logged skips them."""
import json

from scorecard import data
from scorecard.graders import CHECKS, logged, promises_refund

WEEKS = (1, 2, 3, 4)


def emails():
    """{id: email} for the 550 log emails outside the sealed part."""
    return {e["id"]: e for w in WEEKS for e in logged("emails", w)}


def drafts(version):
    """{id: trace} for hd-1 (weeks 1 to 4) or hd-2 (weeks 3 and 4)."""
    weeks = WEEKS if version == "hd-1" else (3, 4)
    return {t["id"]: t for w in weeks for t in logged("traces", w, version)}


def swap():
    """(emails, usual traces, smaller-model traces) for the 149 emails of
    the model-swap run (data/runs/09-model-swap/)."""
    mail = emails() | {e["id"]: e for e in data.emails(launch=True)}
    old = drafts("hd-1") | {t["id"]: t for t in data.traces(launch=True)}
    new = {r["id"]: r for r in data.run("09-model-swap")[
        "hd-1-qwen3.5-2b"]}
    return mail, old, new


def right(email, trace):
    """1 when the triage category is the one Arjun labelled."""
    return int(trace["triage"]["category"] == email["category"])


def clean(email, trace):
    """1 when none of the seven code checks fires on the draft."""
    return int(not any(c(email, trace) for c, _ in CHECKS.values()))


def pool(week):
    """{id: (email, trace)} for one week, leaving out the open part of the
    test set, the 100 held-out judge drafts and the sealed part."""
    taken = {e["id"] for e in data.testset("open")}
    taken |= set(json.loads((data.DATA / "labels" /
                             "04-judge-set-ids.json").read_text()))
    traces = {t["id"]: t for t in logged("traces", week)}
    return {e["id"]: (e, traces[e["id"]])
            for e in logged("emails", week) if e["id"] not in taken}


def flags(email, trace):
    """Why a draft should be read: the checks that fire, and a draft the
    help desk says needs no person that still promises money."""
    why = [n for n, (c, _) in CHECKS.items() if c(email, trace)]
    if not trace["triage"]["needs_human"] and promises_refund(trace["draft"]):
        why.append("needs_human mismatch")
    return why
