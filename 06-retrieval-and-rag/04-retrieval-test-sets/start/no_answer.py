"""Lesson 06.4: the five questions with no answer. The search still returns
chunks for them, with scores that look like the scores of real answers.

From this folder: uv run python no_answer.py
"""
from scorecard import data

runs = {r["id"]: r for r in data.run("06-retrieval")["hd-1"]}
asked = [q for q in data.questions() if q["answer_article"]]
none = [q for q in data.questions() if not q["answer_article"]]
top = lambda q: runs[q["id"]]["top10"][0]["score"]
print("best score, questions with an answer: lowest",
      min(top(q) for q in asked), "highest", max(top(q) for q in asked))
for q in none:
    print(q["id"], top(q), runs[q["id"]]["top10"][0]["article_id"],
          "|", q["question"])

# a cut-off to abstain below would also silence real answers
raise NotImplementedError(
    "TODO 06.4: set cut to the highest best-score among the questions in "
    "none, and low to the ids of the answerable questions whose best-score "
    "is at or below it, see the lesson's 'Questions with no answer' "
    "section")
print(f"a cut-off at {cut} would silence {len(low)} of {len(asked)} "
      f"answerable questions:", low)
