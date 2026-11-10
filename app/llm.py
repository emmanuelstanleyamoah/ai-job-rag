from __future__ import annotations

import logging

import httpx

from app.config import settings

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are an AI engineering career coach for a bootcamp.
Answer ONLY from the provided context. If the context is missing the answer, say so
and suggest what the student should ask next.

Be specific and practical. Prefer checklists, examples, and interview talking points
over generic motivation. Cite sources using the filename in brackets, like [resume.md].
Never invent companies, salary numbers, or interview questions that are not in context.
"""


class LLMError(RuntimeError):
    pass


ABSTAIN = (
    "I could not find anything in the bootcamp knowledge base for that. "
    "Try asking about resumes, portfolio projects, interviews, or job search strategy."
)


def generate_answer(question: str, context: str) -> str:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": (
                f"Context:\n{context}\n\n"
                f"Student question: {question}\n\n"
                "Answer using only the context."
            ),
        },
    ]
    if settings.openai_api_key:
        try:
            return _chat_openai(messages)
        except Exception as exc:
            logger.warning("OpenAI failed (%s); trying Ollama", exc)
    try:
        return _chat_ollama(messages)
    except Exception as exc:
        logger.warning("Ollama failed (%s); using extractive fallback", exc)
        return _extractive_fallback(question, context)


def _chat_openai(messages: list[dict[str, str]]) -> str:
    url = settings.openai_base_url.rstrip("/") + "/chat/completions"
    headers = {"Authorization": f"Bearer {settings.openai_api_key}"}
    payload = {
        "model": settings.openai_model,
        "messages": messages,
        "temperature": 0.2,
    }
    with httpx.Client(timeout=60.0) as client:
        response = client.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
    return data["choices"][0]["message"]["content"].strip()


def _chat_ollama(messages: list[dict[str, str]]) -> str:
    url = settings.ollama_base_url.rstrip("/") + "/api/chat"
    payload = {
        "model": settings.ollama_model,
        "messages": messages,
        "stream": False,
        "options": {"temperature": 0.2},
    }
    with httpx.Client(timeout=120.0) as client:
        response = client.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
    content = data.get("message", {}).get("content", "").strip()
    if not content:
        raise LLMError("Ollama returned an empty response")
    return content


def _extractive_fallback(question: str, context: str) -> str:
    if not context.strip():
        return ABSTAIN
    preview = context[:1800].strip()
    return (
        "No LLM is available (set OPENAI_API_KEY or run Ollama), so here are the most "
        f"relevant notes for **{question.strip()}**:\n\n{preview}"
    )
