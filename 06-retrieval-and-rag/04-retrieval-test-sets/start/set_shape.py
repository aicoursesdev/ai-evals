"""Lesson 06.4: what the 60 questions cover: their kinds, the pages with no
question, and how many of a question's words are copied from its answer
passage.

From this folder: uv run python set_shape.py
"""
from collections import Counter

from scorecard import data

qs = data.questions()
print(Counter(q["kind"] for q in qs))
asked = {q["answer_article"] for q in qs if q["answer_article"]}
pages = [a["id"] for a in data.articles()]
print(len(pages), "pages;", len(asked), "have a question; none for:",
      [p for p in pages if p not in asked])

import re

words = lambda s: set(re.findall(r"[a-z0-9₹]{3,}", s.lower()))
for kind in ("paraphrase", "keyword", "multi-part"):
    raise NotImplementedError(
        "TODO 06.4: set share to a list with one number per question of "
        "this kind: how many of words(q['question']) are also in "
        "words(q['answer_quote']), divided by how many words the question "
        "has, see the lesson's 'Questions people would really ask' section")
    print(f"{kind:11} question words found in the passage: "
          f"{sum(share) / len(share):.0%}")
