# 09-model-swap
`hd-1-qwen3.5-2b.jsonl`: hd-1's prompts and settings with `qwen3.5:2b` in place of `qwen3.5:4b` (a smaller model of the same family; pulled with `ollama pull qwen3.5:2b`), temperature 0, thinking off, on the open part of the test set (`testsets/v1/open.jsonl`) plus the launch set's `test` split. Sealed emails and E-0722 are skipped. Each request had a 120-second limit and one request at a time ran; a case over it would be recorded with an `error`. Embeddings stay `qwen3-embedding:0.6b`.

- Command: `uv run python scripts/record.py swap`
- Recorded 2026-11-19. Lines: 149.
