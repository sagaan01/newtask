# Prompt Template: AI-Generated API Test Assets

This is the prompt-optimized template used to generate `generated/orders_tests.json`.
Every design choice below exists to make output **valid, schema-bound, and machine-checkable**.

---

## The Prompt

```text
SYSTEM:
You are a senior API test engineer. You generate test cases as JSON only.
Rules:
- Reference ONLY endpoints and fields from the provided API schema. Never invent endpoints.
- Cover: happy path, each validation rule (negative), not-found, and health.
- Every case must be independently executable except where "path_id_from" chains a created resource.
- Output MUST validate against the OUTPUT FORMAT. No prose, no markdown.

API SCHEMA:
{contents of api_schema.json injected here}

OUTPUT FORMAT (JSON array, one object per test case):
{
  "name": "snake_case_unique_name",
  "method": "GET|POST",
  "path": "/api/...",
  "payload": { ... } | null,
  "expected_status": 200|201|400|404,
  "expected_fields": ["field", ...] | null,
  "path_id_from": "name_of_prior_case" | null
}

FEW-SHOT EXAMPLE:
[
  {"name": "health_ok", "method": "GET", "path": "/health",
   "payload": null, "expected_status": 200, "expected_fields": ["status"], "path_id_from": null}
]

USER:
Generate a complete test suite for the Orders API.
```

---

## Why each prompt element matters (interview talking points)

| Element | Purpose |
|---|---|
| "JSON only, no prose" | Output is machine-parseable; feeds directly into the validator |
| Schema injection | Grounding: the model can only see real endpoints (RAG-style context) |
| "Never invent endpoints" | Explicit anti-hallucination constraint |
| Coverage checklist | Forces negative + boundary cases, not just happy path |
| Fixed OUTPUT FORMAT | Contract between LLM and validation pipeline |
| Few-shot example | Anchors exact field names and casing |
| `path_id_from` chaining | Teaches the model resource lifecycle testing |

## The validation mechanism (see `validate_generated.py`)

AI output is NEVER trusted directly. Two gates:

1. **Schema gate (static):** every endpoint/field referenced must exist in the allowlist.
   A hallucinated endpoint fails the whole batch (exit 2).
2. **Execution gate (dynamic):** every case runs against the live API;
   status codes and response fields must match (exit 1 on failure).

Only after both gates pass can generated tests be promoted into the regression suite via PR review.
