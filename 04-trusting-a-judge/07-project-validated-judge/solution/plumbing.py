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
    """One True (a clear PASS) or False per draft of the unlabelled
    sample, from the recording."""
    seen = verdicts(RUNS / "04-unlabelled" / "judge.jsonl")
    return [v == "pass" for v in seen.values()]


def three_callers():
    """(ids, Arjun's calls, Divya's calls, the judge's verdicts) on the
    80 held-out drafts both people called pass or fail."""
    a, d = arjun("04-right-rule-arjun"), arjun("04-right-rule-divya")
    j = verdicts(RUNS / "04-heldout" / "judge.jsonl")
    ids = [i for i in held_out() if "unsure" not in (a[i], d[i])]
    return (ids, [a[i] for i in ids], [d[i] for i in ids],
            ["pass" if j[i] == "pass" else "fail" for i in ids])


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


def bias_data():
    """(sample ids, unpadded verdicts, padded verdicts, asked again at
    temperature 0, warm runs {trial: {id: verdict}}) for the 30 drafts
    of lesson 04.6, from the recordings in runs/04-bias."""
    sample = json.loads((RUNS / "04-bias" / "sample-ids.json").read_text())
    return (sample, verdicts(RUNS / "04-dev" / "v4.jsonl"),
            verdicts(RUNS / "04-bias" / "length.jsonl"),
            verdicts(RUNS / "04-bias" / "again-t0.jsonl"),
            read_trials(RUNS / "04-bias" / "again-t07.jsonl"))


def first_won():
    """(requests where the reply shown first won, requests) in the
    recorded pairwise run of lesson 03.7."""
    pairs = data.read_jsonl(RUNS / "03-pairwise" / "pairs.jsonl")
    first = sum(winner(r["reply"], (r["a"], r["b"])) == r["a"]
                for r in pairs)
    return first, len(pairs)
