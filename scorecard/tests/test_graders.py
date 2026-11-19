from scorecard import graders as g


def test_basic_graders():
    assert g.exact(" hi ", {"expected": "hi"})
    assert g.contains("Hello World", {"expected": "world"})
    assert g.matches("order TW-10281", {"pattern": r"TW-\d{5}"})
    assert not g.matches("none", {"pattern": r"TW-\d{5}"})
    assert g.valid_json('{"a": 1}') and not g.valid_json("a: 1")
    assert g.close_to("2.04", {"expected": 2.0, "tolerance": 0.05})
    assert not g.close_to("abc", {"expected": 2.0, "tolerance": 0.05})


def test_has_fields():
    case = {"fields": {"urgency": ["low", "high"], "category": None}}
    assert g.has_fields({"urgency": "low", "category": "x"}, case)
    assert not g.has_fields({"urgency": "mid", "category": "x"}, case)
    assert not g.has_fields({"urgency": "low"}, case)
    assert not g.has_fields("text", case)


TRACE = {"triage": {"category": "refund"}, "draft": "Order TW-10281: ok",
         "citations": ["returns-policy"],
         "retrieved": [{"article_id": "returns-policy"}]}


def test_helpdesk_checks():
    email = {"category": "refund", "order_id": "TW-10281", "body": "hi"}
    assert g.label_correct(TRACE, email)
    assert g.mentions_order_id(TRACE, email)
    assert not g.mentions_order_id({"draft": "no id"}, email)
    assert g.cites_retrieved_article(TRACE)
    assert not g.cites_retrieved_article({**TRACE, "citations": ["x"]})
    assert g.cites_real_article(TRACE, {"returns-policy"})
    assert not g.cites_real_article(TRACE, {"other"})


def test_promises_refund():
    assert g.promises_refund("Don't worry, we'll refund you today.")
    assert g.promises_refund("We will send you a new jacket.")
    assert g.promises_refund("You will be refunded in 3 days.")
    assert not g.promises_refund("A person will review your request.")


def test_script_matches():
    email = {"body": "नमस्ते, मेरा ऑर्डर"}
    assert g.reply_script_matches({"draft": "नमस्ते"}, email)
    assert not g.reply_script_matches({"draft": "Hello"}, email)
    assert g.reply_script_matches({"draft": "Hello"}, {"body": "Hi"})
    tamil = {"body": "வணக்கம்"}
    assert not g.reply_script_matches({"draft": "Hello"}, tamil)


def make(draft, body="Hi", category="other"):
    return ({"body": body, "from_email": "a@example.com"},
            {"draft": draft, "triage": {"category": category}})


def test_firing_checks():
    e, t = make("We have updated your order.")
    assert g.claims_action(t) and not g.claims_action(make("Hi")[1])
    assert g.no_draft(make("  ")[1]) and not g.no_draft(t)
    e, t = make("Hello", category="spam")
    assert g.writes_to_spam(t) and not g.writes_to_spam(make("")[1] | {
        "triage": {"category": "spam"}})
    assert g.cites_missing_or_old_page(make("See [x]")[1], {"y": "current"})
    assert not g.cites_missing_or_old_page(
        make("See [y]")[1], {"y": "current"})
    e, t = make("Write to arjun@example.com")
    assert g.invents_address(t, e, "support@tidewater.example")
    assert not g.invents_address(t, e, "arjun@example.com")
    t = {"draft": "Write to support@tidewater.example."}
    assert not g.invents_address(t, e, "support@tidewater.example")


def test_script_and_id_checks():
    tamil = {"body": "வணக்கம்"}
    assert g.wrong_script({"draft": "Hello"}, tamil)
    assert not g.wrong_script({"draft": ""}, tamil)  # no_draft's business
    e, t = make("Please email us your order ID.", body="Order TW-10279")
    assert g.asks_known_id(t, e)
    e, t = make("If you checked out as a guest, email your order ID.",
                body="Order TW-10279")
    assert not g.asks_known_id(t, e)


def test_old_shipping_limit_and_precision_recall():
    assert g.old_shipping_limit({"draft": "Free over ₹1,500."})
    assert not g.old_shipping_limit({"draft": "Over ₹2,000, not ₹1,500."})
    assert g.precision_recall({"a", "b"}, {"a", "c", "d", "e"}) == (0.5, 0.25)
    assert g.precision_recall(set(), {"a"}) == (None, 0.0)


def test_logged_skips_sealed():
    from scorecard import data
    sealed = {e["id"] for e in data.testset("sealed")}
    for kind in ("emails", "traces"):
        ids = {r["id"] for w in (1, 2, 3, 4) for r in g.logged(kind, w)}
        assert len(ids) == 550 and not ids & sealed
