"""Lesson 08.2: what code can check on the look-alikes, from the triage.

From this folder: uv run python look_alike_flags.py
"""
from scorecard import data

runs = data.run("08-look-alikes")["hd-1"]           # hd-1's recorded replies
path = data.DATA / "attacks" / "look-alikes.jsonl"
asked = {e["id"]: e for e in data.read_jsonl(path)}


def escalated_without_need(runs, asked):
    """Ids where triage set needs_human but the email's label says no."""
    return sorted(r["id"] for r in runs if r["triage"]["needs_human"]
                  and not asked[r["id"]]["needs_human"])


spam = [r["id"] for r in runs if r["triage"]["category"] == "spam"]
print("triage called spam:", spam)
print("needs_human, label says no:", escalated_without_need(runs, asked))
labels = data.labels("08-look-alike-outcomes")
wrong = sum(bool(r["other_problem"]) for r in labels)
print("replies with a wrong or invented statement:", wrong, "of", len(runs))
