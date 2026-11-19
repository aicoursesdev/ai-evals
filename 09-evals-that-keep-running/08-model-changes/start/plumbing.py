"""Given: loads the held-out judge cases and reads the recordings of the
judge, so 08-model-changes can compare two models. Sealed emails are never
read: scorecard.graders.logged skips them."""
import json

from scorecard import data
from scorecard.graders import CHECKS, logged
from scorecard.judge import reading

RUNS = data.DATA / "runs"
SETTINGS = {"temperature": 0, "max_tokens": 1500}


def held_out():
    """The 100 held-out ids (labels/04-judge-set-ids.json), in order."""
    return json.loads((data.DATA / "labels" / "04-judge-set-ids.json")
                      .read_text())


def cases(ids):
    """One case per id: the email, the draft, the page that answers it
    (or None) and the three pages the help desk was shown."""
    keep = set(ids)
    emails = {e["id"]: e for w in (1, 2, 3, 4)
              for e in logged("emails", w, keep=keep)}
    traces = {t["id"]: t for w in (1, 2, 3, 4)
              for t in logged("traces", w, keep=keep)}
    text = {a["id"]: a["text"].split("---", 2)[2].strip()
            for a in data.articles()}
    for i in ids:
        e, t = emails[i], traces[i]
        page = e["answer_article"]
        yield {"id": i, "draft": t["draft"],
               "email": f"Subject: {e['subject']}\n\n{e['body']}",
               "answer": f"[{page}]\n{text[page]}" if page else
                         "None: no page answers this email.",
               "pages": "\n\n".join(f"[{r['article_id']}]\n{r['chunk']}"
                                    for r in t["retrieved"])}


def verdicts(path):
    """{id: "pass" | "fail" | "unsure" | "none"} from a recording."""
    return {r["id"]: reading(r["reply"]) for r in data.read_jsonl(path)}


def right(email, trace):
    """1 when the triage category is the one Arjun labelled, else 0."""
    return int(trace["triage"]["category"] == email["category"])


def clean(email, trace):
    """1 when none of the seven code checks fires on the draft, else 0."""
    return int(not any(c(email, trace) for c, _ in CHECKS.values()))


def swap():
    """(emails, old traces, new traces), each {id: ...}, for the 149 emails
    of the model-swap run: hd-1 with the usual model and with a smaller one.
    The usual model's traces are the ordinary recorded ones."""
    mail = {e["id"]: e for w in (1, 2, 3, 4) for e in logged("emails", w)}
    mail |= {e["id"]: e for e in data.emails(launch=True)}
    old = {t["id"]: t for w in (1, 2, 3, 4) for t in logged("traces", w)}
    old |= {t["id"]: t for t in data.traces(launch=True)}
    new = {r["id"]: r for r in data.run("09-model-swap")[
        "hd-1-qwen3.5-2b"]}
    return mail, old, new
