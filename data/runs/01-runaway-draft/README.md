# 01-runaway-draft: the one email hd-1 never finishes

`E-0722.json`: what `hd-1` writes for email E-0722 (week 4, a refund question in Tamil) when its reply is capped at 4,000 tokens.

`hd-1` sets no limit on a reply's length. For this email the model writes an opening, then repeats one paragraph without end, so the help desk's 300-second limit passes and no draft exists: its trace in `data/traces/hd-1/week-4.jsonl` (and in `hd-2`) has an empty `draft` and an `error`. This run shows what the model was writing.

- Command: `uv run python data/runs/01-runaway-draft/record.py` (needs Ollama).
- Model and settings: `qwen3.5:4b`, temperature 0, thinking off, `max_tokens` 4000; the same prompt and retrieved pages as `hd-1`.
- Recorded: 19 November 2026.
- Result: the reply stops only at the cap (`finish_reason` is `length`).
