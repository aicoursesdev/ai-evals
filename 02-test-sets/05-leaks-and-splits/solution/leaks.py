"""Lesson 02.5: a small leak checker.

A leak is text the system was built from that also sits in the test set.
You write these four functions; `email_text` is given in plumbing.py.
"""
import re

from plumbing import email_text


def words(text):
    """Lower-case words, split on spaces and punctuation (any script)."""
    parts = re.split(r"[\s.,!?:;()\"'“”‘’]+", text.lower())
    return [w for w in parts if w]


def shingles(text, n=3):
    """The set of n-word runs in the text (n=1 is just its words). A text
    shorter than n words is one run on its own."""
    w = words(text)
    return {tuple(w[i:i + n]) for i in range(max(1, len(w) - n + 1))}


def contained(email, source):
    """Share of the email's runs that also occur in the source text.
    1.0 means every three-word run of the email is in the source."""
    mine = shingles(email_text(email))
    return len(mine & shingles(source)) / len(mine)


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
