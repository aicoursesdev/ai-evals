# 09-judge-swap: the chosen judge prompt, run by a smaller model on the 100 held-out drafts

`judge.jsonl`: one record per held-out draft (ids in `labels/04-judge-set-ids.json`, the same 100 as `../04-heldout/`): `id`, `prompt` (the full request, identical to the one in `../04-heldout/judge.jsonl`), `reply`, `finish_reason`, `completion_tokens`, `seconds`, `model`, `settings`, `recorded_at`.

- Made by: `cd 09-evals-that-keep-running/08-model-changes/solution && uv run --frozen python judge_swap.py --live` (needs Ollama and `ollama pull qwen3.5:2b`). Without `--live` the script reads this file and calls no model.
- Model and settings: `qwen3.5:2b` (set for the run with `LLM_MODEL`, through `helpdesk.llm`), thinking off (`reasoning_effort` none), temperature 0, `max_tokens` 1500 (as in `../04-heldout/`), one request at a time, no retries, 180-second limit per request (none came near it).
- Recorded 19 November 2026, 19:45 to 19:46 IST. The first call returned in 2.9 seconds; the slowest also took 2.9 seconds; the 100 together took 65 seconds.
- Count: 100 replies; every `finish_reason` is `stop` (none cut off); longest reply 194 completion tokens. 29 replies have no verdict line (the last line is not alone PASS, FAIL or UNSURE: each ends its last sentence with the verdict word instead); of the rest 16 PASS, 45 FAIL, 10 UNSURE.
- Result against `labels/04-right-rule-arjun.csv` (59 pass, 26 fail, 15 unsure left out; a judge passes only on a clear PASS): 9 of 59 passes kept (15.3%), 21 of 26 fails held back (80.8%). The usual model's recording, `../04-heldout/`, kept 38 of 59 and held back 16 of 26.
