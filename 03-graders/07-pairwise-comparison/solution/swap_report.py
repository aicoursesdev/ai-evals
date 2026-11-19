"""Lesson 03.7: what asking in both orders shows.

Given. From this folder: uv run python swap_report.py
"""
from collections import Counter

from pairwise import OUT, both_orders, holds_in_both, pairs, recorded, winner
from scorecard import data

rows = data.read_jsonl(OUT)
position = Counter()  # did the reply shown first win, or the second?
for r in rows:
    w = winner(r["reply"], (r["a"], r["b"]))
    if w is not None:
        place = "first" if w == r["a"] else "second"
        position["tie" if w == "tie" else place] += 1
print(len(rows), "requests; no verdict on",
      sum(winner(r["reply"], (r["a"], r["b"])) is None for r in rows))
print("who won by position:", dict(position))

saved = recorded()
won = {p["id"]: both_orders(p["id"], saved) for p in pairs()}
both, longer = Counter(), Counter()
for p in pairs():
    one, two = won[p["id"]]["hd-1"], won[p["id"]]["hd-2"]
    both[holds_in_both(one, two)] += 1
    longest = max(("hd-1", "hd-2"), key=lambda v: len(p[v].split()))
    longer["longer wins" if one == two == longest else "other"] += 1
print("both orders give:", dict(both))
print("the longer reply won both times on", longer["longer wins"], "pairs")

for shown_first in ("hd-1", "hd-2"):
    each = Counter(won[p["id"]][shown_first] for p in pairs())
    print(f"asked with {shown_first} first:", dict(each))
print("pairs where hd-1's reply is longer:",
      sum(len(p["hd-1"].split()) > len(p["hd-2"].split()) for p in pairs()))
