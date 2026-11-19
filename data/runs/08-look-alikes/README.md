# 08-look-alikes: hd-1 on 30 harmless look-alike emails

The 30 honest customer emails in `data/attacks/look-alikes.jsonl` (`L-01` to `L-30`, in the log's format), run through `helpdesk.pipeline.handle` with version `hd-1`, live, one trace per email in `hd-1.jsonl` (same fields as `data/traces/hd-1/`).

- Command: `uv run --frozen python record_look_alikes.py` from `08-safety-and-rare-failures/02-two-kinds-of-wrong/solution/` (it was run twice at once, the second time with `--reverse`, to share the job; each email was recorded once).
- Model: `qwen3.5:4b` through Ollama, thinking off, temperature 0, no seed, `k` 3, archived pages not filtered (hd-1's settings).
- Recorded: 19 November 2026, between 15:40 and 15:56 IST, on a laptop shared with other recording jobs (`recorded_at` in each line is exact).
- Counts: 30 emails, 30 traces. Judged by reading in `data/labels/08-look-alike-outcomes.csv` (27 handled, 3 escalated, none refused, none treated as an attack); 10 replies also contain a wrong or invented statement, listed there.
- Live replies differ in wording if rerun.
- Eight emails (`L-07`, `L-12`, `L-13`, `L-17`, `L-20`, `L-21`, `L-23`, `L-30`) were edited after the first recording, because their order numbers or dates did not fit `orders.db` (another customer's order, an order already delivered in October, a wrong item that the order did not hold); `L-02`'s subject was edited to match its body. Those nine were recorded again on 19 November 2026 (about 16:10 IST), and the judgements were redone.
