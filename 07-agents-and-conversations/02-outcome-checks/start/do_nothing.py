"""Lesson 07.2: what agents that never read the order would score on the 30
scenarios. Each is a made-up trial per scenario, run through the checks the
lesson builds. Nothing here is a model: it is the floor a real agent must
beat.

From this folder: uv run python do_nothing.py
"""
from collections import Counter

from scorecard import agents
from trials import scenarios

scenarios = list(scenarios.values())
print("expected outcomes:", dict(Counter(s["expected"] for s in scenarios)))


def trial(outcome=None, amount=None):
    """A recorded-style trial: if a refund is stated, it is proposed too."""
    raise NotImplementedError(
        "TODO 07.2: return {'trajectory': calls, 'outcome': outcome, "
        "'refund_inr': amount}, where calls holds one propose_refund call "
        "with a 'proposed' result (amount, and 'Arjun' or 'Arjun and "
        "Meera' above 10000) when outcome is approve_proposal or "
        "escalate_to_meera, and is empty otherwise, see the lesson's "
        "'A do-nothing agent must fail' section")


AGENTS = {
    "does nothing": trial(),
    "always deny": trial("deny"),
    "always ask for info": trial("ask_for_info"),
    "always approve 2299": trial("approve_proposal", 2299),
    "always escalate 14499": trial("escalate_to_meera", 14499),
}
print(f"{'agent':24}{'state only':>12}{'says':>8}{'both':>8}")
for name, t in AGENTS.items():
    state = sum(agents.state_correct(t, s) for s in scenarios)
    says = sum(agents.outcome_correct(t, s) for s in scenarios)
    both = sum(agents.state_correct(t, s) and agents.outcome_correct(t, s)
               for s in scenarios)
    print(f"{name:24}{state:>9}/30{says:>5}/30{both:>5}/30")
