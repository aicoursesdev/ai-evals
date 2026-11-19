"""Search the help centre: one chunk per ## section, found by embedding.

Every chunk is embedded once and the vectors are cached under .cache/, so a
second run starts at once. A query is embedded the same way and compared by
cosine similarity. hd-1 searches every article, archived ones included.
"""
import hashlib
from pathlib import Path

import numpy as np

from helpdesk.llm import EMBED_MODEL, embed

ROOT = Path(__file__).resolve().parent.parent
INSTRUCTION = ("Instruct: Given a customer question, retrieve help-centre "
               "passages that answer it\nQuery:")


def articles(folder=ROOT / "data" / "help-centre"):
    """Every article as a dict: id, title, updated, status, text."""
    result = []
    for path in sorted(Path(folder).glob("*.md")):
        _, header, text = path.read_text(encoding="utf-8").split("---\n", 2)
        a = dict(line.split(":", 1) for line in header.strip().splitlines())
        a = {k.strip(): v.strip().strip('"') for k, v in a.items()}
        result.append(a | {"text": text.strip()})
    return result


def chunks(article):
    """One chunk per ## section, each starting with the article's title."""
    parts = article["text"].split("\n## ")
    return [{"article_id": article["id"], "status": article["status"],
             "text": f"# {article['title']}\n\n{'## ' if n else ''}{p.strip()}"}
            for n, p in enumerate(parts)]


def _vectors(texts, cache=True):
    """Unit-length vectors for the texts, cached on disk by their content."""
    key = hashlib.sha1((EMBED_MODEL + "\n".join(texts)).encode()).hexdigest()[:16]
    path = ROOT / ".cache" / f"help-index-{key}.npy"
    if cache and path.exists():
        return np.load(path)
    m = np.array([v for i in range(0, len(texts), 16) for v in embed(texts[i:i + 16])])
    m /= np.linalg.norm(m, axis=1, keepdims=True)
    if cache:
        path.parent.mkdir(exist_ok=True)
        np.save(path, m)
    return m


_index = {}


def index():
    if not _index:
        _index["chunks"] = [c for a in articles() for c in chunks(a)]
        _index["matrix"] = _vectors([c["text"] for c in _index["chunks"]])
    return _index


def search(query, k=3, filter_archived=False, extra_articles=()):
    """The k best chunks, best first: dicts with article_id, text, score.

    extra_articles are articles added for one call only (the red-team plants one).
    """
    idx = index()
    found, matrix = idx["chunks"], idx["matrix"]
    if extra_articles:
        more = [c for a in extra_articles for c in chunks(a)]
        found = found + more
        matrix = np.vstack([matrix, _vectors([c["text"] for c in more], cache=False)])
    q = np.array(embed([INSTRUCTION + query])[0])
    scores = matrix @ (q / np.linalg.norm(q))
    if filter_archived:
        scores = np.where([c["status"] == "current" for c in found], scores, -np.inf)
    best = np.argsort(-scores)[:k]
    return [{"article_id": found[i]["article_id"], "text": found[i]["text"],
             "score": round(float(scores[i]), 4)} for i in best]
