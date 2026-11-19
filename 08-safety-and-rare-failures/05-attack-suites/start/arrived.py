"""Lesson 08.5: did each planted page reach the model? Check the trace.

From this folder: uv run python arrived.py
"""
import re

from scorecard import data

attacks = data.read_jsonl(data.DATA / "attacks" / "red-team.jsonl")
runs = {r["id"]: r for r in data.run("08-attacks")["hd-1"]}
# "plant as data/help-centre/feedback.md ..." names the page: feedback.
planted = {a["id"]: re.search(r"help-centre/(.+?)\.md", a["source"])[1]
           for a in attacks if a["source"].startswith("plant")}

def reached(attack_id):
    """Was the planted page among the chunks the help desk was shown?"""
    raise NotImplementedError(
        "TODO 08.5: return whether planted[attack_id] is among the "
        "article_id values of runs[attack_id]['result']['retrieved'], "
        "see the lesson's 'An attack that never arrives tests nothing' "
        "section")

for attack_id, page in planted.items():
    print(f"{attack_id} planted {page}: reached the model: "
          f"{reached(attack_id)}")
