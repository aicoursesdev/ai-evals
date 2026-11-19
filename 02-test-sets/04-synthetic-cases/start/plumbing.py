"""Given for lesson 02.4: the grid's values, the record of a case, writing."""
import json
from collections import Counter

LANGUAGES = ["en", "hi-en", "hi", "ta", "ml"]
ASKS = ["account", "complaint", "order_change", "other", "payment",
        "product_question", "refund", "return", "shipping_delay", "spam",
        "warranty"]
TWISTS = ["plain", "attack", "long", "thin", "two_asks"]


def record(number, row):
    """One row of cases.py as a record in the log's own format."""
    language, ask, twist, labels, sender, subject, body, expect = row
    urgency, human, article, order, attack = labels
    return {
        "id": f"S-{number:02d}", "received_at": None, "from_name": sender,
        "from_email": sender.lower().replace(" ", ".") + "@example.com",
        "subject": subject, "body": body, "order_id": order,
        "language": language, "category": ask, "urgency": urgency,
        "needs_human": human, "answer_article": article, "attack": attack,
        "week": None, "part": "synthetic", "source": "synthetic",
        "added_in": "v1.0", "long": len(body) >= 400, "made_up": True,
        "dimensions": {"language": language, "ask": ask, "twist": twist},
        "expect": expect}


def check_in_empty_cells(rows, empty):
    """Every case sits in a cell the log leaves empty (thin and two_asks
    cells are not in the log's labels, so they pass)."""
    for r in rows:
        d = r["dimensions"]
        cell = (d["language"], d["ask"], d["twist"])
        assert cell in empty or d["twist"] in TWISTS[3:], cell


def write_cases(rows, path):
    """Write the records as one JSON line each."""
    with open(path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def print_summary(rows):
    """How many cases, how many are long, and the language and twist counts."""
    print(len(rows), "made-up cases written;",
          sum(r["long"] for r in rows), "are 400 characters or more")
    for key in ("language", "twist"):
        tally = Counter(r["dimensions"][key] for r in rows)
        print(key, dict(sorted(tally.items())))
