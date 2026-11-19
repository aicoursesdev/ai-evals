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
    raise NotImplementedError(
        "TODO 01.6: for each script in SCRIPTS, return its name when more "
        "than 10 characters of text fall inside its range, else None, see "
        "the lesson's 'Check: a rule a program can apply' section")


def answers_in_wrong_script(email, trace):
    """The email is in Hindi, Tamil or Malayalam script; the draft is not."""
    raise NotImplementedError(
        "TODO 01.6: return True when the email has a script (script_of is "
        "not None) and the draft's script is different, see the lesson's "
        "'Check: a rule a program can apply' section")


def writes_to_spam(trace):
    """The help desk itself labelled the email spam and still wrote a reply."""
    raise NotImplementedError(
        "TODO 01.6: return True when the triage category is 'spam' and "
        "the draft has any text besides spaces, see the lesson's 'Check: "
        "a rule a program can apply' section")


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
