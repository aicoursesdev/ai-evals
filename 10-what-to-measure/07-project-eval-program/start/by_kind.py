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
    raise NotImplementedError(
        "TODO 10.7: return {kind: (drafts read, of them failing)} for the "
        "drafts, see the lesson's 'Steps' section")


def may_go_unread(read, failed):
    """True only when 59 or more were read and none failed."""
    raise NotImplementedError(
        "TODO 10.7: return whether the plan's rule lets a kind go out "
        "unread, see the lesson's 'The brief' section")


if __name__ == "__main__":
    print(f"clean reads needed: {NEEDED} "
          f"(upper limit {exact_upper(0, NEEDED):.3f})")
    print(f"{'kind':16} read  failed  may go out unread")
    for kind, (read, failed) in sorted(by_kind(open_read()).items(),
                                       key=lambda x: -x[1][0]):
        print(f"{kind:16} {read:3}  {failed:4}    "
              f"{'yes' if may_go_unread(read, failed) else 'no'}")
