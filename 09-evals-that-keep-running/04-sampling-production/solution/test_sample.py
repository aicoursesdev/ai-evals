"""Lesson 09.4: the flags and the seeded weekly draw, in your own code.

No model and no network: the tests read the recorded week in the repo.
From the top folder: make check 09.4
"""
import random
import runpy
from pathlib import Path

import plumbing
import weekly_sample

HERE = Path(__file__).parent


def printed(name, capsys):
    """What a script in this folder prints, one string per line."""
    runpy.run_path(str(HERE / name), run_name="__main__")
    return [line.rstrip() for line in capsys.readouterr().out.splitlines()]


def fake_rows(n, flagged=()):
    """n (email, trace) pairs; the ones in `flagged` get a firing check."""
    return {f"E-{i:04d}": ({"fires": i in flagged}, {"i": i})
            for i in range(n)}


def trace(needs_human, draft):
    return {"triage": {"needs_human": needs_human}, "draft": draft}


def test_flags_name_the_checks_that_fire(monkeypatch):
    monkeypatch.setattr(weekly_sample, "CHECKS", {
        "bluff": (lambda e, t: True, ""), "spam": (lambda e, t: False, ""),
        "blank": (lambda e, t: True, "")})
    monkeypatch.setattr(weekly_sample, "promises_refund", lambda d: False)
    assert weekly_sample.flags({}, trace(True, "hi")) == ["bluff", "blank"]


def test_flags_add_a_needs_human_mismatch_only_when_no_person_was_asked(
        monkeypatch):
    monkeypatch.setattr(weekly_sample, "CHECKS", {})
    monkeypatch.setattr(weekly_sample, "promises_refund", lambda d: True)
    assert weekly_sample.flags({}, trace(False, "refund")) == [
        "needs_human mismatch"]
    assert weekly_sample.flags({}, trace(True, "refund")) == []


def test_flags_use_the_real_checks_on_the_recorded_week():
    rows = plumbing.pool(4)
    names = {n for i in rows for n in weekly_sample.flags(*rows[i])}
    assert names and all(isinstance(n, str) for n in names)
    assert sum(bool(weekly_sample.flags(*rows[i])) for i in rows) == 23


def test_draw_takes_20_random_then_5_flagged_from_the_rest(monkeypatch):
    rows = fake_rows(100, flagged=set(range(0, 100, 3)))
    monkeypatch.setattr(weekly_sample, "flags",
                        lambda email, trace: ["x"] if email["fires"] else [])
    random_ids, flag_ids, n_flagged = weekly_sample.draw(rows)
    assert len(random_ids) == 20 and len(flag_ids) == 5
    assert not set(random_ids) & set(flag_ids)
    assert all(rows[i][0]["fires"] for i in flag_ids)
    outside = [i for i in rows if rows[i][0]["fires"] and i not in random_ids]
    assert n_flagged == len(outside)


def test_draw_is_the_same_every_time_and_the_seed_changes_it():
    rows = plumbing.pool(4)
    assert weekly_sample.draw(rows) == weekly_sample.draw(rows)
    assert weekly_sample.draw(rows, seed=8)[0] != weekly_sample.draw(rows)[0]


def test_draw_matches_random_sample_with_seed_7():
    rows = plumbing.pool(4)
    assert weekly_sample.draw(rows)[0] == random.Random(7).sample(
        sorted(rows), 20)


def test_weekly_sample_prints_the_ids_the_lesson_shows(
        capsys, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)         # the sheet is written to the folder
    assert printed("weekly_sample.py", capsys) == [
        'pool 100 emails; 16 flagged outside the random 20',
        ('random: E-0607 E-0610 E-0611 E-0613 E-0614 E-0618 E-0619 E-0626 '
         'E-0637 E-0640 E-0662 E-0667 E-0674 E-0682 E-0684 E-0696 E-0703 '
         'E-0706 E-0712 E-0727'),
        'flagged: E-0621 E-0627 E-0683 E-0715 E-0742',
        'wrote review-sheet.md with 25 entries',
    ]
    sheet = (tmp_path / "review-sheet.md").read_text()
    assert sheet == (HERE / "review-sheet.md").read_text()
    assert sheet.count("\n## ") + 1 == 25


def test_read_sample_counts_the_calls_the_lesson_shows(capsys):
    assert printed("read_sample.py", capsys) == [
        "random   {'pass': 5, 'fail': 15}",
        "flagged  {'fail': 5}",
        'random drafts failing: 15 of 20, range 53% to 89%',
        ("failure types: {'F-bluff': 4, 'F-asks-again': 4, 'F-overreach': "
         "3, 'F-wrong-rule': 3, 'F-misread': 2, 'F-spam-reply': 2, "
         "'F-language': 1, 'F-wrong-page': 1}"),
        "not in Module 01's map: none",
    ]
