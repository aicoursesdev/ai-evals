"""Lesson 03.2: two help desk checks written by hand, run on 550 traces.

From this folder: uv run python own_checks.py
"""
import plumbing


def no_draft(trace):
    """Fires when the help desk wrote nothing."""
    raise NotImplementedError(
        "TODO 03.2: return True when the trace's draft is empty once "
        "spaces are trimmed, see the lesson's 'The help desk’s own "
        "checks' section")


def writes_to_spam(trace):
    """Fires when triage said spam and a reply was written anyway."""
    raise NotImplementedError(
        "TODO 03.2: return True when triage said spam and the draft is "
        "not empty, see the lesson's 'The help desk’s own checks' "
        "section")


if __name__ == "__main__":
    traces = plumbing.traces_by_id()
    for check in (no_draft, writes_to_spam):
        fired = [i for i, trace in traces.items() if check(trace)]
        print(f"{check.__name__:<15} fires on {len(fired)} of {len(traces)}")
