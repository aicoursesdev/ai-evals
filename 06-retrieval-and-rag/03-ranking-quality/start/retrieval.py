"""Lesson 06.3: discounted gain and nDCG for a ranked list of chunk ids.

You write these two functions. The course's own versions are in
scorecard/retrieval.py: compare yours with them when the tests pass.
Check from the repo's top folder with: make check 06.3
"""


def dcg(ranked, relevant, k, exponential=False):
    """Discounted gain: an item at rank r adds gain / log2(r + 1).
    relevant is a set (grade 1 each) or a dict of item to grade. The gain
    is the grade (original form) or 2**grade - 1 (exponential form)."""
    raise NotImplementedError(
        "TODO 06.3: turn a set into a dict of grade 1 each; for the first "
        "k items of ranked (rank counting from 1) add gain(grade) / "
        "math.log2(rank + 1), where gain is the grade, or 2**grade - 1 "
        "when exponential, see the lesson's 'Two forms, one name' section")


def ndcg(ranked, relevant, k, exponential=False):
    """dcg divided by the best dcg possible (best grades first), so 1.0 is a
    perfect order. Say which gain form you used."""
    raise NotImplementedError(
        "TODO 06.3: divide dcg of ranked by dcg of the items sorted by "
        "grade, best first (the ideal order), see the lesson's "
        "'Two forms, one name' section")
