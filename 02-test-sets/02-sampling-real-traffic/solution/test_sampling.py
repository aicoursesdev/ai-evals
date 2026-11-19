"""Lesson 02.2: random_sample, slice_sample and weighted_rate.

The tests need no model and no network:

    make check 02.2
"""

import json
import runpy
from collections import Counter
from pathlib import Path

import pytest

import held_back
from scorecard import data
from slices import log, random_sample, slice_sample, tally
from weighting import weighted_rate

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


def mail(id, language="en", category="refund", attack=False, long=False):
    body = "x" * (400 if long else 10)
    return {"id": id, "language": language, "category": category,
            "week": 1, "attack": attack, "body": body}


def test_a_random_sample_has_n_different_emails_from_the_pool():
    pool = [mail(f"E-{i}") for i in range(30)]
    got = random_sample(pool, 10, seed=1)
    assert len(got) == 10 and len({e["id"] for e in got}) == 10
    assert all(e in pool for e in got)


def test_the_same_seed_picks_the_same_emails_and_another_seed_does_not():
    pool = [mail(f"E-{i}") for i in range(30)]
    assert random_sample(pool, 10, 5) == random_sample(pool, 10, 5)
    assert random_sample(pool, 10, 5) != random_sample(pool, 10, 6)


def test_a_sample_by_slice_picks_the_rare_email_first():
    pool = [mail(f"E-{i}") for i in range(20)] + [mail("E-ta", "ta")]
    for seed in range(5):
        got = slice_sample(pool, 2, seed)
        assert "E-ta" in {e["id"] for e in got}


def test_a_sample_by_slice_never_repeats_an_email():
    pool = [mail(f"E-{i}", "en" if i % 3 else "ta") for i in range(30)]
    got = slice_sample(pool, 20, seed=2)
    assert len({e["id"] for e in got}) == 20


def test_a_slice_stops_counting_as_short_at_the_floor():
    pool = ([mail(f"T-{i}", "ta") for i in range(4)]
            + [mail(f"H-{i}", "hi") for i in range(4)])
    have = [mail(f"X-{i}", "ta") for i in range(2)]
    got = slice_sample(pool, 3, seed=1, have=have, floor=2)
    assert Counter(e["language"] for e in got)["hi"] >= 2


def test_slice_sample_takes_what_exists_when_a_slice_is_short():
    pool = [mail("E-1", "ml")] + [mail(f"E-{i}") for i in range(2, 12)]
    got = slice_sample(pool, 5, seed=3, floor=3)
    assert "E-1" in {e["id"] for e in got} and len(got) == 5


def test_a_weighted_rate_adds_each_rate_times_its_weight():
    rates = {"a": 1.0, "b": 0.5}
    assert weighted_rate(rates, {"a": 0.5, "b": 0.5}) == 0.75
    assert weighted_rate(rates, {"a": 0.25, "b": 0.75}) == 0.625


def test_a_weighted_rate_ignores_a_group_with_no_weight():
    assert weighted_rate({"a": 0.9, "b": 0.1}, {"a": 1, "b": 0}) == 0.9


def test_the_lessons_two_groups_weigh_back_to_the_whole_logs_rate():
    rates = {"English": 389 / 447, "others": 97 / 103}
    weights = {"English": 447 / 550, "others": 103 / 550}
    assert round(weighted_rate(rates, weights), 3) == 0.884
    half = {"English": 0.5, "others": 0.5}
    assert round(weighted_rate(rates, half), 3) == 0.906


def test_a_random_100_holds_1_malayalam_and_a_sample_by_slice_all_8():
    emails = log()
    assert len(emails) == 600 and tally(emails)[("language", "ml")] == 8
    one = tally(random_sample(emails, 100, seed=1))
    sliced = tally(slice_sample(emails, 100, seed=1))
    assert one[("language", "ml")] == 1
    assert sliced[("language", "ml")] == 8
    assert (sliced[("language", "hi")], sliced[("attack", True)]) == (10, 10)


def test_1000_random_hundreds_miss_malayalam_223_times():
    emails = log()
    none = sum(tally(random_sample(emails, 100, s))[("language", "ml")] == 0
               for s in range(1000))
    assert none == 223


def test_random_vs_slice_py_prints_the_lessons_table(capsys):
    runpy.run_path(str(HERE / "random_vs_slice.py"), run_name="__main__")
    out = capsys.readouterr().out
    assert "language=ml             8           1         8\n" in out
    assert "language=ml           0   1.0    5     223\n" in out


def test_the_whole_log_scores_88_4_and_200_random_hundreds_stay_close(
        no_sealed_parse):
    emails, said = held_back.usable_emails(), held_back.usable_triage()
    assert len(emails) == 550
    right = [said[e["id"]]["category"] == e["category"] for e in emails]
    assert sum(right) == 486 and round(sum(right) / 550, 3) == 0.884
    means = []
    for seed in range(200):
        pick = random_sample(emails, 100, seed)
        means.append(sum(said[e["id"]]["category"] == e["category"]
                         for e in pick) / 100)
    assert round(sum(means) / 200, 3) == 0.885


def test_the_sealed_part_is_never_loaded_or_parsed(no_sealed_parse):
    sealed = held_back.sealed_ids()
    assert len(sealed) == 50
    assert not sealed & {e["id"] for e in held_back.usable_emails()}
    assert not sealed & set(held_back.usable_triage())


def test_no_script_opens_a_trace_file_except_through_held_back():
    for path in HERE.glob("*.py"):
        if path.name not in ("held_back.py", "test_sampling.py"):
            assert "traces" not in path.read_text(encoding="utf-8"), path
