"""Lesson 03.2: the four checks on four real help desk cases.

From this folder: uv run python four_cases.py
"""
import re

import plumbing
from hand_checks import CATEGORIES, exact, pattern, schema, within

emails, traces = plumbing.emails_by_id(), plumbing.traces_by_id()
t = traces["E-0152"]
allowed = {"category": CATEGORIES, "urgency": {"low", "normal", "high"},
           "needs_human": {True, False}}
label = emails["E-0152"]["category"]
print("exact   :", exact(t["triage"]["category"], label))
print("schema  :", schema(t["triage"], allowed))
draft = traces["E-0505"]["draft"]
print("pattern :", pattern(draft, r"TW-\d{5}"))
more = int(re.search(r"worth at least ₹(\d+) more", draft)[1])
print("within  :", within(more, 2000 - 1839, tolerance=0), "(says", more, ")")
