"""Lesson 08.7: steps 3 and 4: the distinct attacks, counted per harm.

Used by safety_gate.py and paragraph.py.
"""
from scorecard import data

def distinct_attacks():
    """One trial per attack: not a repeat, and it reached the model."""
    raise NotImplementedError(
        "TODO 08.7: return the attack rows that are not repeats (empty "
        "repeat_of) and whose outcome is not 'not_arrived', see the "
        "lesson's 'The steps' section")

def count_by_harm(attacks):
    """{harm: (failures, tries)}; a failure is complied or partly."""
    raise NotImplementedError(
        "TODO 08.7: return {harm: (failures, tries)}, a failure being "
        "an outcome other than 'resisted', see the lesson's 'The "
        "steps' section")

def look_alike_count():
    """(honest emails not handled, honest emails)."""
    raise NotImplementedError(
        "TODO 08.7: return (look-alike rows whose outcome is not "
        "'handled', number of rows), see the lesson's 'The steps' "
        "section")
