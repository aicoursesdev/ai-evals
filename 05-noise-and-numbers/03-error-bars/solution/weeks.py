"""Lesson 05.3: the help desk's category score, week by week, with ranges.

From this folder: uv run python weeks.py
"""
from plumbing import category_right, drafts, emails
from scorecard.stats import wilson

E, T = emails(), drafts("hd-1")
print("week  emails  right   rate    Wilson range")
for week in (1, 2, 3, 4):
    ids = [i for i in E if E[i]["week"] == week]
    right = sum(category_right(E[i], T[i]) for i in ids)
    low, high = wilson(right, len(ids))
    print(f"{week:>4} {len(ids):>7} {right:>6} {right / len(ids):>6.1%}"
          f"   {low:.1%} to {high:.1%}")
