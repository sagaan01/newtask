#!/usr/bin/env python3
"""Validation mechanism for AI-generated test assets.

Gate 1 (static schema gate): every endpoint/field referenced must exist in the
allowlist (api_schema.json). Hallucinated endpoints/fields -> exit 2.

Gate 2 (dynamic execution gate): run each case against the live API and check
status + response fields -> exit 1 on failures.

Usage:
    python3 validate_generated.py generated/orders_tests.json
    python3 validate_generated.py generated/hallucinated_example.json   # demo rejection
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
import time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent
SCHEMA_PATH = ROOT / "api_schema.json"
APP_SERVER = ROOT.parent / "app" / "server.py"
PORT = 8789


def load_schema() -> dict:
    with open(SCHEMA_PATH, encoding="utf-8") as f:
        schema = json.load(f)
    return {(e["method"], e["path"]): e for e in schema["endpoints"]}


def normalize_path(path: str) -> str:
    """Replace concrete IDs with the {id} placeholder for schema lookup."""
    return re.sub(r"/api/orders/(?!\{id\})[\w-]+", "/api/orders/{id}", path)


def schema_gate(cases: list[dict], schema: dict) -> list[str]:
    violations = []
    for case in cases:
        key = (case["method"], normalize_path(case["path"]))
        endpoint = schema.get(key)
        if endpoint is None:
            violations.append(f"{case['name']}: endpoint {key[0]} {key[1]} not in schema (hallucinated?)")
            continue
        for field in (case.get("payload") or {}):
            if field not in endpoint["request_fields"]:
                violations.append(f"{case['name']}: request field '{field}' not in schema")
        for field in (case.get("expected_fields") or []):
            if field not in endpoint["response_fields"]:
                violations.append(f"{case['name']}: expected field '{field}' not in schema")
    return violations


def execution_gate(cases: list[dict], base_url: str) -> list[dict]:
    results = []
    created_ids: dict[str, str] = {}
    for case in cases:
        path = case["path"]
        if case.get("path_id_from"):
            path = path.replace("{id}", created_ids.get(case["path_id_from"], "MISSING"))
        else:
            path = path.replace("{id}", "unknown123")

        resp = requests.request(case["method"], f"{base_url}{path}", json=case.get("payload"), timeout=5)
        body = resp.json() if resp.content else {}

        status_ok = resp.status_code == case["expected_status"]
        fields_ok = all(f in body for f in (case.get("expected_fields") or []))
        if case["name"] not in created_ids and isinstance(body, dict) and "id" in body:
            created_ids[case["name"]] = body["id"]

        results.append(
            {
                "name": case["name"],
                "passed": status_ok and fields_ok,
                "detail": f"status {resp.status_code} (expected {case['expected_status']})"
                + ("" if fields_ok else f", missing fields in response: {body}"),
            }
        )
    return results


def start_app() -> subprocess.Popen:
    proc = subprocess.Popen(
        [sys.executable, str(APP_SERVER), "--port", str(PORT)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    for _ in range(50):
        try:
            if requests.get(f"http://localhost:{PORT}/health", timeout=1).status_code == 200:
                return proc
        except requests.ConnectionError:
            time.sleep(0.1)
    proc.terminate()
    raise RuntimeError("app under test did not start")


def main() -> None:
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(64)

    with open(sys.argv[1], encoding="utf-8") as f:
        cases = json.load(f)
    schema = load_schema()

    print(f"Validating {len(cases)} AI-generated test cases\n")

    print("GATE 1 - Schema allowlist (anti-hallucination)")
    violations = schema_gate(cases, schema)
    if violations:
        for v in violations:
            print(f"  REJECTED: {v}")
        print("\nRESULT: schema gate FAILED - generated assets rejected, nothing executed")
        sys.exit(2)
    print("  All endpoints and fields are in the allowlist. PASS\n")

    print("GATE 2 - Execution against live API")
    app = start_app()
    try:
        results = execution_gate(cases, f"http://localhost:{PORT}")
    finally:
        app.terminate()

    failed = 0
    for r in results:
        mark = "PASS" if r["passed"] else "FAIL"
        print(f"  [{mark}] {r['name']}: {r['detail']}")
        failed += not r["passed"]

    print(f"\nRESULT: {len(results) - failed}/{len(results)} executed cases passed")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
