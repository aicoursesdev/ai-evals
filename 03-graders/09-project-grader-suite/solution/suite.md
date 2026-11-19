# Grader suite for the Tidewater help desk (hd-1), 19 November 2026

Run `uv run python run_suite.py`. Numbers are against Arjun's failure map of 100 drafts (`labels/01-coded.csv`) and his derived "right rule" calls (`labels/03-right-rule-arjun.csv`): one person's judgement, not the truth.

| Failure type | In the map | Marker | Caught | What the marker cannot do |
| --- | --- | --- | --- | --- |
| F-overreach | 21 | code: claims an action | 10 | Sees only a few phrases; promises in other words pass |
| F-misread | 21 | none yet | - | Needs its own rule and judge |
| F-wrong-rule | 15 | Arjun's rule + judge (`judge_rule.py`) | see below | Judge sees only the three pages the help desk saw |
| F-bluff | 14 | code: missing or old page + invented address | 6 | Sees invented pages and addresses, not other invented facts |
| F-asks-again | 12 | code: asks for known id | 6 | Sees only requests for an order id the email holds |
| F-spam-reply | 7 | code: reply to spam | 6 | Trusts triage's own label; phishing labelled as something else passes |
| F-wrong-page | 5 | code: missing or old page | 3 | Sees archived or missing pages, not a wrong but current one |
| F-off-topic | 5 | none yet | - | Needs its own rule and judge |
| F-language | 3 | code: wrong script | 2 | Sees the script, not whether the language is good |
| F-obeys-injection | 1 | none yet | - | Needs an attack set and an outcome check (Module 08) |
| F-no-draft | 1 | code: empty draft | 1 | Nothing: it is the simplest check |

Every check is right on its own known cases (3 or 4 each), and the verdict reader on its five. One case is a known gap (a promise in words "claims an action" does not know).

Right-rule judge against Arjun, replayed from `data/runs/03-judge/right-rule.jsonl`: where both gave pass or fail (77 drafts) they agree on 52; a marker that always said pass would agree on 50. Three replies had no verdict line and are counted as such. The judge is not yet something to rely on; Module 04 measures it.
