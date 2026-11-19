"""Score a ranked list of article ids against the ids that are right."""
import math


def recall_at_k(ranked, relevant, k):
    """Share of the right articles found in the top k.
    ['a','b','c'], right {'c'}, k=2 gives 0."""
    return len(set(ranked[:k]) & set(relevant)) / len(relevant)


def precision_at_k(ranked, relevant, k):
    """Share of the top k that are right."""
    return len([r for r in ranked[:k] if r in relevant]) / k


def reciprocal_rank(ranked, relevant):
    """1 / rank of the first right article (0 if none).
    ['a','b','c'], right {'b'} gives 0.5."""
    for rank, item in enumerate(ranked, start=1):
        if item in relevant:
            return 1 / rank
    return 0.0


def mrr(rankings, relevants):
    """Mean reciprocal rank over many questions."""
    scores = [reciprocal_rank(r, rel) for r, rel in zip(rankings, relevants)]
    return sum(scores) / len(scores)


def dcg(ranked, relevant, k, exponential=False):
    """Discounted gain: an item at rank r adds gain / log2(r + 1).
    relevant is a set (grade 1 each) or a dict of item to grade. The
    gain is the grade (original form) or 2**grade - 1 (exponential
    form); they agree for grades 0 and 1. Rank 2 is discounted to 0.631."""
    grade = relevant if isinstance(relevant, dict) else dict.fromkeys(relevant, 1)
    gain = (lambda g: 2 ** g - 1) if exponential else (lambda g: g)
    return sum(gain(grade.get(item, 0)) / math.log2(rank + 1)
               for rank, item in enumerate(ranked[:k], start=1))


def ndcg(ranked, relevant, k, exponential=False):
    """dcg divided by the best dcg possible (best grades first), so 1.0
    is a perfect order. Say which gain form you used."""
    grade = relevant if isinstance(relevant, dict) else dict.fromkeys(relevant, 1)
    best = dcg(sorted(grade, key=grade.get, reverse=True), grade, k, exponential)
    return dcg(ranked, grade, k, exponential) / best
