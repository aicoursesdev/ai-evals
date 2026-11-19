"""Lesson 03.9: a model judge for one criterion, "right rule".

By default the recorded replies in data/runs/03-judge/right-rule.jsonl
are replayed and no model is called. NEEDS A MODEL only with --live.
Given: the finished judge from lesson 03.6, with its read_verdict.

From this folder:
    uv run python judge_rule.py          replays the recording
    uv run python judge_rule.py --live   asks the local model, one request
                                         at a time, and re-records
"""
import json
import re
import sys
from datetime import datetime

from scorecard import data
from scorecard.graders import logged

PROMPT = """\
You check one thing about a reply that a shop's help desk drafted: does it \
apply the shop's rules correctly?

FAIL: a help-centre page below answers the customer's question, and the \
reply says something different from the page or applies it to the wrong \
case.
PASS: what the reply says about the shop's rules matches the pages, or it \
states no rule.
UNSURE: no page below answers the question, so the rule cannot be \
checked, or the reply is empty.
Judge only this. Ignore tone, length, spelling and every other mistake.

Examples (written for this prompt):
- Page: a prepaid order can be cancelled until it is packed. Reply: "Your \
order cannot be cancelled." Verdict: FAIL.
- Page: returns are accepted within 30 days of delivery. Reply: "You have \
30 days from delivery." Verdict: PASS.
- No page mentions restocking. Reply: "It will be back on 5 December." \
Verdict: UNSURE.

Customer email:
{email}

Help-centre pages the help desk was shown:
{pages}

Reply to check:
{draft}

First write at most three sentences: which rule the reply states, and what \
the pages say about it. Then write one last line holding only PASS, FAIL \
or UNSURE."""

OUT = data.DATA / "runs" / "03-judge" / "right-rule.jsonl"
SETTINGS = {"temperature": 0, "max_tokens": 1500}


def cases():
    """One case per coded draft: the email, the pages shown, the draft."""
    coded = data.labels("01-coded")
    keep = {row["id"] for row in coded}
    emails = {e["id"]: e for w in (1, 2, 3, 4)
              for e in logged("emails", w, keep=keep)}
    traces = {t["id"]: t for w in (1, 2, 3, 4)
              for t in logged("traces", w, keep=keep)}
    for row in coded:
        e, t = emails[row["id"]], traces[row["id"]]
        pages = "\n\n".join(f"[{r['article_id']}]\n{r['chunk']}"
                            for r in t["retrieved"])
        yield {"id": e["id"], "draft": t["draft"], "pages": pages,
               "email": f"Subject: {e['subject']}\n\n{e['body']}"}


def record():
    """Ask the model about every draft, one request at a time."""
    from helpdesk import llm
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text("")
    for case in cases():
        prompt = PROMPT.format(**case)
        began = datetime.now().astimezone()
        r = llm.client().with_options(timeout=180).chat.completions.create(
            model=llm.MODEL, messages=[{"role": "user", "content": prompt}],
            reasoning_effort="none", **SETTINGS)
        row = {"id": case["id"], "prompt": prompt,
               "reply": r.choices[0].message.content or "",
               "finish_reason": r.choices[0].finish_reason,
               "completion_tokens": r.usage.completion_tokens,
               "seconds": round((datetime.now().astimezone() - began)
                                .total_seconds(), 1),
               "model": llm.MODEL, "settings": SETTINGS,
               "recorded_at": began.isoformat(timespec="seconds")}
        with open(OUT, "a", encoding="utf-8") as f:  # saved as we go
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
        print(case["id"], row["finish_reason"], row["seconds"], flush=True)


def read_verdict(reply):
    """"pass", "fail", "unsure" or "none" (no verdict line) from a reply.

    The verdict is the last line that begins with PASS, FAIL or UNSURE,
    in any capitals and after any marks such as ** or a dash.
    """
    found = re.findall(r"^\W*(PASS|FAIL|UNSURE)\b", reply, re.M | re.I)
    return found[-1].lower() if found else "none"


def judged():
    """{id: "pass" | "fail" | "unsure" | "none"} from the recording."""
    saved = {r["id"]: r["reply"] for r in data.read_jsonl(OUT)}
    return {c["id"]: read_verdict(saved[c["id"]]) for c in cases()}


if __name__ == "__main__":
    if "--live" in sys.argv:
        record()
