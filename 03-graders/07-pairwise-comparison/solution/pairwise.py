"""Lesson 03.7: which of two drafts is better, asked in both orders.

60 emails from weeks 3 and 4 (30 each, drawn with random.Random(3)), each
with hd-1's draft and hd-2's. Every pair is asked twice: hd-1 first, then
hd-2 first. By default the recording in data/runs/03-pairwise/pairs.jsonl
is replayed and no model is called. NEEDS A MODEL only with --live.
Given, except winner, both_orders and holds_in_both, which you write.

From this folder:
    uv run python pairwise.py          replays the recording
    uv run python pairwise.py --live   asks the local model, one request
                                       at a time, and re-records
"""
import json
import random
import re
import sys
from datetime import datetime

from scorecard import data
from scorecard.graders import logged

PROMPT = """\
You compare two replies that a shop's help desk drafted for the same \
customer email. Pick the reply you would rather send: the one that answers \
what the customer asked, correctly according to the help-centre pages \
below, and promises nothing the pages do not support. If neither is \
clearly better, answer TIE.

Customer email:
{email}

Help-centre pages the help desk was shown:
{pages}

Reply A:
{a}

Reply B:
{b}

First write at most three sentences on how the replies differ. Then write \
one last line holding only A, B or TIE."""

OUT = data.DATA / "runs" / "03-pairwise" / "pairs.jsonl"
SETTINGS = {"temperature": 0, "max_tokens": 1500}
ORDERS = (("hd-1", "hd-2"), ("hd-2", "hd-1"))  # who is A, who is B


def pairs():
    """60 pairs: the email, the pages shown and both versions' drafts."""
    chosen = []
    for week in (3, 4):
        ids = [e["id"] for e in data.emails(week=week) if e["id"] != "E-0722"]
        chosen += random.Random(3).sample(ids, 30)
    keep = set(chosen)
    emails = {e["id"]: e for w in (3, 4)
              for e in logged("emails", w, keep=keep)}
    one = {t["id"]: t for w in (3, 4)
           for t in logged("traces", w, "hd-1", keep)}
    two = {t["id"]: t for w in (3, 4)
           for t in logged("traces", w, "hd-2", keep)}
    for i in chosen:
        e = emails[i]
        pages = "\n\n".join(f"[{r['article_id']}]\n{r['chunk']}"
                            for r in one[i]["retrieved"])
        yield {"id": i, "pages": pages, "hd-1": one[i]["draft"],
               "hd-2": two[i]["draft"],
               "email": f"Subject: {e['subject']}\n\n{e['body']}"}


def prompt_for(pair, order):
    first, second = order
    return PROMPT.format(email=pair["email"], pages=pair["pages"],
                         a=pair[first], b=pair[second])


def winner(reply, order):
    """"hd-1", "hd-2", "tie", or None when there is no verdict line."""
    found = re.findall(r"^\W*(A|B|TIE)\b", reply, re.M | re.I)
    if not found:
        return None
    last = found[-1].upper()
    return "tie" if last == "TIE" else order[0 if last == "A" else 1]


def both_orders(pair_id, saved):
    """The winner of one pair when each version is shown first.

    saved maps (email id, version shown first) to the recorded reply.
    Returns {"hd-1": winner, "hd-2": winner}, keyed by who was first.
    """
    return {first: winner(saved[pair_id, first], (first, second))
            for first, second in ORDERS}


def holds_in_both(one, two):
    """The winner when both orders agree, else "split"."""
    return one if one == two else "split"


def recorded():
    """{(email id, version shown first): reply} from the recording."""
    return {(r["id"], r["a"]): r["reply"] for r in data.read_jsonl(OUT)}


def ask_once(prompt):
    """One request to the local model: the reply, why it stopped, tokens."""
    from helpdesk import llm
    r = llm.client().with_options(timeout=180).chat.completions.create(
        model=llm.MODEL, messages=[{"role": "user", "content": prompt}],
        reasoning_effort="none", **SETTINGS)
    choice = r.choices[0]
    return (choice.message.content or "", choice.finish_reason,
            r.usage.completion_tokens, llm.MODEL)


def record():
    """Ask about every pair in both orders, one request at a time."""
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text("")
    for pair in pairs():
        for order in ORDERS:
            prompt = prompt_for(pair, order)
            began = datetime.now().astimezone().isoformat(timespec="seconds")
            reply, why, tokens, model = ask_once(prompt)
            row = {"id": pair["id"], "a": order[0], "b": order[1],
                   "prompt": prompt, "reply": reply, "finish_reason": why,
                   "completion_tokens": tokens, "model": model,
                   "settings": SETTINGS, "recorded_at": began}
            with open(OUT, "a", encoding="utf-8") as f:  # saved as we go
                f.write(json.dumps(row, ensure_ascii=False) + "\n")
            print(pair["id"], order[0], why, flush=True)


if __name__ == "__main__":
    if "--live" in sys.argv:
        record()
