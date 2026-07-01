#!/usr/bin/env python3
"""CLI demo for Category 1 project: RAG failure triage."""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from rag_engine import build_collection, retrieve  # noqa: E402
from triage_agent import triage_failure  # noqa: E402

SAMPLE_QUERY = (
    "Playwright test fails: button Pay Now not visible after currency switch in checkout"
)


def main() -> None:
    parser = argparse.ArgumentParser(description="QE RAG Failure Triage Demo")
    parser.add_argument("query", nargs="?", default=SAMPLE_QUERY, help="Failure description")
    parser.add_argument("--ingest", action="store_true", help="Rebuild vector index")
    parser.add_argument("--retrieve-only", action="store_true", help="Show retrieval without LLM")
    args = parser.parse_args()

    if args.ingest:
        build_collection(reset=True)
        print("Indexed failure knowledge base.")

    if args.retrieve_only:
        chunks = retrieve(args.query)
        print("Top matches:")
        for c in chunks:
            print(f"- {c['id']} | {c['metadata']}")
            print(f"  {c['document'][:160]}...")
        return

    result = triage_failure(args.query)
    print(f"Mode: {result.mode}")
    print(f"Query: {result.query}\n")
    print(result.answer)
    print(f"\nCitations: {', '.join(result.cited_ids)}")


if __name__ == "__main__":
    main()
