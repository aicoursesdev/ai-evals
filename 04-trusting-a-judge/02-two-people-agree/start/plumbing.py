"""Given: the two labellers' calls on the 100 held-out drafts."""
from scorecard import data


def reasons(who):
    """{id: (call, reason)} from labels/04-right-rule-<who>.csv."""
    rows = data.labels(f"04-right-rule-{who}")
    return {r["id"]: (r["call"], r["reason"]) for r in rows}


def two_columns():
    """(ids, arjun's calls, divya's calls), the same 100 drafts in the
    same order, each call "pass", "fail" or "unsure"."""
    a, d = reasons("arjun"), reasons("divya")
    ids = sorted(a)
    return ids, [a[i][0] for i in ids], [d[i][0] for i in ids]


def settled(a, d):
    """The two lists of calls without the drafts where either person
    said unsure."""
    pairs = [(x, y) for x, y in zip(a, d) if "unsure" not in (x, y)]
    return [x for x, _ in pairs], [y for _, y in pairs]
