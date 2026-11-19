"""Lesson 06.2: one question, by hand. Where is the right page in the
ranked list?

From this folder: uv run python one_question.py
"""
from scorecard import data

runs = {r["id"]: r for r in data.run("06-retrieval")["hd-1"]}
q = next(q for q in data.questions() if q["id"] == "Q-03")
ranked = [h["article_id"] for h in runs["Q-03"]["top10"]]

print(q["question"], "| right page:", q["answer_article"])
for rank, page in enumerate(ranked, start=1):
    mark = "  <- right" if page == q["answer_article"] else ""
    print(rank, page, mark)

first = ranked.index(q["answer_article"]) + 1
print("first right result at rank", first,
      "so reciprocal rank", round(1 / first, 2))
print("in the top 3?", q["answer_article"] in ranked[:3])
