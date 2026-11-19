"""Lesson 10.2: three ways to decide "send unread", measured on Meera's
goal and on its guard. A reader's call (labels/01-coded.csv) is the
reference: one reader's judgement, not the truth.

From this folder: uv run python gate_candidates.py
"""
from plumbing import open_drafts
from scorecard.stats import wilson

GATES = {
    "send everything": lambda d: True,
    "no check fires": lambda d: d["quiet"],
    "judge says PASS": lambda d: d["judged"],
    "both": lambda d: d["quiet"] and d["judged"],
}


def goal_and_guard(drafts, gate):
    """(sent unread, of those, wrong): the goal is how many of the sent
    drafts a reader would have called a failure; the guard is how many
    were sent at all."""
    sent = [d for d in drafts if gate(d)]
    return len(sent), sum(not d["fine"] for d in sent)


if __name__ == "__main__":
    drafts = open_drafts()
    print(f"{'gate':16} sent unread  wrong among them   95% range")
    for name, gate in GATES.items():
        sent, wrong = goal_and_guard(drafts, gate)
        low, high = wilson(wrong, sent)
        print(f"{name:16} {sent:4} of {len(drafts)}   {wrong:3} "
              f"({wrong / sent:5.1%})      {low:.1%} to {high:.1%}")
