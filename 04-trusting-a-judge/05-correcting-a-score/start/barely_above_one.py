"""Lesson 04.5: what happens when the two rates add up to barely over one."""
from plumbing import heldout_rates, raw_passes
from scorecard.stats import corrected_interval, corrected_rate

verdicts = raw_passes()
raw, n = sum(verdicts) / len(verdicts), len(verdicts)
tpr, tnr, m1, m0 = heldout_rates()
print(f"raw pass rate {raw:.3f} on {n} drafts; calibration {m1} + {m0}")
print("rates are made up except the third row")
print("  tpr   tnr   sum  corrected  95% range")
for t, s in ((0.90, 0.90), (0.80, 0.80), (tpr, tnr), (0.60, 0.50),
             (0.55, 0.50)):
    if t + s <= 1:
        print(f"{t:5.3f} {s:5.3f} {t + s:5.2f}  no estimate: tpr + tnr <= 1")
        continue
    low, high = corrected_interval(raw, n, t, s, m1, m0)
    print(f"{t:5.3f} {s:5.3f} {t + s:5.2f}  {corrected_rate(raw, t, s):8.3f}"
          f"   {low:.3f} to {high:.3f}")
