"""Offline tests: fakes stand in for the model and the embeddings. No network."""
import json
import sys
from pathlib import Path
from types import SimpleNamespace as NS

import numpy as np

from helpdesk import pipeline, refunds, search
from helpdesk.version import load

ROOT = Path(__file__).resolve().parents[2]
EMAIL = {"id": "E-0001", "subject": "Return bottle", "body": "I'd like to return my bottle."}


def test_versions_differ_only_where_intended():
    a, b = load("hd-1"), load("hd-2")
    assert a["k"] == 3 and a["filter_archived"] is False
    assert a["triage"] == b["triage"] and a["refunds"] == b["refunds"]
    assert a["draft"] != b["draft"] and "warm" in b["draft"]
    assert "language" not in a["draft"].lower()


def test_hd1_triage_prompt_leaks_four_test_emails():
    emails = {json.loads(l)["id"]: json.loads(l) for l in (ROOT / "data/emails/inbox.jsonl").read_text().splitlines()}
    used = [e for e in emails.values() if f"Subject: {e['subject']}\n\n{e['body']}" in load("hd-1")["triage"]]
    assert len(used) == 6 and sum(e["split"] == "test" for e in used) == 4


def test_parse_triage():
    ok = '{"category": "refund", "urgency": "low", "needs_human": true}'
    assert pipeline.parse_triage(ok) == ({"category": "refund", "urgency": "low", "needs_human": True}, None)
    assert pipeline.parse_triage("sorry, no")[1] == "reply is not JSON"
    assert "unknown category" in pipeline.parse_triage(ok.replace("refund", "billing"))[1]


def test_handle_returns_the_trace_record(monkeypatch):
    replies = iter(['{"category": "return", "urgency": "normal", "needs_human": false}',
                    "Hello! See [returns-policy] and [made-up-article]. Tidewater support"])
    monkeypatch.setattr(pipeline, "ask", lambda *a, **k: (next(replies), 10, 5))
    monkeypatch.setattr(pipeline, "search", lambda q, k, **kw: [
        {"article_id": "returns-policy", "text": "chunk", "score": 0.5}] * k)
    r = pipeline.handle(EMAIL, "hd-1", seed=3)
    assert r["triage"]["category"] == "return" and r["seed"] == 3 and r["temperature"] == 0
    assert len(r["retrieved"]) == 3 and r["citations"] == ["returns-policy"]
    assert (r["prompt_tokens"], r["completion_tokens"]) == (20, 10)


def test_chunks_and_search_without_a_model(monkeypatch):
    arts = [{"id": "a", "title": "A", "status": "current", "text": "intro\n\n## One\nx"},
            {"id": "b", "title": "B", "status": "archived", "text": "y"}]
    assert len(search.chunks(arts[0])) == 2
    monkeypatch.setattr(search, "_index", {"chunks": [c for a in arts for c in search.chunks(a)],
                                           "matrix": np.array([[1.0, 0], [0.6, 0.8], [0, 1.0]])})
    monkeypatch.setattr(search, "embed", lambda texts: [[0, 1.0]])
    assert search.search("q", k=1)[0]["article_id"] == "b"
    assert search.search("q", k=1, filter_archived=True)[0]["article_id"] == "a"


def test_policy_tool_reads_orders_db():
    o = refunds.get_order("TW-10193")
    assert o["status"] == "delivered" and o["items"][0]["price_inr"] == 2299
    assert refunds.check_policy("TW-10193", "return")["within_30_days"] is True
    assert "error" in refunds.get_order("TW-99999")
    assert "error" in refunds.call_tool("pay_everyone", "{}")


def test_refund_loop_records_the_trajectory(monkeypatch):
    call = NS(id="1", function=NS(name="get_order", arguments='{"order_id": "TW-10193"}'))
    steps = iter([NS(content=None, tool_calls=[call]),
                  NS(content='{"outcome": "approve_proposal", "refund_inr": 2299, "reply": "ok"}', tool_calls=None)])

    def fake_chat(messages, **kw):
        msg = next(steps)
        msg.model_dump = lambda **k: {"role": "assistant", "content": msg.content}
        return NS(choices=[NS(message=msg)], usage=NS(prompt_tokens=7, completion_tokens=3))
    monkeypatch.setattr(refunds, "chat", fake_chat)
    r = refunds.run({"id": "RF-01", "from_email": "x@example.com", "message": "refund TW-10193"})
    assert [t["tool"] for t in r["trajectory"]] == ["get_order"]
    assert (r["outcome"], r["refund_inr"], r["steps"], r["prompt_tokens"]) == ("approve_proposal", 2299, 2, 14)
