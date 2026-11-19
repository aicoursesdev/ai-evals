"""Given for lesson 02.5: reading the prompts and the launch set, and the
Module 00 grader. It reads launch traces only, never the log's."""
from functools import cache

from scorecard import data

VERSIONS = data.DATA.parent / "helpdesk" / "versions"


def email_text(email):
    """What a customer wrote: the subject, then the body."""
    return email["subject"] + " " + email["body"]


def prompt_sources():
    """{'hd-1/triage.md': its text} for each prompt file of hd-1."""
    return {f"{p.parent.name}/{p.name}": p.read_text(encoding="utf-8")
            for p in sorted(VERSIONS.glob("hd-1/*.md"))}


def launch_halves():
    """The launch set split into its (test, dev) halves."""
    launch = data.emails(launch=True)
    return ([e for e in launch if e["split"] == "test"],
            [e for e in launch if e["split"] == "dev"])


@cache
def launch_triage():
    """{id: the help desk's three labels} for the 150 launch emails."""
    return {t["id"]: t["triage"] for t in data.traces("hd-1", launch=True)}


def right(email):
    """The Module 00 grader: the help desk's category equals Arjun's."""
    return launch_triage()[email["id"]]["category"] == email["category"]


def print_scores(test, leaked, clean):
    """The three lines of lesson 02.5's score: all, leaked and without."""
    print("all test emails :", sum(map(right, test)), "of", len(test))
    hit = sum(right(e) for e in test if e["id"] in leaked)
    print("the leaked ones :", hit, "of", len(leaked), sorted(leaked))
    print("without them    :", sum(map(right, clean)), "of", len(clean),
          f"= {sum(map(right, clean)) / len(clean):.1%}")
