# Data card: the Tidewater help desk test set, version 1.0

Version **1.0**, dated 19 November 2026. Files: `open.jsonl` (100), `sealed.jsonl` (50), `synthetic.jsonl` (20), loaded with `scorecard.data.testset(part)`. Built by `02-test-sets/07-project-test-set/solution/build_testset.py` and `02-test-sets/04-synthetic-cases/solution/build_synthetic.py`. The shop, its customers and every email are invented; the help desk's drafts are real model output.

## What it is for

Scoring the Tidewater help desk (`hd-1` and its successors) on real kinds of email: its triage labels and its drafted replies. Develop graders and judges on the **open** part, which has been read. Score the **sealed** part to decide, rarely, and say how many times it has been scored. Read the **made-up** part on its own: it shows what happens in a case.

Not for: an overall rate from the made-up part; a ranking of models on public tasks; anything about languages or kinds of email listed under "What it does not cover".

## Where the cases came from, and how they were chosen

- **Open (100):** the 100 log emails read in Module 01, drawn at random, 25 from each week of the log (`random.Random(1)`), kept as they were read. They cannot be unread, so they are the part to build on.
- **Sealed (50):** drawn only from emails nothing else in the course opens: log emails of weeks 2, 3 and 4 that are not in the open part, are not attacks, and are in neither `runs/03-pairwise/pairs.jsonl` nor `runs/05-repeats/sample-ids.json` (only their ids were read). 243 emails were eligible (by week 120, 93 and 30). Drawn by `slice_sample` (seed 7, each of category, language, attack and long email topped up to 6 emails in the set where the pool allows, the rest random; the pool holds only 3 Malayalam, 4 Tamil and 7 Hindi emails, so the draw took what exists). Chosen from labels only (category, language, week, attack, length). Its traces and drafts were not opened by the script or by the person who drew it. None is in the launch set, in a prompt file, or a copy or near copy of an open email, and `check_testset.py` checks that none is in week 1, in the open part, an attack, or in either run file. By week the sealed part holds 27, 16 and 7 emails (none from week 1); by language 33 English, 8 Hinglish, 4 Hindi, 3 Malayalam and 2 Tamil.
- **Made up (20):** written by hand for cells of a grid (language x request x twist) that the log's labels show empty: attacks, long emails and rare languages, plus thin and two-request emails. Marked `made_up: true`, ids `S-01` to `S-20`, each with its `dimensions` and a note of what a good reply must do.

## Coverage

| Slice | In the log | Open | Sealed | Real (open + sealed) | Made up |
| --- | ---: | ---: | ---: | ---: | ---: |
| attack=True | 24 | 3 | 0 | 3 (under 10) | 4 |
| category=account | 21 | 2 | 4 | 6 (under 10) | 2 |
| category=complaint | 43 | 9 | 2 | 11 | 2 |
| category=order_change | 59 | 14 | 8 | 22 | 1 |
| category=other | 37 | 6 | 5 | 11 | 2 |
| category=payment | 53 | 11 | 5 | 16 | 2 |
| category=product_question | 83 | 11 | 9 | 20 | 0 |
| category=refund | 70 | 11 | 2 | 13 | 2 |
| category=return | 76 | 7 | 3 | 10 | 2 |
| category=shipping_delay | 98 | 21 | 8 | 29 | 1 |
| category=spam | 31 | 6 | 0 | 6 (under 10) | 3 |
| category=warranty | 29 | 2 | 4 | 6 (under 10) | 3 |
| language=en | 480 | 82 | 33 | 115 | 0 |
| language=hi | 12 | 2 | 4 | 6 (under 10) | 5 |
| language=hi-en | 88 | 11 | 8 | 19 | 3 |
| language=ml | 8 | 1 | 3 | 4 (under 10) | 5 |
| language=ta | 12 | 4 | 2 | 6 (under 10) | 7 |
| long=True | 34 | 6 | 0 | 6 (under 10) | 3 |
| week=1 | 150 | 25 | 0 | 25 | 0 |
| week=2 | 150 | 25 | 27 | 52 | 0 |
| week=3 | 150 | 25 | 16 | 41 | 0 |
| week=4 | 150 | 25 | 7 | 32 | 0 |

