"""Lesson 03.3: known-good and known-bad cases for every check.

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


TAMIL = "வணக்கம், என் ஆர்டர் இன்னும் வரவில்லை, எப்போது வரும்?"
TW = "My order TW-10279 has not come."

CASES = {
    "wrong script": [
        ("Tamil email, English reply (E-0232)", *real("E-0232"), True),
        ("Tamil email, Tamil reply", *made(TAMIL, body=TAMIL), False),
        ("English email, English reply", *made("Hello there"), False),
        ("Tamil email, no draft (E-0722)", *real("E-0722"), False),
    ],
    "missing or old page": [
        ("page that does not exist", *made("See [invoices]."), True),
        ("the archived page", *made("See [shipping-india-2024]."), True),
        ("a current page", *made("See [returns-policy]."), False),
        ("no tags", *made("Tidewater support"), False),
    ],
    "reply to spam": [],  # TODO 03.3: write its cases, see the lesson's
    #   'Test the grader itself' section
    "invented address": [
        ("made-up address (E-0204)", *real("E-0204"), True),
        ("help-centre address", *made("Write to support@tidewater.example"),
         False),
        ("address ends a sentence", *made("Write to bulk@tidewater.example."),
         False),
        ("customer's own address",
         *made("Replying to a@example.com", sender="a@example.com"), False),
    ],
    "claims an action": [
        ("we have updated", *made("We have updated your order."), True),
        ("has been approved", *made("Your refund has been approved."), True),
        ("a person will review", *made("A person will review this."), False),
        ("GAP: promises in other words", *made("I'll sort it out today."),
         True),
    ],
    "asks for known id": [
        ("asks for the id given (E-0181)", *real("E-0181"), True),
        ("asks only guests (E-0745)", *real("E-0745"), False),
        ("no id in the email", *made("Please email us your order ID."),
         False),
        ("draft does not ask", *made("Your order is on its way.", body=TW),
         False),
    ],
    "empty draft": [],  # TODO 03.3: write its cases, see the lesson's
    #   'Test the grader itself' section
}
