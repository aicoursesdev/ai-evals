"""Show one trace from end to end: the email, the labels, the pages, the draft.

    uv run python view.py E-0152            # what you read first
    uv run python view.py E-0152 --chunks   # also the full text of each page
"""
import sys

from plumbing import show
from scorecard import data


def find(email_id):
    """The email and its trace for an id, or a clear error."""
    raise NotImplementedError(
        "TODO 01.2: loop over weeks 1 to 4 for the email whose id matches, "
        "then return it with its trace, or sys.exit a plain message, see "
        "the lesson's 'Open a trace with the viewer' section")


if __name__ == "__main__":
    email, trace = find(sys.argv[1])
    show(email, trace, chunks="--chunks" in sys.argv)
