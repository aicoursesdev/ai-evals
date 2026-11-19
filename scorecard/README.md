# scorecard

The eval harness the course grows. Every function is small enough to read in one go. Stdlib only.

| Function | Meaning | Module |
| --- | --- | --- |
| `TODAY`, `DATA` | the course date; the data folder | `data.py` (given) |
| `read_jsonl`, `emails`, `traces`, `run`, `labels`, `articles`, `questions`, `scenarios`, `attacks` | load the course data as lists of dicts (`run(name)`: every recorded run in `data/runs/<name>/`, by file) | `data.py` (given) |
| `testset` | one part (`open`, `sealed`, `synthetic`) of a test set version, as a list of dicts | `data.py` (given; the set is built in 02) |
| `run.run` | call a system on each case and apply each named grader | `run.py` |
| `save`, `load` | write and read result rows (JSON lines) | `run.py` |
| `pass_rate` | share of rows a grader passed | `run.py` |
| `exact`, `contains`, `matches` | output equals, contains, or matches a pattern | `graders.py` |
| `valid_json`, `has_fields` | parses as JSON; a dict with the needed keys and values | `graders.py` |
| `close_to` | a number within a tolerance | `graders.py` |
| `label_correct`, `cites_real_article`, `cites_retrieved_article`, `mentions_order_id`, `promises_refund`, `reply_script_matches` | the help desk's own checks on a trace | `graders.py` |
| `wrong_script`, `cites_missing_or_old_page`, `writes_to_spam`, `invents_address`, `claims_action`, `asks_known_id`, `no_draft`, `old_shipping_limit` | the help desk's checks that fire (return True when they see the failure); `page_status`, `help_centre_text` give the help centre's pages | `graders.py` |
| `CHECKS` | each fire-check by name, with the failure types it should catch | `graders.py` |
| `logged` | one week of the log (emails or traces) without the sealed part of the test set, which it never parses | `graders.py` |
| `precision_recall` | share of flags that are right; share of real cases flagged | `graders.py` |
| `verdict` | fill a judge prompt, ask (or replay), read PASS/FAIL (and UNSURE with `unsure=True`) | `judge.py` |
| `reading` | what a judge's reply says: `pass`, `fail`, `unsure`, or `none` for no verdict line | `judge.py` |
| `record` | ask the local model for each row, one request at a time with no retries, appending each request and reply to a file; skips rows already recorded | `judge.py` |
| `confusion`, `rates` | the four counts (a judge's `None` counts as not passing); true positive and true negative rate | `judge.py` |
| `agreement`, `kappa` | raw agreement; Cohen's kappa | `judge.py` |
| `standard_error`, `interval` | error of a rate; normal 95% interval | `stats.py` |
| `wilson` | Wilson 95% interval | `stats.py` |
| `at_most`, `solve` | chance of k or fewer failures; bisection that finds a rate from it | `stats.py` |
| `exact_upper`, `exact_interval` | exact one-sided upper bound; Clopper-Pearson interval | `stats.py` |
| `rule_of_three`, `sample_size` | 3/n bound; cases needed for a margin | `stats.py` |
| `pair_counts` | the four kinds of pair (both, only a, only b, neither) for two 0/1 lists on the same cases | `stats.py` |
| `paired`, `mcnemar` | difference on the same cases; exact two-sided test | `stats.py` |
| `bootstrap` | percentile interval by resampling | `stats.py` |
| `clustered_se`, `bonferroni` | error for grouped cases; level for many tests | `stats.py` |
| `corrected_rate`, `corrected_interval` | Rogan-Gladen corrected pass rate and its interval | `stats.py` |
| `recall_at_k`, `precision_at_k` | right articles found in the top k; share of top k that is right | `retrieval.py` |
| `reciprocal_rank`, `mrr` | 1/rank of the first right item; its mean | `retrieval.py` |
| `dcg`, `ndcg` | discounted gain, binary gain; normalised by the best order | `retrieval.py` |
| `outcome_correct`, `proposals`, `state_correct` | check a refund trial's stated outcome; list the proposals it left waiting; check what it left behind | `agents.py` |
| `called`, `called_in_order` | check a refund trial's tool calls | `agents.py` |
| `pass_at_k`, `pass_hat_k` | at least one / all of k trials succeed | `agents.py` |
| `first_failure`, `transitions` | the first check that failed; counts per check | `agents.py` |
| `gate` | pass or fail a change by rules on intervals | `report.py` |
| `figure` | one evidence line: share, n, Wilson range and the file it came from | `report.py` |
| `one_page` | the one-page report: decision, evidence, uncertainty, cost, what would change it | `report.py` |
