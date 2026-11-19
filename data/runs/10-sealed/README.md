# 10-sealed: the one opening of the sealed part of test set v1

**The sealed part is now spent.** Its 50 emails have been scored, and a version 2 of the test set needs fresh emails. Everything here was planned in `plan.md`, which was saved at 20:19 IST on 19 November 2026, before any sealed trace or draft was opened.

- Made by: `cd 10-what-to-measure/03-overfitting-the-test/solution && uv run --frozen python score_sealed.py` (needs Ollama and `qwen3.5:4b`). It refuses to run again once `scores.json` exists. `replay_sealed.py` in the same folder reads these files and calls no model.
- Opened: 19 November 2026, 20:20 to 20:22 IST. The first call returned in 1.9 seconds; the 50 together took 140 seconds of model time.
- Model and settings: `qwen3.5:4b`, thinking off (`reasoning_effort` none), temperature 0, `max_tokens` 1500 (as in `../04-heldout/`), one request at a time, no retries. The prompt is `../04-dev/prompt-v4.txt` (the same text as `../04-heldout/prompt.txt`), filled in as in lesson 04.4.
- Files: `judge.jsonl` holds the 50 replies (fields as in `../04-heldout/judge.jsonl`); `scores.json` holds each measure of the plan on the sealed part (hits, n, Wilson 95% range), the judge's counts and the `hd-2` comparison.
- Counts: 50 replies, every `finish_reason` is `stop`, longest 234 completion tokens. Verdicts: 30 PASS, 9 FAIL, 9 UNSURE, 2 with no verdict line. 50 live calls in all; `hd-2` was scored with code measures only.
- No bug was found in the script, no case was dropped, nothing was re-recorded and no check or prompt was changed after the numbers were seen.
- Fact-check, 19 November 2026: the scores were recomputed independently from the 50 sealed traces and `judge.jsonl` with a separate script (every rate and its Wilson range, the judge's 30 PASS, 9 FAIL, 9 UNSURE and 2 with no verdict, and the 23-pair `hd-2` comparison, also the open part's 87, 68 and 58 of 100). All matched `scores.json`. Nothing was changed because of them.
- No person has called these drafts, so the judge's two error rates cannot be measured here; only its pass share is.
