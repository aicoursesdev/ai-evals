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
    raise NotImplementedError(
        "TODO 04.7: return the lines of the two-rates section, "
        "each rate with its counts, see the lesson's 'The report' "
        "section")


def agreement_section():
    """Agreement and kappa for the three pairs, on the same drafts."""
    raise NotImplementedError(
        "TODO 04.7: return the lines of the agreement section: "
        "Arjun with Divya, the judge with Arjun and the judge "
        "with Divya on the same drafts, see the lesson's 'The "
        "report' section")


def corrected_section():
    """The raw and corrected pass rate on the unlabelled drafts, with
    the 95% range."""
    raise NotImplementedError(
        "TODO 04.7: return the lines of the corrected pass rate "
        "section, with its 95% range, see the lesson's 'The "
        "report' section")


def bias_section():
    """The position, length and asking-twice tests, one line each."""
    raise NotImplementedError(
        "TODO 04.7: return the lines of the bias section: "
        "position, length and asking twice, see the lesson's 'The "
        "report' section")


if __name__ == "__main__":
    sections = [rates_section(), agreement_section(), corrected_section(),
                bias_section()]
    print("\n\n".join("\n".join(lines) for lines in sections))
