"""Given for lesson 02.5: how much two emails overlap, and every close pair."""
from leaks import shingles
from plumbing import email_text


def similar(a, b, n=3):
    """Overlap of two emails, 0 to 1: shared runs over all runs."""
    sa, sb = shingles(email_text(a), n), shingles(email_text(b), n)
    return len(sa & sb) / len(sa | sb)


def near_pairs(emails, floor=0.5, n=3):
    """Pairs of emails that overlap by `floor` or more: [(a, b, overlap)]."""
    runs = [shingles(email_text(e), n) for e in emails]  # once per email
    pairs = []
    for i, a in enumerate(emails):
        for j in range(i + 1, len(emails)):
            s = len(runs[i] & runs[j]) / len(runs[i] | runs[j])
            if s >= floor:
                pairs.append((a["id"], emails[j]["id"], round(s, 2)))
    return sorted(pairs, key=lambda p: -p[2])
