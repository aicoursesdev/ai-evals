"""Lesson 06.5: citations. Which replies cite a page the help desk was not
shown among its top 3 chunks, or cite no page at all?

From this folder: uv run python citations.py
"""
from scorecard import data

for r in data.run("06-retrieval")["hd-1"]:
    shown = {h["article_id"] for h in r["top10"][:3]}
    cited = r["citations"]
    unseen = [c for c in cited if c not in shown]
    if unseen or not cited:
        print(r["id"], "cited", cited, "not shown:", unseen)
