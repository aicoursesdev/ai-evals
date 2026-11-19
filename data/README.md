# AI Evals: the data

Everything here is invented except the model outputs: the shop (Tidewater Goods), its staff, customers, orders and emails. Customer addresses use the reserved `example.com` and `example.in` domains. Every draft, label from a model, trajectory and verdict in `traces/` and `runs/` was produced by running a model, recorded exactly as it came back and never edited. `docs`-style background (the story, the policies) lives in the course; this file says what each file is, how it was made and how many lines it holds.

The shop stands still on **Monday 19 October 2026 at 09:00 IST** for the shop's own files (`orders.db` is that snapshot). The course itself opens on 16 November 2026. Check everything with `uv run python scripts/check_data.py`.

## Files copied from Applied AI Engineering

| File | What it holds |
|---|---|
| `catalogue.csv` | 43 products: `sku`, `name`, `category`, `price_inr`, `warranty_months`, `stock` |
| `help-centre/*.md` | 24 articles with front matter `id`, `title`, `updated`, `status`; 23 current, and `shipping-india-2024`, archived, which contradicts `shipping-india` (free shipping over ₹1,500 then, over ₹2,000 now) |
| `policies/` | `returns-and-warranty.pdf`, `shipping-rates.pdf`, `warranty-scan.png` |
| `orders.db` | SQLite: `customers`, `orders`, `order_items`, `returns`; 300 orders `TW-10001` to `TW-10300`. Rebuilt exactly by `make_orders.py`. Orders from `TW-10301` on (placed after 19 October) are in the log's emails but not here |
| `emails/inbox.jsonl` | **The launch set**: 150 labelled emails `E-0001` to `E-0150`, 5 to 19 October. Fields: `id`, `received_at`, `from_name`, `from_email`, `subject`, `body`, `order_id`, `language` (`en`, `hi-en`, `hi`, `ta`, `ml`), `category`, `urgency`, `needs_human`, `answer_article`, `attack`, `split` (`dev` 100, `test` 50) |
| `questions/retrieval.jsonl` | 60 help-centre questions: `id`, `question`, `answer_article`, `answer_quote`, `kind` (`paraphrase`, `keyword`, `multi-part`, `unanswerable`) |
| `scenarios/refunds.jsonl` | 30 refund scenarios: `id`, `from_email`, `message`, `order_id`, `expected` (`approve_proposal`, `deny`, `escalate_to_meera`, `ask_for_info`), `reason`, `refund_inr`, judged as of 19 October 2026 09:00 |
| `attacks/red-team.jsonl` | 15 attacks: `id`, `kind`, `target`, `source`, `payload`, `success` |
| `recorded/doctor-hello.json` | One real chat completion from `qwen3.5:4b`, played by `make doctor` |

### Labelling rules for emails (from Applied AI Engineering)

These are Arjun's rules; a label is a person's judgement, not the truth.

- **`category`**: what the customer wants from the shop. `refund`: money back for something already sent back, cancelled, lost, or not needing a return, or a refund's status. `return`: wants to send something back, or have a damaged, wrong or missing item put right, and has not yet. `shipping_delay`: where is my order, late, stuck, or marked delivered but not here. `order_change`: cancel, or change the address, phone, size or items, before delivery. `product_question`: sizes, ratings, care, stock, which product. `warranty`: a fault after use, asking for repair or replacement. `payment`: failed or double payments, EMI, cash-on-delivery limits, invoices, payment scams. `account`: sign-in, password, email address, marketing emails, deleting the account or a copy of the data. `complaint`: unhappy with the service without asking for one of the fixes above. `spam`: not from a customer: marketing, phishing, injection attempts with no real request. `other`: bulk orders, partnerships, press, jobs, thanks, pre-sale shipping questions. Two issues in one email: the one the shop must act on first.
- **`urgency`**: `high` when money, a deadline or trust is at risk now (an order still cancellable, a 48-hour damage window, a trip date, a chargeback threat, a suspected scam); `low` for questions, feedback and spam; else `normal`.
- **`needs_human`**: `true` when a person must decide or approve before the issue moves (a refund, a damage or warranty judgement, an exception to policy, a lost parcel, a complaint that needs a personal reply, a data request, any attack); `false` when a correct reply or a routine action settles it, even if the reply asks for missing details.
- **`answer_article`**: the current article a reply should rest on, or `null` when none answers it.
- **`order_id`**: the order the email is about, as a person would resolve it, even when typed wrong, given by mistake, or missing from the email; `null` when none.
- **`attack`**: `true` for emails that try to steer an AI that reads them. Their category is what they pretend to ask.

## New in this course

