"""Record what hd-1 writes for E-0722 when its reply is capped.

hd-1 sets no limit on a reply's length. For this one email the reply never
ends, so the help desk's 300-second limit passes and no draft is recorded
(see its trace in data/traces/hd-1/week-4.jsonl). This script runs the same
draft call with a 4,000-token cap, to show what the model was writing.

NEEDS A MODEL (Ollama, qwen3.5:4b). From the repo's root:
    uv run python data/runs/01-runaway-draft/record.py
"""
import json
import time
from datetime import datetime
from pathlib import Path

from helpdesk import llm
from helpdesk.pipeline import email_text, load, search, triage

HERE = Path(__file__).parent
CAP = 4000

emails = [json.loads(line) for line in
          open(HERE.parent.parent / "emails" / "log-week-4.jsonl",
               encoding="utf-8")]
email = next(e for e in emails if e["id"] == "E-0722")
v = load("hd-1")
tri, _, _ = triage(email, "hd-1", v["temperature"], None, v["model"])
hits = search(email_text(email), k=v["k"],
              filter_archived=v["filter_archived"])
labels = tri["triage"]
passages = "\n\n".join(f"[{h['article_id']}]\n{h['text']}" for h in hits)
prompt = v["draft"].format(passages=passages, **labels)
began = time.time()
reply = llm.chat([{"role": "system", "content": prompt},
                  {"role": "user", "content": email_text(email)}],
                 model=v["model"], temperature=v["temperature"],
                 max_tokens=CAP)
text = reply.choices[0].message.content or ""
record = {"id": "E-0722", "version": "hd-1", "model": v["model"],
          "temperature": v["temperature"], "max_tokens": CAP,
          "finish_reason": reply.choices[0].finish_reason,
          "completion_tokens": reply.usage.completion_tokens,
          "seconds": round(time.time() - began, 1), "draft": text,
          "recorded_at": datetime.now().astimezone().isoformat(
              timespec="seconds")}
(HERE / "E-0722.json").write_text(
    json.dumps(record, ensure_ascii=False, indent=1) + "\n",
    encoding="utf-8")
print(record["finish_reason"], record["completion_tokens"], "tokens,",
      len(text), "characters,", record["seconds"], "seconds")
