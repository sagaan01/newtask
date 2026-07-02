"""Model evaluation harness: golden-set regression for retrieval + classification.

Run on every prompt/model/data change. Fails (exit 1) below thresholds,
so it can act as a CI quality gate for the AI system itself.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from classifier import classify
from knowledge_base import retrieve

GOLDEN_PATH = Path(__file__).resolve().parent.parent / "data" / "golden_eval.json"

RETRIEVAL_THRESHOLD = 0.8  # precision@3 on expected incident
CLASSIFY_THRESHOLD = 0.6   # category accuracy


def run_eval(use_hf: bool = False) -> dict:
    with open(GOLDEN_PATH, encoding="utf-8") as f:
        golden = json.load(f)

    retrieval_hits = 0
    classify_hits = 0
    rows = []

    for case in golden:
        retrieved_ids = [c["id"] for c in retrieve(case["query"], top_k=3)]
        retrieval_ok = case["expected_incident"] in retrieved_ids

        predicted = classify(case["query"], use_hf=use_hf)["category"]
        classify_ok = predicted == case["expected_category"]

        retrieval_hits += retrieval_ok
        classify_hits += classify_ok
        rows.append(
            {
                "query": case["query"][:60],
                "expected_incident": case["expected_incident"],
                "retrieved": retrieved_ids,
                "retrieval_ok": retrieval_ok,
                "expected_category": case["expected_category"],
                "predicted_category": predicted,
                "classify_ok": classify_ok,
            }
        )

    n = len(golden)
    return {
        "cases": n,
        "retrieval_precision_at_3": round(retrieval_hits / n, 3),
        "classification_accuracy": round(classify_hits / n, 3),
        "rows": rows,
    }


def main() -> None:
    use_hf = "--hf" in sys.argv
    results = run_eval(use_hf=use_hf)

    print(f"Golden cases:              {results['cases']}")
    print(f"Retrieval precision@3:     {results['retrieval_precision_at_3']}")
    print(f"Classification accuracy:   {results['classification_accuracy']}")
    print()
    for row in results["rows"]:
        r = "PASS" if row["retrieval_ok"] else "FAIL"
        c = "PASS" if row["classify_ok"] else "FAIL"
        print(f"[retrieval:{r}] [classify:{c}] {row['query']}")
        if not row["retrieval_ok"]:
            print(f"    expected {row['expected_incident']}, got {row['retrieved']}")
        if not row["classify_ok"]:
            print(f"    expected {row['expected_category']}, got {row['predicted_category']}")

    failed = (
        results["retrieval_precision_at_3"] < RETRIEVAL_THRESHOLD
        or results["classification_accuracy"] < CLASSIFY_THRESHOLD
    )
    print()
    print("EVAL GATE:", "FAILED - block deploy" if failed else "PASSED")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
