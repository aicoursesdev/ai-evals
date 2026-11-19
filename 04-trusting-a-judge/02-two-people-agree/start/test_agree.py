"""Lesson 04.2: agreement and kappa from four counts, in your own functions.

No model and no network: the tests read the recorded labels in the repo.
From the top folder: make check 04.2
"""
import runpy
from pathlib import Path

import pytest

import by_hand
from plumbing import settled, two_columns
from scorecard.judge import agreement, kappa

HERE = Path(__file__).parent


def printed(name, capsys):
    """What a script in this folder prints, one string per line."""
    runpy.run_path(str(HERE / name), run_name="__main__")
    return [line.rstrip() for line in capsys.readouterr().out.splitlines()]


def table(both_pass, both_fail, a_only, d_only):
    """Two lists of calls with these four counts."""
    a = ["pass"] * both_pass + ["fail"] * both_fail \
        + ["pass"] * a_only + ["fail"] * d_only
    d = ["pass"] * both_pass + ["fail"] * both_fail \
        + ["fail"] * a_only + ["pass"] * d_only
    return a, d


def test_the_two_labellers_called_the_same_100_drafts():
    ids, arjun, divya = two_columns()
    assert len(ids) == len(arjun) == len(divya) == 100


def test_settled_drops_every_draft_where_either_said_unsure():
    a, d = settled(["pass", "unsure", "fail", "pass"],
                   ["fail", "pass", "unsure", "pass"])
    assert (a, d) == (["pass", "pass"], ["fail", "pass"])


def test_four_counts_counts_each_kind_of_pair():
    a = ["pass", "pass", "fail", "pass", "fail"]
    d = ["pass", "fail", "fail", "pass", "pass"]
    assert by_hand.four_counts(a, d) == (2, 1, 1, 1)


def test_four_counts_on_the_real_80_is_50_25_4_1():
    _, arjun, divya = two_columns()
    assert by_hand.four_counts(*settled(arjun, divya)) == (50, 25, 4, 1)


def test_seen_and_chance_for_the_80_is_0_9375_and_0_548():
    seen, chance = by_hand.seen_and_chance(50, 25, 4, 1)
    assert seen == pytest.approx(0.9375)
    assert chance == pytest.approx(0.548, abs=5e-4)


def test_kappa_from_the_80_is_0_862():
    seen, chance = by_hand.seen_and_chance(50, 25, 4, 1)
    assert by_hand.kappa_from(seen, chance) == pytest.approx(0.862, abs=5e-4)


def test_the_made_up_94_2_2_2_table_agrees_96_and_has_kappa_0_479():
    seen, chance = by_hand.seen_and_chance(94, 2, 2, 2)
    assert (seen, round(chance, 4)) == (0.96, 0.9232)
    assert by_hand.kappa_from(seen, chance) == pytest.approx(0.479, abs=5e-4)


@pytest.mark.parametrize("counts", [(50, 25, 4, 1), (94, 2, 2, 2),
                                    (45, 35, 10, 10), (10, 10, 10, 10)])
def test_the_hand_version_agrees_with_scorecard_judge(counts):
    a, d = table(*counts)
    seen, chance = by_hand.seen_and_chance(*by_hand.four_counts(a, d))
    assert seen == pytest.approx(agreement(a, d))
    assert by_hand.kappa_from(seen, chance) == pytest.approx(kappa(a, d))


def test_always_saying_pass_has_kappa_zero_whatever_the_other_says():
    a, _ = table(59, 26, 0, 0)
    seen, chance = by_hand.seen_and_chance(
        *by_hand.four_counts(a, ["pass"] * len(a)))
    assert by_hand.kappa_from(seen, chance) == pytest.approx(0)


def test_by_hand_prints_what_the_lesson_shows(capsys):
    assert printed("by_hand.py", capsys) == [
        '80 drafts where both said pass or fail',
        ('both pass 50 | both fail 25 | only Arjun passes 4 | only '
         'Divya passes 1'),
        'agreement seen 0.938, expected by chance 0.548',
        'kappa = 0.862',
        'scorecard on the 80: 0.938 0.862',
        'scorecard on all 100: 0.85 0.741',
    ]


def test_disagreements_prints_the_counts_and_three_drafts(capsys):
    out = printed("disagreements.py", capsys)
    assert out[0] == (
        "calls (Arjun, Divya): {('fail', 'fail'): 25, ('pass', 'unsure'): "
        "5, ('pass', 'pass'): 50, ('pass', 'fail'): 4, ('unsure', "
        "'unsure'): 10, ('unsure', 'pass'): 3, ('unsure', 'fail'): 2, "
        "('fail', 'pass'): 1}")
    assert [x for x in out if x.startswith("E-")] == [
        'E-0433  Refund came ₹99 short',
        'E-0505  Shipping charged but site says free',
        'E-0287  ek jacket wapas bheja']
    assert [x.split(":")[0] for x in out
            if x.startswith(("  Arjun,", "  Divya,"))] == [
        "  Arjun, unsure", "  Divya, pass", "  Arjun, fail",
        "  Divya, pass", "  Arjun, pass", "  Divya, fail"]


def test_paradox_prints_the_made_up_table_and_the_always_pass_reader(capsys):
    assert printed("paradox.py", capsys) == [
        'made up: agree 0.96, kappa 0.479',
        'always pass vs Arjun: agree 0.69, kappa 0.000, on 85 drafts',
    ]
