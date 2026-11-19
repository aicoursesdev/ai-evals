# 07-refund-trials
`hd-1.jsonl`: the refund agent (`helpdesk/refunds.py`, prompt `helpdesk/versions/hd-1/refunds.md`) on each of the 30 scenarios in `scenarios/refunds.jsonl`: trial 0 at temperature 0, trials 1 to 5 at temperature 0.7 with seeds 1 to 5 (`trial` is the seed). Full trajectories of tool calls. `outcome` is `null` when the final message held no valid outcome.

- Command: `uv run python scripts/record.py refunds`
- Model `qwen3.5:4b` through Ollama, thinking off, tools `get_order`, `check_policy`, `propose_refund` over `orders.db`, at most 6 model calls per run.
- Recorded 2026-11-19. Lines: 180 (trial 0: 30, trial 1: 30, trial 2: 30, trial 3: 30, trial 4: 30, trial 5: 30).
