"""Lesson 06.4: recall at 3 counted two ways: the right page is in the top
3, or the passage that holds the answer is (chunks recorded in
runs/06-chunks).

From this folder: uv run python page_or_passage.py
"""
from scorecard import data

records = {x["id"]: x["chunks"] for x in data.run("06-chunks")["hd-1"]}
asked = [q for q in data.questions() if q["answer_article"]]
page = [q["id"] for q in asked
        if any(c["article_id"] == q["answer_article"]
               for c in records[q["id"]][:3])]
passage = [q["id"] for q in asked
           if any(c["has_quote"] for c in records[q["id"]][:3])]
print(f"page in top 3:    {len(page)}/{len(asked)}")
print(f"passage in top 3: {len(passage)}/{len(asked)}")
for q in asked:
    if q["id"] in page and q["id"] not in passage:
        got = [c for c in records[q["id"]][:3]
               if c["article_id"] == q["answer_article"]][0]
        print(f"  {q['id']}: right page, but the chunk is "
              f"'{got['section']}', not the answer's")
