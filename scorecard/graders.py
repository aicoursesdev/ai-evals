"""Code graders. Each takes (output, case) and returns True or False."""
import functools
import json
import re

from scorecard import data


def exact(output, case):
    """Output equals case["expected"] after trimming spaces."""
    return str(output).strip() == str(case["expected"]).strip()


def contains(output, case):
    """case["expected"] appears in the output, ignoring capitals."""
    return str(case["expected"]).lower() in str(output).lower()


def matches(output, case):
    """The regular expression case["pattern"] is found in the output."""
    return re.search(case["pattern"], str(output)) is not None


def valid_json(output, case=None):
    """The output parses as JSON. '{"a": 1}' is True; 'a: 1' is False."""
    try:
        json.loads(output)
        return True
    except (TypeError, ValueError):
        return False


def has_fields(output, case):
    """Output is a dict with every key of case["fields"]; a key whose
    value there is a list must hold one of those values.
    {"u": "low"} against {"u": ["low", "high"]} is True."""
    if not isinstance(output, dict):
        return False
    for key, allowed in case["fields"].items():
        if key not in output:
            return False
        if isinstance(allowed, list) and output[key] not in allowed:
            return False
    return True


def close_to(output, case):
    """Output number is within case["tolerance"] of case["expected"]."""
    try:
        return abs(float(output) - case["expected"]) <= case["tolerance"]
    except (TypeError, ValueError):
        return False


# The help desk's own checks. They read a trace: triage, retrieved,
# draft, citations. A retrieved item is a dict with an "article_id" key.


def label_correct(trace, email):
    """The triage category equals the email's label."""
    return trace["triage"]["category"] == email["category"]


def cites_real_article(trace, article_ids):
    """Every cited article id exists in the help centre. No citations
    is True (nothing false was cited)."""
    return all(c in article_ids for c in trace["citations"])


def cites_retrieved_article(trace, case=None):
    """Every cited article was among the retrieved ones."""
    got = {r["article_id"] for r in trace["retrieved"]}
    return all(c in got for c in trace["citations"])


def mentions_order_id(trace, email):
    """The draft contains the email's order id. No order id: True."""
    return not email.get("order_id") or email["order_id"] in trace["draft"]


# "we'll refund", "I will send a replacement", "you will be refunded"
PROMISE = re.compile(
    r"\b(we|i)(\W?ll| will)\b[^.\n]{0,30}"
    r"\b(refund|replace|reship|send you a new)"
    r"|\byou (will|\W?ll) be (refunded|sent a replacement)",
    re.IGNORECASE,
)


def promises_refund(draft):
    """True when the draft promises money back or a replacement
    outright. "We'll refund you" is True; "a person will review" is False."""
    return PROMISE.search(draft) is not None


SCRIPTS = {"hi": r"[ऀ-ॿ]", "ta": r"[஀-௿]",
           "ml": r"[ഀ-ൿ]"}


def reply_script_matches(trace, email):
    """If the email is in Devanagari, Tamil or Malayalam script, the
    draft uses that script too. Other emails: True."""
    for letters in SCRIPTS.values():
        if re.search(letters, email["body"]):
            return re.search(letters, trace["draft"]) is not None
    return True


# The help desk's checks that fire. Each takes a trace and, where it
# needs one, the email, and returns True when it sees the failure.


@functools.cache
def page_status():
    """{article id: "current" or "archived"} for every help-centre page."""
    found = {}
    for a in data.articles():
        found[a["id"]] = re.search(r"^status: (\w+)", a["text"], re.M)[1]
    return found


@functools.cache
def help_centre_text():
    """All the help-centre text in one string (for invents_address)."""
    return " ".join(a["text"] for a in data.articles())


def cites_missing_or_old_page(trace, status):
    """A [tag] in the draft names a page that is not in the help centre
    or is archived. status is page_status()."""
    tags = re.findall(r"\[([a-z0-9-]+)\]", trace["draft"])
    return any(status.get(t, "missing") != "current" for t in tags)


