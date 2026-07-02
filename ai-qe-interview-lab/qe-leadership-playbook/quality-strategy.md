# Quality Strategy Across the SDLC

Risk-based, shift-left and shift-right, with AI accelerating analysis while
humans own judgment. Reference implementation: `qe-automation-framework`.

## Per-phase QE contribution

| SDLC phase | QE activity | Gate |
|---|---|---|
| Requirements | Testability review; acceptance criteria as Gherkin drafts | Story not "ready" without testable criteria |
| Design | Risk analysis; contract-first API specs; test-data strategy | Architecture review sign-off |
| Development | Unit tests (dev-owned); PR-level API contract tests; AI-drafted tests through validation gates | PR checks green |
| CI | Smoke on every PR; full regression nightly; perf smoke on critical APIs | Deterministic pass/fail; AI is advisory |
| Pre-release | Exploratory testing on risk hotspots; compliance checks | Release readiness review (human-chaired) |
| Production | Synthetic monitoring; incident learnings feed the RAG knowledge base | Post-incident review updates tests |

## The test pyramid, enforced not preached

- **Unit (dev-owned, most):** fast, PR-blocking.
- **API/contract (QE-architected):** exact response-shape assertions
  (`api-tests/` pattern) — catches breaking changes before UI ever sees them.
- **UI/E2E (fewest):** business-critical journeys only, BDD for shared language
  (`ui-tests/` pattern), data-testid locator contract with dev.
- **Performance:** SLA-as-code (`perf-tests/` pattern) — perf gates, not reports.

## Risk-based depth

Payments/auth/data-integrity: full pyramid + exploratory + perf gates.
Internal admin tooling: contract tests + smoke. Publish the risk tiers so
depth decisions are transparent and challengeable.

## Flaky test policy

1. Flaky test detected (reruns pass) -> quarantined within 24h WITH a ticket.
2. Quarantine without ticket is forbidden — that's where tests go to die.
3. ML predictor (`ml-qe-pipeline`) ranks the quarantine-review queue; the QE
   lead decides. Weekly quarantine review; anything older than 2 sprints is
   fixed or deleted.
