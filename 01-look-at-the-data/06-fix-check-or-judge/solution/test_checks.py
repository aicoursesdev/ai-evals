"""Lesson 01.6: cheap code checks, and how they do against your notes.

The tests need no model and no network:

    make check 01.6
"""

import runpy
import sys
from pathlib import Path

import checks
import more_checks
from scorecard import data

HERE = Path(__file__).parent
CODED = data.DATA / "labels" / "01-coded.csv"
TAMIL = "வணக்கம், என் ஆர்டர் இன்னும் வரவில்லை, உதவுங்கள்"
HINDI = "नमस्ते, मेरा ऑर्डर अभी तक नहीं आया, कृपया मदद कीजिए"


def test_script_of_names_the_script_a_text_is_mostly_written_in():
    assert checks.script_of(TAMIL) == "Tamil"
    assert checks.script_of(HINDI) == "Devanagari"
    assert checks.script_of("Where is my order? It was due on Monday.") is None
    assert checks.script_of("") is None


def test_script_of_ignores_a_few_stray_characters():
    assert checks.script_of("Thanks " + HINDI[:5]) is None


def test_a_tamil_email_answered_in_english_fires_the_script_check():
    email = {"body": TAMIL}
    assert checks.answers_in_wrong_script(email, {"draft": "Hello, sorry."})
    assert not checks.answers_in_wrong_script(email, {"draft": TAMIL})
    assert checks.answers_in_wrong_script(email, {"draft": HINDI})


def test_an_english_email_never_fires_the_script_check():
    email = {"body": "Where is my order?"}
    assert not checks.answers_in_wrong_script(email, {"draft": "Hello"})
    assert not checks.answers_in_wrong_script(email, {"draft": TAMIL})


def test_writes_to_spam_needs_the_spam_label_and_a_reply():
    spam = {"category": "spam"}
    assert checks.writes_to_spam({"triage": spam, "draft": "Thanks!"})
    assert not checks.writes_to_spam({"triage": spam, "draft": "  "})
    assert not checks.writes_to_spam(
        {"triage": {"category": "refund"}, "draft": "Thanks!"})


def test_the_given_checks_fire_on_small_cases():
    assert more_checks.has_no_draft({"draft": " \n"})
    assert more_checks.claims_an_action({"draft": "We have updated it."})
    assert not more_checks.claims_an_action({"draft": "Please wait."})
    email = {"body": "Order TW-10520 is late"}
    ask = {"draft": "Please reply with your order ID."}
    assert more_checks.asks_for_order_id_it_has(email, ask)
    assert not more_checks.asks_for_order_id_it_has({"body": "hi"}, ask)


def test_checks_py_scores_each_check_as_the_lesson_shows(capsys, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["checks.py", str(CODED)])
    runpy.run_path(str(HERE / "checks.py"), run_name="__main__")
    assert capsys.readouterr().out.splitlines() == [
        "check                type           fires  right  type total  caught",
        "wrong script         F-language         3      2           3       2",
        "missing or old page  F-wrong-page      10      3           5       3",
        "reply to spam        F-spam-reply       6      6           7       6",
        "invented address     F-bluff            2      2          14       2",
        "claims an action     F-overreach       10     10          21      10",
        "asks for known id    F-asks-again       7      6          12       6",
        "empty draft          F-no-draft         1      1           1       1"]
