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
    ids = [r["id"] for rows in parts.values() for r in rows]
    real = parts["open"] + parts["sealed"]
    sizes = (len(parts["open"]), len(parts["sealed"]))
    sealed = {r["id"] for r in parts["sealed"]}
    yield "100 open, 50 sealed", sizes == (100, 50)
    yield "every id appears once", len(ids) == len(set(ids))
    yield "no sealed email is in the launch set", not sealed & launch
    yield "sealed: not week 1, not open, not an attack, in no run", not [
        r["id"] for r in parts["sealed"]
        if r["week"] == 1 or r["attack"] or r["id"] in used
        or r["id"] in {o["id"] for o in parts["open"]}]
    yield "no real email appears in a prompt", not find_leaks(real, prompts)
    yield "no copy or near copy across parts", not [
        p for p in near_pairs(real, floor=0.5, n=1)
        if {p[0], p[1]} & sealed]
    yield "made-up cases are all marked", all(
        r["made_up"] and r["id"].startswith("S-") for r in parts["synthetic"])


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
