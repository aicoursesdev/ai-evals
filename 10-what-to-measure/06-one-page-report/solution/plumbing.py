"""Given: the counts the page needs, read from recordings only (no sealed
email is opened: the sealed rates come from data/runs/10-sealed/)."""
import json

from scorecard import data
from scorecard.graders import CHECKS, logged

WEEKS = (1, 2, 3, 4)


def quiet_and_read():
    """(open emails, those where no check fires, of those the ones a
    reader found a failure in), from labels/01-coded.csv."""
    ids = {e["id"] for e in data.testset("open")}
    mail = {e["id"]: e for w in WEEKS for e in logged("emails", w, keep=ids)}
    seen = {t["id"]: t for w in WEEKS for t in logged("traces", w, keep=ids)}
    ok = {r["id"]: r["ok"] == "yes" for r in data.labels("01-coded")}
    quiet = [i for i in sorted(mail) if not any(
        c(mail[i], seen[i]) for c, _ in CHECKS.values())]
    return len(ids), len(quiet), sum(not ok[i] for i in quiet)


def sealed_no_check():
    """(hits, n) for "no check fires" on the sealed part, replayed."""
    path = data.DATA / "runs" / "10-sealed" / "scores.json"
    hits, n, *_ = json.loads(path.read_text())["rates"]["no check fires"]
    return hits, n
