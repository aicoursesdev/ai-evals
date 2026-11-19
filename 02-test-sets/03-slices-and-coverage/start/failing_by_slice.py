"""Lesson 02.3: Module 01's failure map, cut by slice.

Given: it is `score_by_slice` again, counting the drafts Module 01 marked
as failing instead of the categories that match.
From this folder: uv run python failing_by_slice.py
"""
from scorecard import data
from slices import slices_of


def failing_by_slice(emails, coded):
    """{slice: [failing drafts, emails read]} over the emails you read."""
    failed = {row["id"]: row["ok"] == "no" for row in coded}
    table = {}
    for email in emails:
        for one in slices_of(email):
            row = table.setdefault(one, [0, 0])
            row[0] += failed[email["id"]]
            row[1] += 1
    return table


if __name__ == "__main__":
    table = failing_by_slice(data.testset("open"), data.labels("01-coded"))
    print("slice                     failing of read")
    for (field, value), (bad, n) in sorted(table.items(), key=str):
        print(f"{field + '=' + str(value):<26}{bad:>3} of {n:<3}"
              f"{bad / n:>6.0%}")
