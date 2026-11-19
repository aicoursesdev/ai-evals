"""Lesson 08.4: a rough rule for the template an attack email was cut from.

Used by template_groups.py. The rule is mine, written after reading the
emails: the first marker an email shows names its template.
"""
MARKERS = (("forwarded message", ("Forwarded message",)),
           ("hidden comment", ("<!--",)),
           ("override line", ("SYSTEM NOTICE", "revious instructions",
                              "disregard your earlier", "New policy from")))

def template(body):
    """The name of the first marker the email body shows, else 'other'."""
    raise NotImplementedError(
        "TODO 08.4: return the name of the first marker in MARKERS "
        "with any of its phrases in body, else 'other', see the "
        "lesson's 'How many tries is this suite worth?' section")
