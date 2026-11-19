"""Given for the project (lesson 01.7): the printing and reading the tools of
lessons 01.2 to 01.6 share, and `definitions` for the failure map."""
import csv
import re
import sys
import textwrap
from collections import Counter
from pathlib import Path

from scorecard import data


def wrap(text):
    """Wrap each line to 78 columns, keeping line breaks and blank lines."""
    return "\n".join(textwrap.fill(line, 78) for line in text.split("\n"))


def show(email, trace, chunks=False):
    print(f"{email['id']}  week {email['week']}  {email['language']}  "
          f"from {email['from_name']}")
    print(f"Subject: {email['subject']}\n")
    print(wrap(email["body"]))
    print("\nArjun's labels :", {k: email[k] for k in
                                  ("category", "urgency", "needs_human")})
    print("Help desk said :", trace["triage"])
    print("\nPages it fetched:")
    for hit in trace["retrieved"]:
        title = hit["chunk"].split("\n")[0].lstrip("# ")
        print(f"  {hit['article_id']:<22} {hit['score']:.2f}  {title}")
        if chunks:
            print(textwrap.indent(wrap(hit["chunk"]), "      "))
    print("\nThe draft:\n")
    print(wrap(trace["draft"]))
    print("\nCited:", trace["citations"] or "nothing")
    if trace.get("error"):
        print("\nError:", wrap(trace["error"]))


def print_ids(ids):
    """The count, then the ids ten to a line."""
    print(len(ids), "ids drawn")
    for i in range(0, len(ids), 10):
        print(" ".join(ids[i:i + 10]))


def write_sheet(ids, sheet=Path("my-notes.csv")):
    """Start the sheet: id and week filled in, ok and note left empty."""
    if sheet.exists():  # never overwrite notes you have written
        sys.exit(f"{sheet} exists, left alone")
    week_of = {e["id"]: w for w in (1, 2, 3, 4)
               for e in data.emails(week=w)}
    with open(sheet, "w", encoding="utf-8", newline="") as f:
        out = csv.writer(f)
        out.writerow(["id", "week", "ok", "note"])
        out.writerows([i, week_of[i], "", ""] for i in ids)
    print("wrote", sheet)


def defined_types(path):
    """The type names in a definitions file: lines that start '## F-...'."""
    with open(path, encoding="utf-8") as f:
        return set(re.findall(r"^## (F-[\w-]+)", f.read(), re.M))


def coded_rows(path):
    """Rows of the coded file, skipping comment lines that start with #."""
    with open(path, encoding="utf-8", newline="") as f:
        lines = [line for line in f if not line.startswith("#")]
    return list(csv.DictReader(lines))


def print_report(rows, bad):
    """How many rows were read, how many problems, then each problem."""
    print(len(rows), "rows;", len(bad), "problems")
    for line in bad:
        print(" ", line)


def read(path):
    """Rows of the coded file, skipping comment lines that start with #."""
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(l for l in f if not l.startswith("#")))


def by_week(rows):
    """{type: Counter of week -> traces}, using the log to find each week."""
    week_of = {e["id"]: w for w in (1, 2, 3, 4) for e in data.emails(week=w)}
    table = {}
    for row in rows:
        for t in row["types"].split(";"):
            if t:
                table.setdefault(t, Counter())[week_of[row["id"]]] += 1
    return table


def print_table(rows, tally):
    """The count table: traces read, then one line per type, most first."""
    failed = [r for r in rows if r["ok"] == "no"]
    print(f"{len(rows)} read, {len(rows) - len(failed)} fine, "
          f"{len(failed)} with a failure")
    weeks = by_week(rows)
    print(" n  share  type                  week 1 2 3 4")
    for name, n in tally.most_common():
        w = weeks[name]
        print(f"{n:>2}  {n / len(rows):>4.0%}  {name:<20}  "
              f"{w[1]:>7}{w[2]:>2}{w[3]:>2}{w[4]:>2}")


def print_first_seen(seen, total, batch=25):
    """When each type first appeared, then new types per batch of traces."""
    for name, position in sorted(seen.items(), key=lambda kv: kv[1]):
        print(f"read {position:>3}: {name}")
    for start in range(0, total, batch):
        new = [t for t, p in seen.items() if start < p <= start + batch]
        print(f"traces {start + 1:>3} to {start + batch:>3}: "
              f"{len(new)} new type(s)")


def print_scores(checks, rows):
    """Run every check on every row; compare with the types you gave."""
    emails = {e["id"]: e for w in (1, 2, 3, 4) for e in data.emails(week=w)}
    traces = {t["id"]: t for w in (1, 2, 3, 4)
              for t in data.traces("hd-1", week=w)}
    print(f"{'check':<20} {'type':<14} fires  right  type total  caught")
    for name, (check, wanted) in checks.items():
        fired = {r["id"] for r in rows if check(emails[r["id"]],
                                                traces[r["id"]])}
        has = {r["id"] for r in rows if wanted in r["types"].split(";")}
        print(f"{name:<20} {wanted:<14} {len(fired):>5}  {len(fired & has):>5}"
              f"  {len(has):>10}  {len(fired & has):>6}")


def definitions(path):
    """{type: (definition sentence, example id)} from the definitions file."""
    text = open(path, encoding="utf-8").read()
    found = {}
    for name, body in re.findall(r"^## (F-[\w-]+)\n(.+?)(?=\n## |\Z)", text,
                                 re.M | re.S):
        example = re.search(r"Example: (E-\d{4})", body).group(1)
        found[name] = (body.split(" Example:")[0].strip(), example)
    return found
