"""Lesson 10.6: the evidence line that refuses a number without its n and
its source, and the one-page report built from such lines. The finished
functions are also in scorecard/report.py, which the later lessons use."""
from scorecard.stats import wilson


def figure(name, hits, n, source):
    """One evidence line: the share, the count it rests on, its Wilson
    95% range and the file it came from. Refuses a line with no n or no
    source. figure("no check fires", 36, 50, "run") gives "no check fires:
    36 of 50 (72.0%), 95% range 58.3% to 82.5% [run]"."""
    raise NotImplementedError(
        "TODO 10.6: return the evidence line, and raise ValueError for no "
        "n or no source, see the lesson's 'The rules every number follows' "
        "section")


def one_page(title, decision, evidence, uncertainty, cost, change):
    """The one-page report as Markdown: the decision first, then the
    evidence (a list of (name, hits, n, source), each through figure),
    and lists of strings for what is uncertain, what it costs and what
    would change the decision."""
    raise NotImplementedError(
        "TODO 10.6: return the five parts as Markdown, the decision first, "
        "see the lesson's 'The rules every number follows' section")
