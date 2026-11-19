"""Lesson 04.5: correct a pass rate for the judge's two error rates.

Given: the held-out rates, the unlabelled sample and the lines that print.
You write `corrected` and `expected_raw`.

From this folder: uv run python correct_by_hand.py
"""
from plumbing import heldout_rates, raw_passes
from scorecard.stats import corrected_rate


def corrected(raw, tpr, tnr):
    """The true pass rate behind a judge's raw pass rate, given its
    pass-keeping rate tpr and catch rate tnr."""
    raise NotImplementedError(
        "TODO 04.5: return the true pass rate behind a raw pass "
        "rate from the judge's two rates, see the lesson's 'The "
        "correction' section")


def expected_raw(true, tpr, tnr):
    """The raw pass rate a judge with these two rates shows when the
    true pass rate is `true`: good drafts kept plus bad ones let through."""
    raise NotImplementedError(
        "TODO 04.5: return the raw pass rate a judge with these "
        "rates shows for a given true pass rate, see the lesson's "
        "'The correction' section")


if __name__ == "__main__":
    # Made up for the illustration: the judge passes 70% of the drafts,
    # keeps 90% of the good ones and holds back 80% of the bad ones.
    raw, tpr, tnr = 0.70, 0.90, 0.80
    true = corrected(raw, tpr, tnr)
    print(f"made up: corrected {true:.3f}")
    print(f"check: {expected_raw(true, tpr, tnr):.3f} should be {raw}")

    # Real: the chosen judge on the unlabelled sample, rates from held-out.
    tpr, tnr, passes, fails = heldout_rates()
    verdicts = raw_passes()
    raw = sum(verdicts) / len(verdicts)
    print(f"{len(verdicts)} drafts, judge passes {sum(verdicts)}: "
          f"raw {raw:.3f}")
    print(f"tpr {tpr:.3f} on {passes} passes, tnr {tnr:.3f} on {fails} fails")
    print(f"corrected {corrected(raw, tpr, tnr):.3f}",
          f"(scorecard: {corrected_rate(raw, tpr, tnr):.3f})")
