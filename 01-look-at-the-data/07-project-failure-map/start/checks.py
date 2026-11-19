"""Seven cheap code checks on a trace. Each returns True when it fires.

Run `uv run python checks.py coded.csv` to see how each one does against
your coded notes.
"""
import sys

from more_checks import (asks_for_order_id_it_has, cites_missing_or_old_page,
                         claims_an_action, has_no_draft, invents_an_address)
from plumbing import print_scores, read

# Unicode blocks of the scripts customers wrote in besides Latin letters.
SCRIPTS = {"Devanagari": (0x0900, 0x097F), "Tamil": (0x0B80, 0x0BFF),
           "Malayalam": (0x0D00, 0x0D7F)}


def script_of(text):
    """The non-Latin script a text is mostly written in, or None."""
    for name, (low, high) in SCRIPTS.items():
        if sum(low <= ord(ch) <= high for ch in text) > 10:
            return name
    return None


def answers_in_wrong_script(email, trace):
    """The email is in Hindi, Tamil or Malayalam script; the draft is not."""
    wanted = script_of(email["body"])
    return wanted is not None and script_of(trace["draft"]) != wanted


def writes_to_spam(trace):
    """The help desk itself labelled the email spam and still wrote a reply."""
    return (trace["triage"]["category"] == "spam"
            and bool(trace["draft"].strip()))


# check name: (function, the failure type it is meant to catch)
CHECKS = {
    "wrong script": (answers_in_wrong_script, "F-language"),
    "missing or old page": (lambda e, t: cites_missing_or_old_page(t),
                            "F-wrong-page"),
    "reply to spam": (lambda e, t: writes_to_spam(t), "F-spam-reply"),
    "invented address": (invents_an_address, "F-bluff"),
    "claims an action": (lambda e, t: claims_an_action(t), "F-overreach"),
    "asks for known id": (asks_for_order_id_it_has, "F-asks-again"),
    "empty draft": (lambda e, t: has_no_draft(t), "F-no-draft"),
}

if __name__ == "__main__":
    print_scores(CHECKS, read(sys.argv[1]))
