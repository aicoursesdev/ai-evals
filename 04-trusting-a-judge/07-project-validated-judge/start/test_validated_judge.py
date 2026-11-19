"""Project 04: the validation report, one section at a time.

No model and no network: every number comes from a recorded run in the repo.
From the top folder: make check 04.7
"""
import runpy
from pathlib import Path

import pytest

import report
from plumbing import (RUNS, arjun, bias_data, first_won, held_out,
                      heldout_rates, raw_passes, three_callers, verdicts)
from scorecard.judge import agreement, kappa, rates
from scorecard.stats import corrected_interval, corrected_rate

HERE = Path(__file__).parent

THE_REPORT = [
    '## Two error rates (held-out, against Arjun)',
    '- passes kept: 38 of 59 (64.4%)',
    '- fails held back: 16 of 26 (61.5%)',
    '',
    '## Agreement on the 80 drafts both people settled',
    '- Arjun with Divya: 93.8%, kappa 0.86',
    '- judge with Arjun: 63.7%, kappa 0.24',
    '- judge with Divya: 57.5%, kappa 0.12',
    '',
    '## Corrected pass rate on 250 unlabelled drafts',
    '- raw 53.2%, corrected 56.8%, 95% range 6% to 100%',
    '',
    '## Bias and consistency tests',
    ('- position (lesson 03.7, a comparison judge): the reply shown first '
     'won 79 of 120'),
    ('- length: 30 drafts plus 34 words of filler, verdict changed on 10; '
     'passes 19 to 16'),
    ('- asking twice: same verdict at temperature 0 on 29 of 30; pass rate '
     'over five runs at 0.7: 30.0% to 56.7%'),
]


def test_the_rates_section_gives_both_rates_with_their_counts():
    assert report.rates_section() == THE_REPORT[:3]


def test_the_agreement_section_uses_the_same_80_drafts_for_all_three_pairs():
    ids, a, d, j = three_callers()
    assert len(ids) == len(a) == len(d) == len(j) == 80
    assert report.agreement_section() == THE_REPORT[4:8]


def test_the_agreement_section_matches_scorecard_judge():
    _, a, d, j = three_callers()
    expected = [f"- {who}: {agreement(x, y):.1%}, kappa {kappa(x, y):.2f}"
                for who, x, y in (("Arjun with Divya", a, d),
                                  ("judge with Arjun", j, a),
                                  ("judge with Divya", j, d))]
    assert report.agreement_section()[1:] == expected


def test_the_rates_come_from_the_held_out_drafts_not_the_development_ones():
    kept, held, passes, fails = heldout_rates()
    human, seen = arjun("04-right-rule-arjun"), verdicts(
        RUNS / "04-heldout" / "judge.jsonl")
    ids = [i for i in held_out() if human[i] != "unsure"]
    person = [human[i] == "pass" for i in ids]
    judged = [seen[i] == "pass" for i in ids]
    assert (kept, held) == pytest.approx(rates(person, judged))
    assert (passes, fails) == (59, 26)


def test_the_corrected_section_matches_scorecard_stats():
    kept, held, passes, fails = heldout_rates()
    raw = raw_passes()
    p = sum(raw) / len(raw)
    low, high = corrected_interval(p, len(raw), kept, held, passes, fails)
    assert report.corrected_section() == [
        THE_REPORT[9],
        f"- raw {p:.1%}, corrected {corrected_rate(p, kept, held):.1%}, "
        f"95% range {low:.0%} to {high:.0%}"]
    assert report.corrected_section() == THE_REPORT[9:11]


def test_the_bias_section_has_a_line_for_each_test():
    lines = report.bias_section()
    assert lines == THE_REPORT[12:]
    assert [x.split(":")[0] for x in lines[1:]] == [
        "- position (lesson 03.7, a comparison judge)", "- length",
        "- asking twice"]


def test_the_bias_recordings_cover_the_same_30_drafts():
    sample, base, padded, again, hot = bias_data()
    assert len(sample) == 30
    assert all(i in padded and i in again for i in sample)
    assert sorted(hot) == [1, 2, 3, 4, 5] and first_won() == (79, 120)


def test_report_prints_the_four_sections_the_lesson_shows(capsys):
    runpy.run_path(str(HERE / "report.py"), run_name="__main__")
    out = [x.rstrip() for x in capsys.readouterr().out.splitlines()]
    assert out == THE_REPORT
