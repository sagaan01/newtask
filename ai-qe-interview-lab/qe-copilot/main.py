#!/usr/bin/env python3
"""QE Copilot CLI - unified demo of the full AI QE pipeline."""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from agent_graph import run_triage  # noqa: E402
from knowledge_base import build_collection, retrieve  # noqa: E402

SAMPLES = [
    "TimeoutError: locator('#pay-now') not visible after currency switch in checkout",
    "POST /auth/login returned 500 internal server error for invalid password",
    "net::ERR_CONNECTION_REFUSED at https://app.staging.example.com during nightly run",
    "Refund status still PENDING after 30s, expected REFUNDED",
]


def main() -> None:
    parser = argparse.ArgumentParser(description="QE Copilot - AI failure triage agent")
    parser.add_argument("query", nargs="?", help="Failure description to triage")
    parser.add_argument("--ingest", action="store_true", help="Rebuild the vector index")
    parser.add_argument("--retrieve-only", action="store_true", help="Show raw vector search results")
    parser.add_argument("--samples", action="store_true", help="Triage all built-in sample failures")
    parser.add_argument("--no-hf", action="store_true", help="Skip HuggingFace, use rule-based classifier")
    args = parser.parse_args()

    if args.ingest:
        build_collection(reset=True)
        print("Vector index rebuilt from data/failures.json")
        if not (args.query or args.samples or args.retrieve_only):
            return

    if args.retrieve_only:
        for c in retrieve(args.query or SAMPLES[0]):
            print(f"- {c['id']} | {c['metadata']}")
        return

    queries = SAMPLES if args.samples else [args.query or SAMPLES[0]]
    for q in queries:
        print(json.dumps(run_triage(q, use_hf=not args.no_hf), indent=2))
        print("-" * 70)


if __name__ == "__main__":
    main()
