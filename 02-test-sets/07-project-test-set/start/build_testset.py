"""Lesson 02.7: build the open and sealed parts of test set v1.

From this folder: uv run python build_testset.py
Reads emails, the labels of lesson 01 and the ids of two recorded runs. It
never opens a trace or a draft.
"""
from plumbing import OUT, print_slices, tagged, used_ids, write
from scorecard import data
from slices import log, slice_sample

SEED = 7
FLOOR = 6  # a slice stops counting as short at 6; the pool has only 3 ml


def eligible(emails, coded, used):
    """Emails nothing else in the course opens: weeks 2 to 4, not read in
    Module 01, not an attack, not in a recorded run."""
    raise NotImplementedError(
        "TODO 02.7: return the emails of weeks 2 to 4 that are not "
        "attacks, not in coded and not in used, see the lesson's "
        "'Steps' section")


def main():
    coded = {row["id"] for row in data.labels("01-coded")}
    emails = log()
    opened = [e for e in emails if e["id"] in coded]
    pool = eligible(emails, coded, used_ids())
    sealed = slice_sample(pool, 50, SEED, have=opened, floor=FLOOR)
    sealed.sort(key=lambda e: e["id"])
    write([tagged(e, "open") for e in opened], OUT / "open.jsonl")
    write([tagged(e, "sealed") for e in sealed], OUT / "sealed.jsonl")
    print(len(opened), "open,", len(sealed), "sealed, drawn from", len(pool))
    print_slices(opened, sealed)


if __name__ == "__main__":
    main()
