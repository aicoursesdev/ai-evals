"""Lesson 00.4: score the same 10 emails six times: once at temperature 0,
five times at temperature 0.7 (seeds 1 to 5). Reads the recorded runs.

From this folder: uv run python repeats.py
"""

from scorecard import data

runs = data.run("00-ask-twice")            # {file name: list of traces}
week1 = {e["id"]: e for e in data.emails(week=1)}
first = {t["id"]: t for t in data.traces("hd-1", week=1)}
FIELDS = ("category", "urgency", "needs_human")


def category_right(row):
    raise NotImplementedError(
        "TODO 00.4: True when the row's triage category equals Arjun's "
        "category for that email, week1[row['id']]['category'], see the "
        "lesson's 'Same emails, asked again' section")


def all_right(row):
    raise NotImplementedError(
        "TODO 00.4: True when every field in FIELDS (category, urgency, "
        "needs_human) in the row's triage equals Arjun's for that email, "
        "see the lesson's 'Same emails, asked again' section")


print("run                category   all three labels")
for name, rows in runs.items():
    print(f"{name:<18} {sum(map(category_right, rows))} of {len(rows)}"
          f"    {sum(map(all_right, rows))} of {len(rows)}")

same = sum(r["triage"] == first[r["id"]]["triage"]
           and r["draft"] == first[r["id"]]["draft"] for r in runs["temp-0"])
print(f"\ntemperature 0 vs the original week-1 trace: {same} of 10 identical")

seeded = [rows for name, rows in runs.items() if "seed" in name]
print("\nemail    label sets in 5 runs   different drafts in 5 runs")
for i in range(10):
    labels = {tuple(rows[i]["triage"].values()) for rows in seeded}
    drafts = {rows[i]["draft"] for rows in seeded}   # a set drops repeats
    print(seeded[0][i]["id"],
          f"   {len(labels)}                     {len(drafts)}")
