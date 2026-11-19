"""Lesson 07.2: two outcome checks on the 30 recorded runs at temperature 0,
by hand: what the agent says it did, and what it left behind.

From this folder: uv run python outcome_by_hand.py
"""
from trials import load, scenarios

runs = load(0)


def proposals(run):
    """Refunds waiting for a person, read from the tool results."""
    raise NotImplementedError(
        "TODO 07.2: return the c['result'] of each call c in "
        "run['trajectory'] whose tool is 'propose_refund' and whose result "
        "status is 'proposed', see the lesson's 'What the agent leaves "
        "behind' section")


def said_right(run, s):
    """The final answer names the right outcome (and amount, if any)."""
    raise NotImplementedError(
        "TODO 07.2: False unless run['outcome'] equals s['expected']; "
        "then True when s['refund_inr'] is None, else compare it with "
        "run['refund_inr'], see the lesson's 'What the agent leaves "
        "behind' section")


def left_right(run, s):
    """The world at the end: no proposal for deny and ask; otherwise
    proposals with the right amount, waiting for the right people."""
    raise NotImplementedError(
        "TODO 07.2: for deny and ask_for_info return not proposals(run); "
        "otherwise True only when there is a proposal and every one has "
        "amount_inr equal to s['refund_inr'] and waiting_for 'Arjun' "
        "(approve) or 'Arjun and Meera' (escalate), see the lesson's "
        "'What the agent leaves behind' section")


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
