from scorecard import run, graders


def test_run_save_load_rate(tmp_path):
    cases = [{"id": 1, "expected": "a"}, {"id": 2, "expected": "b"}]
    rows = run.run(cases, lambda c: "a", {"exact": graders.exact})
    assert [r["exact"] for r in rows] == [True, False]
    run.save(rows, tmp_path / "r.jsonl")
    assert run.load(tmp_path / "r.jsonl") == rows
    assert run.pass_rate(rows, "exact") == 0.5