Slices marked "under 10" cannot carry a rate. Report their counts, never a percentage alone.

## What it does not cover

- Nothing before 19 October 2026 (the log's first day) or after 15 November.
- Single emails only: no conversations, no attachments (photos are mentioned, never present), no order lookups.
- Rare languages are thin: Malayalam 4 real emails, Hindi script 6, Tamil 6, and 17 made up. Attacks: 3 real (all in the open part) and 4 made up; the sealed part holds none, because attack emails are read in a later module and could not stay unopened (attacks have their own suite there). Long emails: 6 real and 3 made up, none in the sealed part.
- The sealed part holds no week-1 email (Module 00 scores all of week 1) and only 7 from week 4 (a recorded run uses many week-4 emails). You can only seal what nobody has opened.
- The real traffic is one shop's four weeks, a sale among them. Its mix has moved (returns and refunds rose in week 4), and neither part shows it fully: the open part is drawn evenly by week and the sealed part has 7 week-4 emails.
- The made-up cases are in Hinglish, Hindi script, Tamil and Malayalam only; English is covered by the real emails.

## Who labelled what, and by which rule

- **Real emails:** `category`, `urgency`, `needs_human`, `answer_article`, `order_id` and `attack` are Arjun's judgement under the rules at the top of `data/README.md` ("Labelling rules for emails"). They are one person's calls, not the truth, and no second person has checked them on this set.
- **Open drafts:** the failure notes and types in `labels/01-coded.csv` are one reader's (the course writer's), by `labels/01-failure-types.md`. E-0722 is marked `odd: no_draft`: the reply never ended and no draft exists.
- **Made-up cases:** labels and `expect` notes written by the person who wrote each case, by Arjun's rules. Arjun has not read them. The Hindi, Tamil and Malayalam were written by the course's author and not checked by a native reader.

## Known problems

- The open part was read to build the failure map, so any grader tuned on it is tuned on cases it has seen.
- The sealed part takes most of the eligible rare-language emails (Malayalam: 3 of the 8 in the log, all that were eligible) and a small share of the largest slices, so it cannot stand for the traffic's mix. Overall rates need weights (lesson 02.2).
- Triage is graded here by one rule only (the category matches Arjun's). Drafts need their own graders.

## Rule for adding cases

1. A new failure found in production, or by reading, is added as a case with a note of where it was found and what went wrong. The first was E-0722.
2. It goes to the **open** part, never to the sealed part, because it has been read.
3. It is refused if it is already in any part, or is a near copy of a case that is (`add_case.py`).
4. Adding cases raises the minor number (1.0 to 1.1) and records `added_in`. Changing a label, dropping a case or drawing a new sealed part is a new major version (v2), and old scores are not compared with it.
5. The sealed part grows only by drawing fresh log emails nobody has read, by label.
6. A slice where the help desk is right 95 times in 100 or more gets fewer new cases; look at it only as a guard.

## Sealed part: use

Scored 0 times so far. Anyone building prompts, graders or judges works on the open part and does not open the sealed traces or drafts. Each time it is scored, write the date, the version of the help desk and the number here.

**19 November 2026 (Module 10, lesson 10.3): opened and scored once**, for `hd-1` (and `hd-2` on the 23 emails it answered), by the plan in `runs/10-sealed/plan.md`; the scores are in `runs/10-sealed/`. The sealed part is now spent: it is scored 1 time, nothing may be tuned on it, and a later score needs a version 2 with fresh emails. The text above is what this card said at version 1.0.

## Changelog

- 1.0, 19 November 2026: first version. 100 open, 50 sealed, 20 made up. The same evening the made-up cases `S-07` and `S-12` were given order ids that exist in `orders.db` (`TW-10064`, `TW-10025`) and their replies were recorded again.
