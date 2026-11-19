"""Given: the week-4 emails and hd-1's drafts outside the open, held-out and
sealed sets, and the review sheet's entry. Sealed emails are never
read: scorecard.graders.logged skips them."""
import json

from scorecard import data
from scorecard.graders import logged


def pool(week=4):
    """{id: (email, trace)} for the week's log, leaving out the open part
    of the test set, the 100 held-out judge drafts and the sealed part."""
    taken = {e["id"] for e in data.testset("open")}
    taken |= set(json.loads((data.DATA / "labels" /
                             "04-judge-set-ids.json").read_text()))
    traces = {t["id"]: t for t in logged("traces", week)}
    return {e["id"]: (e, traces[e["id"]])
            for e in logged("emails", week) if e["id"] not in taken}


def sheet_entry(email, trace, why):
    """One entry of the review sheet, as Markdown."""
    pages = ", ".join(r["article_id"] for r in trace["retrieved"])
    return (f"## {email['id']} ({why})\n\n"
            f"**Subject:** {email['subject']}\n\n{email['body']}\n\n"
            f"**Help desk's label:** {trace['triage']}\n\n"
            f"**Pages shown:** {pages}\n\n**Draft:**\n\n{trace['draft']}\n")
