"""Lesson 10.6: the evidence line that refuses a number without its n and
its source, and the one-page report built from such lines. The finished
functions are also in scorecard/report.py, which the later lessons use."""
from scorecard.stats import wilson


def figure(name, hits, n, source):
    """One evidence line: the share, the count it rests on, its Wilson
    95% range and the file it came from. Refuses a line with no n or no
    source. figure("no check fires", 36, 50, "run") gives "no check fires:
    36 of 50 (72.0%), 95% range 58.3% to 82.5% [run]"."""
    if n <= 0 or not source:
        raise ValueError(f"{name}: a number needs its n and its source")
    low, high = wilson(hits, n)
    return (f"{name}: {hits} of {n} ({hits / n:.1%}), "
            f"95% range {low:.1%} to {high:.1%} [{source}]")


def one_page(title, decision, evidence, uncertainty, cost, change):
    """The one-page report as Markdown: the decision first, then the
    evidence (a list of (name, hits, n, source), each through figure),
    and lists of strings for what is uncertain, what it costs and what
    would change the decision."""
    lines = [f"# {title}", "", "## Decision", "", decision, "", "## Evidence",
             ""]
    lines += [f"- {figure(*row)}" for row in evidence]
    for head, items in (("Uncertainty", uncertainty), ("Cost", cost),
                        ("What would change this", change)):
        lines += ["", f"## {head}", ""] + [f"- {x}" for x in items]
    return "\n".join(lines + [""])
