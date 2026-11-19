"""Lesson 03.2: the four kinds of code check, written by hand.

The four cases that use them are in four_cases.py.
"""
import re

CATEGORIES = {"refund", "return", "shipping_delay", "order_change",
              "product_question", "warranty", "payment", "account",
              "complaint", "spam", "other"}


def exact(output, expected):
    """Exact match: the same text, after trimming spaces."""
    raise NotImplementedError(
        "TODO 03.2: return True when output and expected are the same "
        "text after .strip(), see the lesson's 'Four rules a program "
        "can apply' section")


def pattern(output, regex):
    """A pattern: the regular expression is found somewhere in the text."""
    raise NotImplementedError(
        "TODO 03.2: return True when re.search finds regex in output, "
        "see the lesson's 'Four rules a program can apply' section")


def schema(output, allowed):
    """A schema: every key is there and holds one of its allowed values."""
    raise NotImplementedError(
        "TODO 03.2: return True when every key of allowed holds one of "
        "its allowed values, see the lesson's 'Four rules a program can "
        "apply' section")


def within(output, expected, tolerance):
    """A number within a tolerance of the one it should be."""
    raise NotImplementedError(
        "TODO 03.2: return True when output is within tolerance of "
        "expected, see the lesson's 'Four rules a program can apply' "
        "section")
