"""Lesson 06.2: the retrieval scores, by hand and in your own functions.

No model and no network: the tests read the recorded searches in the repo.
From the top folder: make check 06.2
"""
import runpy
from pathlib import Path

import pytest

from retrieval import mrr, precision_at_k, recall_at_k, reciprocal_rank
from scorecard import data

HERE = Path(__file__).parent
KS = (1, 3, 5, 10)


def printed(name, capsys):
    """What a script in this folder prints, one string per line."""
    runpy.run_path(str(HERE / name), run_name="__main__")
    return [line.rstrip() for line in capsys.readouterr().out.splitlines()]


@pytest.fixture(scope="module")
def searches():
    """(ranked page ids, right page) for the 55 answerable questions."""
    runs = {r["id"]: r for r in data.run("06-retrieval")["hd-1"]}
    return [([h["article_id"] for h in runs[q["id"]]["top10"]],
             {q["answer_article"]})
            for q in data.questions() if q["answer_article"]]


def test_a_right_page_in_fourth_place_gives_recall_0_at_3_and_rank_0_25():
    ranked = ["a", "b", "c", "d", "e"]
    assert recall_at_k(ranked, {"d"}, 3) == 0
    assert recall_at_k(ranked, {"d"}, 5) == 1
    assert reciprocal_rank(ranked, {"d"}) == 0.25


def test_recall_is_the_share_of_the_right_pages_found_in_the_top_k():
    assert recall_at_k(["a", "b", "c"], {"a", "c"}, 2) == 0.5
    assert recall_at_k(["a", "b", "c"], {"c"}, 2) == 0


def test_precision_is_the_share_of_the_top_k_that_is_right():
    assert precision_at_k(["a", "b", "c"], {"c"}, 3) == pytest.approx(1 / 3)
    assert precision_at_k(["a", "b", "c"], {"a"}, 1) == 1


def test_a_right_page_nowhere_in_the_list_scores_0_reciprocal_rank():
    assert reciprocal_rank(["a", "b"], {"z"}) == 0


def test_mrr_is_the_average_reciprocal_rank_over_the_questions():
    assert mrr([["a", "b"], ["x", "a"]], [{"a"}, {"a"}]) == 0.75


def test_hd1_recall_at_1_3_5_and_10_is_0_855_0_945_1_and_1(searches):
    got = [sum(recall_at_k(p, r, k) for p, r in searches) / len(searches)
           for k in KS]
    assert [round(x, 3) for x in got] == [0.855, 0.945, 1.0, 1.0]


def test_hd1_precision_falls_as_k_grows_and_mrr_is_0_91(searches):
    got = [sum(precision_at_k(p, r, k) for p, r in searches) / len(searches)
           for k in KS]
    assert [round(x, 3) for x in got] == [0.855, 0.618, 0.531, 0.387]
    ranked, right = zip(*searches)
    assert round(mrr(ranked, right), 3) == 0.91


def test_your_functions_agree_with_the_course_s_on_every_question(searches):
    from scorecard import retrieval as course
    for ranked, right in searches:
        assert reciprocal_rank(ranked, right) == course.reciprocal_rank(
            ranked, right)
        for k in KS:
            assert recall_at_k(ranked, right, k) == course.recall_at_k(
                ranked, right, k)
            assert precision_at_k(ranked, right, k) == course.precision_at_k(
                ranked, right, k)


def test_one_question_py_finds_the_right_page_for_q_03_at_rank_5(capsys):
    out = printed("one_question.py", capsys)
    assert out[0] == ("Can I swap my jacket for a different size? "
                      "| right page: returns-policy")
    assert out[5] == "5 returns-policy   <- right"
    assert out[-2:] == ["first right result at rank 5 so reciprocal rank 0.2",
                        "in the top 3? False"]


def test_by_hand_py_prints_the_table_and_the_mean_reciprocal_rank(capsys):
    assert printed("by_hand.py", capsys) == [
        "55 questions with an answer page",
        "k= 1  recall 47/55 = 0.855   precision 47/55 = 0.855",
        "k= 3  recall 52/55 = 0.945   precision 102/165 = 0.618",
        "k= 5  recall 55/55 = 1.000   precision 146/275 = 0.531",
        "k=10  recall 55/55 = 1.000   precision 213/550 = 0.387",
        "mean reciprocal rank 0.91",
    ]


def test_recall_py_prints_recall_precision_mrr_and_the_three_misses(capsys):
    out = printed("recall.py", capsys)
    assert out[:4] == ["k= 1  recall 0.855", "k= 3  recall 0.945",
                       "k= 5  recall 1.000", "k=10  recall 1.000"]
    assert out[4:8] == ["k= 1  precision 0.855", "k= 3  precision 0.618",
                        "k= 5  precision 0.531", "k=10  precision 0.387"]
    assert out[8:] == ["mrr 0.91",
                       "paraphrase  recall@3 27/30",
                       "multi-part  recall@3 10/10",
                       "keyword     recall@3 15/15",
                       "missed at k=3: ['Q-03', 'Q-31', 'Q-32']"]


def test_bigger_k_py_shows_the_archived_page_creeping_in_as_k_grows(capsys):
    assert printed("bigger_k.py", capsys) == [
        "k= 1  questions with the archived page in the top k:  0"
        "   words handed over per question: 71",
        "k= 3  questions with the archived page in the top k:  4"
        "   words handed over per question: 184",
        "k= 5  questions with the archived page in the top k:  4"
        "   words handed over per question: 294",
        "k=10  questions with the archived page in the top k: 15"
        "   words handed over per question: 575",
    ]
