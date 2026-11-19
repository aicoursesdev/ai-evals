"""Lesson 02.5: a small leak checker.

A leak is text the system was built from that also sits in the test set.
You write these four functions; `email_text` is given in plumbing.py.
"""
import re

from plumbing import email_text


def words(text):
    """Lower-case words, split on spaces and punctuation (any script)."""
    raise NotImplementedError(
        "TODO 02.5: return the lower-case words of the text, split on "
        "spaces and punctuation with re.split, see the lesson's 'A "
        "leak checker' section")


def shingles(text, n=3):
    """The set of n-word runs in the text (n=1 is just its words). A text
    shorter than n words is one run on its own."""
    raise NotImplementedError(
        "TODO 02.5: return the set of n-word runs as tuples, see the "
        "lesson's 'A leak checker' section")


def contained(email, source):
    """Share of the email's runs that also occur in the source text.
    1.0 means every three-word run of the email is in the source."""
    raise NotImplementedError(
        "TODO 02.5: return the share of the email's runs that are "
        "also in the source, see the lesson's 'A leak checker' "
        "section")


def find_leaks(emails, sources, floor=0.8):
    """Emails of the test set found inside a source: [(id, source, share)].
    `sources` is {name: text}; anything at or above `floor` is reported."""
    raise NotImplementedError(
        "TODO 02.5: return (id, source name, share) for each email at "
        "or above the floor, see the lesson's 'A leak checker' "
        "section")
