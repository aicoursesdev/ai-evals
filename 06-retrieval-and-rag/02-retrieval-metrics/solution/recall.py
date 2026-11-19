"""Lesson 06.2: the same numbers from scorecard.retrieval, and recall by
question kind.

From this folder: uv run python recall.py
"""
from collections import defaultdict

from scorecard import data
from scorecard import retrieval as r

runs = {x["id"]: x for x in data.run("06-retrieval")["hd-1"]}
asked = [q for q in data.questions() if q["answer_article"]]
pages = lambda q: [h["article_id"] for h in runs[q["id"]]["top10"]]
right = lambda q: {q["answer_article"]}

for k in (1, 3, 5, 10):
    rec = sum(r.recall_at_k(pages(q), right(q), k) for q in asked) / len(asked)
    print(f"k={k:2}  recall {rec:.3f}")
for k in (1, 3, 5, 10):
    pre = sum(r.precision_at_k(pages(q), right(q), k)
              for q in asked) / len(asked)
    print(f"k={k:2}  precision {pre:.3f}")
print("mrr", round(r.mrr([pages(q) for q in asked],
                         [right(q) for q in asked]), 3))

by_kind = defaultdict(list)
for q in asked:
    by_kind[q["kind"]].append(r.recall_at_k(pages(q), right(q), 3))
for kind, got in by_kind.items():
    print(f"{kind:11} recall@3 {sum(got):.0f}/{len(got)}")
missed = [q["id"] for q in asked if r.recall_at_k(pages(q), right(q), 3) == 0]
print("missed at k=3:", missed)
