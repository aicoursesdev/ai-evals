"""Lesson 06.2: score a ranked list of article ids against the right ones.

You write these four functions. The course's own versions are in
scorecard/retrieval.py: compare yours with them when the tests pass.
Check from the repo's top folder with: make check 06.2
"""


def recall_at_k(ranked, relevant, k):
    """Share of the right articles found in the top k.
    ['a', 'b', 'c'], right {'c'}, k=2 gives 0."""
    raise NotImplementedError(
        "TODO 06.2: count how many of the first k items of ranked are in "
        "relevant and divide by len(relevant), see the lesson's 'Recall, "
        "precision and rank, counted by hand' section")


def precision_at_k(ranked, relevant, k):
    """Share of the top k that are right."""
    raise NotImplementedError(
        "TODO 06.2: count how many of the first k items of ranked are in "
        "relevant and divide by k, see the lesson's 'Recall, precision "
        "and rank, counted by hand' section")


def reciprocal_rank(ranked, relevant):
    """1 / rank of the first right article (0 if none).
    ['a', 'b', 'c'], right {'b'} gives 0.5."""
    raise NotImplementedError(
        "TODO 06.2: find the first item of ranked that is in relevant and "
        "return 1 / its rank (counting from 1), or 0.0 if none is, see the "
        "lesson's 'Recall, precision and rank, counted by hand' section")


def mrr(rankings, relevants):
    """Mean reciprocal rank over many questions."""
    raise NotImplementedError(
        "TODO 06.2: the average of reciprocal_rank over every pair in "
        "rankings and relevants, see the lesson's 'Recall, precision and "
        "rank, counted by hand' section")
