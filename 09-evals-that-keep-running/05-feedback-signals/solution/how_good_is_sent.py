"""Lesson 09.5: how well does "sent unchanged" predict "fine"?

Given: the coded drafts, the simulated actions and the lines that print.
You write `precision_recall`.

From this folder: uv run python how_good_is_sent.py
All numbers come from the SIMULATED actions in data/feedback/actions.jsonl.
"""
from collections import Counter

from plumbing import actions, coded


def precision_recall(flagged, actual):
    """(precision, recall) of a set of flagged ids against the set that
    really has the property: the share of flags that are right, and the
    share of real cases that were flagged. None when there is nothing to
    divide by."""
    hit = len(flagged & actual)
    return (hit / len(flagged) if flagged else None,
            hit / len(actual) if actual else None)


if __name__ == "__main__":
    todo, done = coded(), actions()
    fine = {i for i, (_, ok) in todo.items() if ok}
    sent = {i for i, a in done.items() if a == "sent"}
    print("actions:", dict(Counter(done.values())))
    p, r = precision_recall(sent, fine)
    print(f"sent unchanged: {len(sent)} drafts; {len(sent & fine)} are fine")
    print(f"precision {p:.2f} (of sent, share fine); recall {r:.2f} "
          f"(of fine, share sent)")
    for weeks, name in (({1, 4}, "weeks 1 and 4"),
                        ({2, 3}, "sale weeks 2, 3")):
        s = {i for i in sent if todo[i][0] in weeks}
        f = {i for i in todo if todo[i][0] in weeks and todo[i][1]}
        p, r = precision_recall(s, f)
        print(f"{name}: {len(s)} sent, {len(s & f)} fine, precision {p:.2f}")
    changed = set(done) - sent
    p, r = precision_recall(changed, set(todo) - fine)
    print(f"edited or rewritten: {len(changed)} drafts; "
          f"precision {p:.2f} for 'has a failure', recall {r:.2f}")
