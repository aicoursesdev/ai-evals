"""The refund agent: a capped tool loop over orders.db.

The model may look up an order, check the policy on it and propose a refund
for a person to approve. run(scenario) returns what it did: every tool call
with its arguments and result, and the outcome it finally gave.
"""
import csv
import json
import re
import sqlite3
import time
from datetime import date, datetime
from pathlib import Path

from helpdesk.llm import chat
from helpdesk.version import load

DB = Path(__file__).resolve().parent.parent / "data" / "orders.db"
TODAY = date(2026, 10, 19)   # the snapshot's Monday
NOW = datetime(2026, 10, 19, 9, 0)
OUTCOMES = {"approve_proposal", "deny", "escalate_to_meera", "ask_for_info"}

TOOLS = [{"type": "function", "function": {
    "name": name, "description": text,
    "parameters": {"type": "object", "properties": props, "required": list(props)}}}
    for name, text, props in [
    ("get_order", "Look up an order: status, customer email, payment, items, returns.",
     {"order_id": {"type": "string"}}),
    ("check_policy", "Check the return policy on an order. claim is return, damaged_or_wrong or cancel.",
     {"order_id": {"type": "string"}, "claim": {"type": "string"}}),
    ("propose_refund", "Propose a refund for a person to approve. Pays nothing.",
     {"order_id": {"type": "string"}, "amount_inr": {"type": "integer"},
      "reason": {"type": "string"}})]]


def _db():
    return sqlite3.connect(f"file:{DB}?mode=ro", uri=True, check_same_thread=False)


def products():
    """sku -> name and category, from the catalogue."""
    with open(DB.parent / "catalogue.csv", encoding="utf-8", newline="") as f:
        return {r["sku"]: r for r in csv.DictReader(f)}


def get_order(order_id):
    db = _db()
    o = db.execute("SELECT o.id, o.status, c.email, o.payment_method, o.shipping_method, "
                   "o.total_inr, o.placed_at, o.delivered_at FROM orders o JOIN customers c "
                   "ON c.id = o.customer_id WHERE o.id = ?", (order_id,)).fetchone()
    if o is None:
        return {"error": f"no order {order_id}"}
    keys = ["order_id", "status", "customer_email", "paid_by", "shipping", "total_inr",
            "placed_at", "delivered_at"]
    p = products()
    items = [{"name": p[s]["name"], "category": p[s]["category"], "qty": q, "price_inr": pr}
             for s, q, pr in db.execute("SELECT sku, qty, price_inr FROM order_items "
                                        "WHERE order_id = ?", (order_id,))]
    returns = [{"item": p[s]["name"], "status": st} for s, st in db.execute(
        "SELECT sku, status FROM returns WHERE order_id = ?", (order_id,))]
    return dict(zip(keys, o)) | {"items": items, "returns": returns}


def check_policy(order_id, claim):
    """The rules of the policy applied to an order, as facts the model must read."""
    o = get_order(order_id)
    if "error" in o:
        return o
    out = {"order_id": order_id, "claim": claim, "status": o["status"]}
    if o["delivered_at"]:
        delivered = datetime.fromisoformat(o["delivered_at"][:19])
        out["days_since_delivery"] = (TODAY - delivered.date()).days
        out["hours_since_delivery"] = round((NOW - delivered).total_seconds() / 3600)
        out["within_30_days"] = out["days_since_delivery"] <= 30
        out["within_48_hours"] = out["hours_since_delivery"] <= 48
    out["not_returnable_items"] = [i["name"] for i in o["items"]
                                   if i["category"] == "gift-card" or "name patch" in i["name"].lower()]
    out["already_refunded"] = any(r["status"] == "refunded" for r in o["returns"])
    out["can_cancel"] = o["status"] == "placed"
    return out


def propose_refund(order_id, amount_inr, reason):
    return {"status": "proposed", "order_id": order_id, "amount_inr": amount_inr,
            "waiting_for": "Arjun" if amount_inr <= 10000 else "Arjun and Meera"}


RUNNERS = {"get_order": get_order, "check_policy": check_policy, "propose_refund": propose_refund}


def call_tool(name, arguments):
    """Run one tool; a bad call becomes an error message for the model."""
    if name not in RUNNERS:
        return {"error": f"no tool named {name}; the tools are {', '.join(RUNNERS)}"}
    try:
        return RUNNERS[name](**json.loads(arguments))
    except Exception as e:  # noqa: BLE001 - the model should read its own mistake
        return {"error": f"{name} failed: {e}"}


def run(scenario, version="hd-1", temperature=None, seed=None, model=None):
    """One scenario (id, from_email, message) through the agent. Returns the record."""
    v = load(version)
    temperature = v["temperature"] if temperature is None else temperature
    model = model or v["model"]
    messages = [{"role": "system", "content": v["refunds"]},
                {"role": "user", "content": f"From: {scenario['from_email']}\n\n{scenario['message']}"}]
    began, pt, ct, trajectory, final, steps = time.time(), 0, 0, [], None, 0
    for step in range(1, v["max_steps"] + 1):
        steps += 1
        r = chat(messages, model=model, temperature=temperature, seed=seed, tools=TOOLS)
        pt, ct = pt + r.usage.prompt_tokens, ct + r.usage.completion_tokens
        msg = r.choices[0].message
        messages.append(msg.model_dump(exclude_none=True))
        if not msg.tool_calls:
            final = msg.content or ""
            break
        for c in msg.tool_calls:
            result = call_tool(c.function.name, c.function.arguments)
            trajectory.append({"step": step, "tool": c.function.name,
                               "arguments": c.function.arguments, "result": result})
            messages.append({"role": "tool", "tool_call_id": c.id,
                             "content": json.dumps(result, ensure_ascii=False)})
    outcome, refund, reply = parse_final(final)
    return {"id": scenario["id"], "version": version, "model": model,
            "temperature": temperature, "seed": seed, "trajectory": trajectory,
            "stop": "answered" if final is not None else "step cap",
            "outcome": outcome, "refund_inr": refund, "reply": reply, "final_raw": final,
            "steps": steps,
            "prompt_tokens": pt, "completion_tokens": ct,
            "seconds": round(time.time() - began, 2),
            "recorded_at": datetime.now().astimezone().isoformat(timespec="seconds")}


def parse_final(text):
    """(outcome, refund_inr, reply) from the model's final JSON; outcome None if it is not one."""
    try:
        got = json.loads(re.search(r"\{.*\}", text or "", re.S).group(0))
    except (AttributeError, ValueError):
        return None, None, text
    outcome = got.get("outcome") if got.get("outcome") in OUTCOMES else None
    return outcome, got.get("refund_inr"), got.get("reply")
