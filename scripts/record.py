"""Record the help desk's runs: a resumable recorder.

    uv run python scripts/record.py <run> [--workers 2]

Runs: launch, weeks, retrieval, refunds, attacks, hd2, repeats-triage,
repeats-draft, swap. Each run appends one JSON line per case to its file and
skips cases already in it, so it is safe to stop and restart. Model outputs
are written exactly as they came back; nothing is edited afterwards.
"""
import argparse
import json
import re
import sqlite3
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from helpdesk import llm  # noqa: E402
from helpdesk.pipeline import handle, triage  # noqa: E402
from helpdesk.refunds import run as refund_run  # noqa: E402
from helpdesk.search import articles, search  # noqa: E402
from helpdesk.version import load  # noqa: E402

DATA = ROOT / "data"
EMAILS = DATA / "emails"


def jsonl(path):
    path = Path(path)
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()] if path.exists() else []


def sealed_ids():
    """Emails whose traces nobody may read until the sealed test is scored (Module 02)."""
    return {e["id"] for e in jsonl(DATA / "testsets/v1/sealed.jsonl")}


RUNAWAY = "E-0722"   # its reply never ends: see runs/01-runaway-draft/


def log_week(n):
    return jsonl(EMAILS / f"log-week-{n}.jsonl")


def week_ready(n):
    """A log week is ready when it has 150 lines and its hard-cases file exists."""
    notes = "hard-cases-weeks-1-2.md" if n <= 2 else "hard-cases-weeks-3-4.md"
    return len(log_week(n)) == 150 and (EMAILS / notes).exists()


