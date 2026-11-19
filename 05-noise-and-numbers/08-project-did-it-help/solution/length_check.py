"""Lesson 05.8: do longer drafts set off the checks more? (hd-1 only)

From this folder: uv run python length_check.py
"""
from plumbing import clean, drafts, emails

E, T1 = emails(), drafts("hd-1")
ids = sorted(i for i in T1 if T1[i]["draft"].strip())
words = {i: len(T1[i]["draft"].split()) for i in ids}
print("hd-1 drafts by length   drafts  with a check firing")
for low, high in ((0, 60), (60, 80), (80, 100), (100, 1000)):
    part = [i for i in ids if low <= words[i] < high]
    fired = sum(1 - clean(E[i], T1[i]) for i in part)
    print(f"{low:>4} to {high:<4} words   {len(part):>6}  {fired:>6} "
          f"({fired / len(part):.0%})")
