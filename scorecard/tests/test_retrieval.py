import math
import pytest
from scorecard import retrieval as r

RANKED = ["a", "b", "c", "d", "e"]
RIGHT = {"b", "d"}


def test_by_hand():
    assert r.recall_at_k(RANKED, RIGHT, 2) == 0.5
    assert r.recall_at_k(RANKED, RIGHT, 4) == 1.0
    assert r.precision_at_k(RANKED, RIGHT, 4) == 0.5
    assert r.reciprocal_rank(RANKED, RIGHT) == 0.5
    assert r.reciprocal_rank(RANKED, {"z"}) == 0.0
    assert r.mrr([RANKED, ["b", "a"]], [RIGHT, {"b"}]) == 0.75
    # dcg = 1/log2(3) + 1/log2(5); best = 1 + 1/log2(3)
    d = 1 / math.log2(3) + 1 / math.log2(5)
    assert r.dcg(RANKED, RIGHT, 5) == pytest.approx(d)
    best = 1 + 1 / math.log2(3)
    assert r.ndcg(RANKED, RIGHT, 5) == pytest.approx(d / best)
    assert r.ndcg(["b", "d", "a"], RIGHT, 3) == pytest.approx(1.0)


def test_graded_gain():
    grades = {"a": 2, "b": 1}
    assert r.dcg(["a", "b"], grades, 2) == pytest.approx(2 + 1 / math.log2(3))
    assert r.dcg(["a", "b"], grades, 2, exponential=True) == pytest.approx(3 + 1 / math.log2(3))
    assert r.ndcg(["a", "b"], grades, 2) == pytest.approx(1.0)
    assert r.ndcg(["b", "a"], grades, 2) < 1.0
