"""Lesson 00.3: run cases through a system, grade, save and load.

The course's own finished version is scorecard/run.py.
"""
import json


def run(cases, system, graders):
    """Call system(case) for each case and apply every named grader."""
    raise NotImplementedError(
        "TODO 00.3: for each case get output = system(case), then return "
        "one row per case: {'id': case.get('id'), 'output': output} plus "
        "bool(grader(output, case)) under each grader's name, see the "
        "lesson's 'From twenty lines to a tool' section")


def save(results, path):
    """Write the rows to path, one JSON object per line."""
    raise NotImplementedError(
        "TODO 00.3: open path for writing (utf-8) and write each row as "
        "json.dumps(row, ensure_ascii=False) plus a newline, see the "
        "lesson's 'From twenty lines to a tool' section")


def load(path):
    """Read the rows save wrote."""
    raise NotImplementedError(
        "TODO 00.3: read path line by line and return json.loads of each "
        "non-empty line, see the lesson's 'From twenty lines to a tool' "
        "section")


def pass_rate(results, grader):
    """The share of rows where the named grader passed."""
    raise NotImplementedError(
        "TODO 00.3: return the number of rows with row[grader] true "
        "divided by the number of rows, see the lesson's 'From twenty "
        "lines to a tool' section")
