"""Project 10.7: the rule applied by kind, the evidence and the program.

No model and no network: the open part and the sealed part's replay come
from recordings, nothing is scored again and no sealed trace is opened.
The report is written to a temporary folder. From the top folder:
make check 10.7
"""
import runpy
from pathlib import Path

import pytest

import by_kind

HERE = Path(__file__).parent

EVIDENCE = [
    "- open drafts a reader found fine: 23 of 100 (23.0%), 95% range 15.8% to 32.2% [labels/01-coded.csv]",
    "- random weekly sample found fine: 5 of 20 (25.0%), 95% range 11.2% to 46.9% [labels/09-weekly-sample]",
    "- quiet drafts a reader found failing: 45 of 68 (66.2%), 95% range 54.3% to 76.3% [labels/01-coded.csv, graders.CHECKS]",
    "- triage right, open: 87 of 100 (87.0%), 95% range 79.0% to 92.2% [testsets/v1/open]",
    "- triage right, sealed: 45 of 50 (90.0%), 95% range 78.6% to 95.7% [runs/10-sealed]",
    "- no check fires, sealed: 36 of 50 (72.0%), 95% range 58.3% to 82.5% [runs/10-sealed]",
    "- judge: bad drafts held back: 16 of 26 (61.5%), 95% range 42.5% to 77.6% [runs/04-heldout]",
    "- judge: good drafts kept: 38 of 59 (64.4%), 95% range 51.7% to 75.4% [runs/04-heldout]",
    "- refund agent right, one run: 20 of 30 (66.7%), 95% range 48.8% to 80.8% [runs/07-refund-trials]",
    "- attacks that got through: 14 of 40 (35.0%), 95% range 22.1% to 50.5% [labels/08-attack-outcomes]",
    "- hd-2 no check fires: 226 of 277 (81.6%), 95% range 76.6% to 85.7% [traces/hd-2]",
    "- hd-1 no check fires, same emails: 211 of 277 (76.2%), 95% range 70.8% to 80.8% [traces/hd-1]",
]


def test_by_kind_counts_reads_and_failures_for_each_kind():
    drafts = [{"category": "refund", "fine": True},
              {"category": "refund", "fine": False},
              {"category": "spam", "fine": False}]
    assert by_kind.by_kind(drafts) == {"refund": (2, 1), "spam": (1, 1)}
    assert by_kind.by_kind([]) == {}


def test_a_kind_may_go_out_unread_only_with_59_clean_reads():
    assert by_kind.may_go_unread(59, 0) is True
    assert by_kind.may_go_unread(58, 0) is False
    assert by_kind.may_go_unread(200, 1) is False


def test_by_kind_prints_every_kind_with_a_no(capsys):
    runpy.run_path(str(HERE / "by_kind.py"), run_name="__main__")
    lines = [x.rstrip() for x in capsys.readouterr().out.splitlines()]
    assert lines[:3] == [
        "clean reads needed: 59 (upper limit 0.050)",
        "kind             read  failed  may go out unread",
        "shipping_delay    21    19    no"]
    assert len(lines) == 13 and all(x.endswith("no") for x in lines[2:])


@pytest.fixture
def report(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    runpy.run_path(str(HERE / "report_to_meera.py"), run_name="__main__")
    return (tmp_path / "report.md").read_text()


def test_the_report_decides_first_and_says_no(report):
    assert report.startswith("# Which emails may go out unread?\n\n"
                             "## Decision\n\nNo kind of email may go out "
                             "unread yet.")
    assert "shipping delay, has 21 reads and 19 failures" in report


def test_the_report_has_the_twelve_evidence_lines_of_the_lesson(report):
    evidence = report.split("## Evidence\n\n")[1].split("\n\n## ")[0]
    assert evidence.splitlines() == EVIDENCE


def test_the_report_keeps_its_other_four_parts(report):
    for head in ("Uncertainty", "Cost", "What would change this"):
        assert f"\n## {head}\n" in report
    assert "now spent" in report and "assumed 60 s a draft" in report


def test_the_program_has_a_row_for_each_of_the_six_moments():
    rows = [r for r in (HERE / "program.md").read_text().splitlines()
            if r.startswith("|")][2:]
    assert len(rows) >= 6
    for row in rows:
        cells = [c.strip() for c in row.strip("|").split("|")]
        assert len(cells) == 4 and all(cells)
    text = (HERE / "program.md").read_text().lower()
    for moment in ("every change", "nightly", "weekly", "model",
                   "unread", "test set"):
        assert moment in text


def test_the_program_never_reads_the_sealed_part_again():
    text = (HERE / "program.md").read_text().lower()
    assert "sealed" in text
