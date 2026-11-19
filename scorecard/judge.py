"""Run a judge prompt, and measure the judge against human labels."""
import json
import re
from datetime import datetime


def verdict(prompt, case, ask, replay=None, unsure=False):
    """Fill the prompt with the case, ask the judge, read PASS or FAIL.

    prompt uses {name} slots filled from case. With replay (a dict of
    saved replies keyed by case id) no model is called. Returns True for
    PASS and False for FAIL; with unsure=True a last line UNSURE gives
    None. Raises if no verdict line is found.
    """
    if replay is not None:
        reply = replay[case["id"]]
    else:
        reply = ask(prompt.format(**case))
    words = "PASS|FAIL|UNSURE" if unsure else "PASS|FAIL"
    found = re.findall(rf"^\W*({words})\b", reply, re.M | re.I)
    if not found:
        raise ValueError(f"no {words} line in: {reply!r}")
    last = found[-1].upper()  # the last line is the verdict
    return None if last == "UNSURE" else last == "PASS"


def confusion(human, judge):
    """Four counts (tp, fp, fn, tn). Positive means PASS: tp is judge
    PASS and human PASS; fp is judge PASS, human FAIL."""
    pairs = [(bool(h), bool(j)) for h, j in zip(human, judge)]
    return {  # a judge's None (unsure) counts as "did not pass"
        "tp": sum(h and j for h, j in pairs),
        "fp": sum(j and not h for h, j in pairs),
        "fn": sum(h and not j for h, j in pairs),
        "tn": sum(not h and not j for h, j in pairs),
    }


def rates(human, judge):
    """(TPR, TNR) with positive = PASS. TPR: of the outputs a person
    passed, the share the judge passed. TNR: of those a person failed,
    the share the judge failed."""
    c = confusion(human, judge)
    return c["tp"] / (c["tp"] + c["fn"]), c["tn"] / (c["tn"] + c["fp"])


def agreement(a, b):
    """Share of items where two labellers gave the same label."""
    return sum(x == y for x, y in zip(a, b)) / len(a)


def kappa(a, b):
    """Cohen's kappa: (observed - chance) / (1 - chance), where chance
    is the agreement two labellers would reach by their label shares."""
    po = agreement(a, b)
    pe = sum((a.count(v) / len(a)) * (b.count(v) / len(b))
             for v in set(a) | set(b))
    return (po - pe) / (1 - pe)


def reading(reply):
    """"pass", "fail", "unsure" or "none" (no verdict line) for a reply."""
    try:
        v = verdict("{x}", {"id": 0}, None, {0: reply}, unsure=True)
    except ValueError:
        return "none"
    return "unsure" if v is None else "pass" if v else "fail"


def record(path, rows, settings):
    """Ask the local model for each row, one request at a time and no
    retries, appending each request and reply to path as it arrives.
    A row is {"id", "prompt", ...}; extra keys (like "trial") are kept.
    Rows already in the file (same id and trial) are skipped."""
    from helpdesk import llm
    key = lambda r: (r["id"], r.get("trial"))
    done = set(map(key, map(json.loads, path.read_text().splitlines()))
               if path.exists() else [])
    for row in rows:
        if key(row) in done:
            continue
        began = datetime.now().astimezone()
        r = llm.client().with_options(timeout=180).chat.completions.create(
            model=llm.MODEL, reasoning_effort="none", **settings,
            messages=[{"role": "user", "content": row["prompt"]}])
        took = (datetime.now().astimezone() - began).total_seconds()
        row |= {"reply": r.choices[0].message.content or "",
                "finish_reason": r.choices[0].finish_reason,
                "completion_tokens": r.usage.completion_tokens,
                "seconds": round(took, 1), "model": llm.MODEL,
                "settings": settings,
                "recorded_at": began.isoformat(timespec="seconds")}
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
