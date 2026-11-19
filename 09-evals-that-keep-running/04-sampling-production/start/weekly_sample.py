"""Lesson 09.4: draw the week-4 sample and write its review sheet.

Given: the week's emails and traces, the sheet's layout and the lines that
print. You write `flags` and `draw`.

From this folder: uv run python weekly_sample.py
"""
import random

from plumbing import pool, sheet_entry
from scorecard.graders import CHECKS, promises_refund


def flags(email, trace):
    """Why a draft should be read: the names of the checks that fire, and
    'sure it needs no person, yet promises money' (a needs_human mismatch).
    Uses only what production has: the email and the trace, no label."""
    raise NotImplementedError(
        "TODO 09.4: return the names of the checks that fire and add "
        "needs_human mismatch where it applies, see the lesson's 'Two "
        "ways to choose what to read' section")


def draw(rows, seed=7):
    """(20 random ids, 5 flagged ids, how many were flagged outside the
    random 20) from {id: (email, trace)}; the same seed, the same draw."""
    raise NotImplementedError(
        "TODO 09.4: draw 20 random ids and 5 flagged ones with a seeded "
        "Random, see the lesson's 'Drawing the sample' section")


if __name__ == "__main__":
    rows = pool(4)
    random_ids, flag_ids, n_flagged = draw(rows)
    print(f"pool {len(rows)} emails; {n_flagged} flagged outside the "
          "random 20")
    print("random:", " ".join(sorted(random_ids)))
    print("flagged:", " ".join(sorted(flag_ids)))
    entries = [sheet_entry(*rows[i], "random") for i in sorted(random_ids)]
    entries += [sheet_entry(*rows[i], "flagged: " + ", ".join(flags(*rows[i])))
                for i in sorted(flag_ids)]
    open("review-sheet.md", "w").write("\n".join(entries))
    print("wrote review-sheet.md with", len(entries), "entries")
