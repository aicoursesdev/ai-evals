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
    low, high = wilson(k, n)
    return f"{k}/{n} = {k / n:.0%} (95% range {low:.0%} to {high:.0%})"


def faulty_half(q):
    """For a wrong answer: 'nothing to find', 'retrieval' or 'generation'.
    Retrieval means the right page was not in the top 3, or the archived
    page was in the top 3 and the draft cited it."""
    top3 = pages(q)[:3]
    if not q["answer_article"]:
        return "nothing to find"
    if q["answer_article"] not in top3:
        return "retrieval"
    if ARCHIVED in top3 and ARCHIVED in runs[q["id"]]["citations"]:
        return "retrieval"
    return "generation"


def finding_lines():
    """The finding half, on the 55 questions that have an answer."""
    hit = sum(r.recall_at_k(pages(q), {q["answer_article"]}, 3)
              for q in asked)
    mrr = r.mrr([pages(q) for q in asked],
                [{q["answer_article"]} for q in asked])
    old = [q["id"] for q in qs if ARCHIVED in pages(q)[:3]]
    cited = [i for i in old if ARCHIVED in runs[i]["citations"]]
    wrong = [i for i in cited if not ok(i, "correct")]
    return [
        "## Finding the page (55 questions with an answer)",
        f"- right page in the top 3: {rng(int(hit), len(asked))}",
        f"- mean reciprocal rank: {mrr:.3f}",
        f"- archived page in the top 3: {len(old)} questions "
        f"({', '.join(old)}); cited in {len(cited)}, wrong because of it "
        f"in {len(wrong)}"]


def using_lines():
    """The using half, from Arjun's labels on all 60 answers."""
    correct = sum(ok(q["id"], "correct") for q in qs)
    grounded = sum(ok(q["id"], "grounded") for q in qs)
    none = [q for q in qs if not q["answer_article"]]
    handled = sum(ok(q["id"], "correct") for q in none)
    return [
        "## Using the page (all 60, Arjun's labels)",
        f"- answer correct: {rng(correct, len(qs))}",
        f"- answer grounded in the chunks shown: {rng(grounded, len(qs))}",
        f"- questions with no answer handled correctly: "
        f"{handled}/{len(none)}"]


def wrong_answer_lines():
    """One line per wrong answer: its id, the faulty half, Arjun's note."""
    return ["## Wrong answers and the half that failed"] + [
        f"- {q['id']} ({faulty_half(q)}): {label[q['id']]['note']}"
        for q in qs if not ok(q["id"], "correct")]


def main():
    lines = (["# RAG scorecard, hd-1, 60 questions", ""]
             + finding_lines() + [""] + using_lines() + [""]
             + wrong_answer_lines())
    with open("rag_scorecard.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
