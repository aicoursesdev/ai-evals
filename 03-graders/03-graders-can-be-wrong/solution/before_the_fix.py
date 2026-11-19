"""Lesson 03.3: what the known cases showed about the first versions.

Given: the two first versions, and a loop that runs your run_cases on them.

From this folder: uv run python before_the_fix.py
"""
import re

from check_cases import run_cases
from grader_cases import CASES
from scorecard.graders import reply_script_matches


def first_wrong_script(email, trace):
    """The first version: the draft is not in the email's script."""
    return not reply_script_matches(trace, email)


def first_asks_known_id(email, trace):
    """The first version: asks for an order id the email already holds."""
    ask = r"(reply|email|send).{0,40}order (id|number)"
    return bool(re.search(ask, trace["draft"], re.I)
                and re.search(r"TW-\d{4,5}", email["body"]))


FIRST = {"wrong script": first_wrong_script,
         "asks for known id": first_asks_known_id}

if __name__ == "__main__":
    for name, check in FIRST.items():
        for what, want in run_cases(check, CASES[name])[0]:
            print(f"{name}: wrong on {what!r}: fired {not want}")
