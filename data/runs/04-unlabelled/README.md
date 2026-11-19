# 04-unlabelled: the chosen judge on 250 logged drafts nobody has labelled

`judge.jsonl`: one record per draft: `id`, `prompt`, `reply`, `finish_reason`, `completion_tokens`, `seconds`, `model`, `settings`, `recorded_at`. `sample-ids.json` holds the 250 ids.

- The sample: drawn with `random.Random(5).sample` from the sorted logged ids that are in none of the open part, the held-out set or the sealed part (350 ids; `scorecard.graders.logged` never reads the sealed part).
- Made by: `cd 04-trusting-a-judge/05-correcting-a-score/solution && uv run --frozen python judge_unlabelled.py --live` (needs Ollama), with the prompt in `../04-heldout/prompt.txt`.
- Model and settings: `qwen3.5:4b`, thinking off, temperature 0, `max_tokens` 1500, one request at a time, no retries.
- Recorded 19 November 2026, 19:15 to 19:25 IST. Count: 250 replies, all `stop`, longest 400 completion tokens; 9 replies have no verdict line. Verdicts: pass 133, fail 51, unsure 57, none 9.
