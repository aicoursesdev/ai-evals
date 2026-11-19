"""Given: the recorded drafts and judge runs the cost table reads. Sealed
emails are never read: scorecard.graders.logged skips them."""
from scorecard import data
from scorecard.graders import logged


def log_pairs():
    """[(email, trace)] for the 550 log emails outside the sealed part,
    hd-1's drafts."""
    out = []
    for w in (1, 2, 3, 4):
        traces = {t["id"]: t for t in logged("traces", w)}
        out += [(e, traces[e["id"]]) for e in logged("emails", w)]
    return out


def open_traces():
    """hd-1's traces for the 100 emails of the open part of the test set."""
    keep = {e["id"] for e in data.testset("open")}
    return [t for _, t in log_pairs() if t["id"] in keep]


def judge_calls(folder):
    """The recorded replies of one judge run: seconds and tokens each."""
    return data.read_jsonl(data.DATA / "runs" / folder / "judge.jsonl")
