"""Lesson 06.6: the right page fetched (in the top 3) against the answer
right (Arjun's label), for the 55 questions that have an answer.

From this folder: uv run python two_by_two.py
"""
from scorecard import data

runs = {r["id"]: r for r in data.run("06-retrieval")["hd-1"]}
label = {r["id"]: r for r in data.labels("06-answers-arjun")}
cells = {(True, True): [], (True, False): [],
         (False, True): [], (False, False): []}
for q in data.questions():
    if q["answer_article"]:
        raise NotImplementedError(
            "TODO 06.6: add q['id'] to the list in cells whose key is "
            "(is q['answer_article'] among the first 3 article_ids of "
            "runs[q['id']]['top10'], is label[q['id']]['correct'] == '1'), "
            "see the lesson's 'The two-by-two' section")

print("                     answer right   answer wrong")
for fetched in (True, False):
    row = [len(cells[(fetched, ok)]) for ok in (True, False)]
    print(f"right page {'fetched' if fetched else 'missing':8} "
          f"{row[0]:8} {row[1]:14}")
for cell in ((True, False), (False, False), (False, True)):
    print(cell, cells[cell])
