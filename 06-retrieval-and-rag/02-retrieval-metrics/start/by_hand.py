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
        raise NotImplementedError(
            "TODO 06.2: add 1 to found when q['answer_article'] is in top, "
            "and add how many times it appears in top to right_slots, see "
            "the lesson's 'Recall, precision and rank, counted by hand' "
            "section")
    print(f"k={k:2}  recall {found}/{n} = {found / n:.3f}"
          f"   precision {right_slots}/{k * n} = {right_slots / (k * n):.3f}")

total = 0
for q in asked:
    pages = [h["article_id"] for h in runs[q["id"]]["top10"]]
    raise NotImplementedError(
        "TODO 06.2: when the right page is in pages, add 1 divided by its "
        "rank (counting from 1) to total, see the lesson's 'Recall, "
        "precision and rank, counted by hand' section")
print("mean reciprocal rank", round(total / n, 3))
