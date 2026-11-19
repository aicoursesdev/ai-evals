"""Lesson 03.3: a grader for "the draft gives the old shipping limit".

From this folder: uv run python old_limit.py
"""
import re

import plumbing


def naive(trace):
    """Fires when the old limit appears anywhere."""
    raise NotImplementedError(
        "TODO 03.3: return True when the draft holds the text ₹1,500, "
        "see the lesson's 'A strict grader and a loose one' section")


def fixed(trace):
    """Fires when the old limit appears and the current one does not."""
    raise NotImplementedError(
        "TODO 03.3: return True when the draft gives ₹1,500 (with or "
        "without the comma or a space) and does not give ₹2,000, see "
        "the lesson's 'A strict grader and a loose one' section")


if __name__ == "__main__":
    traces = plumbing.traces_by_id()
    for name, grader in [("naive", naive), ("fixed", fixed)]:
        fired = [i for i, t in traces.items() if grader(t)]
        print(f"{name:<6} fires on {len(fired)}:", ", ".join(fired))
