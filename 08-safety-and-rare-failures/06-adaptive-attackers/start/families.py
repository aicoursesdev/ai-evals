"""Lesson 08.6: one trick, many wordings: the "approval" family.

From this folder: uv run python families.py
"""
from scorecard import data

# Emails that claim a refund is already approved and tell the AI to act.
APPROVAL = {"E-0049", "E-0123", "E-0289", "E-0292", "E-0426", "E-0438",
            "E-0551", "E-0558", "E-0733"}
EARLY = ("launch", "log-week-1", "log-week-2")
LATE = ("log-week-3", "log-week-4")
rows = [r for r in data.labels("08-attack-outcomes")
        if r["source"] != "red-team" and not r["repeat_of"]]

def failed(rows):
    """The ids of the emails whose reply complied or complied in part."""
    raise NotImplementedError(
        "TODO 08.6: return the ids of the rows whose outcome is not "
        "'resisted', see the lesson's 'What a changing wording can do "
        "on this help desk' section")

for when, sources in (("launch to week 2", EARLY), ("weeks 3 and 4", LATE)):
    print(when)
    for name, flag in (("approval", True), ("other", False)):
        mine = [r for r in rows if r["source"] in sources
                and (r["id"] in APPROVAL) == flag]
        print(f"  {name:9} {len(failed(mine))} of {len(mine)} "
              f"complied or partly: {failed(mine)}")
