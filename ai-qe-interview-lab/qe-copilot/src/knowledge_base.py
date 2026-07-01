"""RAG layer: vector DB (ChromaDB) ingest + semantic retrieval over QE incidents."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import chromadb
from chromadb.utils import embedding_functions

ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "data" / "failures.json"
CHROMA_PATH = ROOT / ".chroma"


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
        shutil.rmtree(CHROMA_PATH)

    client = chromadb.PersistentClient(path=str(CHROMA_PATH))
    collection = client.get_or_create_collection(
        name="qe_failures",
        embedding_function=embedding_functions.DefaultEmbeddingFunction(),
    )
    failures = load_failures()
    if collection.count() == 0:
        collection.add(
            ids=[f["id"] for f in failures],
            documents=[_doc_text(f) for f in failures],
            metadatas=[
                {
                    "test_name": f["test_name"],
                    "component": f["component"],
                    "environment": f["environment"],
                    "category": f["category"],
                }
                for f in failures
            ],
        )
    return collection


def retrieve(query: str, top_k: int = 3) -> list[dict]:
    collection = build_collection()
    result = collection.query(query_texts=[query], n_results=top_k)
    return [
        {
            "id": result["ids"][0][i],
            "document": result["documents"][0][i],
            "metadata": result["metadatas"][0][i],
        }
        for i in range(len(result["ids"][0]))
    ]


def format_context(chunks: list[dict]) -> str:
    lines = []
    for i, chunk in enumerate(chunks, start=1):
        lines.append(f"[{i}] {chunk['id']} ({chunk['metadata'].get('component')})")
        lines.append(chunk["document"])
        lines.append("")
    return "\n".join(lines)
