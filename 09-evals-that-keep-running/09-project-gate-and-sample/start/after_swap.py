"""Project 09: the scorecard rerun after the model swap, as Markdown.

Given: the recordings, the paired range and the lines that print.
You write `triage_line` and `judge_line`.

From this folder: uv run python after_swap.py
Reads the recordings of data/runs/09-model-swap/ and 09-judge-swap/.
"""
import json

from plumbing import clean, right, swap
from scorecard import data
from scorecard.judge import confusion, reading
from scorecard.stats import mcnemar, paired


def triage_line(a, b):
    """One bullet for two 0/1 lists (usual, smaller) on the same emails:
    the two counts, the paired change with its range and McNemar's p."""
    raise NotImplementedError(
        "TODO 09.9: write the bullet for the paired triage change, see "
        "the lesson's 'Step 3: rerun the scorecard after the swap' "
        "section")


def judge_line(name, human, said, ids):
    """One bullet: how many of Arjun's passes the judge kept and how many
    of his fails it held back. human maps id to his call, said to the
    judge's reading; only a clear "pass" counts as a pass."""
    raise NotImplementedError(
        "TODO 09.9: write the bullet for a judge's two rates, see the "
        "lesson's 'Step 3: rerun the scorecard after the swap' section")


if __name__ == "__main__":
    mail, old, new = swap()
    ids = sorted(new)
    print("## Triage, same 149 emails")
    a, b = [[right(mail[i], t[i]) for i in ids] for t in (old, new)]
    print(triage_line(a, b))

    print("\n## Code checks, same 149 emails")
    a, b = [[clean(mail[i], t[i]) for i in ids] for t in (old, new)]
    print(f"- no check fires: usual {sum(a)}, smaller {sum(b)}, "
          f"McNemar p {mcnemar(a, b):.2f}")

    print("\n## The judge, 100 held-out drafts, against Arjun")
    human = {r["id"]: r["call"] for r in data.labels("04-right-rule-arjun")}
    held = json.loads((data.DATA / "labels" / "04-judge-set-ids.json")
                      .read_text())
    keep = [i for i in held if human[i] != "unsure"]
    for name, folder in (("usual", "04-heldout"),
                         ("smaller", "09-judge-swap")):
        said = {r["id"]: reading(r["reply"]) for r in
                data.read_jsonl(data.DATA / "runs" / folder / "judge.jsonl")}
        print(judge_line(name, human, said, keep))
