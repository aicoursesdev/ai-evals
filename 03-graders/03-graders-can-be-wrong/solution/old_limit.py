"""Lesson 03.3: a grader for "the draft gives the old shipping limit".

From this folder: uv run python old_limit.py
"""
import re

import plumbing


def naive(trace):
    """Fires when the old limit appears anywhere."""
    return "₹1,500" in trace["draft"]


def fixed(trace):
    """Fires when the old limit appears and the current one does not."""
    old = re.search(r"₹\s?1,?500\b", trace["draft"])
    new = re.search(r"₹\s?2,?000\b", trace["draft"])
    return bool(old and not new)


if __name__ == "__main__":
    traces = plumbing.traces_by_id()
    for name, grader in [("naive", naive), ("fixed", fixed)]:
        fired = [i for i, t in traces.items() if grader(t)]
        print(f"{name:<6} fires on {len(fired)}:", ", ".join(fired))
