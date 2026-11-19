"""Check that every data file loads and agrees with the others and with data/README.md.

Run from the repo root:  uv run python scripts/check_data.py
After recording more of a run:  uv run python scripts/check_data.py --write-counts
Prints what it counted, then every problem it found; exits with 1 if there was any.
The shop files (orders.db, the help centre, ...) were checked in Applied AI
Engineering; here they are checked only against the files that point at them.
"""
import json
import re
import sqlite3
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from helpdesk.search import articles  # noqa: E402

DATA = ROOT / "data"
CATEGORIES = {"refund", "return", "shipping_delay", "order_change", "product_question", "warranty",
              "payment", "account", "complaint", "spam", "other"}
OUTCOMES = {"approve_proposal", "deny", "escalate_to_meera", "ask_for_info"}
problems = []


def check(ok, message):
    if not ok:
        problems.append(message)


def jsonl(rel):
    return [json.loads(line) for line in (DATA / rel).read_text(encoding="utf-8").splitlines()]


counts = {}  # file -> lines, compared with data/README.md at the end


def load(rel):
    if not (DATA / rel).exists():
        return None
    rows = counts[rel] = jsonl(rel)
    return rows


# ---- the shop's files -------------------------------------------------
print("shop")
arts = {a["id"]: a for a in articles()}
current = {k for k, a in arts.items() if a["status"] == "current"}
check(len(arts) == 24 and len(current) == 23, f"help centre: {len(arts)} articles, {len(current)} current")
orders = {r[0]: r[1] for r in sqlite3.connect(DATA / "orders.db").execute(
    "SELECT o.id, c.email FROM orders o JOIN customers c ON c.id = o.customer_id")}
check(len(orders) == 300, f"orders.db: {len(orders)} orders")
print(f"  {len(arts)} articles ({len(current)} current), {len(orders)} orders")

# ---- emails -----------------------------------------------------------
print("emails")
launch = load("emails/inbox.jsonl")
log = {n: load(f"emails/log-week-{n}.jsonl") for n in (1, 2, 3, 4)}
emails = {}
for rows, name in [(launch, "inbox")] + [(log[n], f"log-week-{n}") for n in log]:
    for e in rows or []:
        check(e["id"] not in emails, f"{name}: {e['id']} is not unique")
        emails[e["id"]] = e
        n = int(e["id"][2:])
        check(re.fullmatch(r"E-\d{4}", e["id"]) and 1 <= n <= 750, f"{name}: {e['id']} out of range")
        check(e["category"] in CATEGORIES, f"{e['id']}: category {e['category']}")
        check(e["urgency"] in ("low", "normal", "high"), f"{e['id']}: urgency {e['urgency']}")
        check(isinstance(e["needs_human"], bool) and isinstance(e["attack"], bool), f"{e['id']}: flags")
        check(e["answer_article"] is None or e["answer_article"] in current, f"{e['id']}: answer_article {e['answer_article']}")
        check(e["order_id"] is None or re.fullmatch(r"TW-\d{5}", e["order_id"]), f"{e['id']}: order_id {e['order_id']}")
        check(set(e) >= {"id", "received_at", "from_email", "subject", "body", "language"}, f"{e['id']}: fields")
for n, rows in log.items():
    for e in rows or []:
        check(e.get("week") == n, f"{e['id']}: week {e.get('week')} in log-week-{n}")
if launch:
    check([e["id"] for e in launch] == [f"E-{i:04d}" for i in range(1, 151)], "inbox: ids not E-0001 to E-0150")
    check(Counter(e["split"] for e in launch) == {"dev": 100, "test": 50}, "inbox: split is not 100 dev, 50 test")
print(f"  {len(emails)} emails: " + ", ".join(f"launch {len(launch or [])}" if k == 0 else f"week {k} {len(log[k] or [])}"
                                              for k in (0, 1, 2, 3, 4)))

# ---- questions, scenarios, attacks ------------------------------------
questions = load("questions/retrieval.jsonl")
scenarios = load("scenarios/refunds.jsonl")
attacks = load("attacks/red-team.jsonl")
for q in questions:
    check(q["answer_article"] is None or q["answer_article"] in current, f"{q['id']}: answer_article")
for s in scenarios:
    check(s["expected"] in OUTCOMES, f"{s['id']}: expected {s['expected']}")
    check(s["order_id"] is None or s["order_id"] in orders, f"{s['id']}: order {s['order_id']} not in orders.db")
