# 06-chunks: the chunks hd-1 retrieved for the 60 retrieval questions

`hd-1.jsonl`: one record per question of `questions/retrieval.jsonl`: `id` and `chunks`, the top 10 chunks in rank order with `rank`, `article_id`, `section` (the `##` heading, or `(intro)`), `score`, `has_quote` (the question's `answer_quote` is in the chunk, ignoring spaces, bold marks and table bars) and `text`.

- Made by: `06-retrieval-and-rag/04-retrieval-test-sets/solution/record_chunks.py` (needs Ollama with `qwen3-embedding:0.6b`).
- It calls `helpdesk.search.search(question, k=10)`, the call hd-1 makes, and asserts every article id and score matches `runs/06-retrieval/hd-1.jsonl` (scores within 0.002). All 60 matched.
- Embedding model: `qwen3-embedding:0.6b` through Ollama. Date: 2026-11-19. Count: 60 questions, 600 chunks.
