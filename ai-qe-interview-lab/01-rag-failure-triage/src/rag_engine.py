"""Simple RAG engine for QE failure knowledge base."""

from __future__ import annotations

import json
import os
from pathlib import Path

import chromadb
from chromadb.utils import embedding_functions

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "failures.json"
CHROMA_PATH = Path(__file__).resolve().parent.parent / ".chroma"


def _doc_text(item: dict) -> str:
    return (
        f"Incident {item['id']} | test: {item['test_name']} | "
        f"error: {item['error']} | component: {item['component']} | "
        f"root cause: {item['root_cause']} | resolution: {item['resolution']} | "
        f"tags: {', '.join(item['tags'])}"
    )


def load_failures() -> list[dict]:
    with open(DATA_PATH, encoding="utf-8") as f:
        return json.load(f)


def build_collection(reset: bool = False):
    if reset and CHROMA_PATH.exists():
        import shutil

        shutil.rmtree(CHROMA_PATH)

    client = chromadb.PersistentClient(path=str(CHROMA_PATH))
    embedder = embedding_functions.DefaultEmbeddingFunction()
    collection = client.get_or_create_collection(
        name="qe_failures",
        embedding_function=embedder,
        metadata={"purpose": "qe-failure-triage-demo"},
    )

    failures = load_failures()
    if collection.count() == 0:
        collection.add(
            ids=[item["id"] for item in failures],
            documents=[_doc_text(item) for item in failures],
            metadatas=[
                {
                    "test_name": item["test_name"],
                    "component": item["component"],
                    "environment": item["environment"],
                }
                for item in failures
            ],
        )
    return collection


def retrieve(query: str, top_k: int = 3) -> list[dict]:
    collection = build_collection()
    result = collection.query(query_texts=[query], n_results=top_k)
    docs = result.get("documents", [[]])[0]
    ids = result.get("ids", [[]])[0]
    metas = result.get("metadatas", [[]])[0]
    return [
        {"id": ids[i], "document": docs[i], "metadata": metas[i]}
        for i in range(len(docs))
    ]


def format_context(chunks: list[dict]) -> str:
    lines = []
    for i, chunk in enumerate(chunks, start=1):
        lines.append(f"[{i}] {chunk['id']} ({chunk['metadata'].get('component')})")
        lines.append(chunk["document"])
        lines.append("")
    return "\n".join(lines)
