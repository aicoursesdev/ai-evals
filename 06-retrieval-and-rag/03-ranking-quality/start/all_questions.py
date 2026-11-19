"""Lesson 06.3: mean nDCG@3 over the 55 questions in both gain forms, and
the questions that score lowest.

From this folder: uv run python all_questions.py
"""
from graded import grades, ranked_ids
from scorecard import data
from scorecard import retrieval as r

records = {x["id"]: x for x in data.run("06-chunks")["hd-1"]}
asked = [q for q in data.questions() if q["answer_article"]]
scores = {}
for q in asked:
    ranked, grade = ranked_ids(records[q["id"]]), grades(q)
    scores[q["id"]] = (r.ndcg(ranked, grade, 3),
                       r.ndcg(ranked, grade, 3, exponential=True))
for n, name in enumerate(("original gain", "exponential gain")):
    mean = sum(s[n] for s in scores.values()) / len(scores)
    print(f"mean nDCG@3, {name}: {mean:.3f}")
perfect = sum(s[0] > 0.9999 for s in scores.values())
print("perfect (1.0):", perfect, "of", len(scores))
low = sorted(scores, key=lambda i: scores[i][0])[:5]
print("lowest five:", [(i, round(scores[i][0], 2)) for i in low])
