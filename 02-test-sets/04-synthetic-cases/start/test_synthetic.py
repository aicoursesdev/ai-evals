"""Lesson 02.4: real_twist and the grid, with the made-up cases checked.

The tests need no model and no network:

    make check 02.4
"""

import runpy
import sqlite3
from datetime import date
from pathlib import Path

import httpx
import openai

import check_synthetic
import run_synthetic
from build_synthetic import empty_cells, real_twist
from cases import CASES
from plumbing import record, write_cases
from scorecard import data
from slices import log

HERE = Path(__file__).parent
TODAY = date(2026, 11, 14)  # the day the made-up emails are written on


def mail(id, language="en", category="refund", attack=False, long=False):
    return {"id": id, "language": language, "category": category,
            "attack": attack, "body": "x" * (400 if long else 10)}


def test_real_twist_is_attack_long_or_plain():
    assert real_twist(mail("E-1", attack=True)) == "attack"
    assert real_twist(mail("E-2", long=True)) == "long"
    assert real_twist(mail("E-3")) == "plain"


def test_an_attack_that_is_also_long_counts_as_an_attack():
    assert real_twist(mail("E-1", attack=True, long=True)) == "attack"


def test_a_body_of_399_characters_is_plain_and_400_is_long():
    short = mail("E-1") | {"body": "x" * 399}
    assert real_twist(short) == "plain"
    assert real_twist(short | {"body": "x" * 400}) == "long"


def test_the_grid_has_165_cells_and_one_email_fills_one_of_them():
    shown, empty = empty_cells([mail("E-1")])
    assert len(shown) == 165 and len(empty) == 164
    assert ("en", "refund", "plain") in shown
    assert ("en", "refund", "plain") not in empty


def test_two_emails_in_one_cell_fill_it_once():
    shown, empty = empty_cells([mail("E-1"), mail("E-2")])
    assert len(empty) == 164


def test_an_attack_and_a_long_email_fill_their_own_cells():
    emails = [mail("E-1", "ta", "spam", attack=True),
              mail("E-2", "ml", "payment", long=True)]
    _, empty = empty_cells(emails)
    assert ("ta", "spam", "attack") not in empty
    assert ("ml", "payment", "long") not in empty
    assert len(empty) == 163


def test_the_log_leaves_107_of_the_165_cells_empty():
    shown, empty = empty_cells(log())
    assert (len(shown), len(empty)) == (165, 107)


def test_the_made_up_cases_are_all_in_empty_cells_or_thin_or_two_asks():
    _, empty = empty_cells(log())
    for number, row in enumerate(CASES, start=1):
        r = record(number, row)
        d = r["dimensions"]
        cell = (d["language"], d["ask"], d["twist"])
        assert cell in empty or d["twist"] in ("thin", "two_asks"), r["id"]


def test_the_cases_file_is_the_one_build_synthetic_writes(tmp_path):
    rows = [record(i, row) for i, row in enumerate(CASES, start=1)]
    write_cases(rows, tmp_path / "synthetic.jsonl")
    real = data.DATA / "testsets" / "v1" / "synthetic.jsonl"
    assert (tmp_path / "synthetic.jsonl").read_bytes() == real.read_bytes()
    assert [r["id"] for r in rows][::19] == ["S-01", "S-20"]
    assert sum(r["long"] for r in rows) == 3


def orders():
    db = sqlite3.connect(data.DATA / "orders.db")
    rows = db.execute(
        "select o.id, o.placed_at, group_concat(i.sku) from orders o "
        "join order_items i on i.order_id = o.id group by o.id").fetchall()
    return {i: (placed, skus) for i, placed, skus in rows}


def test_an_order_id_is_in_orders_db_or_is_from_19_october_on():
    known = orders()
    for case in data.testset("synthetic"):
        order = case["order_id"]
        if order and int(order[3:]) <= 10300:
            assert order in known, case["id"]


def test_s_07_and_s_12_name_real_old_orders_that_fit_their_emails():
    known, cases = orders(), {c["id"]: c for c in data.testset("synthetic")}

    def days_ago(order):
        return (TODAY - date.fromisoformat(known[order][0][:10])).days

    bag, jacket = cases["S-07"]["order_id"], cases["S-12"]["order_id"]
    assert "BPK-DRYTREK-25" in known[bag][1] and 180 <= days_ago(bag) <= 210
    assert "JKT-MONSOON" in known[jacket][1]
    assert 240 <= days_ago(jacket) <= 275
    assert cases["S-07"]["order_id"] in cases["S-07"]["body"]
    assert jacket in cases["S-12"]["subject"] + cases["S-12"]["body"]


def test_run_one_returns_the_help_desks_trace(monkeypatch):
    monkeypatch.setattr(run_synthetic, "handle",
                        lambda case: {"id": case["id"], "draft": "Hello"})
    assert run_synthetic.run_one({"id": "S-01"}) == {
        "id": "S-01", "draft": "Hello"}


def test_run_one_records_an_error_instead_of_stopping(monkeypatch):
    def broken(case):
        raise openai.APIConnectionError(
            request=httpx.Request("POST", "http://localhost"))
    monkeypatch.setattr(run_synthetic, "handle", broken)
    got = run_synthetic.run_one({"id": "S-02"})
    assert got["id"] == "S-02" and got["draft"] == ""
    assert got["error"].startswith("APIConnectionError after ")


def test_in_script_looks_for_the_customers_own_script():
    assert check_synthetic.in_script("நன்றி", "ta")
    assert not check_synthetic.in_script("Thank you", "ta")
    assert check_synthetic.in_script("धन्यवाद", "hi")
    assert check_synthetic.in_script("നന്ദി", "ml")


def test_invented_ids_are_bracketed_names_that_are_not_articles():
    real = sorted(check_synthetic.REAL)[0]
    draft = f"See [{real}] and [charged-twice] and [warranty]."
    assert check_synthetic.invented_ids(draft) == ["charged-twice",
                                                   "warranty"]


def test_check_synthetic_py_prints_19_of_20_and_8_and_6(capsys):
    runpy.run_path(str(HERE / "check_synthetic.py"), run_name="__main__")
    out = capsys.readouterr().out
    assert out.splitlines()[-1] == (
        "category agrees on 19 of 20, all three on 8; 6 replies to hi, ta "
        "or ml emails are not in that script")
    assert "S-07  yes       yes        own           []\n" in out
    assert "S-12  yes       yes        English       []\n" in out


def test_no_script_opens_a_trace_file():
    for path in HERE.glob("*.py"):
        if path.name != "test_synthetic.py":
            text = path.read_text(encoding="utf-8")
            assert "data.traces" not in text and '"traces"' not in text, path
