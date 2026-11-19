"""Lesson 10.3: THE COURSE'S ONE OPENING of the sealed part. Run once.

From this folder: uv run python score_sealed.py   (NEEDS THE LOCAL MODEL)
It scores the planned measures of data/runs/10-sealed/plan.md on the 50
sealed emails and writes data/runs/10-sealed/. To read the result later,
run replay_sealed.py: it never opens a sealed trace.
"""
import json
import re
import sys
from datetime import datetime

from plumbing import RUNS, WEEKS, judge_pass, line, measures
from scorecard import data
from scorecard.judge import reading, record
from scorecard.stats import mcnemar, pair_counts, paired, wilson

OUT = RUNS / "10-sealed"
SETTINGS = {"temperature": 0, "max_tokens": 1500}


def _open_sealed_traces(version):
    """THE ONE OPENING: the sealed ids' traces, read line by line. The
    course's `logged` loader skips these lines and is not weakened."""
    sealed = {e["id"] for e in data.testset("sealed")}
    found = {}
    for week in WEEKS:
        path = data.DATA / "traces" / version / f"week-{week}.jsonl"
        if not path.exists():
            continue
        for text in path.read_text(encoding="utf-8").splitlines():
            if re.match(r'\{"id": "([^"]+)"', text)[1] in sealed:
                found[json.loads(text)["id"]] = json.loads(text)
    return found


def judge_rows(mail, seen):
    """One request per sealed draft, from the exact prompt of version 4."""
    template = (RUNS / "04-dev" / "prompt-v4.txt").read_text()
    text = {a["id"]: a["text"].split("---", 2)[2].strip()
            for a in data.articles()}
    rows = []
    for i in sorted(seen):
        e, t, page = mail[i], seen[i], mail[i]["answer_article"]
        rows.append({"id": i, "prompt": template.format(
            email=f"Subject: {e['subject']}\n\n{e['body']}",
            answer=f"[{page}]\n{text[page]}" if page else
            "None: no page answers this email.",
            draft=t["draft"],
            pages="\n\n".join(f"[{r['article_id']}]\n{r['chunk']}"
                              for r in t["retrieved"]))})
    return rows


def ask_all(rows):
    """Ask once per row, one at a time. Stops if the first call is slow."""
    for n, row in enumerate(rows):
        record(OUT / "judge.jsonl", [row], SETTINGS)
        if n == 0:
            first = data.read_jsonl(OUT / "judge.jsonl")[0]["seconds"]
            print(f"first call: {first} s")
            if first > 60:
                sys.exit("first call took over a minute: stop and look")


def hd2_pairs(mail, old):
    """hd-1 against hd-2 on the sealed emails hd-2 answered, for the two
    code measures: the four kinds of pair, and the paired difference."""
    new = _open_sealed_traces("hd-2")
    ids = sorted(set(new) & set(old))
    out = {"n": len(ids)}
    for name in ("triage right", "no check fires"):
        x, y = ([measures(mail, {i: t[i]})[name][0] for i in ids]
                for t in (old, new))
        p = paired(x, y)
        out[name] = {"hd-1": sum(x), "hd-2": sum(y), "pairs": pair_counts(
            x, y), "diff": p["diff"], "low": p["low"], "high": p["high"],
            "mcnemar": mcnemar(x, y)}
    return out


if __name__ == "__main__":
    if (OUT / "scores.json").exists():
        sys.exit("the sealed part is spent: run replay_sealed.py")
    mail = {e["id"]: e for e in data.testset("sealed")}
    seen = _open_sealed_traces("hd-1")
    assert set(seen) == set(mail), "a sealed email has no hd-1 trace"
    began = datetime.now().astimezone()
    rates = measures(mail, seen)
    ask_all(judge_rows(mail, seen))
    rep = data.read_jsonl(OUT / "judge.jsonl")
    count = {k: sum(reading(r["reply"]) == k for r in rep)
             for k in ("pass", "fail", "unsure", "none")}
    rates["judge: clear PASS (v4)"] = judge_pass(OUT / "judge.jsonl")
    two = hd2_pairs(mail, seen)
    out = {"opened_at": began.isoformat(timespec="seconds"),
           "rates": {k: [h, n, *wilson(h, n)] for k, (h, n) in rates.items()},
           "judge": count | {"replies": len(rep), "finish": sorted(
               {r["finish_reason"] for r in rep}),
               "longest": max(r["completion_tokens"] for r in rep),
               "seconds": round(sum(r["seconds"] for r in rep))},
           "hd2": two}
    (OUT / "scores.json").write_text(json.dumps(out, indent=1))
    for k, (h, n) in rates.items():
        print(line(k, h, n))
    print(count, "hd-2 pairs:", two["n"])
