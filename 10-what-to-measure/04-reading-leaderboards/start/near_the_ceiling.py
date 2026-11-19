"""Lesson 10.4: why two scores near 100% cannot be told apart. The scores
are made up for the arithmetic; the range is lesson 05.3's.

From this folder: uv run python near_the_ceiling.py
"""
from scorecard.stats import wilson

QUESTIONS = 500   # a benchmark of 500 questions

def score_line(right):
    """One line: the score on QUESTIONS questions and its 95% range."""
    raise NotImplementedError(
        "TODO 10.4: return the line the lesson shows, the score and its "
        "Wilson range, see the lesson's 'Is it saturated' section")


if __name__ == "__main__":
    for right in (400, 490, 495):
        print(score_line(right))
