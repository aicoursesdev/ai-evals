"""Where the course's data lives, and loaders that return lists of dicts."""
import csv
import json
from datetime import date
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"
TODAY = date(2026, 11, 16)  # the course opens on this Monday


def read_jsonl(path):
    """Read a .jsonl file: one dict per line. Names the file if missing."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"missing data file: {path}")
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def emails(week=None, launch=False):
    """The launch set (launch=True) or the log of one week (1 to 4)."""
    if launch:
        return read_jsonl(DATA / "emails" / "inbox.jsonl")
    return read_jsonl(DATA / "emails" / f"log-week-{week}.jsonl")


def traces(version="hd-1", week=None, launch=False):
    """Recorded traces of one help desk version, for a week or the launch."""
    name = "launch.jsonl" if launch else f"week-{week}.jsonl"
    return read_jsonl(DATA / "traces" / version / name)


def run(name):
    """Every .jsonl in runs/<name>/, as {file stem: list of dicts}."""
    folder = DATA / "runs" / name
    if not folder.is_dir():
        raise FileNotFoundError(f"missing data folder: {folder}")
    return {p.stem: read_jsonl(p) for p in sorted(folder.glob("*.jsonl"))}


def labels(name):
    """A labels CSV (labels/<name>.csv) as a list of dicts. Lines that
    start with # hold the rule the labeller followed, and are skipped."""
    path = DATA / "labels" / (name if name.endswith(".csv") else name + ".csv")
    if not path.exists():
        raise FileNotFoundError(f"missing data file: {path}")
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(r for r in f if not r.startswith("#")))


def articles():
    """Help-centre articles: id, title and text, from help-centre/*.md."""
    folder = DATA / "help-centre"
    if not folder.is_dir():
        raise FileNotFoundError(f"missing data folder: {folder}")
    return [{"id": p.stem, "text": p.read_text(encoding="utf-8")}
            for p in sorted(folder.glob("*.md"))]


def questions():
    """The 60 retrieval questions."""
    return read_jsonl(DATA / "questions" / "retrieval.jsonl")


def scenarios():
    """The 30 refund scenarios."""
    return read_jsonl(DATA / "scenarios" / "refunds.jsonl")


def attacks():
    """The 15 red-team attacks."""
    return read_jsonl(DATA / "attacks" / "red-team.jsonl")


def testset(part, version="v1"):
    """One part of a test set: "open", "sealed" or "synthetic"."""
    if part not in ("open", "sealed", "synthetic"):
        raise ValueError(f"part must be open, sealed or synthetic, not {part!r}")
    return read_jsonl(DATA / "testsets" / version / f"{part}.jsonl")
