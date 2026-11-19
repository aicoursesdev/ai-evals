"""Given: loads the log's emails and traces by id. Nothing to write here."""
from scorecard import data
from scorecard.graders import logged

WEEKS = (1, 2, 3, 4)


def emails_by_id():
    """{id: email} for the 550 logged emails outside the sealed part."""
    return {e["id"]: e for w in WEEKS for e in logged("emails", w)}


def traces_by_id(version="hd-1"):
    """{id: trace} for those emails, from one help desk version."""
    return {t["id"]: t for w in WEEKS for t in logged("traces", w, version)}


def coded():
    """{id: set of failure types} for the 100 drafts in the failure map."""
    return {r["id"]: set(r["types"].split(";")) - {""}
            for r in data.labels("01-coded")}
