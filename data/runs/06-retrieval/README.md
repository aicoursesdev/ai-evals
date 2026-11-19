# 06-retrieval
`hd-1.jsonl`: for each of the 60 questions in `questions/retrieval.jsonl`, the top 10 retrieved chunks (article id, score, rank) and the answer hd-1 drafted from its top 3 (`k` = 3, archived articles not filtered). Each question is sent through `handle()` as an email with no subject.

- Command: `uv run python scripts/record.py retrieval`
- Model `qwen3.5:4b` through Ollama (thinking off, `reasoning_effort: none`), embeddings `qwen3-embedding:0.6b`, version `hd-1` (`helpdesk/versions/hd-1/`). Temperature 0.
- Recorded 2026-11-19. Lines: 60.
