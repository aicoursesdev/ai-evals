"""Lesson 02.5: a small leak checker.

A leak is text the system was built from that also sits in the test set.
Given in lesson 02.7: the checker you wrote in 02.5, in one file.
"""
import re


def words(text):
    """Lower-case words, split on spaces and punctuation (any script)."""
    parts = re.split(r"[\s.,!?:;()\"'“”‘’]+", text.lower())
    return [w for w in parts if w]


def shingles(text, n=3):
    """The set of n-word runs in the text (n=1 is just its words). A text
    shorter than n words is one run on its own."""
    w = words(text)
    return {tuple(w[i:i + n]) for i in range(max(1, len(w) - n + 1))}


def email_text(email):
    """What a customer wrote: the subject, then the body."""
    return email["subject"] + " " + email["body"]


def contained(email, source):
    """Share of the email's runs that also occur in the source text.
    1.0 means every three-word run of the email is in the source."""
    mine = shingles(email_text(email))
    return len(mine & shingles(source)) / len(mine)


def similar(a, b, n=3):
    """Overlap of two emails, 0 to 1: shared runs over all runs."""
    sa, sb = shingles(email_text(a), n), shingles(email_text(b), n)
    return len(sa & sb) / len(sa | sb)


def find_leaks(emails, sources, floor=0.8):
    """Emails of the test set found inside a source: [(id, source, share)].
    `sources` is {name: text}; anything at or above `floor` is reported."""
    found = []
    for email in emails:
        for name, text in sources.items():
            share = contained(email, text)
            if share >= floor:
                found.append((email["id"], name, round(share, 2)))
    return found


def near_pairs(emails, floor=0.5, n=3):
    """Pairs of emails that overlap by `floor` or more: [(a, b, overlap)]."""
    pairs = []
    for i, a in enumerate(emails):
        for b in emails[i + 1:]:
            s = similar(a, b, n)
            if s >= floor:
                pairs.append((a["id"], b["id"], round(s, 2)))
    return sorted(pairs, key=lambda p: -p[2])
