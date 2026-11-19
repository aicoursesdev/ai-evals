"""Lesson 02.6: which slices have no room left to show an improvement?

Given: it reads the table of your `score_by_slice` from lesson 02.3.
From this folder: uv run python too_easy.py
"""
from held_back import usable_emails, usable_triage
from score_by_slice import score_by_slice


def main():
    table = score_by_slice(usable_emails(), usable_triage())
    print("slice                     right  left to fix")
    for (field, value), (right, total) in sorted(table.items(), key=str):
        if field == "category" and right / total >= 0.95 and total >= 15:
            print(f"{field + '=' + value:<26}{right:>2}/{total:<3} "
                  f"{total - right:>5}")


if __name__ == "__main__":
    main()
