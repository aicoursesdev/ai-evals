"""Lesson 06.2: what a larger k buys, and what it lets in: the archived page
and the amount of text handed to the model (chunks recorded in
runs/06-chunks).

From this folder: uv run python bigger_k.py
"""
from scorecard import data

chunks = {r["id"]: r["chunks"] for r in data.run("06-chunks")["hd-1"]}
for k in (1, 3, 5, 10):
    old = sum(any(c["article_id"] == "shipping-india-2024"
                  for c in chunks[q][:k])
              for q in chunks)
    words = sum(len(c["text"].split())
                for q in chunks for c in chunks[q][:k]) / len(chunks)
    print(f"k={k:2}  questions with the archived page in the top k: {old:2}"
          f"   words handed over per question: {words:.0f}")
