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
    rng = random.Random(1)  # the same seed gives the same choices
    ids = []
    for week in (1, 2, 3, 4):
        week_ids = [e["id"] for e in data.emails(week=week)]
        ids += sorted(rng.sample(week_ids, 25))  # 25 different, in order
    return ids


if __name__ == "__main__":
    ids = draw_ids()
    print_ids(ids)
    if "--sheet" in sys.argv:
        write_sheet(ids)
