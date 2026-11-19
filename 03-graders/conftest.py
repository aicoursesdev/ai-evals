"""Module 03 guard: no test may parse a sealed trace.

The sealed part of the test set stays unread until a late module scores on
it once. The module's scripts load traces only through
scorecard.graders.logged, which checks each line's id before parsing it. This
fixture watches json.loads during every test and fails if a line of a
sealed email's trace is parsed.
"""
import json
import re

import pytest

from scorecard import data


@pytest.fixture(autouse=True)
def sealed_guard(monkeypatch):
    sealed = {e["id"] for e in data.testset("sealed")}
    real = json.loads

    def guarded(text, *args, **kwargs):
        line = text.decode() if isinstance(text, bytes) else str(text)
        found = re.match(r'\{"id": "([^"]+)"', line)
        if found and found[1] in sealed and '"triage":' in line:
            pytest.fail(f"parsed the trace of sealed email {found[1]}")
        return real(text, *args, **kwargs)

    monkeypatch.setattr(json, "loads", guarded)
