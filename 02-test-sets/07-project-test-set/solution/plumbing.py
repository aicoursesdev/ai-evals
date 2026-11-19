"""Given for lesson 02.7: the files and the printing around your code.

Nothing here opens a trace: `trace_lines` hands over raw lines, and the code
you write decides which to parse."""
import json
from collections import Counter

from scorecard import data
from slices import tally

OUT = data.DATA / "testsets" / "v1"
PARTS = ("open", "sealed", "synthetic")
# Found by reading Module 01's hundred: the reply never ended, no draft.
ODD = {"E-0722": "no_draft"}


def used_ids():
    """Ids that other lessons open: the ids of two recorded runs, nothing
    else read from them."""
    runs = data.DATA / "runs"
    pairs = {r["id"] for r in data.read_jsonl(runs / "03-pairwise"
                                              / "pairs.jsonl")}
    repeats = set(json.loads((runs / "05-repeats" / "sample-ids.json")
                             .read_text(encoding="utf-8")))
    return pairs | repeats


def tagged(email, part):
    """The email as logged, plus the part it belongs to and its length."""
    row = email | {"part": part, "source": "log", "added_in": "v1.0",
                   "long": len(email["body"]) >= 400}
    return row | ({"odd": ODD[email["id"]]} if email["id"] in ODD else {})


def write(rows, path):
    """Write the rows as one JSON line each."""
    with open(path, "w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def print_slices(opened, sealed):
    """How many of each slice the open part, the sealed part and both hold."""
    before, after = tally(opened), tally(opened + sealed)
    print("slice                     open  sealed  together")
    for (field, value) in sorted(after, key=lambda s: (s[0], str(s[1]))):
        name = f"{field}={value}"
        print(f"{name:<24}{before[(field, value)]:>6}"
              f"{after[(field, value)] - before[(field, value)]:>8}"
              f"{after[(field, value)]:>10}")


def prompt_files():
    """{file name: text} for every prompt file of every help desk version."""
    folder = data.DATA.parent / "helpdesk" / "versions"
    return {p.name: p.read_text(encoding="utf-8")
            for p in folder.glob("*/*.md")}


def trace_lines():
    """Every raw line of the log's four trace files, unparsed."""
    for week in (1, 2, 3, 4):
        path = data.DATA / "traces" / "hd-1" / f"week-{week}.jsonl"
        yield from path.read_text(encoding="utf-8").splitlines()


def print_first_score(opened, said):
    """The first score, by week, and a note that the seal is unbroken."""
    right = Counter(e["week"] for i, e in opened.items()
                    if said[i] == e["category"])
    print("open part, triage category:", sum(right.values()), "of",
          len(opened))
    print("by week:", {w: f"{right[w]} of 25" for w in (1, 2, 3, 4)})
    print("sealed part: not scored (0 times so far)")
