"""Lesson 08.4: do attack emails of one template rise and fall together?

From this folder: uv run python template_groups.py
"""
from markers import template
from scorecard import data
from scorecard.stats import exact_upper

emails = data.emails(launch=True)
for week in (1, 2, 3, 4):
    emails += data.emails(week=week)
bodies = {e["id"]: e["body"] for e in emails}
rows = [r for r in data.labels("08-attack-outcomes")
        if r["source"] != "red-team" and not r["repeat_of"]]
tally = {}
for r in rows:
    name = template(bodies[r["id"]])
    k, n = tally.get(name, (0, 0))
    tally[name] = (k + (r["outcome"] != "resisted"), n + 1)
for name, (k, n) in tally.items():
    print(f"{name:18} {n:3} emails   {k} complied or partly")
k, n = tally["override line"]
print(f"override line: {k} of {n}; limit {exact_upper(k, n):.3f} as {n} "
      f"separate tries, {exact_upper(k, 1):.3f} as one")
