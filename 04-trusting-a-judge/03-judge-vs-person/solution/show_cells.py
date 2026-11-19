"""Lesson 04.3: four real drafts, each in a different cell of the table."""
from plumbing import JUDGE_V1, arjun_dev, drafts, judge_v1, notes
from scorecard import data

arjun, judge, note = arjun_dev(), judge_v1(), notes()
reply = {r["id"]: r["reply"] for r in data.read_jsonl(JUDGE_V1)}
shown = ("E-0602", "E-0660", "E-0158", "E-0216")
for i, (email, draft) in drafts(shown).items():
    print(f"\n{i}  {email['subject']}")
    print("  customer:", email["body"][:150].replace("\n", " "))
    print("  help desk:", draft[:230].replace("\n", " "))
    print(f"  Arjun, {arjun[i]}:", note[i])
    print(f"  judge, {judge[i]}:", reply[i].replace("\n", " "))
