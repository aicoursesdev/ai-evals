"""Given: the planned measures of lesson 10.3, the same code for the open
part and the sealed part, and the recordings they read."""
from scorecard import data
from scorecard.graders import CHECKS, label_correct, logged
from scorecard.judge import reading
from scorecard.stats import wilson

RUNS = data.DATA / "runs"
WEEKS = (1, 2, 3, 4)


def open_part(version="hd-1"):
    """(emails, traces) of the 100 open emails, as {id: dict}. The open
    part is never sealed, so logged() reads it."""
    ids = {e["id"] for e in data.testset("open")}
    mail = {e["id"]: e for w in WEEKS for e in logged("emails", w, keep=ids)}
    seen = {t["id"]: t for w in WEEKS
            for t in logged("traces", w, version, keep=ids)}
    return mail, seen


def measures(mail, seen):
    """{measure name: (hits, n)} on the emails that have a trace: the
    triage label against the email's own, each of the seven checks
    (hits are emails where it fires), and no check firing."""
    ids = sorted(seen)
    out = {"triage right": (sum(label_correct(seen[i], mail[i])
                                 for i in ids), len(ids))}
    fired = {i: [name for name, (check, _) in CHECKS.items()
                 if check(mail[i], seen[i])] for i in ids}
    for name in CHECKS:
        out["fires: " + name] = (sum(name in f for f in fired.values()),
                                 len(ids))
    out["no check fires"] = (sum(not f for f in fired.values()), len(ids))
    return out


def judge_pass(path, ids=None):
    """(clear PASS verdicts, replies) in a judge recording, for all its
    rows or only those whose id is in ids."""
    rows = [r for r in data.read_jsonl(path) if ids is None or r["id"] in ids]
    return sum(reading(r["reply"]) == "pass" for r in rows), len(rows)


def line(name, hits, n):
    """One reported rate: share, the count it rests on and its range."""
    low, high = wilson(hits, n)
    return f"{name:28} {hits:3} of {n:<3} {hits / n:6.1%}  " \
           f"range {low:.1%} to {high:.1%}"
