"""Lesson 06.4: record the chunks hd-1 retrieved for the 60 questions.

NEEDS A MODEL: it embeds each question with the local embedding model (run
`make doctor` first). The recording is already in the repo, in
runs/06-chunks, and no test runs this file. Before it writes anything it
checks that every article and score matches the earlier recording in
runs/06-retrieval.

From this folder: uv run python record_chunks.py
"""
import json
import re
from datetime import datetime

from helpdesk.search import search
from scorecard import data

OUT = data.DATA / "runs" / "06-chunks" / "hd-1.jsonl"


def squash(text):
    """Lower case, with runs of spaces, stars and bars as one space."""
    return re.sub(r"[\s*|]+", " ", text).strip().lower()


def record():
    recorded = {r["id"]: r for r in data.run("06-retrieval")["hd-1"]}
    rows = []
    for q in data.questions():
        hits = search(q["question"], k=10)  # the same call hd-1 made
        old = recorded[q["id"]]["top10"]
        assert all(h["article_id"] == o["article_id"]
                   and abs(h["score"] - o["score"]) < 0.002
                   for h, o in zip(hits, old)), q["id"]
        quote = squash(q["answer_quote"] or "")
        chunks = []
        for rank, h in enumerate(hits, start=1):
            parts = h["text"].split("\n\n", 2)
            head = parts[1] if len(parts) > 1 else ""
            chunks.append({
                "rank": rank, "article_id": h["article_id"],
                "section": head[3:] if head.startswith("## ") else "(intro)",
                "score": h["score"],
                "has_quote": bool(quote) and quote in squash(h["text"]),
                "text": h["text"]})
        rows.append({"id": q["id"], "chunks": chunks})
    OUT.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n"
                           for r in rows), encoding="utf-8")
    print(len(rows), "questions recorded", datetime.now().date())


if __name__ == "__main__":
    record()
