# Is hd-2 really better than hd-1?

**To:** Meera. **From:** the evals owner. **Date:** 19 November 2026.

## The answer

Not shown. On the one thing we can count for free, hd-2's drafts set off the code checks less often, by about five points, and luck alone would rarely give a gap this large. But that is not the same as better replies, and a second view leans the other way. Nobody has yet read the emails that changed.

## What was compared, and what was held fixed

- The 277 emails of weeks 3 and 4 of the log that both versions answered (the 23 sealed emails are left out; E-0722 is counted, with an empty draft under both versions).
- Same emails, same triage and retrieval, same model (qwen3.5:4b, temperature 0), recorded on one laptop on 19 November 2026. The only change is the draft prompt: warmer and shorter (a median of 70 words against 89).
- Outcome: no Module 03 check fires on the draft. These checks are careful but narrow and catch only some failures, so this is not "the draft is good".

## Result

| | n | no check fires | 95% range |
| --- | --- | --- | --- |
| hd-1 | 277 | 211 (76.2%) | 70.8% to 80.8% |
| hd-2 | 277 | 226 (81.6%) | 76.6% to 85.7% |

Same emails, as pairs: 199 clean under both, 39 firing under both, 12 only clean under hd-1, 27 only clean under hd-2. Difference (hd-2 minus hd-1): +5.4 points, 95% range +1.0 to +9.8 (bootstrap +1.1 to +9.7). McNemar exact p = 0.024 on the 39 emails that changed. Compared as two separate scores, the range would be -1.4 to +12.2, which is why the pairing matters.

The biggest single difference is one check, "claims an action": it fires on 10 of hd-1's drafts and 2 of hd-2's; on 8 emails it fires only on hd-1's draft and on none only on hd-2's (p = 0.008). The other six checks show no clear difference (the closest, missing or old page and asking for a known order id, are 11 against 7). Seven checks were looked at, which makes one lucky win likelier: against 0.05 / 7 = 0.007, 0.008 just misses. Without that check the other six leave 13 emails clean only under hd-1 and 21 only under hd-2 (p = 0.229), so it carries about half of the gain, not all of it.

Second view: the order-swap judge (60 emails, both orders, 03.7): hd-1 won both orders on 22, hd-2 on 10, 28 split. It leans to hd-1, but it favours the first-shown reply and hd-1's drafts are longer, so this is not a clean verdict. Length is not an easy explanation for the checks: among hd-1's drafts, 15% of those of 100 words or more set off a check and 31% of those of 60 to 80.

## What this does not cover

Sampling wobble only. It says nothing about wrong labels, other models or machines, or other weeks. A person has not read the 39 emails that changed.

## Recommendation

Do not report hd-2 as better. It can stay in draft mode, since a person reads every draft. Before deciding, Arjun reads the 39 changed pairs without knowing which version wrote which, and says which draft he would send. If hd-2 wins that reading, adopt it. If not, the drop in "claims an action" is a finding to keep, not a reason to switch.
