"""Lesson 04.2: high agreement, low kappa. The 94-2-2-2 table is made up."""
from plumbing import two_columns
from scorecard.judge import agreement, kappa

# Made up for the illustration: 94 both pass, 2 both fail, 2 only the
# first passes, 2 only the second passes.
a = ["pass"] * 94 + ["fail"] * 2 + ["pass"] * 2 + ["fail"] * 2
d = ["pass"] * 94 + ["fail"] * 2 + ["fail"] * 2 + ["pass"] * 2
print(f"made up: agree {agreement(a, d):.2f}, kappa {kappa(a, d):.3f}")

# Real: a labeller who says pass to everything, against Arjun's 85 calls.
ids, arjun, divya = two_columns()
rows = [x for x in arjun if x != "unsure"]
always = ["pass"] * len(rows)
print(f"always pass vs Arjun: agree {agreement(rows, always):.2f}, "
      f"kappa {kappa(rows, always):.3f}, on {len(rows)} drafts")
