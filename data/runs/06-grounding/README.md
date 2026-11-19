# 06-grounding: a model judge for "did the reply stick to the chunks it was shown?"

`judge.jsonl`: one record per question: `id`, `prompt` (the full request), `reply` (the model's full text), `model`, `settings`, `recorded_at`.

- Made by: `cd 06-retrieval-and-rag/05-grounded-answers/solution && uv run --frozen python judge_grounded.py --live`
- Model: `qwen3.5:4b` through Ollama, thinking off (`LLM_REASONING_EFFORT=none`), temperature 0, `max_tokens` 8000.
- The prompt shows the top 3 chunks hd-1 was given (from `runs/06-chunks/hd-1.jsonl`), the question and the drafted reply (from `runs/06-retrieval/hd-1.jsonl`), asks the model to list each claim as SUPPORTED or UNSUPPORTED, and to end with a PASS or FAIL line.
- Recorded 2026-11-19, 16:06 to 16:29 IST. Count: 60 replies, the longest about 20,000 characters, none cut off by the limit. 4 of them end after the list of claims with no PASS or FAIL line (Q-41, Q-52, Q-53, Q-55); the replay counts them as FAIL and says so.
- This replaces a first recording (15:40 to 15:48 earlier the same day, `max_tokens` 700, then a run at 4000) in which replies were cut off by the limit and counted as FAIL (11 at 700 tokens, 5 at 4000, one of them still cut off). The judge's numbers on that first recording (29 of 60 passed; 59% and 81%) are not used anywhere.
- Compared with `labels/06-answers-arjun.csv` (`grounded`) by the same script (without `--live` it replays and needs no model).
- Result: judge passes 31 of 60 (Arjun: 44); of Arjun's grounded answers it passes 64% (28 of 44), of his ungrounded it fails 81% (13 of 16); on the 56 replies with a verdict, 70% and 81%.
