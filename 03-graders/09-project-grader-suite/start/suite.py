"""Lesson 03.9: the grader suite: a marker for each failure type.

Each failure type from the failure map gets a marker: the code checks that
target it, the written rule and model judge, or a note saying what is
still to build. Run the report: uv run python run_suite.py
"""
from scorecard.graders import CHECKS

RULE_AND_JUDGE = {"F-wrong-rule": "right rule: Arjun's rule + judge_rule"}
LATER = {"F-misread": "needs its own rule and judge (not built here)",
         "F-off-topic": "needs its own rule and judge (not built here)",
         "F-obeys-injection": "attack set and outcome check (Module 08)"}
TYPES = ["F-overreach", "F-misread", "F-wrong-rule", "F-bluff",
         "F-asks-again", "F-spam-reply", "F-wrong-page", "F-off-topic",
         "F-language", "F-obeys-injection", "F-no-draft"]


def checks_for(failure):
    """Names of the code checks meant to catch one failure type."""
    raise NotImplementedError(
        "TODO 03.9: return the names of the checks in CHECKS whose "
        "wanted types include failure, see the lesson's 'Steps' section")


def marker(failure):
    """How the suite marks one failure type, in words."""
    raise NotImplementedError(
        "TODO 03.9: return the code checks as 'code: name + name', else "
        "the RULE_AND_JUDGE or LATER note, see the lesson's 'Steps' "
        "section")
