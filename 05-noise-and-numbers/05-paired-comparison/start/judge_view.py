"""Lesson 05.5: the order-swap judge comparison, as a second view.

From this folder: uv run python judge_view.py
"""
import re
import statistics

from plumbing import drafts
from scorecard import data
from scorecard.stats import at_most, wilson

T1, T2 = drafts("hd-1"), drafts("hd-2")


def winner(row):
    """hd-1, hd-2 or tie: the last A, B or TIE line, turned back into a
    version."""
    last = re.findall(r"^\W*(A|B|TIE)\b", row["reply"], re.M | re.I)[-1]
    return "tie" if last.upper() == "TIE" else (
        row["a"] if last.upper() == "A" else row["b"])


by_email = {}
for row in data.run("03-pairwise")["pairs"]:
    by_email.setdefault(row["id"], []).append(winner(row))
both = [w[0] if w[0] == w[1] else "split" for w in by_email.values()]
won1, won2 = both.count("hd-1"), both.count("hd-2")
print(f"{len(by_email)} pairs: hd-1 won both orders {won1}, hd-2 {won2}, "
      f"split {both.count('split')}")
lo, hi = wilson(won1, won1 + won2)
print(f"hd-1 won {won1} of the {won1 + won2} that held both ways; "
      f"range for that share {lo:.0%} to {hi:.0%}")
p = min(1, 2 * at_most(min(won1, won2), won1 + won2, 0.5))
print("exact p-value, if each were a coin toss:", round(p, 4))
ids = sorted(T2)            # the 277 emails both versions answered
words = lambda t: len(t["draft"].split())
print("mean words, hd-1:", round(statistics.mean(words(T1[i]) for i in ids)),
      " hd-2:", round(statistics.mean(words(T2[i]) for i in ids)))
