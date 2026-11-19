"""Given: builds judge cases from the log and reads the recordings."""
import json

from scorecard import data
from scorecard.graders import logged
from scorecard.judge import reading

RUNS = data.DATA / "runs"
WEEKS = (1, 2, 3, 4)
SETTINGS = {"temperature": 0, "max_tokens": 1500}


def template(version):
    """The prompt text of a judge version, with {slots} to fill."""
    return (RUNS / "04-dev" / f"prompt-{version}.txt").read_text()


def cases(ids):
    """One case per id, in order: the email, the draft, the page that
    answers it (or None) and the three pages the help desk was shown.
    Sealed emails are never read: logged() skips them."""
    keep = set(ids)
    emails = {e["id"]: e for w in WEEKS
              for e in logged("emails", w, keep=keep)}
    traces = {t["id"]: t for w in WEEKS
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


def arjun(name):
    """{id: a person's call} from a labels file."""
    return {r["id"]: r["call"] for r in data.labels(name)}


def replies(path):
    """{id: reply} from a recording."""
    return {r["id"]: r["reply"] for r in data.read_jsonl(path)}


def verdicts(path):
    """{id: "pass" | "fail" | "unsure" | "none"} from a recording."""
    return {i: reading(r) for i, r in replies(path).items()}


def chosen():
    """The prompt text of the judge chosen in lesson 04.4."""
    return (RUNS / "04-heldout" / "prompt.txt").read_text()


def held_out():
    """The 100 held-out ids (labels/04-judge-set-ids.json), in order."""
    return json.loads((data.DATA / "labels" / "04-judge-set-ids.json")
                      .read_text())


def two_rates(human, judged):
    """(pass-keeping rate, catch rate, counts) for lists of a person's
    calls and the judge's verdicts on the same drafts. Drafts the person
    called unsure are left out; the judge passes only on a clear pass."""
    from scorecard.judge import confusion, rates
    keep = [i for i, h in enumerate(human) if h != "unsure"]
    person = [human[i] == "pass" for i in keep]
    judge = [judged[i] == "pass" for i in keep]
    return (*rates(person, judge), confusion(person, judge))


def winner(reply, order):
    """"hd-1", "hd-2", "tie" or None for a pairwise reply; order names
    the version shown as Reply A and as Reply B (as in lesson 03.7)."""
    import re
    found = re.findall(r"^\W*(A|B|TIE)\b", reply, re.M | re.I)
    if not found:
        return None
    last = found[-1].upper()
    return "tie" if last == "TIE" else order[0 if last == "A" else 1]


def read_trials(path):
    """{trial: {id: verdict}} from a recording with a "trial" field."""
    out = {}
    for r in data.read_jsonl(path):
        out.setdefault(r["trial"], {})[r["id"]] = reading(r["reply"])
    return out
