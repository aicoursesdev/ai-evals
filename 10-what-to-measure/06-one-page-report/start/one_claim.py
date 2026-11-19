"""Lesson 10.6: a one-page report on one claim: may "no check fires" let a
draft go out unread? Work in start/, then `make check 10.6`.

From this folder: uv run python one_claim.py
"""
from plumbing import quiet_and_read, sealed_no_check
from report_page import one_page

total, quiet, failing = quiet_and_read()
hits, n = sealed_no_check()
page = one_page(
    "May “no check fires” send a draft unread?",
    "No. A quiet suite does not show a draft is fine. Keep a person on "
    "every draft.",
    [("open drafts where no check fires", quiet, total, "checks, open"),
     ("of those, a reader found a failure", failing, quiet, "01-coded"),
     ("sealed drafts where no check fires", hits, n, "runs/10-sealed")],
    [f"One reader's calls, on the open part only: nobody has read the {n} "
     "sealed drafts.",
     "The seven checks are a short list; a failure none of them names "
     "stays quiet."],
    ["The seven checks take about 0.05 milliseconds a draft; a "
     "person reading every draft costs about 60 s a draft (an assumed "
     "pace, lesson 09.2)."],
    ["A reader's calls on 59 or more quiet drafts of one kind of email, "
     "none failing, would justify trying that kind."])
print(page)
