"""Project 09: the gate, the weekly sample and the rerun after the swap.

No model and no network: the tests read the recorded runs in the repo, and
the sealed emails are never read. The tests accept any ship rule that you
wrote, as long as it lets hd-2 through and stops the smaller model.
From the top folder: make check 09.9
"""
import random
import runpy
import sys
from pathlib import Path

import pytest

import after_swap
import gate
import plumbing
import weekly
from scorecard import report, stats

HERE = Path(__file__).parent
NAMES = {"triage right", "no check fires", "triage change", "checks change"}


def printed(name, capsys, *args, code=0):
    """What a script in this folder prints, one string per line, when run
    with these arguments; it must end with exit code `code`."""
    sys.argv = [name, *args]
    try:
        runpy.run_path(str(HERE / name), run_name="__main__")
        ended = 0
    except SystemExit as stop:
        ended = stop.code
    assert ended == code
    return [line.rstrip() for line in capsys.readouterr().out.splitlines()]


@pytest.fixture(autouse=True)
def restore_argv():
    saved = sys.argv
    yield
    sys.argv = saved


def test_the_ship_rule_is_made_of_rules_on_the_scores_the_gate_builds():
    assert gate.RULES
    for name, minimum, use_low in gate.RULES:
        assert name in NAMES and isinstance(minimum, float)
        assert isinstance(use_low, bool)


def test_scores_measure_the_new_version_and_its_change(monkeypatch):
    monkeypatch.setattr(gate, "clean", lambda e, t: 1)
    mail = {i: {"category": "refund"} for i in range(10)}
    pick = lambda hits: {i: {"triage": {"category": "refund" if i in hits
                                        else "other"}} for i in range(10)}
    found, n = gate.scores(mail, pick(range(5)), pick(range(8)))
    assert n == 10 and found["triage right"][1] == 0.8
    assert found["triage right"][::2] == pytest.approx(stats.wilson(8, 10))
    p = stats.paired([1] * 5 + [0] * 5, [1] * 8 + [0] * 2)
    assert found["triage change"] == pytest.approx(
        (p["low"], p["diff"], p["high"]))
    assert found["no check fires"][1] == 1 and found["checks change"][1] == 0


def test_scores_use_only_emails_both_versions_answered(monkeypatch):
    monkeypatch.setattr(gate, "clean", lambda e, t: 1)
    mail = {i: {"category": "refund"} for i in range(4)}
    old = {i: {"triage": {"category": "refund"}} for i in range(4)}
    new = {i: old[i] for i in range(3)}
    assert gate.scores(mail, old, new)[1] == 3


def test_your_rule_lets_hd_2_through_and_stops_the_smaller_model():
    found, _ = gate.scores(plumbing.emails(), plumbing.drafts("hd-1"),
                           plumbing.drafts("hd-2"))
    assert report.gate(found, gate.RULES)[0] is True
    found, _ = gate.scores(*plumbing.swap())
    passed, reasons = report.gate(found, gate.RULES)
    assert passed is False and reasons


def test_gate_says_yes_to_hd_2_and_exits_with_0(capsys):
    lines = printed("gate.py", capsys, "hd-2")
    assert lines[:5] == [
        'hd-2 against hd-1 on 277 emails',
        'triage right    +0.856  range +0.809 to +0.892',
        'triage change   +0.000  range +0.000 to +0.000',
        'no check fires  +0.816  range +0.766 to +0.857',
        'checks change   +0.054  range +0.010 to +0.098']
    assert lines[5] == 'gate passed: True'


def test_gate_says_no_to_the_swap_with_reasons_and_exits_with_1(capsys):
    lines = printed("gate.py", capsys, "swap", code=1)
    assert lines[:5] == [
        'swap against hd-1 on 149 emails',
        'triage right    +0.732  range +0.655 to +0.796',
        'triage change   -0.128  range -0.196 to -0.059',
        'no check fires  +0.685  range +0.606 to +0.754',
        'checks change   +0.007  range -0.082 to +0.095']
    assert lines[5] == 'gate passed: False' and len(lines) > 6


