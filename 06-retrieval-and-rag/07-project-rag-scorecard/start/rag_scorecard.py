"""Lesson 06.7, project: the RAG scorecard for hd-1.

Retrieval and answers are scored apart, each rate has a range, and every
wrong answer names the half that failed. Writes rag_scorecard.md here.

From this folder: uv run python rag_scorecard.py
"""
from scorecard import data
from scorecard import retrieval as r
from scorecard.stats import wilson

ARCHIVED = "shipping-india-2024"
runs = {x["id"]: x for x in data.run("06-retrieval")["hd-1"]}
label = {x["id"]: x for x in data.labels("06-answers-arjun")}
qs = data.questions()
asked = [q for q in qs if q["answer_article"]]


def pages(q):
    """The article ids hd-1 retrieved for question q, best first."""
    return [h["article_id"] for h in runs[q["id"]]["top10"]]


def ok(qid, field):
    """Arjun's label for a question: field is 'correct' or 'grounded'."""
    return label[qid][field] == "1"


def rng(k, n):
    """k out of n as text with its 95% range: 46/60 = 77% (95% range ...)."""
    raise NotImplementedError(
        "TODO 06.7: the share k / n as a whole percent, then the "
        "Wilson range from scorecard.stats.wilson(k, n), as "
        "'46/60 = 77% (95% range 65% to 86%)', see the lesson's "
        "'Steps' section")


def faulty_half(q):
    """For a wrong answer: 'nothing to find', 'retrieval' or 'generation'.
    Retrieval means the right page was not in the top 3, or the archived
    page was in the top 3 and the draft cited it."""
    raise NotImplementedError(
        "TODO 06.7: return 'nothing to find' when q has no "
        "answer_article, 'retrieval' when the right page is not "
        "in the top 3 or the archived page is in the top 3 and "
        "the draft cites it, else 'generation', see the lesson's "
        "'Steps' section")


def finding_lines():
    """The finding half, on the 55 questions that have an answer."""
    raise NotImplementedError(
        "TODO 06.7: a heading line and bullet lines for recall at "
        "3 (use rng), the mean reciprocal rank and the archived "
        "page, as in the worked solution's page, see the lesson's "
        "'Steps' section")


def using_lines():
    """The using half, from Arjun's labels on all 60 answers."""
    raise NotImplementedError(
        "TODO 06.7: a heading line and bullet lines for answers "
        "correct and answers grounded (use rng) and the no-answer "
        "questions handled correctly, see the lesson's 'Steps' "
        "section")


def wrong_answer_lines():
    """One line per wrong answer: its id, the faulty half, Arjun's note."""
    raise NotImplementedError(
        "TODO 06.7: a heading line, then one bullet per wrong "
        "answer: its id, its faulty half in brackets and Arjun's "
        "note, see the lesson's 'Steps' section")


def main():
    lines = (["# RAG scorecard, hd-1, 60 questions", ""]
             + finding_lines() + [""] + using_lines() + [""]
             + wrong_answer_lines())
    with open("rag_scorecard.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
