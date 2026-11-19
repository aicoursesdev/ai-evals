"""Lesson 07.2: two outcome checks on the 30 recorded runs at temperature 0,
by hand: what the agent says it did, and what it left behind.

From this folder: uv run python outcome_by_hand.py
"""
from trials import load, scenarios

runs = load(0)


def proposals(run):
    """Refunds waiting for a person, read from the tool results."""
    return [c["result"] for c in run["trajectory"]
            if c["tool"] == "propose_refund"
            and c["result"].get("status") == "proposed"]


def said_right(run, s):
    """The final answer names the right outcome (and amount, if any)."""
    if run["outcome"] != s["expected"]:
        return False
    return s["refund_inr"] is None or run["refund_inr"] == s["refund_inr"]


def left_right(run, s):
    """The world at the end: no proposal for deny and ask; otherwise
    proposals with the right amount, waiting for the right people."""
    left = proposals(run)
    if s["expected"] in ("deny", "ask_for_info"):
        return not left
    who = ("Arjun" if s["expected"] == "approve_proposal"
           else "Arjun and Meera")
    return bool(left) and all(p["amount_inr"] == s["refund_inr"]
                              and p["waiting_for"] == who for p in left)


said = sum(said_right(r, scenarios[r["id"]]) for r in runs)
left = sum(left_right(r, scenarios[r["id"]]) for r in runs)
both = sum(said_right(r, scenarios[r["id"]])
           and left_right(r, scenarios[r["id"]]) for r in runs)
print(f"said the right outcome  {said}/30")
print(f"left the right state    {left}/30")
print(f"both                    {both}/30")
for r in runs:
    s = scenarios[r["id"]]
    if left_right(r, s) and not said_right(r, s):
        print(r["id"], "expected", s["expected"], "| state fine, said",
              r["outcome"], "| steps", r["steps"], "|", r["stop"])
