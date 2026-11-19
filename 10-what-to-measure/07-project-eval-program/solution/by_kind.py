"""Lesson 10.7: the decision rule of the report, applied to each kind of
email. The rule (written before the sealed part was opened, in
data/runs/10-sealed/plan.md): a kind may go out unread only if a person
has read at least 59 of its drafts, none with a failure that matters.

From this folder: uv run python by_kind.py
"""
from collections import defaultdict

from plumbing import open_read
from scorecard.stats import exact_upper

NEEDED = 59   # clean reads that put the exact 95% upper limit at 5% or less


def by_kind(drafts):
    """{category: (drafts a person read, of them with a failure)}."""
    seen = defaultdict(lambda: [0, 0])
    for d in drafts:
        seen[d["category"]][0] += 1
        seen[d["category"]][1] += not d["fine"]
    return {k: tuple(v) for k, v in seen.items()}


def may_go_unread(read, failed):
    """True only when 59 or more were read and none failed."""
    return read >= NEEDED and failed == 0


if __name__ == "__main__":
    print(f"clean reads needed: {NEEDED} "
          f"(upper limit {exact_upper(0, NEEDED):.3f})")
    print(f"{'kind':16} read  failed  may go out unread")
    for kind, (read, failed) in sorted(by_kind(open_read()).items(),
                                       key=lambda x: -x[1][0]):
        print(f"{kind:16} {read:3}  {failed:4}    "
              f"{'yes' if may_go_unread(read, failed) else 'no'}")
