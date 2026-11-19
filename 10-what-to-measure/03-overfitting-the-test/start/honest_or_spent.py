"""Lesson 10.3: the plan's rule, in code. Given a score on the open part
and the sealed part's range, say what the comparison shows."""


def verdict(open_hits, open_n, low, high):
    """'honest' when the open share is inside the sealed range, 'spent'
    when it is above the top end, 'sealed is higher' when below the
    bottom end. 87 of 100 against a range of 0.786 to 0.957 is honest."""
    raise NotImplementedError(
        "TODO 10.3: return 'honest', 'spent' or 'sealed is higher' by where "
        "the open share falls against the sealed range, see the lesson's "
        "'The plan, written first' section")
