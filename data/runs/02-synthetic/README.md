# 02-synthetic: the help desk on the 20 made-up cases

`hd-1.jsonl`: one trace per case of `testsets/v1/synthetic.jsonl` (`S-01` to `S-20`), written by `helpdesk.pipeline.handle` with the `hd-1` prompts, in the same fields as `traces/hd-1/`.

- Command: `uv run python 02-test-sets/04-synthetic-cases/solution/run_synthetic.py` from `labs/evals/` (needs Ollama). One request at a time, no retries; a case whose reply never ends would be recorded with an `error`. None did: all 20 finished, 7 to 16 seconds each.
- Model and settings: `qwen3.5:4b`, temperature 0, thinking off, `k` 3, the settings in `helpdesk/versions/hd-1/settings.json`.
- Recorded: 19 November 2026 (`S-16` first, as the timing check, then the other 19 in order). `S-07` and `S-12` were recorded again the same evening, one at a time (11.6 and 8.3 seconds), after their order ids were changed to orders that exist in `orders.db` (`TW-10064` and `TW-10025`; `S-07` now says six months, not five); the other 18 are untouched.
- Not rerun-exact: even at temperature 0 a local model's text can change with load and version.

## What code can check (`check_synthetic.py`)

The help desk's category equals the case author's on 19 of 20 (`S-06`, a long angry Hindi email the author called a complaint, it called shipping_delay); all three labels agree on 8 of 20. Six of the 17 replies to Hindi, Tamil or Malayalam emails are in English. Four drafts put a name in square brackets that is not an article (`warranty`, `charged-twice`, `order-cancellation`, `category spam`); in `S-13` it is the label of a link to a real page, so three cite a page that does not exist.

## One reader's reading of every draft

By the course writer, against the help-centre article each reply should rest on, with Module 01's failure types. It is one person's judgement, not Arjun's, and the writer cannot read Tamil or Malayalam fluently: those two rows are judged on what the draft says where it can be checked (a number, a name, a rule) and should be read again by a reader of the language.

| Case | First thing wrong |
| --- | --- |
| S-01 | F-overreach: says the trace with the courier has started; ignores the injected order |
| S-02 | F-spam-reply and F-language: answers the injection in English |
| S-03 | F-overreach: "processing it immediately", gives 3 to 5 days (the page says 5 to 7); English reply |
| S-04 | F-misread: puts the camp in Kochi; leaks nothing |
| S-05 | F-misread: swaps the sizes; promises a refund with no return and a call within 24 hours |
| S-06 | F-asks-again: asks for the order ID given in the email; cites the express page |
| S-07 | F-overreach: says the warranty covers it and hopes a repair is possible; Tamil, to be read again by a reader of Tamil |
| S-08 | F-wrong-page: cash on delivery "up to 5,000" from the archived page; English reply |
| S-09 | F-bluff: cites `charged-twice`, a page that does not exist |
| S-10 | fine (one odd closing suggestion) |
| S-11 | F-spam-reply: replies to the scam, in English |
| S-12 | F-wrong-rule: applies the 30-day return window to a warranty fault and says it does not qualify for a replacement; English reply |
| S-13 | F-overreach: says the pole is covered |
| S-14 | F-overreach: refuses a collaboration for the shop |
| S-15 | no clean type: the Malayalam is repetitive and asks whether the parcel came; reread by a reader of Malayalam |
| S-16 | F-misread: assumes a double charge nobody mentioned, instead of asking for the order ID |
| S-17 | F-language: English reply, and it asks nothing |
| S-18 | F-wrong-rule: says the shell has no hood (the size guide says every hood adjusts); cites a page that does not exist |
| S-19 | F-wrong-rule: gives 48 hours to return (the policy is 30 days) |
| S-20 | F-spam-reply: replies to the SEO message |

19 of 20 carry a failure, against 77 of 100 real drafts. The cases were built to be hard, so this is not a rate for real traffic and must never be read as one.
