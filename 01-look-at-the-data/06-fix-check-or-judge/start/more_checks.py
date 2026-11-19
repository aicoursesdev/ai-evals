"""Given for lesson 01.6: the other five of the seven checks.

Each takes the email and/or the trace and returns True when it fires.
"""
import re

from scorecard import data


def pages():
    """{article id: status} for every help-centre article."""
    found = {}
    for a in data.articles():
        found[a["id"]] = re.search(r"^status: (\w+)", a["text"], re.M).group(1)
    return found


def cites_missing_or_old_page(trace, status=pages()):
    """A [tag] in the draft names a page that does not exist or is archived."""
    tags = re.findall(r"\[([a-z0-9-]+)\]", trace["draft"])
    return any(status.get(t, "missing") != "current" for t in tags)


def invents_an_address(email, trace):
    """An email address in the draft that is in neither the email nor the
    help centre."""
    known = email["body"] + email["from_email"] + " ".join(
        a["text"] for a in data.articles())
    found = re.findall(r"[\w.+-]+@[\w-]+\.[\w.-]+", trace["draft"])
    return any(addr not in known for addr in found)


def has_no_draft(trace):
    """The help desk wrote nothing: the draft is empty."""
    return not trace["draft"].strip()


CLAIMS = re.compile(
    r"we have (updated|opened|flagged|corrected|processed|marked)"
    r"|(i|we) will personally|has been approved|prioriti[sz]ing", re.I)


def claims_an_action(trace):
    """The draft uses a phrase that claims an action or a promise."""
    return bool(CLAIMS.search(trace["draft"]))


def asks_for_order_id_it_has(email, trace):
    """The draft asks for an order ID although the email contains one."""
    asks = re.search(r"(reply|email|send).{0,40}order (id|number)",
                     trace["draft"], re.I)
    return bool(asks and re.search(r"TW-\d{4,5}", email["body"]))
