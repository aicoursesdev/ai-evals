# 04-bias: three small experiments on the chosen judge

`length.jsonl` (30 records), `again-t0.jsonl` (30) and `again-t07.jsonl` (150; a `trial` field, 1 to 5): `id`, `prompt`, `reply`, `finish_reason`, `completion_tokens`, `seconds`, `model`, `settings`, `recorded_at`. `sample-ids.json` holds the 30 ids.

- The sample: 30 of the 90 development drafts Arjun called pass (20 here) or fail (10 here), drawn with `random.Random(6).sample` from the sorted ids. The prompt is the chosen judge's (`../04-heldout/prompt.txt`).
- `length.jsonl`: each draft with a filler paragraph of 34 words added after its last line ("Thank you for choosing Tidewater Goods. ..." in `bias_runs.py`); no rule or promise in it. Drafts average 87 words.
- `again-t0.jsonl`: the same unpadded prompts again at temperature 0. `again-t07.jsonl`: the same prompts at temperature 0.7 with seeds 1 to 5, one run per trial. The first run at temperature 0 is the chosen judge's development recording, `../04-dev/v4.jsonl`.
- Made by: `cd 04-trusting-a-judge/06-judge-biases/solution && uv run --frozen python bias_runs.py --live` (needs Ollama). Without `--live` it reads these files. Position bias reuses `../03-pairwise/`, not re-recorded.
- Model and settings: `qwen3.5:4b`, thinking off, `max_tokens` 1500, one request at a time, no retries.
- Recorded 19 November 2026, 19:25 to 19:33 IST. Count: 210 replies, every `finish_reason` is `stop`, longest 199 completion tokens; no verdict line in 1 reply of `length.jsonl`, 1 of `again-t0.jsonl` and 5 of `again-t07.jsonl`.
- Results (`length_test.py`, `again_test.py`, `position_test.py`): padded, the verdict changed on 10 of 30 (the judge passes 19 unpadded, 16 padded); at temperature 0 asked twice, the same verdict on 29 of 30; at temperature 0.7 the judge passes 43.3%, 36.7%, 56.7%, 30.0% and 50.0% of the 30 in the five runs, and all six runs agree on 4 of 30 drafts.
- One of the 30 drafts, E-0398, is also one of the three examples inside the chosen prompt (see `../04-dev/README.md`); its unpadded verdict is pass, its padded reply has no verdict line, and at temperature 0.7 it gets unsure in three runs and pass in two.
