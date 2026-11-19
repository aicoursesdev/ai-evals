"""Project 04: the validation report, printed as Markdown from the
recordings.

Given: the recordings (plumbing.py) and the lines that print.
You write `rates_section`, `agreement_section`, `corrected_section` and
`bias_section`; each returns the lines of one section.

From this folder: uv run python report.py
"""
from plumbing import (bias_data, first_won, heldout_rates, raw_passes,
                      three_callers)
from scorecard.judge import agreement, kappa
from scorecard.stats import corrected_interval, corrected_rate


def rates_section():
    """The judge's two error rates on the held-out drafts."""
    kept, held, passes, fails = heldout_rates()
    return ["## Two error rates (held-out, against Arjun)",
            f"- passes kept: {round(kept * passes)} of {passes} "
            f"({kept:.1%})",
            f"- fails held back: {round(held * fails)} of {fails} "
            f"({held:.1%})"]


def agreement_section():
    """Agreement and kappa for the three pairs, on the same drafts."""
    ids, a, d, j = three_callers()
    lines = [f"## Agreement on the {len(ids)} drafts both people settled"]
    for who, x, y in (("Arjun with Divya", a, d), ("judge with Arjun", j, a),
                      ("judge with Divya", j, d)):
        lines.append(f"- {who}: {agreement(x, y):.1%}, "
                     f"kappa {kappa(x, y):.2f}")
    return lines


def corrected_section():
    """The raw and corrected pass rate on the unlabelled drafts, with
    the 95% range."""
    kept, held, passes, fails = heldout_rates()
    raw = raw_passes()
    p = sum(raw) / len(raw)
    low, high = corrected_interval(p, len(raw), kept, held, passes, fails)
    return [f"## Corrected pass rate on {len(raw)} unlabelled drafts",
            f"- raw {p:.1%}, corrected {corrected_rate(p, kept, held):.1%}, "
            f"95% range {low:.0%} to {high:.0%}"]


def bias_section():
    """The position, length and asking-twice tests, one line each."""
    sample, base, padded, again, hot = bias_data()
    first, total = first_won()
    warm = [sum(v == "pass" for v in r.values()) / len(r)
            for r in hot.values()]
    return ["## Bias and consistency tests",
            "- position (lesson 03.7, a comparison judge): the reply "
            f"shown first won {first} of {total}",
            f"- length: {len(sample)} drafts plus 34 words of filler, "
            f"verdict changed on {sum(base[i] != padded[i] for i in sample)}"
            f"; passes {sum(base[i] == 'pass' for i in sample)} to "
            f"{sum(padded[i] == 'pass' for i in sample)}",
            "- asking twice: same verdict at temperature 0 on "
            f"{sum(base[i] == again[i] for i in sample)} of {len(sample)}; "
            f"pass rate over five runs at 0.7: {min(warm):.1%} to "
            f"{max(warm):.1%}"]


if __name__ == "__main__":
    sections = [rates_section(), agreement_section(), corrected_section(),
                bias_section()]
    print("\n\n".join("\n".join(lines) for lines in sections))
