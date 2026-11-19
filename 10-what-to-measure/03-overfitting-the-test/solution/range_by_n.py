"""Lesson 10.3: how wide a range a score has, by the number of emails.

From this folder: uv run python range_by_n.py
"""
from scorecard.stats import sample_size, wilson

def range_row(n, share=0.9):
    """(low, high, points wide) of the 95% range of a score of `share` on
    `n` emails."""
    low, high = wilson(round(share * n), n)
    return low, high, (high - low) * 100


if __name__ == "__main__":
    print("a score of 90%, by the emails behind it")
    for n in (20, 50, 100, 400):
        low, high, width = range_row(n)
        print(f"{n:4} emails: {low:.1%} to {high:.1%}  "
              f"({width:.0f} points wide)")
    print("emails for a range of plus or minus 5 points:", sample_size(0.05))
