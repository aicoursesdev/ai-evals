"""Lesson 10.7: the one-page report to Meera, every number from a recording
or a script of an earlier lesson. Work in start/, then `make check 10.7`.

From this folder: uv run python report_to_meera.py   (writes report.md)
"""
from pathlib import Path

import plumbing as p
from by_kind import NEEDED, by_kind
from scorecard.report import one_page

drafts = p.open_read()
read, fine = len(drafts), sum(d["fine"] for d in drafts)
quiet = [d for d in drafts if d["quiet"]]
silent_bad = sum(not d["fine"] for d in quiet)
seal = p.sealed()["rates"]
kept, of_pass, held, of_fail = p.judge_rates()
cold, pass3 = p.refund_agent()
hurt = p.attacks()
fail = sum(k for k, _ in hurt.values())
tries = sum(n for _, n in hurt.values())
one, two, n277 = p.two_versions()
weekly = p.weekly_random()
tokens, mails = p.tokens_per_email()

top, (top_read, top_failed) = max(by_kind(drafts).items(),
                                  key=lambda x: x[1][0])
decision = (
    "No kind of email may go out unread yet. Keep draft mode: a person "
    "reads every draft before it is sent, for all eleven kinds. A kind "
    f"may go out unread when a person has read {NEEDED} of its drafts with "
    f"none failing; the best-read kind, {top.replace('_', ' ')}, has "
    f"{top_read} reads and {top_failed} failures.")
# TODO 10.7: write the twelve evidence rows, each (name, hits, n, source),
# see the lesson's 'What the evidence says' section.
evidence = []
uncertainty = [
    "Every call is one reader's, under a written rule, not the truth; two "
    "careful readers agreed on 75 of 80 drafts (04.7).",
    f"The sealed part's {seal['triage right'][1]} drafts were never read by "
    "a person, and it is now spent.",
    f"The refund agent gets three tries in a row right {pass3:.1%} of the "
    "time, estimated from five tries on each of 30 scenarios (07.7).",
    "The attack suite is fixed: tool results and an attacker who adapts "
    "were not tried.",
    "hd-2 leaves the checks quiet more often, but nobody has read the "
    "emails that changed, so it is not shown to be better.",
    "One shop, four weeks including a sale, one small local model.",
]
cost = [
    f"Writing a draft: {tokens:,.0f} tokens an email on average ({mails} "
    "log emails).",
    "The seven checks run in about 0.05 milliseconds a draft; the judge "
    "takes about 2.2 seconds a verdict.",
    "A person at an assumed 60 s a draft: about 400 emails a week is 6 "
    "hours 40 minutes; the weekly sample of 25 is 25 minutes.",
]
change = [
    f"{NEEDED} drafts of one kind read clean (none failing), with the "
    "safety rows for its harms proven under their limits.",
    "A judge that holds back far more than 16 of 26 bad drafts, measured on "
    "fresh drafts that people have called.",
    "A new version that fixes the largest failure types, read by a person.",
]
page = one_page("Which emails may go out unread?", decision, evidence,
                uncertainty, cost, change)
Path("report.md").write_text(page)
print(page)
