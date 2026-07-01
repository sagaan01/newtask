"""LLM layer: LangChain prompt template + OpenAI/Ollama-compatible client.

Set env vars to switch providers with zero code changes:
    OPENAI_API_KEY=sk-...                      -> OpenAI cloud
    LLM_BASE_URL=http://localhost:11434/v1     -> local Ollama
    LLM_MODEL=llama3.1                         -> model name for either provider
"""

from __future__ import annotations

import os

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

TRIAGE_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a Senior QE triage assistant.\n"
            "Use ONLY the provided incident context. If unsure, say what is missing.\n"
            "Output sections:\n"
            "1) Likely root cause\n"
            "2) Recommended next steps\n"
            "3) Similar incident IDs cited\n"
            "Do not invent APIs, tests, or incidents not in context.",
        ),
        (
            "user",
            "New failure:\n{failure}\n\n"
            "Classified category: {category} (confidence {confidence})\n\n"
            "Retrieved incidents:\n{context}",
        ),
    ]
)


def llm_available() -> bool:
    return bool(os.getenv("OPENAI_API_KEY") or os.getenv("LLM_BASE_URL"))


def generate_triage(failure: str, category: str, confidence: float, context: str) -> str:
    """Grounded generation via OpenAI or Ollama; deterministic fallback offline."""
    messages = TRIAGE_PROMPT.format_messages(
        failure=failure, category=category, confidence=confidence, context=context
    )

    if not llm_available():
        return _offline_answer(category, context)

    from openai import OpenAI

    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY", "ollama"),
        base_url=os.getenv("LLM_BASE_URL"),  # None -> OpenAI default
    )
    response = client.chat.completions.create(
        model=os.getenv("LLM_MODEL", "gpt-4o-mini"),
        temperature=0,
        messages=[
            {"role": "system" if m.type == "system" else "user", "content": m.content}
            for m in messages
        ],
    )
    return response.choices[0].message.content or ""


def _offline_answer(category: str, context: str) -> str:
    cited = [line.split()[1] for line in context.splitlines() if line.startswith("[")]
    return (
        "Likely root cause:\n"
        f"- Classified as '{category}'; review top cited incident's resolution pattern.\n\n"
        "Recommended next steps:\n"
        "- Compare failure text with cited incident resolutions.\n"
        "- Re-run with trace/video enabled; apply the matching fix pattern.\n\n"
        f"Similar incident IDs cited: {', '.join(cited)}"
    )
