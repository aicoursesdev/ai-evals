"""Lesson 03.3: measure every check against the 100 coded drafts.

Precision: of the drafts a check flags, the share the map agrees fail in
the way the check is meant to catch. Recall: of the drafts the map says
fail that way, the share the check flags.

From this folder: uv run python measure.py
"""
import plumbing
from scorecard.graders import CHECKS, precision_recall

emails, traces = plumbing.emails_by_id(), plumbing.traces_by_id()
coded = plumbing.coded()

print(f"{'check':<20} flags right real caught  precision  recall")
for name, (check, wanted) in CHECKS.items():
    flagged = {i for i in coded if check(emails[i], traces[i])}
    real = {i for i, types in coded.items() if types & wanted}
    p, r = precision_recall(flagged, real)
    print(f"{name:<20} {len(flagged):>5} {len(flagged & real):>5} "
          f"{len(real):>4} {len(flagged & real):>6}  {p:>9.0%} {r:>7.0%}")
