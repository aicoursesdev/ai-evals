import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("record", ROOT / "scripts" / "record.py")
record = importlib.util.module_from_spec(spec)
spec.loader.exec_module(record)


def test_record_resumes_and_appends(tmp_path):
    path = tmp_path / "out.jsonl"
    cases = [((i, None), lambda i=i: {"id": i}) for i in ("a", "b", "c")]
    record.record(path, cases[:2])
    record.record(path, cases)
    assert sorted(json.loads(l)["id"] for l in path.read_text().splitlines()) == ["a", "b", "c"]


def test_a_failed_case_is_recorded_and_not_retried(tmp_path):
    path = tmp_path / "out.jsonl"
    def boom():
        raise RuntimeError("model down")
    assert record.record(path, [(("a", 3), boom)]) == 1
    assert record.record(path, [(("a", 3), lambda: {"id": "a"})]) == 0
    rows = [json.loads(l) for l in path.read_text().splitlines()]
    assert len(rows) == 1 and rows[0]["seed"] == 3 and "model down" in rows[0]["error"]
