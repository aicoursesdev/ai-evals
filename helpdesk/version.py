"""A version of the help desk is a folder: prompts and settings.json."""
import json
from pathlib import Path

FOLDER = Path(__file__).parent / "versions"


def load(name):
    """settings (a dict) plus the prompts: triage, draft and refunds."""
    folder = FOLDER / name
    settings = json.loads((folder / "settings.json").read_text())
    for prompt in ("triage", "draft", "refunds"):
        settings[prompt] = (folder / f"{prompt}.md").read_text(encoding="utf-8").strip()
    return settings