def record(path, cases, workers=2):
    """cases: list of (key, function returning a dict). Appends each finished record.

    A record's key is (id, trial or seed or None); a case already in the file is skipped.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    done = {(r["id"], r.get("trial", r.get("seed"))) for r in jsonl(path)}
    todo = [c for c in cases if c[0] not in done]
    print(f"{path}: {len(done)} done, {len(todo)} to do", flush=True)
    lock, began, failed = threading.Lock(), time.time(), 0
    with open(path, "a", encoding="utf-8") as out, ThreadPoolExecutor(workers) as pool:
        futures = {pool.submit(fn): key for key, fn in todo}
        for n, f in enumerate(as_completed(futures), 1):
            try:
                rec = f.result()
            except Exception as e:  # noqa: BLE001 - a failure is recorded, never retried
                failed += 1
                key = futures[f]
                tag = "trial" if "refund" in path.name + path.parent.name else "seed"
                rec = {"id": key[0], "error": f"failed: {type(e).__name__}: {e}"[:300],
                       "recorded_at": datetime.now().astimezone().isoformat(timespec="seconds")}
                if key[1] is not None:
                    rec[tag] = key[1]
                print(f"  failed {key}: {rec['error']}", flush=True)
            with lock:
                out.write(json.dumps(rec, ensure_ascii=False) + "\n")
                out.flush()
            if n % 5 == 0 or n == len(todo):
                print(f"  {n}/{len(todo)}  {time.time() - began:.0f} s", flush=True)
    if failed:
        print(f"  {failed} failed; each is recorded with an `error` and is not retried "
              "(delete its line to try it again)")
    return failed


# ---- the runs ---------------------------------------------------------

def traces(path, emails, version="hd-1", **kw):
    return record(path, [((e["id"], None), lambda e=e: handle(e, version, 0, **kw)) for e in emails], WORKERS)


def run_launch():
    traces(DATA / "traces/hd-1/launch.jsonl", jsonl(EMAILS / "inbox.jsonl"))


def run_weeks(version="hd-1", weeks=(1, 2, 3, 4)):
    for n in weeks:
        if week_ready(n):
            traces(DATA / f"traces/{version}/week-{n}.jsonl", log_week(n), version)
        else:
            print(f"week {n} is not ready yet (needs 150 emails and its hard-cases file)")


def run_hd2():
    run_weeks("hd-2", (3, 4))


def run_retrieval():
    questions = jsonl(DATA / "questions/retrieval.jsonl")

    def one(q):
        began = time.time()
        top = search(q["question"], k=10)
        trace = handle({"id": q["id"], "subject": "", "body": q["question"]}, "hd-1", 0)
        return {"id": q["id"], "question": q["question"], "version": "hd-1", "k": load("hd-1")["k"],
                "top10": [{"rank": i + 1, "article_id": h["article_id"], "score": h["score"]}
                          for i, h in enumerate(top)],
                "triage": trace["triage"], "draft": trace["draft"], "citations": trace["citations"],
                "model": trace["model"], "temperature": 0, "prompt_tokens": trace["prompt_tokens"],
                "completion_tokens": trace["completion_tokens"],
                "seconds": round(time.time() - began, 2), "recorded_at": trace["recorded_at"]}
    record(DATA / "runs/06-retrieval/hd-1.jsonl",
           [((q["id"], None), lambda q=q: one(q)) for q in questions], WORKERS)


def run_refunds():
    cases = []
    for s in jsonl(DATA / "scenarios/refunds.jsonl"):
        for trial in range(6):  # 0: temperature 0; 1 to 5: temperature 0.7, seed = trial
            cases.append(((s["id"], trial), lambda s=s, t=trial: refund_run(
                s, "hd-1", 0 if t == 0 else 0.7, None if t == 0 else t) | {"trial": t}))
    record(DATA / "runs/07-refund-trials/hd-1.jsonl", cases, WORKERS)


def owner_email(text):
    """The email of the customer who owns the first order named in a text."""
    oid = re.search(r"TW-\d{5}", text).group(0)
    row = sqlite3.connect(DATA / "orders.db").execute(
        "SELECT c.email FROM orders o JOIN customers c ON c.id = o.customer_id WHERE o.id = ?", (oid,)).fetchone()
    return row[0]


PLANTED = {"RT-12": "How do refunds work, and how fast is the money paid?",
           "RT-13": "What is the waterproof rating of the Storm Pro?"}


def run_attacks():
    inbox = {e["id"]: e for e in jsonl(EMAILS / "inbox.jsonl")}
    chat_from = "chat-visitor@example.com"

    def one(a):
        t = a["target"]
        src = a["source"].split()[-1] if a["source"].startswith("emails/") else None
        if a["id"] in PLANTED:  # the planted article is added to the help centre for this call only
            planted = a["payload"].split("---\n", 2)
            head = dict(l.split(": ", 1) for l in planted[1].strip().splitlines())
            extra = [head | {"text": planted[2].strip()}]
            email = {"id": a["id"], "subject": "", "body": PLANTED[a["id"]]}
            kind, res = "pipeline", handle(email, "hd-1", 0, extra_articles=extra)
        elif t == "refund_agent":
            msg, sender = (inbox[src]["body"], inbox[src]["from_email"]) if src else (a["payload"], owner_email(a["payload"]))
            kind, res = "refund_agent", refund_run({"id": a["id"], "from_email": sender, "message": msg}, "hd-1", 0)
        elif src:  # triage, order_tools and help_desk_chat attacks arriving as emails
            kind, res = "pipeline", handle(inbox[src], "hd-1", 0)
        else:      # the chat: a visitor's message goes through the same pipeline
            kind, res = "pipeline", handle({"id": a["id"], "subject": "", "body": a["payload"],
                                            "from_email": chat_from}, "hd-1", 0)
        return {"id": a["id"], "attack_kind": a["kind"], "target": t, "source": a["source"],
                "ran_as": kind, "version": "hd-1", "result": res}
    record(DATA / "runs/08-attacks/hd-1.jsonl",
           [((a["id"], None), lambda a=a: one(a)) for a in jsonl(DATA / "attacks/red-team.jsonl")], WORKERS)


def sample_ids():
    """The 100 ids of runs/05-repeats/sample-ids.json (see its README); never a sealed id."""
    path = DATA / "runs/05-repeats/sample-ids.json"
    ids = json.loads(path.read_text())
    bad = sealed_ids() & set(ids) | ({RUNAWAY} & set(ids))
    if bad:
        sys.exit(f"sample-ids.json holds ids that must not be recorded: {sorted(bad)}")
    return ids


def run_repeats_triage():
    sample_ids()
    emails = {e["id"]: e for e in log_week(4)}

    def one(e, seed):
        began = time.time()
        out, pt, ct = triage(e, "hd-1", 0.7, seed)
        return {"id": e["id"], "seed": seed, "version": "hd-1", "model": load("hd-1")["model"],
                "temperature": 0.7} | out | {
            "prompt_tokens": pt, "completion_tokens": ct, "seconds": round(time.time() - began, 2),
            "recorded_at": datetime.now().astimezone().isoformat(timespec="seconds")}
    record(DATA / "runs/05-repeats/triage-seeds.jsonl",
           [((i, s), lambda i=i, s=s: one(emails[i], s)) for s in range(1, 21) for i in sample_ids()], WORKERS)


def run_repeats_draft():
    emails = {e["id"]: e for e in log_week(4)}
    record(DATA / "runs/05-repeats/draft-seeds.jsonl",
           [((i, s), lambda i=i, s=s: handle(emails[i], "hd-1", 0.7, s))
            for s in range(1, 6) for i in sample_ids()], WORKERS)


def run_swap():
    """The test set's open part plus the launch set's test split, never a sealed id or E-0722."""
    pool = {e["id"]: e for e in jsonl(DATA / "testsets/v1/open.jsonl")}
    pool |= {e["id"]: e for e in jsonl(EMAILS / "inbox.jsonl") if e["split"] == "test"}
    emails = [e for i, e in sorted(pool.items()) if i not in sealed_ids() and i != RUNAWAY]
    traces(DATA / "runs/09-model-swap/hd-1-qwen3.5-2b.jsonl", emails, "hd-1", model="qwen3.5:2b")


RUNS = {"launch": run_launch, "weeks": run_weeks, "retrieval": run_retrieval, "refunds": run_refunds,
        "attacks": run_attacks, "hd2": run_hd2, "repeats-triage": run_repeats_triage,
        "repeats-draft": run_repeats_draft, "swap": run_swap}
WORKERS = 4

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("run", choices=RUNS)
    ap.add_argument("--workers", type=int, default=2)
    args = ap.parse_args()
    WORKERS = args.workers
    # A timed-out request counts as failed for this pass and is not retried here, so a busy
    # server is not piled up with abandoned work; the next pass picks the case up.
    llm.ATTEMPTS = 1
    llm.TIMEOUT = 120 if args.run == "swap" else llm.TIMEOUT
    RUNS[args.run]()
