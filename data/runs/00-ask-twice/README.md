# 00-ask-twice: the same 10 week-1 emails, asked six times

Six files, one record per email, in the order of the emails: `temp-0.jsonl` (temperature 0, no seed) and `temp-0.7-seed-1.jsonl` to `temp-0.7-seed-5.jsonl` (temperature 0.7, seeds 1 to 5). Each record is the trace `helpdesk.pipeline.handle` returns (triage, retrieved passages, draft, citations, tokens, seconds), written as it came back.

- Emails: every 15th email of `emails/log-week-1.jsonl` (`E-0151`, `E-0166`, ... `E-0286`), 10 in all.
- Made by: `00-hello-evals/04-same-question-twice/solution/record_repeats.py`, which calls `handle(email, temperature=..., seed=...)` with version `hd-1`.
- Model: `qwen3.5:4b` through Ollama, thinking off. Date: 2026-11-19, on a laptop shared with other jobs (the `seconds` field is not a speed measurement).
- Count: 6 files, 60 traces.
- What it shows: at temperature 0 all 10 triage labels and drafts are identical to the original `traces/hd-1/week-1.jsonl` records; at temperature 0.7 all 10 emails got a different draft in each of the 5 runs.
