"""Lesson 03.2: the four kinds of code check, written by hand.

The four cases that use them are in four_cases.py.
"""
import re

CATEGORIES = {"refund", "return", "shipping_delay", "order_change",
              "product_question", "warranty", "payment", "account",
              "complaint", "spam", "other"}


def exact(output, expected):
    """Exact match: the same text, after trimming spaces."""
    return output.strip() == expected.strip()


def pattern(output, regex):
    """A pattern: the regular expression is found somewhere in the text."""
    return re.search(regex, output) is not None


def schema(output, allowed):
    """A schema: every key is there and holds one of its allowed values."""
    return all(output.get(key) in values for key, values in allowed.items())


def within(output, expected, tolerance):
    """A number within a tolerance of the one it should be."""
    return abs(output - expected) <= tolerance
