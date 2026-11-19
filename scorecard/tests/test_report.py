from scorecard import report


def test_gate():
    rules = [("refunds", 0.90, True), ("tone", 0.80, False)]
    ok, why = report.gate(
        {"refunds": (0.92, 0.95, 0.97), "tone": (0.7, 0.85, 0.9)}, rules)
    assert ok and why == []
    ok, why = report.gate(
        {"refunds": (0.85, 0.95, 0.99), "tone": (0.7, 0.85, 0.9)}, rules)
    assert not ok and len(why) == 1 and "refunds" in why[0]


def test_one_page():
    page = report.one_page(
        "Report", "Keep every draft with a person.",
        [("no check fires", 36, 50, "10-sealed")], ["50 emails"],
        ["a person reads every draft"], ["59 clean reads of one kind"])
    assert page.startswith("# Report\n\n## Decision\n\nKeep every")
    assert "- no check fires: 36 of 50 (72.0%), 95% range 58.3% to 82.5% " \
           "[10-sealed]" in page
    for head in ("Evidence", "Uncertainty", "Cost", "What would change this"):
        assert f"## {head}" in page


def test_a_number_needs_its_n_and_its_source():
    import pytest
    with pytest.raises(ValueError):
        report.figure("x", 0, 0, "file")
    with pytest.raises(ValueError):
        report.figure("x", 1, 2, "")
