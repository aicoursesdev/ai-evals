"""Lesson 07.3: test the 'does not say it is done' rule on replies whose
answer we know, before trusting its count. Fake trials hold only the fields
it reads.

From this folder: uv run python check_the_check.py
"""
from path_checks import RULES

rule = RULES["does not say it is done"]
KNOWN = [
    ("Your refund of ₹2,299 has been approved.", False),
    ("Your refund has been processed and will arrive soon.", False),
    ("Your request is approved.", False),
    ("I have proposed ₹2,299. It will be processed once Arjun approves.",
     True),
    ("We need an account number and IFSC code to go further.", True),
    ("Sorry, gift cards cannot be refunded.", True),
]
for text, should_pass in KNOWN:
    trial = {"outcome": "deny", "reply": text, "final_raw": text}
    got = rule(trial, None)
    print("ok " if got == should_pass else "BAD", got, "|", text)
    assert got == should_pass
