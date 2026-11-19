import json
import pytest
from scorecard import data


def put(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(json.dumps(r) for r in rows) + "\n")


def test_loaders_read_fixture(tmp_path, monkeypatch):
    monkeypatch.setattr(data, "DATA", tmp_path)
    put(tmp_path / "emails/log-week-2.jsonl", [{"id": "E-1"}])
    put(tmp_path / "emails/inbox.jsonl", [{"id": "E-2"}, {"id": "E-3"}])
    put(tmp_path / "traces/hd-2/week-3.jsonl", [{"id": "E-9"}])
    put(tmp_path / "traces/hd-1/launch.jsonl", [{"id": "E-4"}])
    put(tmp_path / "runs/x/a.jsonl", [{"n": 1}])
    (tmp_path / "labels").mkdir()
    (tmp_path / "labels/arjun.csv").write_text("id,label\nE-1,pass\n")
    assert data.emails(week=2) == [{"id": "E-1"}]
    assert len(data.emails(launch=True)) == 2
    assert data.traces("hd-2", week=3)[0]["id"] == "E-9"
    assert data.traces(launch=True)[0]["id"] == "E-4"
    assert data.run("x") == {"a": [{"n": 1}]}
    assert data.labels("arjun") == [{"id": "E-1", "label": "pass"}]


def test_missing_file_is_named(tmp_path, monkeypatch):
    monkeypatch.setattr(data, "DATA", tmp_path)
    with pytest.raises(FileNotFoundError, match="log-week-4.jsonl"):
        data.emails(week=4)


def test_today_and_real_files():
    assert str(data.TODAY) == "2026-11-16"
    assert len(data.scenarios()) == 30
    assert len(data.questions()) == 60
    assert len(data.attacks()) == 15
    assert len(data.emails(launch=True)) == 150
    assert "returns-policy" in [a["id"] for a in data.articles()]


def test_testset_parts(tmp_path, monkeypatch):
    monkeypatch.setattr(data, "DATA", tmp_path)
    put(tmp_path / "testsets/v1/open.jsonl", [{"id": "E-1"}, {"id": "E-2"}])
    put(tmp_path / "testsets/v2/sealed.jsonl", [{"id": "E-3"}])
    assert len(data.testset("open")) == 2
    assert data.testset("sealed", version="v2") == [{"id": "E-3"}]
    with pytest.raises(ValueError, match="open, sealed or synthetic"):
        data.testset("secret")
    with pytest.raises(FileNotFoundError, match="synthetic.jsonl"):
        data.testset("synthetic")


def test_real_testset_v1():
    parts = {p: data.testset(p) for p in ("open", "sealed")}
    assert [len(parts[p]) for p in parts] == [100, 50]
    ids = {p: {e["id"] for e in parts[p]} for p in parts}
    assert not ids["open"] & ids["sealed"]
    assert {e["part"] for e in parts["sealed"]} == {"sealed"}
    # sealed: only emails nothing else in the course opens
    assert all(e["week"] > 1 and not e["attack"] for e in parts["sealed"])
