"""Project 09: draw a week's review sample and write its sheet.

Given: the week's emails and traces, the flags and the lines that print.
You write `draw` and `entries`.

From this folder: uv run python weekly.py 3     (a week from 1 to 4)
Twenty emails at random and five more that a signal flagged, seed 7.
"""
import random
import sys

from plumbing import flags, pool


def draw(rows, seed=7):
    """(20 random ids, up to 5 flagged ids from the rest, how many were
    flagged outside the random 20) from {id: (email, trace)}."""
    rng = random.Random(seed)
    chosen = rng.sample(sorted(rows), 20)
    flagged = [i for i in sorted(rows) if i not in chosen and flags(*rows[i])]
    return chosen, rng.sample(flagged, min(5, len(flagged))), len(flagged)


def entries(rows, chosen, extra):
    """The sheet's entries as Markdown: the random ones, then the flagged
    ones, each with its email, the draft and why it was picked."""
    parts = []
    for how, ids in (("random", chosen), ("flagged", extra)):
        for i in sorted(ids):
            email, trace = rows[i]
            why = how if how == "random" else "flagged: " + ", ".join(
                flags(email, trace))
            parts.append(f"## {i} ({why})\n\n**Subject:** {email['subject']}"
                         f"\n\n{email['body']}\n\n**Draft:**\n\n"
                         f"{trace['draft']}\n")
    return parts


if __name__ == "__main__":
    week = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    rows = pool(week)
    chosen, extra, n_flagged = draw(rows)
    print(f"week {week}: pool {len(rows)}, {n_flagged} flagged outside the 20")
    parts = entries(rows, chosen, extra)
    open(f"review-sheet-week-{week}.md", "w").write("\n".join(parts))
    print(f"wrote review-sheet-week-{week}.md with {len(parts)} entries")
