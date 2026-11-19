# 04-heldout: the chosen judge, run once on the 100 held-out drafts

`judge.jsonl`: one record per held-out draft (ids in `labels/04-judge-set-ids.json`): `id`, `prompt`, `reply`, `finish_reason`, `completion_tokens`, `seconds`, `model`, `settings`, `recorded_at`. `prompt.txt` is the template that was used: a copy of `../04-dev/prompt-v4.txt`.

- Made by: `cd 04-trusting-a-judge/04-improving-a-judge/solution && uv run --frozen python judge_heldout.py v4 --live` (needs Ollama). Without `--live` it reads this file.
- The version was chosen on the development drafts before this run (highest sum of the two rates on the 97 drafts outside its examples), and this was the only run on these drafts.
- Model and settings: `qwen3.5:4b`, thinking off, temperature 0, `max_tokens` 1500, one request at a time, no retries.
- Recorded 19 November 2026, 19:12 to 19:16 IST. Count: 100 replies, all `stop`, longest 182 completion tokens; 1 reply has no verdict line (on a draft Arjun called unsure).
- Result against `labels/04-right-rule-arjun.csv` (59 pass, 26 fail, 15 unsure; the 15 left out): 38 of 59 passes kept (64.4%), 16 of 26 fails held back (61.5%; 12 of them with a FAIL verdict, 4 with UNSURE), 10 fails let through, 21 passes held back.
