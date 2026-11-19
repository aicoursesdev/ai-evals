"""Lesson 02.5: Kiran's test score with and without the leaked emails.

From this folder: uv run python score_without_leaks.py
"""
from leaks import find_leaks
from plumbing import launch_halves, print_scores, prompt_sources


def split_leaked(test, sources):
    """The ids of the test emails found in a source, and the clean rest."""
    raise NotImplementedError(
        "TODO 02.5: return the set of leaked ids and the list of "
        "clean emails, see the lesson's 'The score with and without' "
        "section")


if __name__ == "__main__":
    test, _ = launch_halves()
    leaked, clean = split_leaked(test, prompt_sources())
    print_scores(test, leaked, clean)
