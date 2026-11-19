"""Lesson 03.9: the suite's known-good and known-bad cases, one set per check.

Each case is (what it is, email, trace, should the check fire). Real ones
come from the log by id; the rest are written by hand, as small as they
can be. A case marked GAP should fire and is known to be missed.
"""
import plumbing

E, T = plumbing.emails_by_id(), plumbing.traces_by_id()


def real(id_):
    return E[id_], T[id_]


def made(draft, body="Hello", category="other", sender="a@example.com"):
    """A tiny email and trace, written by hand for one case."""
    email = {"body": body, "from_email": sender, "subject": ""}
    trace = {"draft": draft, "triage": {"category": category}}
    return email, trace


TAMIL = "வணக்கம், என் ஆர்டர் இன்னும் வரவில்லை, எப்போது வரும்?"  # noqa
TW = "My order TW-10279 has not come."

CASES = {
    "wrong script": [],
    "missing or old page": [],
    "reply to spam": [],
    "invented address": [],
    "claims an action": [],
    "asks for known id": [],
    "empty draft": [],
}
# TODO 03.9: for each check give at least three cases, some that fire and
# some that do not, a few from real drafts by id (real) and a GAP case for
# anything you know it misses, as in lesson 03.3. See the lesson's 'Steps'.


# Known cases for read_verdict in judge_rule.py: (a judge's reply, what it
# should read as): "pass", "fail", "unsure", or "none" when no line holds one.
JUDGE_REPLIES = []
# TODO 03.9: give it replies for each of the four, as the lesson's 'Steps'
# say; one should end a sentence with PASS.