def writes_to_spam(trace):
    """The help desk labelled the email spam and still wrote a reply."""
    return trace["triage"]["category"] == "spam" and bool(
        trace["draft"].strip())


def invents_address(trace, email, known=""):
    """The draft holds an email address found in neither the email nor
    known (the help centre's text)."""
    seen = email["body"] + email["from_email"] + known
    found = re.findall(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+", trace["draft"])
    return any(address not in seen for address in found)


CLAIMS = re.compile(
    r"we have (updated|opened|flagged|corrected|processed|marked)"
    r"|(i|we) will personally|has been approved|prioriti[sz]ing", re.I)


def claims_action(trace):
    """The draft uses a phrase that claims an action or makes a promise."""
    return CLAIMS.search(trace["draft"]) is not None


def asks_known_id(trace, email):
    """The draft asks for an order id although the email holds one. "If
    you checked out as a guest, email us your id" asks only guests."""
    draft = trace["draft"]
    ask = r"(reply|email|send).{0,40}order (id|number)"
    only_guests = re.search(r"\bif you\b[^.]{0,40}guest", draft, re.I)
    return bool(re.search(ask, draft, re.I) and not only_guests
                and re.search(r"TW-\d{4,5}", email["body"]))


def no_draft(trace):
    """The draft is empty."""
    return not trace["draft"].strip()


def wrong_script(trace, email):
    """The email is in Devanagari, Tamil or Malayalam script and the
    draft is not. An empty draft is no_draft's business, not this one's."""
    return bool(trace["draft"].strip()) and not reply_script_matches(
        trace, email)


def old_shipping_limit(trace):
    """The draft gives the old free-shipping limit (1,500 rupees) and not
    the current one (2,000). A reply that names both is correcting it."""
    old = re.search(r"₹\s?1,?500\b", trace["draft"])
    return bool(old and not re.search(r"₹\s?2,?000\b", trace["draft"]))


# name: (function of (email, trace), the failure types it should catch)
CHECKS = {
    "wrong script": (lambda e, t: wrong_script(t, e), {"F-language"}),
    "missing or old page": (
        lambda e, t: cites_missing_or_old_page(t, page_status()),
        {"F-wrong-page", "F-bluff"}),
    "reply to spam": (lambda e, t: writes_to_spam(t), {"F-spam-reply"}),
    "invented address": (
        lambda e, t: invents_address(t, e, help_centre_text()),
        {"F-bluff"}),
    "claims an action": (lambda e, t: claims_action(t), {"F-overreach"}),
    "asks for known id": (
        lambda e, t: asks_known_id(t, e), {"F-asks-again"}),
    "empty draft": (lambda e, t: no_draft(t), {"F-no-draft"}),
}


def logged(kind, week, version="hd-1", keep=None):
    """Rows of the log for one week ("emails" or "traces"), leaving out
    the sealed part of the test set. The id is read from the start of
    each line, so a sealed line is never parsed. With keep (a set of
    ids), only those rows."""
    folder = ("emails", f"log-week-{week}.jsonl") if kind == "emails" else (
        "traces", version, f"week-{week}.jsonl")
    sealed = {e["id"] for e in data.testset("sealed")}
    rows = []
    with open(data.DATA.joinpath(*folder), encoding="utf-8") as f:
        for line in f:
            id_ = re.match(r'\{"id": "([^"]+)"', line)[1]
            if id_ not in sealed and (keep is None or id_ in keep):
                rows.append(json.loads(line))
    return rows


def precision_recall(flagged, actual):
    """(precision, recall) of a set of flagged ids against the ids that
    really have the failure. Precision: the share of flags that are
    right. Recall: the share of real cases that were flagged."""
    hit = len(flagged & actual)
    return (hit / len(flagged) if flagged else None,
            hit / len(actual) if actual else None)
