"""Build the failure map: types ranked, with counts, examples and decisions.

    uv run python failure_map.py coded.csv failure-types.md > failure-map.md
"""
import sys

from count import count, read
from plumbing import definitions

# What each type needs (lesson 01.6): fix, check or judge, in your words.
DECISION = {
    "F-overreach": "fix: no promises or actions in the prompt; "
                   "check: phrase list; judge for the rest",
    "F-wrong-rule": "fix: give the whole page; judge: draft against page",
    "F-bluff": "fix: say 'no page answers' and hand over; "
               "check: made-up pages and addresses; judge",
    "F-misread": "judge: draft against email",
    "F-spam-reply": "fix: no draft for spam; "
                    "check: triage label spam plus a draft",
    "F-asks-again": "fix: prompt; check: order ID already in the email; judge",
    "F-wrong-page": "fix: skip archived pages; check: page status",
    "F-off-topic": "judge (often a wrong-page problem)",
    "F-language": "fix: reply in the customer's language; "
                  "check: script; person for quality",
    "F-obeys-injection": "attack set in Module 08; check on the reply",
    "F-no-draft": "fix: a length limit that stops a runaway reply; "
                  "check: the draft is empty",
}


def map_lines(rows, defs, decision):
    """The failure map as lines of Markdown: a heading and a ranked table."""
    failed = sum(r["ok"] == "no" for r in rows)
    lines = [f"# Failure map: {len(rows)} traces read, {len(rows) - failed} "
             f"fine, {failed} with at least one failure", "",
             "| rank | type | traces | example | what it is | what it needs |",
             "| --- | --- | --- | --- | --- | --- |"]
    for rank, (name, n) in enumerate(count(rows).most_common(), start=1):
        text, example = defs[name]
        lines.append(f"| {rank} | {name} | {n} | {example} | {text} | "
                     f"{decision.get(name, 'decide: fix, check or judge')} |")
    return lines


if __name__ == "__main__":
    rows = read(sys.argv[1])
    print("\n".join(map_lines(rows, definitions(sys.argv[2]), DECISION)))
