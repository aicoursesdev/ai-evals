# Plan for opening the sealed part of test set v1

Written and saved on **Thursday 19 November 2026 at 20:19 IST**, before any sealed trace or sealed draft was opened, by the writer of lesson 10.3. The sealed part is `data/testsets/v1/sealed.jsonl`: 50 logged emails (27, 16 and 7 from weeks 2, 3 and 4). Until this plan was saved, nothing had read what the help desk wrote for them.

## What will be computed, and on what

On the sealed part, once, with `10-what-to-measure/03-overfitting-the-test/solution/score_sealed.py`, for `hd-1` (the version that wrote every draft in the log). Every rate is given as hits out of n with its Wilson 95% range (`scorecard.stats.wilson`).

1. **Triage right**: the triage category equals the email's own label (`scorecard.graders.label_correct`).
2. **Each of the seven code checks**, as the share of emails where it fires (`scorecard.graders.CHECKS`: wrong script, missing or old page, reply to spam, invented address, claims an action, asks for known id, empty draft).
3. **No check fires**: none of the seven fires.
4. **The chosen judge**: version 4 (`data/runs/04-dev/prompt-v4.txt`, the same text as `data/runs/04-heldout/prompt.txt`), criterion "right rule", on all 50 sealed drafts, as the share of replies with a clear PASS. 50 live calls to `qwen3.5:4b`, settings as `data/runs/04-heldout/` (temperature 0, `max_tokens` 1500, thinking off, one request at a time, no retries). No person has called these drafts, so the judge's two rates cannot be measured on this part; only its pass share is reported, beside the open part's.
5. `hd-2` answered weeks 3 and 4 only, so 23 sealed emails have an `hd-2` trace. On those 23, `hd-2` and `hd-1` are scored on measures 1 and 3 and compared as pairs. 23 pairs cannot decide anything and the result will be said to be that. No judge call is made for `hd-2`. Total live calls: 50.

## The same measures on the open part (computed first)

`open_scores.py`, from the 100 open emails' traces, hd-1:

| Measure | Open part | 95% range |
| --- | --- | --- |
| triage right | 87 of 100 (87.0%) | 79.0% to 92.2% |
| wrong script fires | 2 of 100 | 0.6% to 7.0% |
| missing or old page fires | 10 of 100 | 5.5% to 17.4% |
| reply to spam fires | 6 of 100 | 2.8% to 12.5% |
| invented address fires | 2 of 100 | 0.6% to 7.0% |
| claims an action fires | 10 of 100 | 5.5% to 17.4% |
| asks for known id fires | 6 of 100 | 2.8% to 12.5% |
| empty draft fires | 1 of 100 | 0.2% to 5.4% |
| no check fires | 68 of 100 (68.0%) | 58.3% to 76.3% |
| judge v4, clear PASS | 58 of 100 (58.0%) | 48.2% to 67.2% |

(The open part is where the checks were written and the judge's prompt was shaped, and the three drafts that are examples in version 4's prompt are among the 100.)

## The rule: was the open part's score honest, or did tuning spend it?

For each measure, put the open part's score beside the sealed part's 95% range:

- **Honest.** The open part's score lies inside the sealed range. The test cannot tell the two apart. This is not proof that nothing was spent: with 50 emails a range is about 20 points wide.
- **Tuning spent it.** The open part's score lies above the top end of the sealed range, for the measures where a higher score is better for the help desk (triage right, no check fires, judge PASS share). The open score then flattered the system by more than luck over 50 emails explains.
- **Neither.** The open part's score lies below the bottom end of the sealed range. That is not the pattern of tuning, and it will be reported as it is, with the reason left open.
- For the seven "fires" rates, the same comparison is made but no verdict of "spent" is given: the checks were written by reading the open drafts, which is the point of them, and the rates are reported as a table only.

## After the opening

- Nothing in the suite (the checks, the judge prompt, the settings) is changed. If a script has a bug, the bug is fixed and said so in the run's README; the judge's recorded verdicts are never re-recorded; no case is dropped.
- The sealed part is then spent: the run folder says so, and a version 2 of the test set needs fresh emails.
- After the opening every lesson script replays `data/runs/10-sealed/`; nothing else opens a sealed trace.

## The decision rule of the final report (written now, before any count by kind of email)

A **kind of email** (one of the eleven categories Arjun's labels use) may go out unread only if all four hold:

1. **Read.** A person has read, under a written rule, at least 59 drafts of that kind, and none had a failure that matters. 59 is the smallest number of clean reads whose exact one-sided 95% upper limit on the failure rate is 5% or less (`ceil(ln 0.05 / ln 0.95)`, as in lesson 08.7).
2. **Checks.** No code check fires on any of those drafts, and every check has passed its own known cases.
3. **Safety.** The safety gate's rows for every harm that kind of email can touch are "proven under" their limits.
4. **Watched.** The gate of Module 09 stands in front of every change, and a person reads a weekly random sample of what went out unread.

A kind that fails any of the four stays with a person: every draft is read before it is sent.
