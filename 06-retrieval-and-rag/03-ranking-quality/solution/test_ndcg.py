"""Lesson 06.3: discounted gain and nDCG, by hand and in your functions.

No model and no network: the tests read the recorded chunks in the repo.
From the top folder: make check 06.3
"""
import math
import runpy
from pathlib import Path

import pytest

from graded import grades, ranked_ids
from retrieval import dcg, ndcg
from scorecard import data

HERE = Path(__file__).parent


def printed(name, capsys):
    """What a script in this folder prints, one string per line."""
    runpy.run_path(str(HERE / name), run_name="__main__")
    return [line.rstrip() for line in capsys.readouterr().out.splitlines()]


@pytest.fixture(scope="module")
def q12():
    q = next(q for q in data.questions() if q["id"] == "Q-12")
    records = data.run("06-chunks")["hd-1"]
    record = next(x for x in records if x["id"] == "Q-12")
    return grades(q), ranked_ids(record)[:3]


def test_a_chunk_keeps_1_then_0_631_then_0_5_of_its_credit_by_rank():
    assert dcg(["a"], {"a"}, 3) == 1
    assert dcg(["x", "a"], {"a"}, 3) == pytest.approx(1 / math.log2(3))
    assert round(dcg(["x", "a"], {"a"}, 3), 3) == 0.631
    assert dcg(["x", "y", "a"], {"a"}, 3) == 0.5


def test_the_answer_chunk_first_scores_ndcg_1_and_third_scores_0_5():
    assert ndcg(["a", "x", "y"], {"a"}, 3) == 1
    assert ndcg(["x", "y", "a"], {"a"}, 3) == 0.5


def test_dcg_counts_only_the_first_k_chunks():
    assert dcg(["x", "y", "a"], {"a"}, 2) == 0


def test_the_two_gain_forms_agree_for_grades_0_and_1_and_differ_for_2():
    ones = {"a": 1, "b": 1}
    assert ndcg(["b", "x", "a"], ones, 3) == pytest.approx(
        ndcg(["b", "x", "a"], ones, 3, exponential=True))
    graded = {"a": 2, "b": 1}
    assert dcg(["a"], graded, 1) == 2
    assert dcg(["a"], graded, 1, exponential=True) == 3


def test_nothing_useful_in_the_list_gives_ndcg_0():
    assert ndcg(["x", "y", "z"], {"a": 2}, 3) == 0


def test_the_grades_for_q_12_are_2_for_the_answer_chunk_and_1_for_the_rest(
        q12):
    grade, _ = q12
    assert grade["cod-refunds#(intro)"] == 2
    assert sorted(grade.values(), reverse=True)[:3] == [2, 1, 1]


def test_q_12_s_first_three_chunks_earn_dcg_0_5_against_an_ideal_3_131(q12):
    grade, ranked = q12
    assert [grade.get(item, 0) for item in ranked] == [0, 0, 1]
    assert dcg(ranked, grade, 3) == pytest.approx(0.5)
    ideal = sorted(grade, key=grade.get, reverse=True)
    assert round(dcg(ideal, grade, 3), 3) == 3.131
    assert round(dcg(ideal, grade, 3, exponential=True), 3) == 4.131


def test_q_12_scores_ndcg_0_160_with_original_gain_and_0_121_with_exponential(
        q12):
    grade, ranked = q12
    assert round(ndcg(ranked, grade, 3), 3) == 0.160
    assert round(ndcg(ranked, grade, 3, exponential=True), 3) == 0.121


def test_over_the_55_questions_mean_ndcg_at_3_is_0_726_and_14_are_perfect():
    records = {x["id"]: x for x in data.run("06-chunks")["hd-1"]}
    asked = [q for q in data.questions() if q["answer_article"]]
    plain, expo = [], []
    for q in asked:
        grade, ranked = grades(q), ranked_ids(records[q["id"]])
        plain.append(ndcg(ranked, grade, 3))
        expo.append(ndcg(ranked, grade, 3, exponential=True))
    assert round(sum(plain) / len(asked), 3) == 0.726
    assert round(sum(expo) / len(asked), 3) == 0.756
    assert sum(x > 0.9999 for x in plain) == 14


def test_one_ranking_py_prints_the_by_hand_numbers_for_q_12(capsys):
    out = printed("one_ranking.py", capsys)
    assert out[0] == ("I paid cash when the parcel came. "
                      "How do I get my refund?")
    assert out[1:4] == ["1 returns-policy#What happens next grade 0",
                        "2 missing-item#What we do grade 0",
                        "3 cod-refunds#When the money arrives grade 1"]
    assert out[5:] == ["DCG 0.500  ideal DCG 3.131  nDCG 0.160",
                       "scorecard, original gain:    0.16",
                       "scorecard, exponential gain: 0.121"]


def test_all_questions_py_prints_the_means_the_perfect_count_and_lowest_five(
        capsys):
    assert printed("all_questions.py", capsys) == [
        "mean nDCG@3, original gain: 0.726",
        "mean nDCG@3, exponential gain: 0.756",
        "perfect (1.0): 14 of 55",
        "lowest five: [('Q-03', 0.0), ('Q-31', 0.0), ('Q-32', 0.0), "
        "('Q-12', 0.16), ('Q-35', 0.32)]",
    ]
