"""Lesson 00.2: the help desk's recorded work, read the way the lesson reads it.

The tests need no model and no network:

    make check 00.2
"""

import runpy
from pathlib import Path

from scorecard import data

HERE = Path(__file__).parent


def run_script(name, capsys):
    runpy.run_path(str(HERE / name), run_name="__main__")
    return capsys.readouterr().out


def test_the_launch_set_has_150_emails_split_100_dev_and_50_test():
    launch = data.emails(launch=True)
    splits = [e["split"] for e in launch]
    assert len(launch) == 150
    assert (splits.count("dev"), splits.count("test")) == (100, 50)


def test_week_1_has_150_emails_and_150_traces_from_e_0151_to_e_0300():
    week1 = data.emails(week=1)
    assert (week1[0]["id"], week1[-1]["id"]) == ("E-0151", "E-0300")
    assert len(data.traces("hd-1", week=1)) == 150


def test_first_look_py_prints_what_the_lesson_shows(capsys):
    assert run_script("first_look.py", capsys).splitlines() == [
        "launch set: 150 emails",
        "  splits: {'dev': 100, 'test': 50}",
        "week 1: 150 emails",
        "  first: E-0151 last: E-0300",
        "traces for week 1: 150",
    ]


def test_one_trace_py_prints_arjuns_labels_and_the_help_desks_for_e_0156(
        capsys):
    out = run_script("one_trace.py", capsys)
    assert out.startswith('EMAIL      COD refund how | Hello, I returned')
    assert "ARJUN SAID refund normal False\n" in out
    assert ("TRIAGE     {'category': 'refund', 'urgency': 'high', "
            "'needs_human': True}\n") in out


def test_one_trace_py_prints_three_retrieved_passages_all_cod_refunds(capsys):
    out = run_script("one_trace.py", capsys)
    assert out.count("RETRIEVED  cod-refunds ") == 3
    assert "RETRIEVED  cod-refunds 0.6646\n" in out


def test_one_trace_py_prints_the_draft_and_the_article_it_cites(capsys):
    out = run_script("one_trace.py", capsys)
    assert "DRAFT      Hi Bhavya, since your order was cash on delivery" in out
    assert out.endswith("CITED      ['cod-refunds']\n")