def test_draw_takes_20_at_random_and_up_to_5_flagged(monkeypatch):
    rows = {f"E-{i:03d}": ({"hot": i % 4 == 0}, {}) for i in range(100)}
    monkeypatch.setattr(weekly, "flags",
                        lambda email, trace: ["x"] if email["hot"] else [])
    chosen, extra, n_flagged = weekly.draw(rows)
    assert len(chosen) == 20 and len(extra) == 5
    assert not set(chosen) & set(extra)
    assert all(rows[i][0]["hot"] for i in extra)
    assert n_flagged == sum(rows[i][0]["hot"] and i not in chosen
                            for i in rows)


def test_draw_takes_fewer_when_fewer_are_flagged(monkeypatch):
    rows = {f"E-{i:03d}": ({"hot": i < 22}, {}) for i in range(100)}
    monkeypatch.setattr(weekly, "flags",
                        lambda email, trace: ["x"] if email["hot"] else [])
    chosen, extra, n_flagged = weekly.draw(rows)
    assert len(extra) == min(5, n_flagged) <= 5


def test_draw_is_seeded_the_way_the_lesson_says():
    rows = plumbing.pool(4)
    chosen = weekly.draw(rows)[0]
    assert weekly.draw(rows) == weekly.draw(rows)
    assert chosen == random.Random(7).sample(sorted(rows), 20)


def test_entries_list_the_random_then_the_flagged(monkeypatch):
    monkeypatch.setattr(weekly, "flags", lambda email, trace: ["bluff", "x"])
    rows = {i: ({"subject": f"s{i}", "body": f"b{i}"}, {"draft": f"d{i}"})
            for i in "abc"}
    parts = weekly.entries(rows, ["b", "a"], ["c"])
    assert [p.split(" (")[0] for p in parts] == ["## a", "## b", "## c"]
    assert parts[0].startswith("## a (random)\n\n**Subject:** sa\n\nba\n")
    assert parts[2].startswith("## c (flagged: bluff, x)")
    assert parts[2].endswith("**Draft:**\n\ndc\n")


def test_weekly_prints_week_3_and_writes_25_entries(
        capsys, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert printed("weekly.py", capsys, "3") == [
        'week 3: pool 82, 18 flagged outside the 20',
        'wrote review-sheet-week-3.md with 25 entries']
    sheet = (tmp_path / "review-sheet-week-3.md").read_text()
    assert sheet.count("\n## ") + 1 == 25
    assert sheet.count("(random)") == 20 and sheet.count("(flagged:") == 5


def test_weekly_takes_week_3_when_given_no_week(capsys, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert printed("weekly.py", capsys)[0].startswith("week 3:")


def test_triage_line_agrees_with_scorecard_stats():
    a = [1] * 104 + [1] * 24 + [0] * 5 + [0] * 16
    b = [1] * 104 + [0] * 24 + [1] * 5 + [0] * 16
    line = after_swap.triage_line(a, b)
    p = stats.paired(a, b)
    assert line.startswith("- usual 128, smaller 109: change ")
    assert f"{p['diff']:+.1%}" in line and f"{stats.mcnemar(a, b):.4f}" in line


def test_judge_line_counts_only_clear_passes():
    human = {1: "pass", 2: "pass", 3: "fail", 4: "fail"}
    said = {1: "pass", 2: "none", 3: "pass", 4: "fail"}
    assert after_swap.judge_line("x", human, said, [1, 2, 3, 4]) == (
        "- x: passes kept 1 of 2, fails held back 1 of 2")


def test_after_swap_prints_the_three_sections_the_lesson_shows(capsys):
    assert printed("after_swap.py", capsys) == [
        '## Triage, same 149 emails',
        ('- usual 128, smaller 109: change -12.8%, range -19.6% to -5.9%, '
         'McNemar p 0.0005'),
        '',
        '## Code checks, same 149 emails',
        '- no check fires: usual 101, smaller 102, McNemar p 1.00',
        '',
        '## The judge, 100 held-out drafts, against Arjun',
        '- usual: passes kept 38 of 59, fails held back 16 of 26',
        '- smaller: passes kept 9 of 59, fails held back 21 of 26',
    ]
