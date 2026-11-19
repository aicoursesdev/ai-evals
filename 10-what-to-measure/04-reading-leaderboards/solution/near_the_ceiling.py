"""Lesson 10.4: why two scores near 100% cannot be told apart. The scores
are made up for the arithmetic; the range is lesson 05.3's.

From this folder: uv run python near_the_ceiling.py
"""
from scorecard.stats import wilson

QUESTIONS = 500   # a benchmark of 500 questions

def score_line(right):
    """One line: the score on QUESTIONS questions and its 95% range."""
    low, high = wilson(right, QUESTIONS)
    return (f"{right} of {QUESTIONS} right ({right / QUESTIONS:.1%}): "
            f"range {low:.1%} to {high:.1%}")


if __name__ == "__main__":
    for right in (400, 490, 495):
        print(score_line(right))
