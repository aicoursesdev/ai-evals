"""Lesson 06.2: recall, precision and reciprocal rank, the finished versions.

The course's own file is scorecard/retrieval.py: every later lesson imports
it from there. This file only points at it, so your start/retrieval.py can
be compared with it (make diff 06.2).
"""
from scorecard.retrieval import (  # noqa: F401
    mrr, precision_at_k, recall_at_k, reciprocal_rank)
