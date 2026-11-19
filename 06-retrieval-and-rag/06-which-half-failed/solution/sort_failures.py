"""Lesson 06.6: name the half that failed for every wrong answer, the five
questions with no answer included, and say whether the archived page was
used.

From this folder: uv run python sort_failures.py
"""
from scorecard import data

runs = {r["id"]: r for r in data.run("06-retrieval")["hd-1"]}
label = {r["id"]: r for r in data.labels("06-answers-arjun")}


def half_that_failed(q):
    top3 = [h["article_id"] for h in runs[q["id"]]["top10"][:3]]
    if not q["answer_article"]:
        return "no page can help: the reply should say it does not know"
    if q["answer_article"] not in top3:
        return "retrieval: the right page was not in the top 3"
    if "shipping-india-2024" in runs[q["id"]]["citations"]:
        return "retrieval: the archived page was fetched and cited"
    return "generation: the right page was there"


rows = [(q["id"], half_that_failed(q)) for q in data.questions()
        if label[q["id"]]["correct"] != "1"]
for qid, half in rows:
    print(qid, "|", half)
print(len(rows), "wrong answers;",
      sum(h.startswith("retrieval") for _, h in rows), "retrieval,",
      sum(h.startswith("generation") for _, h in rows), "generation,",
      sum(h.startswith("no page") for _, h in rows), "with nothing to find")
