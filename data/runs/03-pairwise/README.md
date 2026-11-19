# 03-pairwise: a model judge picks the better of two drafts, in both orders

`pairs.jsonl`: one record per request: `id` (the email), `a` and `b` (which help desk version was shown as Reply A and as Reply B), `prompt` (the full request), `reply` (the model's full text), `finish_reason`, `completion_tokens`, `model`, `settings`, `recorded_at`.

- Made by: `cd 03-graders/07-pairwise-comparison/solution && uv run --frozen python pairwise.py --live` (needs Ollama). Without `--live` the same script replays this file and calls no model; `swap_report.py` reads it.
- The pairs: 60 emails, 30 from week 3 and 30 from week 4 of the log (E-0722, whose hd-1 draft is empty, left out), drawn with `random.Random(3).sample`. For each, `hd-1`'s draft and `hd-2`'s draft (`traces/hd-1/`, `traces/hd-2/`) and the three pages hd-1 was shown (retrieval is the same in both versions). Each pair is asked twice, once with hd-1 as Reply A and once with hd-2 as Reply A: 120 requests.
- Model and settings: `qwen3.5:4b` through Ollama, thinking off (`reasoning_effort` none), temperature 0, `max_tokens` 1500, one request at a time, no retries.
- The prompt asks which reply the judge would rather send (answers what the customer asked, correct against the pages, promises nothing the pages do not support), at most three sentences of reasoning, then a last line with A, B or TIE.
- Recorded 19 November 2026, 17:55 to 18:04 IST. Count: 120 replies; every `finish_reason` is `stop` (none cut off); every reply has a verdict line; 91 completion tokens on average, 144 at most.
- Result (from `swap_report.py`): the reply shown first won 79 of 120, the second 40, 1 tie. With hd-1 first: hd-1 won 45, hd-2 14, 1 tie. With hd-2 first: hd-2 won 34, hd-1 26. Over the 60 pairs, the two orders agreed on hd-1 for 22, on hd-2 for 10, and split on 28. hd-1's draft is the longer one in 52 of 60 pairs.
