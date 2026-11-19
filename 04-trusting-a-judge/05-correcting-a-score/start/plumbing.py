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


def heldout_rates():
    """(passes kept, fails held back, passes, fails) for the chosen
    judge on the held-out drafts, against Arjun's calls."""
    human, seen = arjun("04-right-rule-arjun"), verdicts(
        RUNS / "04-heldout" / "judge.jsonl")
    ids = held_out()
    kept, held, c = two_rates([human[i] for i in ids],
                              [seen[i] for i in ids])
    return kept, held, c["tp"] + c["fn"], c["tn"] + c["fp"]


def raw_passes():
    """The judge's verdicts on the unlabelled sample: a list of True
    (a clear PASS) and False (anything else), one per draft."""
    seen = verdicts(RUNS / "04-unlabelled" / "judge.jsonl")
    return [v == "pass" for v in seen.values()]


def heldout_pairs():
    """[(Arjun passes, judge passes)] on the held-out drafts Arjun
    called pass or fail."""
    human, seen = arjun("04-right-rule-arjun"), verdicts(
        RUNS / "04-heldout" / "judge.jsonl")
    return [(human[i] == "pass", seen[i] == "pass")
            for i in held_out() if human[i] != "unsure"]
