"""Minimal agentic triage loop: retrieve -> analyze -> recommend."""

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv
from openai import OpenAI

from rag_engine import format_context, retrieve

load_dotenv()

SYSTEM_PROMPT = """You are a Senior QE triage assistant.
Use ONLY the provided incident context. If unsure, say what is missing.
Output sections:
1) Likely root cause
2) Recommended next steps
3) Similar incident IDs cited
Do not invent APIs, tests, or incidents not in context."""


@dataclass
class TriageResult:
    query: str
    cited_ids: list[str]
    answer: str
    mode: str


def _offline_answer(query: str, chunks: list[dict]) -> str:
  """Deterministic fallback when no LLM API key is configured."""
  if not chunks:
      return "No similar incidents found. Expand the knowledge base or refine the query."

  top = chunks[0]
  return (
      "Likely root cause:\n"
      f"- Best match {top['id']}: review component '{top['metadata'].get('component')}'.\n\n"
      "Recommended next steps:\n"
      "- Compare current failure text with cited incident resolutions.\n"
      "- Re-run in staging with trace/video enabled.\n"
      "- If UI locator issue, update Page Object; if API timing, add polling/contract tests.\n\n"
      f"Similar incident IDs cited: {', '.join(c['id'] for c in chunks)}"
  )


def triage_failure(query: str, top_k: int = 3) -> TriageResult:
    chunks = retrieve(query, top_k=top_k)
    context = format_context(chunks)
    cited_ids = [c["id"] for c in chunks]

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return TriageResult(
            query=query,
            cited_ids=cited_ids,
            answer=_offline_answer(query, chunks),
            mode="offline-rag",
        )

    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        temperature=0,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"New failure:\n{query}\n\nRetrieved incidents:\n{context}",
            },
        ],
    )
    return TriageResult(
        query=query,
        cited_ids=cited_ids,
        answer=response.choices[0].message.content or "",
        mode="llm-rag",
    )
