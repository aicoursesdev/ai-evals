"""Lesson 06.2: recall at k, precision at k and reciprocal rank over the 55
questions that have an answer, counted with plain loops.

From this folder: uv run python by_hand.py
"""
from scorecard import data

runs = {r["id"]: r for r in data.run("06-retrieval")["hd-1"]}
asked = [q for q in data.questions() if q["answer_article"]]
n = len(asked)
print(n, "questions with an answer page")

for k in (1, 3, 5, 10):
    found, right_slots = 0, 0
    for q in asked:
        top = [h["article_id"] for h in runs[q["id"]]["top10"][:k]]
        found += q["answer_article"] in top
        right_slots += top.count(q["answer_article"])
    print(f"k={k:2}  recall {found}/{n} = {found / n:.3f}"
          f"   precision {right_slots}/{k * n} = {right_slots / (k * n):.3f}")

total = 0
for q in asked:
    pages = [h["article_id"] for h in runs[q["id"]]["top10"]]
    if q["answer_article"] in pages:
        total += 1 / (pages.index(q["answer_article"]) + 1)
print("mean reciprocal rank", round(total / n, 3))
