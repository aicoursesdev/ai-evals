"""make doctor: check this laptop, the data, your settings and your model, then play a recorded reply.

Uses only Python's standard library (and python-dotenv when it is installed),
so it runs before anything else works: no .env, no Ollama, no internet.
"""

import json
import os
import platform
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GB = 1024**3


def ok(text):
    print(f"  ok    {text}")


def warn(text):
    print(f"  !     {text}")


def note(text):
    print(f"        {text}")


def total_ram_bytes():
    """Total memory, asked of the operating system in its own way. None if we can't tell."""
    try:
        if sys.platform == "darwin":
            return int(subprocess.check_output(["sysctl", "-n", "hw.memsize"], text=True))
        if sys.platform.startswith("linux"):
            for line in Path("/proc/meminfo").read_text().splitlines():
                if line.startswith("MemTotal:"):
                    return int(line.split()[1]) * 1024  # the file counts in kB
        if sys.platform == "win32":
            import ctypes

            class MemoryStatus(ctypes.Structure):
                _fields_ = [("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong)] + [
                    (name, ctypes.c_ulonglong)
                    for name in ("total", "avail", "totalPage", "availPage", "totalVirtual", "availVirtual", "extended")
                ]

            status = MemoryStatus()
            status.dwLength = ctypes.sizeof(MemoryStatus)
            ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(status))
            return status.total
    except Exception:
        pass
    return None


def recommended_model(ram_bytes):
    """The course's choice of local model for this much memory."""
    if ram_bytes < 12 * GB:
        return "qwen3.5:2b"
    if ram_bytes < 24 * GB:
        return "qwen3.5:4b"
    return "qwen3.5:9b"


def load_settings():
    """Read .env if there is one. Returns True when the file exists."""
    env_file = ROOT / ".env"
    try:
        from dotenv import load_dotenv

        load_dotenv(env_file)
    except ImportError:
        # Without python-dotenv (before `uv sync`), read the simple KEY=value lines ourselves.
        if env_file.exists():
            for line in env_file.read_text().splitlines():
                line = line.split("#", 1)[0].strip()
                if "=" in line:
                    key, value = line.split("=", 1)
                    os.environ.setdefault(key.strip(), value.strip())
    return env_file.exists()


def models_at(base_url, api_key):
    """Ask the server which models it has (GET /models). Returns a list of names, or None if nobody answers."""
    request = urllib.request.Request(
        base_url.rstrip("/") + "/models",
        headers={"Authorization": f"Bearer {api_key}"},
    )
    try:
        with urllib.request.urlopen(request, timeout=3) as response:
            return [m["id"] for m in json.load(response).get("data", [])]
    except (urllib.error.URLError, OSError, ValueError):
        return None


def play_recorded_reply():
    """Show a real reply, recorded earlier from a local model, word by word as if it were arriving."""
    path = ROOT / "data" / "recorded" / "doctor-hello.json"
    record = json.loads(path.read_text(encoding="utf-8"))
    question = record["request"]["messages"][-1]["content"]
    answer = record["response"]["choices"][0]["message"]["content"].strip()
    print(f"  Model: {record['response']['model']} (recorded {record['recorded_at'][:10]}, no model needed)")
    print(f"  Customer: {question}\n")
    print("  Reply: ", end="", flush=True)
    delay = 0.03 if sys.stdout.isatty() else 0
    for word in answer.split(" "):
        print(word, end=" ", flush=True)
        time.sleep(delay)
    print("\n")


def main():
    print("\nAI Evals: doctor\n")

    print("This laptop")
    version = platform.python_version()
    if sys.version_info >= (3, 12):
        ok(f"Python {version}")
    else:
        warn(f"Python {version}: the course needs 3.12 or newer. Run `uv sync`, then `make doctor` again.")

    ok("uv " + subprocess.run(["uv", "--version"], capture_output=True, text=True).stdout.split()[1]) \
        if shutil.which("uv") else warn("uv not found: install it from https://docs.astral.sh/uv/")

    ram = total_ram_bytes()
    suggested = recommended_model(ram) if ram else "qwen3.5:4b"
    if ram:
        ok(f"{ram / GB:.0f} GB of memory: the course suggests {suggested} as your local model")
    else:
        warn(f"Couldn't read this laptop's memory; start with {suggested}")
    note("The recorded runs in this repo came from qwen3.5:4b: use it to reproduce them closely.")
    note("(The course's choices: under 12 GB qwen3.5:2b, 12 to 24 GB qwen3.5:4b, 24 GB and up qwen3.5:9b.)")

    print("\nData")
    needed = ["catalogue.csv", "orders.db", "emails/inbox.jsonl", "questions/retrieval.jsonl",
              "scenarios/refunds.jsonl", "attacks/red-team.jsonl", "recorded/doctor-hello.json"]
    missing = [f for f in needed if not (ROOT / "data" / f).exists()]
    if not (ROOT / "data" / "help-centre").is_dir():
        missing.append("help-centre/")
    if missing:
        warn("missing from data/: " + ", ".join(missing) + ". Re-clone the repo.")
    else:
        ok("the data files are there (`uv run python scripts/check_data.py` checks them against each other)")

    print("\nSettings")
    if load_settings():
        ok(".env found")
    else:
        warn(".env not found: using the defaults. Copy .env.example to .env to change them.")
    base_url = os.getenv("LLM_BASE_URL", "http://localhost:11434/v1")
    api_key = os.getenv("LLM_API_KEY", "ollama")
    model = os.getenv("LLM_MODEL", "qwen3.5:4b")
    note(f"LLM_BASE_URL = {base_url}")
    note(f"LLM_MODEL    = {model}")

    print("\nModel server")
    names = models_at(base_url, api_key)
    local = "localhost" in base_url or "127.0.0.1" in base_url
    if names is None:
        if local:
            warn(f"Ollama isn't answering at {base_url}.")
            note("Install it from https://ollama.com and open it, or use a free API (see README.md).")
        else:
            warn(f"Nothing answered at {base_url}. Check the URL and LLM_API_KEY in .env.")
    else:
        ok(f"{'Ollama' if local else 'The server'} answers at {base_url}")
        if model in names:
            ok(f"{model} is ready")
        elif local:
            warn(f"{model} isn't pulled yet. Run: ollama pull {model}")
        else:
            warn(f"{model} isn't in this provider's model list. Check LLM_MODEL in .env.")

    print("\nA recorded reply")
    play_recorded_reply()
    print("That reply was played from data/recorded/. When your model server is ready, lessons ask it live.\n")


if __name__ == "__main__":
    main()
