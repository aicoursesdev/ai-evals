"""Lesson 06.6: name the half that failed for every wrong answer, the five
questions with no answer included, and say whether the archived page was
used.

From this folder: uv run python sort_failures.py
"""
from scorecard import data

runs = {r["id"]: r for r in data.run("06-retrieval")["hd-1"]}
label = {r["id"]: r for r in data.labels("06-answers-arjun")}


def half_that_failed(q):
    raise NotImplementedError(
        "TODO 06.6: return 'no page can help: ...' when q has no "
        "answer_article, 'retrieval: ...' when it is not among the first 3 "
        "pages of runs[q['id']]['top10'] or 'shipping-india-2024' is in "
        "that run's citations, else 'generation: the right page was "
        "there', see the lesson's 'Sorting every wrong answer' section")


rows = [(q["id"], half_that_failed(q)) for q in data.questions()
        if label[q["id"]]["correct"] != "1"]
for qid, half in rows:
    print(qid, "|", half)
print(len(rows), "wrong answers;",
      sum(h.startswith("retrieval") for _, h in rows), "retrieval,",
      sum(h.startswith("generation") for _, h in rows), "generation,",
      sum(h.startswith("no page") for _, h in rows), "with nothing to find")
