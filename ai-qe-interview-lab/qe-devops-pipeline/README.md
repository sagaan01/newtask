# QE DevOps Pipeline — Category 4 (Cloud, DevOps & Integration)

| JD requirement | Artifact |
|---|---|
| GitHub Actions integration | `.github/workflows/qe-pipeline.yml` (repo root — **actually runs** on this repo) |
| Jenkins integration | `Jenkinsfile` (reference, same gates) |
| Azure DevOps integration | `azure-pipelines.yml` (reference, same gates) |
| AWS/Azure/GCP architectures + AI/ML services | `cloud-architecture.md` |
| Scalable, secure, governed environments | security section of `cloud-architecture.md` |

## The live pipeline

Six parallel quality gates + an aggregated report, wiring every lab project
into one CI run:

```
push/PR ──┬── api-tests            PyTest contract suite (8 tests)
          ├── ui-bdd-tests         Cucumber + Playwright (3 scenarios)
          ├── typescript-concepts  tsc --noEmit + 9 Playwright tests
          ├── ai-testgen-validation  valid batch passes; hallucinated batch
          │                          MUST exit 2 (governance as a test!)
          ├── ai-eval-gate         qe-copilot golden-set eval (blocks on regression)
          └── ml-model-gate        train candidate -> champion/challenger gate
                     │
             quality-report        one summary table; fails if any gate failed
```

Design points worth defending in an interview:

- **Parallel jobs** — feedback time is the max of gates, not the sum.
- **The AI is gated like code** — eval regression fails the build exactly like
  a failing unit test.
- **Governance is itself tested** — the pipeline asserts that the hallucinated
  batch gets REJECTED. If someone weakens the schema gate, CI goes red.
- **Artifacts** — model registry and failure screenshots uploaded per run.
- **Same gates, three CI dialects** — GitHub Actions (live), Jenkins and
  Azure DevOps (reference) prove the pipeline design is tool-portable.
