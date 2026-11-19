"""Lesson 02.5: words, shingles, contained and find_leaks.

The tests need no model and no network:

    make check 02.5
"""

import json
import runpy
from pathlib import Path

import pytest

from leaks import contained, find_leaks, shingles, words
from near import near_pairs, similar
from plumbing import launch_halves, print_scores, prompt_sources
from scorecard import data
from score_without_leaks import split_leaked

HERE = Path(__file__).parent


@pytest.fixture
def no_sealed_parse(monkeypatch):
    """Fail if anything parses a trace line whose id is in the sealed part."""
    sealed = {e["id"] for e in data.testset("sealed")}
    real = json.loads

    def guard(text, *args, **kwargs):
        if isinstance(text, str) and '"triage":' in text \
                and text[8:14] in sealed:
            raise AssertionError("a sealed trace line was parsed")
        return real(text, *args, **kwargs)

    monkeypatch.setattr(json, "loads", guard)


def mail(id, subject, body=""):
    return {"id": id, "subject": subject, "body": body}


def test_words_are_lower_case_and_split_on_spaces_and_punctuation():
    assert words("Tent floor, on WET ground!") == [
        "tent", "floor", "on", "wet", "ground"]
    assert words("  “Hello”... (again)  ") == ["hello", "again"]


def test_words_split_other_scripts_too():
    assert words("नमस्ते, मेरा ऑर्डर") == ["नमस्ते", "मेरा", "ऑर्डर"]


def test_shingles_are_the_runs_of_three_words():
    assert shingles("Tent floor on wet ground") == {
        ("tent", "floor", "on"), ("floor", "on", "wet"),
        ("on", "wet", "ground")}


def test_shingles_of_n_1_are_the_words_and_repeats_collapse():
    assert shingles("a b a", n=1) == {("a",), ("b",)}


def test_a_text_shorter_than_n_is_one_run_on_its_own():
    assert shingles("hello there") == {("hello", "there")}
    assert shingles("") == {()}


def test_contained_is_1_for_a_copy_and_0_for_an_unrelated_text():
    email = mail("E-1", "Tent floor", "on wet ground")
    assert contained(email, "see: tent floor on wet ground, thanks") == 1.0
    assert contained(email, "nothing in common here at all") == 0.0


def test_contained_is_the_share_of_the_emails_runs_found():
    email = mail("E-1", "one two three", "four")  # runs: 1-2-3, 2-3-4
    assert contained(email, "one two three") == 0.5


def test_find_leaks_reports_emails_at_or_above_the_floor():
    inside = mail("E-1", "refund for my torn", "jacket please")
    outside = mail("E-2", "where is", "my parcel today")
    sources = {"a.md": "x refund for my torn jacket please y",
               "b.md": "something else"}
    assert find_leaks([inside, outside], sources) == [("E-1", "a.md", 1.0)]


def test_find_leaks_rounds_the_share_and_honours_a_lower_floor():
    email = mail("E-1", "one two three", "four")
    assert find_leaks([email], {"s": "one two three"}) == []
    assert find_leaks([email], {"s": "one two three"}, floor=0.5) == [
        ("E-1", "s", 0.5)]


def test_similar_and_near_pairs_are_given_and_use_your_shingles():
    a, b = mail("A", "one two three four"), mail("B", "one two three five")
    assert similar(a, b, n=1) == 3 / 5
    c = mail("C", "nothing shared")
    assert near_pairs([a, b, c], floor=0.5, n=1) == [("A", "B", 0.6)]


def test_the_help_desks_prompt_holds_four_test_emails_and_two_dev_emails():
    sources, (test, dev) = prompt_sources(), launch_halves()
    assert list(sources) == ["hd-1/draft.md", "hd-1/refunds.md",
                             "hd-1/triage.md"]
    assert (len(test), len(dev)) == (50, 100)
    assert find_leaks(test, sources) == [
        (i, "hd-1/triage.md", 1.0)
        for i in ("E-0013", "E-0019", "E-0023", "E-0031")]
    assert find_leaks(dev, sources) == [
        ("E-0003", "hd-1/triage.md", 1.0), ("E-0021", "hd-1/triage.md", 1.0)]


def test_a_floor_of_0_05_flags_two_more_test_emails():
    sources, (test, _) = prompt_sources(), launch_halves()
    assert len(find_leaks(test, sources, floor=0.05)) == 6


def test_split_leaked_separates_the_leaked_ids_from_the_clean_emails():
    leak = mail("E-1", "refund for my torn", "jacket please")
    fine = mail("E-2", "where is", "my parcel today")
    leaked, clean = split_leaked([leak, fine],
                                 {"a.md": "refund for my torn jacket please"})
    assert leaked == {"E-1"} and clean == [fine]


def test_taking_the_four_leaks_out_leaves_38_of_46(capsys):
    test, _ = launch_halves()
    leaked, clean = split_leaked(test, prompt_sources())
    assert len(leaked) == 4 and len(clean) == 46
    print_scores(test, leaked, clean)
    assert capsys.readouterr().out == (
        "all test emails : 42 of 50\n"
        "the leaked ones : 4 of 4 ['E-0013', 'E-0019', 'E-0023', 'E-0031']\n"
        "without them    : 38 of 46 = 82.6%\n")


def test_find_leaks_py_prints_the_six_files_the_lesson_shows(capsys):
    runpy.run_path(str(HERE / "find_leaks.py"), run_name="__main__")
    out = capsys.readouterr().out
    assert out.startswith("50 test emails against 3 prompt files\n"
                          "   E-0013 hd-1/triage.md 1.0\n")
    assert out.endswith("   E-0021 hd-1/triage.md 1.0\n")


def test_duplicates_py_finds_no_copy_and_18_pairs_sharing_40_percent(capsys):
    runpy.run_path(str(HERE / "duplicates.py"), run_name="__main__")
    lines = capsys.readouterr().out.splitlines()
    assert lines[0] == "750 emails: 150 launch, 600 log"
    assert lines[1] == "exact copies of a body: 0"
    assert lines[2] == "pairs sharing half their 3-word runs: 0"
    assert lines[3] == "pairs sharing 40% of their words: 18 (closest first)"
    assert lines[4] == "   E-0348 E-0628 0.5"


def test_the_scripts_score_only_launch_traces_and_parse_no_sealed_line(
        no_sealed_parse, capsys):
    for name in ("find_leaks.py", "score_without_leaks.py"):
        runpy.run_path(str(HERE / name), run_name="__main__")
    for path in HERE.glob("*.py"):
        if path.name != "test_leaks.py":
            text = path.read_text(encoding="utf-8")
            assert text.count("data.traces") == text.count(
                "data.traces(\"hd-1\", launch=True)"), path
            assert "week-" not in text, path
