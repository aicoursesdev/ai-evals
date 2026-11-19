"""Lesson 06.4: what the 60 questions are made of, page against passage, and
the five questions with no answer.

No model and no network: the tests read the recorded chunks in the repo.
From the top folder: make check 06.4
"""
import re
import runpy
from pathlib import Path

import pytest

from scorecard import data

HERE = Path(__file__).parent


def printed(name, capsys):
    """What a script in this folder prints, one string per line."""
    runpy.run_path(str(HERE / name), run_name="__main__")
    return [line.rstrip() for line in capsys.readouterr().out.splitlines()]


def squash(text):
    return re.sub(r"[\s*|]+", " ", text).strip().lower()


def test_the_60_questions_split_30_15_10_and_5_by_kind():
    kinds = {}
    for q in data.questions():
        kinds[q["kind"]] = kinds.get(q["kind"], 0) + 1
    assert kinds == {"paraphrase": 30, "keyword": 15, "multi-part": 10,
                     "unanswerable": 5}


def test_only_the_five_unanswerable_questions_have_no_answer_page_or_passage():
    for q in data.questions():
        has_none = q["kind"] == "unanswerable"
        assert (not q["answer_article"]) == has_none
        assert (not q["answer_quote"]) == has_none


def test_every_answer_passage_sits_inside_its_answer_page():
    pages = {a["id"]: squash(a["text"]) for a in data.articles()}
    for q in data.questions():
        if q["answer_article"]:
            assert squash(q["answer_quote"]) in pages[q["answer_article"]]


def test_the_recorded_has_quote_flag_matches_the_passage_in_each_chunk():
    quotes = {q["id"]: squash(q["answer_quote"] or "")
              for q in data.questions()}
    for record in data.run("06-chunks")["hd-1"]:
        for chunk in record["chunks"]:
            expected = bool(quotes[record["id"]]) and (
                quotes[record["id"]] in squash(chunk["text"]))
            assert chunk["has_quote"] == expected, (record["id"],
                                                    chunk["rank"])


def test_set_shape_py_says_23_of_24_pages_have_a_question_and_the_overlap(
        capsys):
    out = printed("set_shape.py", capsys)
    assert out == [
        "Counter({'paraphrase': 30, 'keyword': 15, 'multi-part': 10, "
        "'unanswerable': 5})",
        "24 pages; 23 have a question; none for: ['shipping-india-2024']",
        "paraphrase  question words found in the passage: 20%",
        "keyword     question words found in the passage: 24%",
        "multi-part  question words found in the passage: 26%",
    ]


def test_page_or_passage_py_counts_52_pages_and_50_passages_and_two_misses(
        capsys):
    assert printed("page_or_passage.py", capsys) == [
        "page in top 3:    52/55",
        "passage in top 3: 50/55",
        "  Q-12: right page, but the chunk is 'When the money arrives', "
        "not the answer's",
        "  Q-35: right page, but the chunk is '(intro)', not the answer's",
    ]


def test_no_answer_py_shows_a_cut_off_that_silences_six_real_answers(
        capsys):
    out = printed("no_answer.py", capsys)
    assert out[0] == ("best score, questions with an answer: "
                      "lowest 0.4988 highest 0.8199")
    assert out[1].startswith("Q-56 0.4904 backpack-care | ")
    assert out[3].startswith("Q-58 0.562 backpack-care | ")
    assert out[-1] == ("a cut-off at 0.562 would silence 6 of 55 answerable "
                       "questions: ['Q-11', 'Q-23', 'Q-31', 'Q-35', 'Q-36', "
                       "'Q-48']")


def test_importing_record_chunks_py_does_not_call_a_model_or_write():
    recording = data.DATA / "runs" / "06-chunks" / "hd-1.jsonl"
    before = recording.stat().st_mtime_ns
    runpy.run_path(str(HERE / "record_chunks.py"), run_name="not_main")
    assert recording.stat().st_mtime_ns == before
