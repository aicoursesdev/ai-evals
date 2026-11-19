"""Show one trace from end to end: the email, the labels, the pages, the draft.

    uv run python view.py E-0152            # what you read first
    uv run python view.py E-0152 --chunks   # also the full text of each page
"""
import sys

from plumbing import show
from scorecard import data


def find(email_id):
    """The email, the trace and Arjun's labels for an id, or a clear error."""
    for week in (1, 2, 3, 4):
        for email in data.emails(week=week):
            if email["id"] == email_id:
                traces = {t["id"]: t for t in data.traces("hd-1", week=week)}
                if email_id not in traces:
                    sys.exit(f"{email_id} has no recorded trace yet")
                return email, traces[email_id]
    sys.exit(f"no email called {email_id}")


if __name__ == "__main__":
    email, trace = find(sys.argv[1])
    show(email, trace, chunks="--chunks" in sys.argv)
