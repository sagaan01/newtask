"""Data/embedding pipeline for RAG with retrieval optimization.

Stages (each printed as it runs):
  1. INGEST   raw QE documents (some contain PII)
  2. CLEAN    redact PII (emails, tokens) BEFORE anything is embedded
  3. CHUNK    sentence-aware chunking (NLTK) with metadata tagging
  4. EMBED    store chunks + metadata in a vector DB
  5. RETRIEVE optimization demo: plain vector search vs metadata-filtered search
"""

from __future__ import annotations

import re

import chromadb
from chromadb.utils import embedding_functions

# --- raw corpus: runbook-style QE docs; two contain PII on purpose -----------
RAW_DOCS = [
    {
        "id": "doc-checkout-1",
        "component": "checkout",
        "text": (
            "Checkout payment failures often stem from the payment iframe loading slowly. "
            "Reported by shopper john.doe@example.com with session token sk-live-abc123XYZ. "
            "Always wait for the payment-frame-ready testid before clicking Pay Now. "
            "If the failure persists, check the currency service latency dashboard."
        ),
    },
    {
        "id": "doc-checkout-2",
        "component": "checkout",
        "text": (
            "Currency switching re-renders the checkout form. "
            "Locators bound to CSS classes break after the re-render. "
            "Use data-testid attributes which survive the currency switch."
        ),
    },
    {
        "id": "doc-auth-1",
        "component": "auth",
        "text": (
            "Login failures returning 500 instead of 401 indicate a regression in the auth service. "
            "Customer jane.smith@corp.io escalated this during the last release. "
            "Contract tests must assert 401 for invalid credentials."
        ),
    },
    {
        "id": "doc-search-1",
        "component": "search",
        "text": (
            "Search latency above the 2 second SLA usually points to missing database indexes. "
            "After catalog migrations, verify indexes on products.name. "
            "A perf smoke test on /search runs in every CI pipeline."
        ),
    },
    {
        "id": "doc-infra-1",
        "component": "infra",
        "text": (
            "Connection refused errors during nightly runs mean the staging environment is down. "
            "Run the pre-flight health check job before blaming the product. "
            "Quarantine infra failures so they never count as product defects."
        ),
    },
]

# Golden retrieval checks: query -> the chunk's source doc we expect first.
GOLDEN_QUERIES = [
    {"query": "pay button click fails while iframe still loading", "expect_doc": "doc-checkout-1", "component": "checkout"},
    {"query": "css class selectors break when currency changes", "expect_doc": "doc-checkout-2", "component": "checkout"},
    {"query": "wrong http status for bad password", "expect_doc": "doc-auth-1", "component": "auth"},
    {"query": "slow queries after schema migration", "expect_doc": "doc-search-1", "component": "search"},
]

PII_PATTERNS = [
    (re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+"), "<EMAIL_REDACTED>"),
    (re.compile(r"sk-live-\w+"), "<TOKEN_REDACTED>"),
]


def clean(text: str) -> tuple[str, int]:
    hits = 0
    for pattern, replacement in PII_PATTERNS:
        text, n = pattern.subn(replacement, text)
        hits += n
    return text, hits


def sentence_chunks(text: str, sentences_per_chunk: int = 2) -> list[str]:
    try:
        import nltk

        try:
            nltk.data.find("tokenizers/punkt_tab")
        except LookupError:
            nltk.download("punkt_tab", quiet=True)
        sentences = nltk.sent_tokenize(text)
    except Exception:
        sentences = re.split(r"(?<=[.!?])\s+", text)  # offline fallback

    return [
        " ".join(sentences[i : i + sentences_per_chunk])
        for i in range(0, len(sentences), sentences_per_chunk)
    ]


def main() -> None:
    print("STAGE 1 - INGEST")
    print(f"  {len(RAW_DOCS)} raw documents\n")

    print("STAGE 2 - CLEAN (PII redaction before embedding)")
    cleaned_docs = []
    total_redactions = 0
    for doc in RAW_DOCS:
        text, hits = clean(doc["text"])
        cleaned_docs.append({**doc, "text": text})
        total_redactions += hits
        if hits:
            print(f"  {doc['id']}: {hits} PII value(s) redacted")
    print(f"  Total redactions: {total_redactions}\n")

    print("STAGE 3 - CHUNK (sentence-aware, NLTK)")
    chunks = []
    for doc in cleaned_docs:
        for i, chunk_text in enumerate(sentence_chunks(doc["text"])):
            chunks.append(
                {
                    "id": f"{doc['id']}#c{i}",
                    "text": chunk_text,
                    "metadata": {"source_doc": doc["id"], "component": doc["component"]},
                }
            )
    print(f"  {len(RAW_DOCS)} docs -> {len(chunks)} chunks with metadata\n")

    print("STAGE 4 - EMBED + STORE")
    client = chromadb.EphemeralClient()
    collection = client.create_collection(
        "qe_runbooks", embedding_function=embedding_functions.DefaultEmbeddingFunction()
    )
    collection.add(
        ids=[c["id"] for c in chunks],
        documents=[c["text"] for c in chunks],
        metadatas=[c["metadata"] for c in chunks],
    )
    print(f"  {collection.count()} chunks embedded into vector store\n")

    print("STAGE 5 - RETRIEVAL OPTIMIZATION (plain vs metadata-filtered)")
    plain_hits = filtered_hits = 0
    for case in GOLDEN_QUERIES:
        plain = collection.query(query_texts=[case["query"]], n_results=1)
        plain_doc = plain["metadatas"][0][0]["source_doc"]
        plain_ok = plain_doc == case["expect_doc"]
        plain_hits += plain_ok

        filtered = collection.query(
            query_texts=[case["query"]],
            n_results=1,
            where={"component": case["component"]},  # metadata pre-filter
        )
        filtered_doc = filtered["metadatas"][0][0]["source_doc"]
        filtered_ok = filtered_doc == case["expect_doc"]
        filtered_hits += filtered_ok

        print(f"  [{'OK ' if plain_ok else 'MISS'}] plain    -> {plain_doc}   query: {case['query'][:48]}")
        print(f"  [{'OK ' if filtered_ok else 'MISS'}] filtered -> {filtered_doc}")

    n = len(GOLDEN_QUERIES)
    print(f"\n  precision@1 plain search:    {plain_hits}/{n}")
    print(f"  precision@1 with metadata:   {filtered_hits}/{n}")
    print("  Filtering shrinks the candidate set -> higher precision and lower latency at scale.")


if __name__ == "__main__":
    main()
