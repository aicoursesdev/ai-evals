"""Given: every number the report to Meera uses, read from recordings.
No sealed email is opened: the sealed rates come from data/runs/10-sealed/.
The refund and attack figures are computed with the finished files of
lessons 07.7 and 08.7, loaded by path."""
import importlib.util
import json
from pathlib import Path

from scorecard import agents, data
from scorecard.graders import CHECKS, logged
from scorecard.judge import confusion, reading, rates

ROOT = Path(__file__).resolve().parents[3]
WEEKS = (1, 2, 3, 4)


def load(relative):
    """Import a lesson's solution file by its path from the repo root."""
    path = ROOT / relative
    spec = importlib.util.spec_from_file_location(path.stem, path.parent
                                                  / path.name)
    module = importlib.util.module_from_spec(spec)
    import sys
    sys.path.insert(0, str(path.parent))
    spec.loader.exec_module(module)
    return module


def open_read():
    """One dict per open email: id, category, fine (a reader found no
    failure, labels/01-coded.csv), quiet (no check fires), triage right."""
    ids = {e["id"] for e in data.testset("open")}
    mail = {e["id"]: e for w in WEEKS for e in logged("emails", w, keep=ids)}
    seen = {t["id"]: t for w in WEEKS for t in logged("traces", w, keep=ids)}
    ok = {r["id"]: r["ok"] == "yes" for r in data.labels("01-coded")}
    return [{"id": i, "category": mail[i]["category"], "fine": ok[i],
             "quiet": not any(c(mail[i], seen[i]) for c, _ in CHECKS.values()),
             "triage": seen[i]["triage"]["category"] == mail[i]["category"]}
            for i in sorted(mail)]


def sealed():
    """The sealed part's scores, replayed from data/runs/10-sealed/."""
    return json.loads((data.DATA / "runs" / "10-sealed"
                       / "scores.json").read_text())


def judge_rates():
    """(passes kept, of passes, fails held back, of fails) on the 100
    held-out drafts against Arjun (his unsure calls left out)."""
    arjun = {r["id"]: r["call"] for r in data.labels("04-right-rule-arjun")}
    said = {r["id"]: reading(r["reply"]) for r in data.read_jsonl(
        data.DATA / "runs" / "04-heldout" / "judge.jsonl")}
    keep = [i for i in said if arjun[i] != "unsure"]
    c = confusion([arjun[i] == "pass" for i in keep],
                  [said[i] == "pass" for i in keep])
    return c["tp"], c["tp"] + c["fn"], c["tn"], c["tn"] + c["fp"]


def refund_agent():
    """(right at temperature 0 of 30, pass^3 over five hot trials)."""
    checks = load("07-agents-and-conversations/07-project-agent-eval/"
                  "solution/checks.py")
    scen = {s["id"]: s for s in data.scenarios()}
    trials = [t | {"scenario": scen[t["id"]]}
              for t in data.run("07-refund-trials")["hd-1"]]
    cold = sum(checks.outcome_ok(t) for t in trials if t["temperature"] == 0)
    right = [sum(checks.outcome_ok(t) for t in trials
                 if t["temperature"] == 0.7 and t["id"] == s) for s in scen]
    return cold, agents.pass_hat_k(right, [5] * 30, 3)


def attacks():
    """{harm: (failures, tries)} over the distinct attacks (lesson 08.7)."""
    counts = load("08-safety-and-rare-failures/07-project-safety-gate/"
                  "solution/counts.py")
    return counts.count_by_harm(counts.distinct_attacks())


def two_versions():
    """(hd-1 quiet, hd-2 quiet, emails) on the 277 log emails (weeks 3 and
    4, outside the sealed part) that both versions answered."""
    mail = {e["id"]: e for w in (3, 4) for e in logged("emails", w)}
    one = {t["id"]: t for w in (3, 4) for t in logged("traces", w, "hd-1")}
    two = {t["id"]: t for w in (3, 4) for t in logged("traces", w, "hd-2")}
    ids = sorted(set(one) & set(two))
    quiet = lambda t, i: not any(c(mail[i], t[i]) for c, _ in CHECKS.values())
    return (sum(quiet(one, i) for i in ids), sum(quiet(two, i) for i in ids),
            len(ids))


def tokens_per_email():
    """(mean tokens per email, emails) for hd-1 over the log outside the
    sealed part: prompt plus reply tokens of triage and draft."""
    rows = [t for w in WEEKS for t in logged("traces", w)]
    return sum(t["prompt_tokens"] + t["completion_tokens"]
               for t in rows) / len(rows), len(rows)


def weekly_random():
    """(passes, drafts) among the 20 randomly drawn of the weekly sample."""
    rows = [r for r in data.labels("09-weekly-sample")
            if r["selected"] == "random"]
    return sum(r["call"] == "pass" for r in rows), len(rows)