for a in attacks:
    src = re.search(r"E-\d{4}", a["source"])
    check(src is None or src.group(0) in emails, f"{a['id']}: source {a['source']} is not an email")
print(f"  {len(questions)} questions, {len(scenarios)} scenarios, {len(attacks)} attacks")

# ---- traces and runs --------------------------------------------------
print("traces and runs")


PLANTED = {"refund-update", "feedback"}   # articles the red-team plants for one call (RT-12, RT-13)


def trace_ok(t, where):
    ok = set(arts) | (PLANTED if "08-attacks" in where else set())
    for h in t.get("retrieved", []):
        check(h["article_id"] in ok, f"{where} {t['id']}: retrieved unknown article {h['article_id']}")
    for c in t.get("citations", []):
        check(c in ok, f"{where} {t['id']}: cites unknown article {c}")


for path in sorted((DATA / "traces").glob("*/*.jsonl")):
    rel = str(path.relative_to(DATA))
    rows = load(rel)
    ids = [t["id"] for t in rows]
    check(len(ids) == len(set(ids)), f"{rel}: an id appears twice")
    check(all(i in emails for i in ids), f"{rel}: an id is not an email")
    version = path.parent.name
    check(all(t["version"] == version for t in rows), f"{rel}: version field is not {version}")
    week = re.search(r"week-(\d)", rel)
    want = {"launch": launch}.get(path.stem) or (log[int(week.group(1))] if week else None)
    check(want is None or ids and set(ids) <= {e["id"] for e in want}, f"{rel}: ids are not that file's emails")
    for t in rows:
        trace_ok(t, rel)
    print(f"  {rel}: {len(rows)}")

for path in sorted((DATA / "runs").glob("*/*.jsonl")):
    rel = str(path.relative_to(DATA))
    rows = load(rel)
    for r in rows:
        trace_ok(r, rel)
        trace_ok(r.get("result", {}), rel)
        for h in r.get("top10", []):
            check(h["article_id"] in arts, f"{rel} {r['id']}: unknown article {h['article_id']}")
        if "outcome" in r:
            check(r["outcome"] in OUTCOMES | {None}, f"{rel} {r['id']}: outcome {r['outcome']}")
    sample = {"06-retrieval": questions, "07-refund-trials": scenarios, "08-attacks": attacks}.get(path.parent.name)
    if sample and path.name == "hd-1.jsonl":
        check({r["id"] for r in rows} <= {s["id"] for s in sample}, f"{rel}: an id is not in its source file")
    print(f"  {rel}: {len(rows)}")

# ---- sealed emails are in no recorded run ------------------------------------
sealed = {e["id"] for e in jsonl("testsets/v1/sealed.jsonl")} if (DATA / "testsets/v1/sealed.jsonl").exists() else set()
for path in sorted(DATA.glob("runs/*/*")):
    if path.parent.name == "10-sealed":   # the course's one opening of the sealed part (lesson 10.3)
        continue
    text = path.read_text(encoding="utf-8")
    check(not any(f'"{i}"' in text for i in sealed), f"{path.relative_to(DATA)} holds a sealed id")

# ---- data/README.md states the counts ----
START, END = "<!-- counts:start -->", "<!-- counts:end -->"
if "--write-counts" in sys.argv:   # rewrite the table in data/README.md from the files
    table = "| File | Lines |\n|---|---|\n" + "\n".join(f"| `{rel}` | {len(rows)} |" for rel, rows in sorted(counts.items()))
    text = (DATA / "README.md").read_text(encoding="utf-8")
    head, rest = text.split(START)
    (DATA / "README.md").write_text(head + START + "\n" + table + "\n" + END + rest.split(END)[1], encoding="utf-8")
    print("data/README.md counts rewritten")
# ---------------------------------
readme = (DATA / "README.md").read_text(encoding="utf-8") if (DATA / "README.md").exists() else ""
stated = {m.group(1): int(m.group(2)) for m in re.finditer(r"^\| `([^`]+\.jsonl)` \| (\d+) \|", readme, re.M)}
for rel, n in stated.items():
    check(rel in counts and len(counts[rel]) == n, f"data/README.md says {rel} has {n} lines; the file has "
          f"{len(counts[rel]) if rel in counts else 'not been found'}")
for rel in counts:
    if rel.startswith(("traces", "emails/log")):
        check(rel in stated, f"data/README.md does not state a count for {rel}")

if problems:
    print(f"\n{len(problems)} problems:")
    for p in problems[:60]:
        print("  -", p)
    sys.exit(1)
print("\nAll data files agree.")
