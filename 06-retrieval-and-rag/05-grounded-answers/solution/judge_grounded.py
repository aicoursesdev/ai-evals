"""Lesson 06.5: a model judge for "did the reply stick to the chunks it was
shown?"

NEEDS A MODEL only with --live. By default the recorded replies in
runs/06-grounding/judge.jsonl are replayed and no model is called.

From this folder:
    uv run python judge_grounded.py          replays the recording
    uv run python judge_grounded.py --live   calls the local model and
                                             re-records (replies will differ)
"""
import json
import sys
from datetime import datetime

from helpdesk.llm import MODEL, ask
from scorecard import data
from scorecard.judge import rates, verdict

PROMPT = (
    "You check a customer-support reply against the help-centre text it "
    "was written from.\n\n"
    "Help-centre text:\n{passages}\n\n"
    "Customer question: {question}\n\n"
    "Reply to check:\n{reply}\n\n"
    "List each fact, number, condition or step the reply states (ignore "
    "greetings, sign-offs, offers to help and the [citation] tags).\n"
    "For each one write SUPPORTED if the help-centre text above says it, "
    "or UNSUPPORTED if it does not.\n"
    "Then write one final line: PASS if every item is SUPPORTED, FAIL if "
    "any is UNSUPPORTED.")

OUT = data.DATA / "runs" / "06-grounding" / "judge.jsonl"
SETTINGS = {"temperature": 0, "max_tokens": 8000}
grounded = {r["id"]: r["grounded"] == "1"
            for r in data.labels("06-answers-arjun")}


def cases():
    runs = {r["id"]: r for r in data.run("06-retrieval")["hd-1"]}
    chunks = {r["id"]: r["chunks"] for r in data.run("06-chunks")["hd-1"]}
    for q in data.questions():
        shown = "\n\n".join(c["text"] for c in chunks[q["id"]][:3])
        yield {"id": q["id"], "question": q["question"], "passages": shown,
               "reply": runs[q["id"]]["draft"]}


def record():
    """Ask the model about every reply and save what it says."""
    OUT.write_text("")
    for case in cases():
        prompt = PROMPT.format(**case)
        reply, *_ = ask([{"role": "user", "content": prompt}], **SETTINGS)
        row = {"id": case["id"], "prompt": prompt, "reply": reply,
               "model": MODEL, "settings": SETTINGS,
               "recorded_at": datetime.now().astimezone().isoformat(
                   timespec="seconds")}
        with open(OUT, "a", encoding="utf-8") as f:  # saved as we go
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
        print(case["id"], flush=True)


def report():
    saved = {r["id"]: r["reply"] for r in data.read_jsonl(OUT)}
    passed, no_verdict = {}, []
    for c in cases():
        try:
            passed[c["id"]] = verdict(PROMPT, c, None, replay=saved)
        except ValueError:  # the reply has no PASS or FAIL line
            passed[c["id"]] = False
            no_verdict.append(c["id"])
    tpr, tnr = rates([grounded[i] for i in passed], list(passed.values()))
    print("judge says grounded:", sum(passed.values()), "of", len(passed),
          "| Arjun:", sum(grounded.values()))
    print("replies with no verdict line (counted as FAIL):", no_verdict)
    print(f"of Arjun's grounded answers the judge passes {tpr:.0%}; "
          f"of his ungrounded it fails {tnr:.0%}")
    kept = [i for i in passed if i not in no_verdict]
    tpr, tnr = rates([grounded[i] for i in kept], [passed[i] for i in kept])
    print(f"only the {len(kept)} replies with a verdict: passes {tpr:.0%} "
          f"of grounded, fails {tnr:.0%} of ungrounded")


if __name__ == "__main__":
    if "--live" in sys.argv:
        record()
    report()
