# The help desk's eval program

| When | What runs | Who or what says no | Costs (from lesson 09.2 and the recordings) |
| --- | --- | --- | --- |
| Every change to a prompt or setting | The seven code checks and triage right, hd-new against hd-old on the same emails; `gate.py` | The gate (09.3): lower ends of ranges against written floors | The checks take about 0.05 milliseconds a draft; writing the drafts is the cost |
| Nightly | The judge on a fixed sample, replayed against Arjun's rates | A person looks only when a rate moves outside its range | About 2.2 seconds a verdict, about 91 reply tokens |
| Weekly | A random sample of 20 drafts plus 5 flagged, read by a person (09.4) | The reader's calls, counted by failure type | 25 minutes at an assumed 60 seconds a draft |
| When the model changes | Everything above, plus the judge against Arjun's calls again (09.8) | The gate and the judge's two rates | One more run of each |
| Before any kind of email goes out unread | `by_kind.py`: 59 clean reads, safety rows proven under their limits | A person decides; the rule is in `data/runs/10-sealed/plan.md` | Reading 59 drafts of that kind |
| When the test set is replaced | A version 2 with fresh emails and a new sealed part; nothing scored on v1's sealed part again | The data card | Drawing and labelling new emails |

What is never run: anything that reads a sealed trace of version 1. It was opened once, for lesson 10.3.
