"""Lesson 06.3: nDCG@3 for Q-12 by hand, then with scorecard.retrieval.

From this folder: uv run python one_ranking.py
"""
import math

from graded import grades, ranked_ids
from scorecard import data
from scorecard import retrieval as r


def dcg(items, grade):
    raise NotImplementedError(
        "TODO 06.3: add up grade.get(item, 0) / math.log2(rank + 1) over "
        "items, with rank counting from 1, see the lesson's "
        "'Two forms, one name' section")


q = next(q for q in data.questions() if q["id"] == "Q-12")
record = next(x for x in data.run("06-chunks")["hd-1"] if x["id"] == "Q-12")
grade, ranked = grades(q), ranked_ids(record)[:3]
print(q["question"])
for rank, item in enumerate(ranked, start=1):
    print(rank, item, "grade", grade.get(item, 0))
ideal = sorted(grade, key=grade.get, reverse=True)[:3]
print("ideal order:", ideal)
got, best = dcg(ranked, grade), dcg(ideal, grade)
print(f"DCG {got:.3f}  ideal DCG {best:.3f}  nDCG {got / best:.3f}")
print("scorecard, original gain:   ", round(r.ndcg(ranked, grade, 3), 3))
print("scorecard, exponential gain:",
      round(r.ndcg(ranked, grade, 3, exponential=True), 3))
