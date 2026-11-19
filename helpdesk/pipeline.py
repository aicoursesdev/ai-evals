"""One customer email through the help desk: triage, retrieve, draft.

handle(email) returns the trace record every later lesson reads.
"""
import json
import re
import time
from datetime import datetime

import openai

from helpdesk import llm
from helpdesk.llm import ask
from helpdesk.search import articles, search
from helpdesk.version import load

CATEGORIES = {"refund", "return", "shipping_delay", "order_change", "product_question",
              "warranty", "payment", "account", "complaint", "spam", "other"}
URGENCIES = {"low", "normal", "high"}


def email_text(email):
    """What the model reads: the subject (if any) and the body."""
    return f"Subject: {email['subject']}\n\n{email['body']}" if email["subject"] else email["body"]


def parse_triage(reply):
    """(labels, error): the three labels from the model's JSON, or why not."""
    try:
        match = re.search(r"\{.*\}", reply, re.S)
        got = json.loads(match.group(0))
        labels = {k: got.get(k) for k in ("category", "urgency", "needs_human")}
    except (AttributeError, ValueError, TypeError):
        return dict.fromkeys(("category", "urgency", "needs_human")), "reply is not JSON"
    if labels["category"] not in CATEGORIES:
        return labels, f"unknown category {labels['category']!r}"
    if labels["urgency"] not in URGENCIES:
        return labels, f"unknown urgency {labels['urgency']!r}"
    if not isinstance(labels["needs_human"], bool):
        return labels, f"needs_human is {labels['needs_human']!r}"
    return labels, None


def triage(email, version="hd-1", temperature=None, seed=None, model=None):
    """Step 1: three labels. Returns (record fields, prompt tokens, completion tokens)."""
    v = load(version)
    temperature = v["temperature"] if temperature is None else temperature
    reply, pt, ct = ask(
        [{"role": "system", "content": v["triage"]},
         {"role": "user", "content": email_text(email)}],
        model=model or v["model"], temperature=temperature, seed=seed,
        response_format={"type": "json_object"})
    labels, error = parse_triage(reply)
    out = {"triage": labels}
    if error:
        out |= {"triage_error": error, "triage_raw": reply}
    return out, pt, ct


def handle(email, version="hd-1", temperature=None, seed=None, model=None, extra_articles=()):
    """Triage, retrieve, draft. Returns the trace record for this email."""
    v = load(version)
    temperature = v["temperature"] if temperature is None else temperature
    model = model or v["model"]
    began = time.time()
    record = {"id": email["id"], "version": version, "model": model,
              "temperature": temperature, "seed": seed}
    tri, pt, ct = triage(email, version, temperature, seed, model)
    hits = search(email_text(email), k=v["k"], filter_archived=v["filter_archived"],
                  extra_articles=extra_articles)
    labels = tri["triage"]
    passages = "\n\n".join(f"[{h['article_id']}]\n{h['text']}" for h in hits)
    prompt = v["draft"].format(passages=passages, **{k: labels[k] for k in
                                                     ("category", "urgency", "needs_human")})
    try:
        draft, p2, c2 = ask([{"role": "system", "content": prompt},
                             {"role": "user", "content": email_text(email)}],
                            model=model, temperature=temperature, seed=seed)
    except openai.APITimeoutError:   # a reply that never ends: record it as no draft
        draft, p2, c2 = "", 0, 0
        record["error"] = (f"no draft: the reply did not end within the help desk's "
                           f"{llm.TIMEOUT:g}-second limit")
    known = {a["id"] for a in articles()} | {a["id"] for a in extra_articles}
    cited = [c for c in dict.fromkeys(re.findall(r"\[([a-z0-9-]+)\]", draft)) if c in known]
    return record | tri | {
        "retrieved": [{"article_id": h["article_id"], "chunk": h["text"], "score": h["score"]}
                      for h in hits],
        "draft": draft, "citations": cited,
        "prompt_tokens": pt + p2, "completion_tokens": ct + c2,
        "seconds": round(time.time() - began, 2),
        "recorded_at": datetime.now().astimezone().isoformat(timespec="seconds")}
