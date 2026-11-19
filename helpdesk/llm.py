"""Talk to a model: Ollama, a free API or a paid one, chosen in .env.

chat() sends one request and returns the reply's text and token counts;
embed() turns texts into vectors. Connection problems are retried with a
short wait; anything else is raised. Settings (see .env.example):
LLM_BASE_URL, LLM_API_KEY, LLM_MODEL, LLM_REASONING_EFFORT, EMBED_MODEL.
"""
import functools
import os
import time

import openai
from dotenv import load_dotenv

load_dotenv()

MODEL = os.getenv("LLM_MODEL", "qwen3.5:4b")
EMBED_MODEL = os.getenv("EMBED_MODEL", "qwen3-embedding:0.6b")
ATTEMPTS = 4
TIMEOUT = float(os.getenv("LLM_TIMEOUT", "300"))   # seconds a request may take, in all


@functools.cache
def client():
    """One client for the whole program, so connections are reused, never piled up."""
    return openai.OpenAI(
        base_url=os.getenv("LLM_BASE_URL", "http://localhost:11434/v1"),
        api_key=os.getenv("LLM_API_KEY", "ollama"),
        timeout=TIMEOUT, max_retries=0)


def _retry(call):
    for attempt in range(ATTEMPTS):
        try:
            return call()
        except openai.APITimeoutError:
            raise   # the server may still be busy with this request: never send it again
        except (openai.APIConnectionError, openai.InternalServerError,
                openai.RateLimitError):
            if attempt == ATTEMPTS - 1:
                raise
            time.sleep(2 ** attempt)


def chat(messages, model=None, temperature=0, seed=None, **kw):
    """One chat completion: returns the raw response.

    Thinking is off for qwen3.5 (reasoning_effort "none"); set
    LLM_REASONING_EFFORT to empty for a model that rejects it.
    """
    kw["model"] = model or MODEL
    kw["temperature"] = temperature
    if seed is not None:
        kw["seed"] = seed
    effort = os.getenv("LLM_REASONING_EFFORT", "none")
    if effort:
        kw["reasoning_effort"] = effort
    return _retry(lambda: client().chat.completions.create(
        messages=messages, **kw))


def ask(messages, **kw):
    """The reply's text and the usage: (text, prompt_tokens, completion_tokens)."""
    r = chat(messages, **kw)
    return r.choices[0].message.content or "", r.usage.prompt_tokens, r.usage.completion_tokens


def embed(texts):
    """One vector per text."""
    r = _retry(lambda: client().embeddings.create(model=EMBED_MODEL, input=texts))
    return [d.embedding for d in r.data]
