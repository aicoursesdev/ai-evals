"""Lesson 08.3: what the red-team attacks support, per kind of harm.

From this folder: uv run python our_counts.py
"""
from scorecard import data
from scorecard.stats import exact_interval, exact_upper

rows = [r for r in data.labels("08-attack-outcomes")
        if r["source"] == "red-team" and r["outcome"] != "not_arrived"]

def count_by_harm(rows, bad):
    """{harm: (failures, tries)}; a failure has an outcome in `bad`."""
    counts = {}
    for r in rows:
        k, n = counts.get(r["harm"], (0, 0))
        counts[r["harm"]] = (k + (r["outcome"] in bad), n + 1)
    return counts

counts = count_by_harm(rows, {"complied", "partly"})
counts["all harms"] = (sum(k for k, n in counts.values()), len(rows))
print("harm           fail/trials   upper limit   95% interval")
for harm, (k, n) in counts.items():
    low, high = exact_interval(k, n)
    print(f"{harm:14} {k:3}/{n:<3}        {exact_upper(k, n):.3f}"
          f"         {low:.3f} to {high:.3f}")
