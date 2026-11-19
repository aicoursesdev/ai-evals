"""Given: Arjun's calls on the development drafts and the first judge's
recorded verdicts on them."""
from scorecard import data
from scorecard.graders import logged
from scorecard.judge import reading

WEEKS = (1, 2, 3, 4)
JUDGE_V1 = data.DATA / "runs" / "03-judge" / "right-rule.jsonl"


def arjun_dev():
    """{id: "pass" | "fail" | "unsure"}: Arjun's calls on the 100
    development drafts (labels/03-right-rule-arjun.csv)."""
    return {r["id"]: r["call"] for r in data.labels("03-right-rule-arjun")}


def judge_v1():
    """{id: "pass" | "fail" | "unsure" | "none"}: what the first judge's
    recorded reply says; "none" is a reply with no verdict line."""
    return {r["id"]: reading(r["reply"]) for r in data.read_jsonl(JUDGE_V1)}


def notes():
    """{id: Arjun's note from Module 01} for the 100 drafts."""
    return {r["id"]: r["note"] for r in data.labels("01-open-notes")}


def drafts(ids):
    """{id: (email, draft)} for some of the 100 drafts."""
    keep = set(ids)
    mails = {x["id"]: x for w in WEEKS
             for x in logged("emails", w, keep=keep)}
    traces = {x["id"]: x for w in WEEKS
              for x in logged("traces", w, keep=keep)}
    return {i: (mails[i], traces[i]["draft"]) for i in ids}
