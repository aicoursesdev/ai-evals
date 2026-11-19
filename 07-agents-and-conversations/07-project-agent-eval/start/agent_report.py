"""Lesson 07.7: is the refund agent reliable? Write the report for Meera
here, from the 180 recorded trials of hd-1.

From this folder: uv run python agent_report.py
The finished script is in solution/agent_report.py.
"""
from collections import Counter  # noqa: F401

from checks import CHECKS, RULES, outcome_ok  # noqa: F401
from scorecard import agents, data, stats  # noqa: F401

raise NotImplementedError(
    "TODO 07.7: do steps 1 to 6 of 'What to build', printing each figure "
    "as you go: load the scenarios and the 180 trials with scorecard.data "
    "and attach each trial's scenario as t['scenario'], then the outcome "
    "rate at temperature 0 with its Wilson range, pass@k and pass^k from "
    "the five trials at 0.7, the rules broken, the first failing links "
    "and the tokens, see the lesson's 'What to build' section")
