"""Lesson 02.7: the seal checks. Exits 1 if any fails.

From this folder: uv run python check_testset.py
Reads emails, the set's parts and the ids of two recorded runs. It never
opens a trace.
"""
import sys

from leaks import find_leaks, near_pairs
from plumbing import PARTS, prompt_files, used_ids
from scorecard import data


def checks(parts, launch, prompts, used):
    """Yield (what is checked, whether it holds) for the seven checks."""
    raise NotImplementedError(
        "TODO 02.7: yield (what is checked, whether it holds) for "
        "each of the seven checks, see the lesson's 'Steps' section")


def main():
    parts = {p: data.testset(p) for p in PARTS}
    launch = {e["id"] for e in data.emails(launch=True)}
    failed = 0
    for name, ok in checks(parts, launch, prompt_files(), used_ids()):
        print("ok  " if ok else "FAIL", name)
        failed += not ok
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