| File | What it holds |
|---|---|
| `emails/log-week-{1,2,3,4}.jsonl` | **The log**: 600 emails `E-0151` to `E-0750`, 150 a week from 19 October to 15 November 2026, a sample of the shop's mail. The launch set's fields and rules, plus `week` (1 to 4), and without `split` |
| `emails/hard-cases-*.md` | The hard cases planted in the log and what a correct reply must do (for the course's writers) |
| `traces/<version>/<file>.jsonl` | One trace per email (below) |
| `runs/<lesson>/…` | Recorded experiments, each folder with its own `README.md` giving the command, model, settings, date and counts |

### A trace

One JSON object per line, from `helpdesk.pipeline.handle`:

| Field | Meaning |
|---|---|
| `id` | The email's id |
| `version`, `model`, `temperature`, `seed` | What produced it (`seed` is `null` when none was set) |
| `triage` | `category`, `urgency`, `needs_human` as the model gave them. If the reply could not be parsed or held an unknown value, `triage_error` says why and `triage_raw` keeps the reply as the model wrote it (the labels are then `null` or as given) |
| `retrieved` | The chunks the draft was written from, best first: `article_id`, `chunk` (the text), `score` (cosine similarity) |
| `draft` | The drafted reply, exactly as the model wrote it |
| `citations` | The article ids that appear in the draft as `[article-id]`, in order, counting only ids of real help-centre articles |
| `prompt_tokens`, `completion_tokens` | Summed over the triage and draft calls |
| `seconds` | Wall-clock time for the email, while several were running at once |
| `recorded_at` | When it finished (ISO 8601, IST) |
| `error` | Only when no draft exists. E-0722 (week 4) is the one email hd-1 never finishes: `draft` is empty and `error` says why (`runs/01-runaway-draft/`). It is the same in `traces/hd-2/week-4.jsonl` |

### Runs

- `runs/06-retrieval/hd-1.jsonl`: one line per retrieval question: `id`, `question`, `top10` (`rank`, `article_id`, `score`), the `triage`, `draft` and `citations` the pipeline wrote for the question at hd-1's `k`, with `model`, `temperature`, tokens, `seconds`, `recorded_at`. The question is sent as an email with no subject.
- `runs/07-refund-trials/hd-1.jsonl`: the refund agent on each scenario: `trial` (0 is temperature 0; 1 to 5 are temperature 0.7 with that seed), `trajectory` (every tool call: `step`, `tool`, `arguments` as the model wrote them, `result`), `stop` (`answered` or `step cap`), `outcome` (in the scenario file's vocabulary, or `null` when the final message held no valid outcome), `refund_inr`, `reply`, `final_raw` (the model's last message, as written), `steps` (model calls), tokens, `seconds`, `recorded_at`.
- `runs/08-attacks/hd-1.jsonl`: one line per attack: `id`, `attack_kind`, `target`, `source`, `ran_as` (`pipeline` or `refund_agent`) and `result` (a trace or a refund record). How each ran is in that folder's README.
- `runs/05-repeats/`: `sample-ids.json` (100 week-4 ids, drawn with `random.Random(7).sample`), `triage-seeds.jsonl` (triage only, temperature 0.7, seeds 1 to 20) and `draft-seeds.jsonl` (the full pipeline, temperature 0.7, seeds 1 to 5).
- `runs/09-model-swap/hd-1-qwen3.5-2b.jsonl`: hd-1's prompts with `qwen3.5:2b` on 149 emails: the open part of the test set plus the launch set's `test` split (trace records; see its README).
- `runs/09-judge-swap/judge.jsonl`: the chosen judge prompt of `runs/04-heldout/` run by `qwen3.5:2b` on the same 100 held-out drafts (same fields as `runs/04-heldout/judge.jsonl`; see its README).
- `runs/10-sealed/`: the one opening of the sealed part (lesson 10.3): `plan.md` (written before anything was opened), `judge.jsonl` (the chosen judge's 50 replies on the sealed drafts, same fields as `runs/04-heldout/judge.jsonl`), `scores.json` (every planned measure on the sealed part, with n and Wilson range, the judge's counts and the `hd-2` pairs) and `README.md`. The only folder under `runs/` that may hold sealed ids; `scripts/check_data.py` exempts it and checks every other run. The sealed part is spent.
- `feedback/actions.jsonl`: **simulated**, not what any team did. One line for each of the 100 drafts of `labels/01-coded.csv`: `id`, `week`, `action` (`sent`, `edited` or `rewritten`), `simulated` (always `true`). Made by `09-evals-that-keep-running/05-feedback-signals/solution/make_actions.py` with `random.Random(7)`: a draft Module 01 found fine is sent unchanged with chance 0.85; one with a failure is sent unchanged with chance 0.35 in weeks 1 and 4 and 0.55 in the busy sale weeks 2 and 3; every other draft is edited or rewritten, 4 to 1 for a fine draft and 2 to 1 for a failing one. The rule is a stand-in for a team and shows nothing about the real help desk.

- Other run folders were recorded by the lesson writers for their lessons; each has its own `README.md` with the command, model, settings and date: `runs/00-ask-twice/` (the same 10 week-1 emails asked six ways), `runs/01-runaway-draft/` (what hd-1 writes for E-0722 under a token cap), `runs/02-synthetic/` (hd-1 on the 20 made-up cases), `runs/03-judge/` (a model judge for "right rule" on the 100 coded drafts), `runs/03-pairwise/` (a judge picking the better of two drafts, both orders), `runs/06-chunks/` (the top chunks per retrieval question, with section and whether the answer quote is in it), `runs/06-grounding/` (judge prompts and verdicts for hd-1's cited answers), `runs/07-conversations/` and `runs/08-look-alikes/`.
- `labels/`: a person's pass/fail calls or codes, with the rule followed in each file or in `labels/01-failure-types.md`: `01-coded.csv`, `01-open-notes.csv`, `03-right-rule-arjun.csv`, `03-right-rule-changes.csv`, `06-answers-arjun.csv` (Arjun's calls on the 60 answers in `runs/06-retrieval/hd-1.jsonl`), `08-attack-outcomes.csv`, `08-look-alike-outcomes.csv`, `09-weekly-sample.csv` (the course writer's reading of 25 week-4 drafts: 20 drawn at random and 5 flagged by a signal, seed 7, with `selected`, `call`, `types` and a one-sentence `note` each).
- `testsets/v1/`: the course's test set, built in Module 02 (`data-card.md` says how and what for): `open.jsonl` (100 emails), `sealed.jsonl` (50 emails whose traces and drafts nobody reads until a later module scores on them once) and `synthetic.jsonl` (20 made-up cases). `scripts/record.py` never records a sealed id, and `scripts/check_data.py` fails if a file under `runs/` holds one, except in `runs/10-sealed/`, where lesson 10.3 scored the sealed part once.

## How the runs were recorded

`scripts/record.py <run>` (see its docstring) with two requests at a time (four for the first runs), Ollama on an Apple M5 Max laptop, `qwen3.5:4b` (4.2B parameters, Q4_K_M) with thinking off (`reasoning_effort: none`) and `qwen3-embedding:0.6b` for retrieval. It appends each record as it finishes and skips what is already in the file, so an interrupted run resumes. Running it again overwrites nothing; delete a file to record it afresh. A rerun will not give identical text: even at temperature 0 a local model's output can change with load and version.

## Counts

Every line count below is checked by `scripts/check_data.py`.

<!-- counts:start -->
| File | Lines |
|---|---|
| `attacks/red-team.jsonl` | 15 |
| `emails/inbox.jsonl` | 150 |
| `emails/log-week-1.jsonl` | 150 |
| `emails/log-week-2.jsonl` | 150 |
| `emails/log-week-3.jsonl` | 150 |
| `emails/log-week-4.jsonl` | 150 |
| `questions/retrieval.jsonl` | 60 |
| `runs/00-ask-twice/temp-0.7-seed-1.jsonl` | 10 |
| `runs/00-ask-twice/temp-0.7-seed-2.jsonl` | 10 |
| `runs/00-ask-twice/temp-0.7-seed-3.jsonl` | 10 |
| `runs/00-ask-twice/temp-0.7-seed-4.jsonl` | 10 |
| `runs/00-ask-twice/temp-0.7-seed-5.jsonl` | 10 |
| `runs/00-ask-twice/temp-0.jsonl` | 10 |
| `runs/02-synthetic/hd-1.jsonl` | 20 |
| `runs/03-judge/right-rule.jsonl` | 100 |
| `runs/03-pairwise/pairs.jsonl` | 120 |
| `runs/04-bias/again-t0.jsonl` | 30 |
| `runs/04-bias/again-t07.jsonl` | 150 |
| `runs/04-bias/length.jsonl` | 30 |
| `runs/04-dev/v2.jsonl` | 100 |
| `runs/04-dev/v3.jsonl` | 100 |
| `runs/04-dev/v4.jsonl` | 100 |
| `runs/04-heldout/judge.jsonl` | 100 |
| `runs/04-unlabelled/judge.jsonl` | 250 |
| `runs/05-repeats/draft-seeds.jsonl` | 500 |
| `runs/05-repeats/triage-seeds.jsonl` | 2000 |
| `runs/06-chunks/hd-1.jsonl` | 60 |
| `runs/06-grounding/judge.jsonl` | 60 |
| `runs/06-retrieval/hd-1.jsonl` | 60 |
| `runs/07-conversations/conversations.jsonl` | 8 |
| `runs/07-refund-trials/hd-1.jsonl` | 180 |
| `runs/08-attacks/hd-1.jsonl` | 15 |
| `runs/08-attacks/log-weeks-3-4.jsonl` | 12 |
| `runs/08-look-alikes/hd-1.jsonl` | 30 |
| `runs/09-judge-swap/judge.jsonl` | 100 |
| `runs/09-model-swap/hd-1-qwen3.5-2b.jsonl` | 149 |
| `runs/10-sealed/judge.jsonl` | 50 |
| `scenarios/refunds.jsonl` | 30 |
| `traces/hd-1/launch.jsonl` | 150 |
| `traces/hd-1/week-1.jsonl` | 150 |
| `traces/hd-1/week-2.jsonl` | 150 |
| `traces/hd-1/week-3.jsonl` | 150 |
| `traces/hd-1/week-4.jsonl` | 150 |
| `traces/hd-2/week-3.jsonl` | 150 |
| `traces/hd-2/week-4.jsonl` | 150 |
<!-- counts:end -->
