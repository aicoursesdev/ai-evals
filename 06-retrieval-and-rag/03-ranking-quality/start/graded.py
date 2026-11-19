"""Lesson 06.3: grade every chunk of the help centre for one question.

A chunk is 2 if it holds the answer passage, 1 if it is another part of the
answer page, and 0 otherwise. Other files here import this one.
"""
import re

from helpdesk.search import articles, chunks


def squash(text):
    """Lower case, with runs of spaces, stars and bars as one space."""
    return re.sub(r"[\s*|]+", " ", text).strip().lower()


def section(chunk):
    """The section heading a chunk sits under, or '(intro)'."""
    parts = chunk["text"].split("\n\n", 2)
    head = parts[1] if len(parts) > 1 else ""
    return head[3:] if head.startswith("## ") else "(intro)"


def grades(question):
    """{'page#section': grade} for the answer page's chunks."""
    page = next(a for a in articles() if a["id"] == question["answer_article"])
    quote = squash(question["answer_quote"])
    return {f"{c['article_id']}#{section(c)}":
            2 if quote in squash(c["text"]) else 1
            for c in chunks(page)}


def ranked_ids(record):
    """The recorded chunks of one question as 'page#section' ids."""
    return [f"{c['article_id']}#{c['section']}" for c in record["chunks"]]
