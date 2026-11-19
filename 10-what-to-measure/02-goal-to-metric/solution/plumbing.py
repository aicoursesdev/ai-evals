"""Given: the 100 open drafts with the checks' firing, the judge's verdict
and one reader's call on each, from recordings (no sealed email)."""
from scorecard import data
from scorecard.graders import CHECKS, logged
from scorecard.judge import reading

WEEKS = (1, 2, 3, 4)


def open_drafts():
    """One dict per open email: id, category, quiet (no check fires),
    judged (the judge's clear PASS), fine (the reader found no failure,
    labels/01-coded.csv) and triage (the label equals Arjun's)."""
    ids = {e["id"] for e in data.testset("open")}
    mail = {e["id"]: e for w in WEEKS for e in logged("emails", w, keep=ids)}
    seen = {t["id"]: t for w in WEEKS for t in logged("traces", w, keep=ids)}
    verdict = {r["id"]: reading(r["reply"])
               for r in data.read_jsonl(data.DATA / "runs" / "04-dev"
                                        / "v4.jsonl")}
    read = {r["id"]: r["ok"] == "yes" for r in data.labels("01-coded")}
    return [{"id": i, "category": mail[i]["category"],
             "quiet": not any(c(mail[i], seen[i]) for c, _ in CHECKS.values()),
             "judged": verdict[i] == "pass", "fine": read[i],
             "triage": seen[i]["triage"]["category"] == mail[i]["category"]}
            for i in sorted(mail)]
