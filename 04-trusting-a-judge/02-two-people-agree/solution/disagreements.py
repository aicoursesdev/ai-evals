"""Lesson 04.2: where the two disagree, in their own words."""
from collections import Counter

from plumbing import reasons, two_columns
from scorecard import data

ids, arjun, divya = two_columns()
print("calls (Arjun, Divya):", dict(Counter(zip(arjun, divya))))
a, d = reasons("arjun"), reasons("divya")
subject = {e["id"]: e["subject"] for w in (1, 2, 3, 4)
           for e in data.emails(w)}
for i in ("E-0433", "E-0505", "E-0287"):
    print(f"\n{i}  {subject[i]}")
    print(f"  Arjun, {a[i][0]}: {a[i][1]}")
    print(f"  Divya, {d[i][0]}: {d[i][1]}")
