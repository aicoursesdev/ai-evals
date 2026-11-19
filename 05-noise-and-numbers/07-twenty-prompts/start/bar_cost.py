"""Lesson 05.7: what a stricter bar costs, on 80 fresh emails.

From this folder: uv run python bar_cost.py
"""
import statistics

from plumbing import emails, sample_ids, seed_runs
from scorecard.stats import at_most

E, runs, ids = emails(), seed_runs("triage-seeds"), sample_ids()
good = {(i, s): all(runs[i][s]["triage"][k] == E[i][k] for k in
                    ("category", "urgency", "needs_human"))
        for i in ids for s in range(1, 21)}
differ = [sum(good[i, s] != good[i, 1] for i in ids[:80])
          for s in range(2, 21)]
print("emails where a seed disagrees with seed 1, of 80: mean",
      round(statistics.mean(differ), 1), "range", min(differ), "to",
      max(differ))

print("disagreeing emails  lead needed  as points of 80")
for c in (10, 20, 30, 40):
    for lead in range(c + 1):
        wins = (c + lead) // 2              # emails the new version wins
        if (c + lead) % 2 == 0 and 2 * at_most(c - wins, c, 0.5) < 0.05:
            break
    print(f"{c:>18}  {lead:>11}  {lead / 80 * 100:>14.1f}")
