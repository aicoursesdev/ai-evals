# Which emails may go out unread?

## Decision

No kind of email may go out unread yet. Keep draft mode: a person reads every draft before it is sent, for all eleven kinds. A kind may go out unread when a person has read 59 of its drafts with none failing; the best-read kind, shipping delay, has 21 reads and 19 failures.

## Evidence

- open drafts a reader found fine: 23 of 100 (23.0%), 95% range 15.8% to 32.2% [labels/01-coded.csv]
- random weekly sample found fine: 5 of 20 (25.0%), 95% range 11.2% to 46.9% [labels/09-weekly-sample]
- quiet drafts a reader found failing: 45 of 68 (66.2%), 95% range 54.3% to 76.3% [labels/01-coded.csv, graders.CHECKS]
- triage right, open: 87 of 100 (87.0%), 95% range 79.0% to 92.2% [testsets/v1/open]
- triage right, sealed: 45 of 50 (90.0%), 95% range 78.6% to 95.7% [runs/10-sealed]
- no check fires, sealed: 36 of 50 (72.0%), 95% range 58.3% to 82.5% [runs/10-sealed]
- judge: bad drafts held back: 16 of 26 (61.5%), 95% range 42.5% to 77.6% [runs/04-heldout]
- judge: good drafts kept: 38 of 59 (64.4%), 95% range 51.7% to 75.4% [runs/04-heldout]
- refund agent right, one run: 20 of 30 (66.7%), 95% range 48.8% to 80.8% [runs/07-refund-trials]
- attacks that got through: 14 of 40 (35.0%), 95% range 22.1% to 50.5% [labels/08-attack-outcomes]
- hd-2 no check fires: 226 of 277 (81.6%), 95% range 76.6% to 85.7% [traces/hd-2]
- hd-1 no check fires, same emails: 211 of 277 (76.2%), 95% range 70.8% to 80.8% [traces/hd-1]

## Uncertainty

- Every call is one reader's, under a written rule, not the truth; two careful readers agreed on 75 of 80 drafts (04.7).
- The sealed part's 50 drafts were never read by a person, and it is now spent.
- The refund agent gets three tries in a row right 30.7% of the time, estimated from five tries on each of 30 scenarios (07.7).
- The attack suite is fixed: tool results and an attacker who adapts were not tried.
- hd-2 leaves the checks quiet more often, but nobody has read the emails that changed, so it is not shown to be better.
- One shop, four weeks including a sale, one small local model.

## Cost

- Writing a draft: 1,733 tokens an email on average (550 log emails).
- The seven checks run in about 0.05 milliseconds a draft; the judge takes about 2.2 seconds a verdict.
- A person at an assumed 60 s a draft: about 400 emails a week is 6 hours 40 minutes; the weekly sample of 25 is 25 minutes.

## What would change this

- 59 drafts of one kind read clean (none failing), with the safety rows for its harms proven under their limits.
- A judge that holds back far more than 16 of 26 bad drafts, measured on fresh drafts that people have called.
- A new version that fixes the largest failure types, read by a person.
