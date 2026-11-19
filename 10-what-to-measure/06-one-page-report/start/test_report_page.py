"""Lesson 10.6: an evidence line that refuses a number without its n and
its source, and the one-page report built from such lines.

No model and no network: the sealed rates are replayed from data/runs/10-sealed/
and no sealed trace is opened. From the top folder: make check 10.6
"""
import runpy
from pathlib import Path

import pytest

import plumbing
from report_page import figure, one_page

HERE = Path(__file__).parent


def test_a_figure_gives_the_share_the_count_the_range_and_the_source():
    assert figure("no check fires", 36, 50, "run") == (
        "no check fires: 36 of 50 (72.0%), 95% range 58.3% to 82.5% [run]")


def test_a_figure_refuses_a_number_with_no_n_or_no_source():
    with pytest.raises(ValueError):
        figure("x", 0, 0, "file")
    with pytest.raises(ValueError):
        figure("x", 1, 2, "")


def test_the_page_has_the_five_parts_in_order():
    page = one_page("Title", "Keep a person on every draft.",
                    [("no check fires", 36, 50, "run")], ["one reader"],
                    ["60 s a draft"], ["59 clean reads"])
    assert page.startswith("# Title\n\n## Decision\n\nKeep a person")
    heads = [h for h in page.splitlines() if h.startswith("## ")]
    assert heads == ["## Decision", "## Evidence", "## Uncertainty",
                     "## Cost", "## What would change this"]
    assert "- no check fires: 36 of 50 (72.0%)" in page
    assert page.endswith("- 59 clean reads\n")


def test_a_page_with_an_unsourced_number_is_refused():
    with pytest.raises(ValueError):
        one_page("t", "d", [("x", 1, 2, "")], [], [], [])


def test_the_counts_the_page_needs_come_from_recordings():
    assert plumbing.quiet_and_read() == (100, 68, 45)
    assert plumbing.sealed_no_check() == (36, 50)


def test_one_claim_prints_the_page_of_the_lesson(capsys):
    runpy.run_path(str(HERE / "one_claim.py"), run_name="__main__")
    lines = capsys.readouterr().out.splitlines()
    assert lines[0] == "# May “no check fires” send a draft unread?"
    assert lines[2:5] == [
        "## Decision", "",
        "No. A quiet suite does not show a draft is fine. Keep a person on "
        "every draft."]
    assert lines[8:11] == [
        "- open drafts where no check fires: 68 of 100 (68.0%), 95% range "
        "58.3% to 76.3% [checks, open]",
        "- of those, a reader found a failure: 45 of 68 (66.2%), 95% range "
        "54.3% to 76.3% [01-coded]",
        "- sealed drafts where no check fires: 36 of 50 (72.0%), 95% range "
        "58.3% to 82.5% [runs/10-sealed]"]
    assert lines[-2] == (
        "- A reader's calls on 59 or more quiet drafts of one kind of email, "
        "none failing, would justify trying that kind.")
