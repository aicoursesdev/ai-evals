"""Draw the 100 emails you will read: 25 from each of the four weeks.

    uv run python sample.py          # print the ids
    uv run python sample.py --sheet  # also start your notes sheet
"""
import random
import sys

from plumbing import print_ids, write_sheet
from scorecard import data


def draw_ids():
    """25 ids from each of weeks 1 to 4, the same 100 every time."""
    raise NotImplementedError(
        "TODO 01.3: seed random.Random(1), then for each week add "
        "sorted(rng.sample(that week's ids, 25)) to a list and return it, "
        "see the lesson's 'Draw the 100' section")


if __name__ == "__main__":
    ids = draw_ids()
    print_ids(ids)
    if "--sheet" in sys.argv:
        write_sheet(ids)
