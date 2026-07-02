# QE/AI Governance Policy

Rules that make AI safe enough to be useful. Each rule exists because of a
concrete failure mode, and each has a reference implementation in this repo.

## The non-negotiables

| # | Rule | Failure it prevents | Reference implementation |
|---|---|---|---|
| 1 | AI output with pipeline consequences is **advisory**; deterministic gates decide merges/releases | AI error blocks a release or ships a bug | `advisory` field on every qe-copilot report |
| 2 | Every AI answer must **cite sources** (incident IDs, doc IDs) | Unverifiable claims; hallucination laundering | citation list in qe-copilot analysis |
| 3 | Low confidence **always routes to a human** | Confidently-wrong automation | confidence gate in agent_graph.py |
| 4 | **PII is redacted before embedding**, never after | Vector store leaks PII through retrieval forever | embedding_pipeline.py stage 2 |
| 5 | AI-generated test assets pass a **schema allowlist + execution gate** before human review | Hallucinated endpoints entering the suite | ai-test-gen/validate_generated.py |
| 6 | Every model/prompt change re-runs the **golden-set eval**; regression fails the build | Silent quality decay | evaluate.py exit-code gates (both projects) |
| 7 | Models are **versioned with a registry**; promotion is champion/challenger | Untracked model changes; metric gaming | ml-qe-pipeline registry.json |
| 8 | Every AI decision logs **which engine produced it** and its inputs | Undebuggable, unauditable automation | `engine`/`llm_mode` fields in reports |
| 9 | Secrets never enter prompts; agents get **least-privilege tool access** (MCP RBAC) | Credential leakage via context windows | MCP tool design in qe-copilot |
| 10 | Sensitive workloads can run **local models** (Ollama); routing is a config decision | Regulated data leaving the network | LLM_BASE_URL switch in llm_client.py |

## Quality review cadence

- **Weekly:** triage quality audit — sample 10 AI triage reports, score usefulness/correctness.
- **Per release:** eval metrics reviewed alongside test results; both are release evidence.
- **Quarterly:** governance review — new failure modes, threshold tuning, autonomy expansion decisions.

## Compliance mapping (interview talking points)

- **GDPR/PII:** rule 4 + data-residency via rule 10.
- **SOX-style auditability:** rules 2, 7, 8 — every decision traceable.
- **Change management:** rules 6, 7 — AI changes gated like code changes.
