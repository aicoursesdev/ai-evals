# Ship rule for a change to the help desk's drafts or triage

A change ships only if, on every email that the old and the new version both
answered (the log outside the sealed part), all four hold:

1. The lower end of the 95% range of the new version's triage-right rate is at
   least 0.80.
2. The lower end of the 95% range of its no-check-fires rate is at least 0.70.
3. The lower end of the paired change in triage-right is at least -0.02.
4. The lower end of the paired change in no-check-fires is at least -0.02.

The gate says "may not ship" when any one fails, and prints which. It never
looks at the sealed emails. The numbers are floors Meera accepts, set at hd-1's
own lower ends; they are reviewed when the test set changes.
