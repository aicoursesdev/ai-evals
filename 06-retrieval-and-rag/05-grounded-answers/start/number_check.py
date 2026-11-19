"""Lesson 06.5: a check code can do. Every number in the reply (not counting
the [citation] tags) must appear in the chunks the help desk was shown or
in the question. Compared with Arjun's grounded labels.

From this folder: uv run python number_check.py
"""
import re

from scorecard import data
from scorecard.judge import confusion, rates

nums = lambda text: {n.rstrip(".,").replace(",", "")
                     for n in re.findall(r"\d[\d,.]*", text)}
runs = {r["id"]: r for r in data.run("06-retrieval")["hd-1"]}
chunks = {r["id"]: r["chunks"] for r in data.run("06-chunks")["hd-1"]}
grounded = {r["id"]: r["grounded"] == "1"
            for r in data.labels("06-answers-arjun")}
ids = list(runs)
seen = [" ".join(c["text"] for c in chunks[i][:3]) for i in ids]
asked = {q["id"]: q["question"] for q in data.questions()}
reply = lambda i: re.sub(r"\[[^\]]*\]", "", runs[i]["draft"])  # drop tags
raise NotImplementedError(
    "TODO 06.5: set unseen to a dict from each question id i (with its "
    "chunks text t, from zip(ids, seen)) to the numbers in reply(i) that "
    "are in neither t nor the question asked[i], using nums, see the "
    "lesson's 'A check code can do' section")
check = [not unseen[i] for i in ids]          # True means the check passes
human = [grounded[i] for i in ids]
print("check passes:", sum(check), "of", len(ids),
      "| Arjun says grounded:", sum(human))
print(confusion(human, check))
tpr, tnr = rates(human, check)
print(f"catches {tnr:.0%} of the ungrounded answers; "
      f"passes {tpr:.0%} of the grounded ones")
print("numbers not in the chunks:",
      {i: sorted(v) for i, v in unseen.items() if v})
