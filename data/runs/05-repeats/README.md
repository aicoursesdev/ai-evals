# 05-repeats
Asking the same question many times. `sample-ids.json` holds 100 week-4 email ids (`emails/log-hd-1-qwen3.5-2b.jsonl`), in two draws:

1. 100 ids drawn with `random.Random(7).sample` from the sorted week-4 ids.
2. Ten of them (E-0694, E-0615, E-0712, E-0632, E-0671, E-0673, E-0740, E-0647, E-0714, E-0645) were in the sealed part of the test set (`testsets/v1/sealed.jsonl`) as it was then drawn, so their recorded lines were deleted (filtered by id, unread) and ten replacements were drawn with `random.Random(7).sample(pool, 10)`, pool = the sorted week-4 ids not in the first draw, not sealed and not E-0722 (its reply never ends; see `runs/01-runaway-draft/`; 43 ids). They are the last ten of `sample-ids.json` (E-0679, E-0633, E-0690, E-0612, E-0617, E-0707, E-0628, E-0686, E-0724, E-0703); the other 90 keep their order.

The sealed part has been redrawn since; `sample-ids.json` as it stands is the sample. `scripts/record.py` refuses to run if the sample holds a sealed id or E-0722, and `scripts/check_data.py` fails if any file in this folder holds a sealed id.

- `triage-seeds.jsonl`: hd-1's triage step only, temperature 0.7, seeds 1 to 20 on the 100 emails (2,000 calls). Command: `uv run python scripts/record.py repeats-triage`. Lines: 2000.
- `draft-seeds.jsonl`: hd-1's full pipeline (trace records), temperature 0.7, seeds 1 to 5 on the same 100 (500). Command: `uv run python scripts/record.py repeats-draft`. Lines: 500. One draft never ended: E-0686 at seed 5 (1 of 500) has `draft` empty and an `error` saying the reply did not end within the help desk's 300-second limit, as E-0722's trace does (`runs/01-runaway-draft/`); it was recorded once and not retried.
- Model `qwen3.5:4b` through Ollama (thinking off, `reasoning_effort: none`), embeddings `qwen3-embedding:0.6b`, version `hd-1` (`helpdesk/versions/hd-1/`). Recorded 2026-11-19.
