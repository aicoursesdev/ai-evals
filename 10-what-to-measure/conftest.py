"""Module 10 guard: the sealed part was opened once, in lesson 10.3, and it
is spent. No test may parse a sealed trace, and the lessons that must not
read the opening's files (10.2, 10.4) may not open data/runs/10-sealed/ at all.

Lessons 10.3, 10.6 and 10.7 read the recorded opening (scores.json) and
nothing else of it, so the second guard leaves them alone. Their scripts load
traces only through scorecard.graders.logged, which checks each line's id
before parsing it; the first guard watches json.loads during every test and
fails if a line of a sealed email's trace is parsed. score_sealed.py, the
one script that opens sealed traces, is never run by a test: its test only
checks that it refuses to run again.
"""
import builtins
import json
import pathlib
import re

import pytest

from scorecard import data

MAY_READ_THE_OPENING = {"03-overfitting-the-test", "06-one-page-report",
                        "07-project-eval-program"}


@pytest.fixture(autouse=True)
def sealed_guard(monkeypatch, request):
    sealed = {e["id"] for e in data.testset("sealed")}
    real = json.loads

    def guarded(text, *args, **kwargs):
        line = text.decode() if isinstance(text, bytes) else str(text)
        found = re.match(r'\{"id": "([^"]+)"', line)
        if found and found[1] in sealed and '"triage":' in line:
            pytest.fail(f"parsed the trace of sealed email {found[1]}")
        return real(text, *args, **kwargs)

    monkeypatch.setattr(json, "loads", guarded)

    lesson = next((p for p in request.node.path.parents
                   if p.parent.name == "10-what-to-measure"), None)
    if lesson is None or lesson.name in MAY_READ_THE_OPENING:
        return

    def check(path):
        if "10-sealed" in str(path):
            pytest.fail(f"lesson {lesson.name} opened {path}")

    real_open, real_path_open = builtins.open, pathlib.Path.open
    real_read_text = pathlib.Path.read_text

    def open_(file, *args, **kwargs):
        check(file)
        return real_open(file, *args, **kwargs)

    def path_open(self, *args, **kwargs):
        check(self)
        return real_path_open(self, *args, **kwargs)

    def read_text(self, *args, **kwargs):
        check(self)
        return real_read_text(self, *args, **kwargs)

    monkeypatch.setattr(builtins, "open", open_)
    monkeypatch.setattr(pathlib.Path, "open", path_open)
    monkeypatch.setattr(pathlib.Path, "read_text", read_text)
