"""Lesson 02.7: the coverage table of test set v1, as Markdown.

From this folder: uv run python coverage_table.py
Reads emails and the set's parts only. It never opens a trace.
"""
from plumbing import PARTS
from scorecard import data
from slices import log, tally


def table(traffic, parts):
    """Markdown: one row per slice with its count in the log, in each part,
    in open + sealed together (" (under 10)" when fewer than 10) and made
    up. `traffic` and each part in `parts` come from `tally`."""
    lines = ["| Slice | In the log | Open | Sealed | Real (open + sealed) | "
             "Made up |", "| --- | ---: | ---: | ---: | ---: | ---: |"]
    for one in sorted(traffic, key=lambda s: (s[0], str(s[1]))):
        o, s, m = (parts[p][one] for p in PARTS)
        thin = " (under 10)" if o + s < 10 else ""
        lines.append(f"| {one[0]}={one[1]} | {traffic[one]} | {o} | {s} | "
                     f"{o + s}{thin} | {m} |")
    return "\n".join(lines)


if __name__ == "__main__":
    parts = {p: tally(data.testset(p)) for p in PARTS}
    print(table(tally(log()), parts))
