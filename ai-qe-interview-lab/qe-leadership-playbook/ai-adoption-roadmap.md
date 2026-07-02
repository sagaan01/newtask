# AI Adoption Roadmap for QE

Four phases. Each phase must hit its exit criteria (measured, not felt) before
the next phase starts. Autonomy is earned by evidence.

## Phase 1 — Assist (low risk, fast trust)

**Capabilities:** failure summarization, doc/spec Q&A over RAG, log analysis.
**Reference:** `qe-copilot` retrieval + offline analysis mode.
**Guardrails:** read-only; no pipeline integration; output is informational.
**Exit criteria:**
- Triage time on piloted squad down 30%+ (baseline measured first)
- Retrieval precision@3 >= 0.8 on SME-built golden set
- 2 squads using it weekly without prompting

## Phase 2 — Recommend (AI enters the pipeline, advisory only)

**Capabilities:** failure classification, similar-incident citation, suggested
CI actions posted as PR comments; AI-generated test drafts behind validation gates.
**Reference:** `qe-copilot` full agent graph; `qe-automation-framework/ai-test-gen`
two-gate validator.
**Guardrails:** advisory-only flag on every output; schema allowlist rejects
hallucinated test assets; human approves every generated test via PR review.
**Exit criteria:**
- Classification accuracy >= 0.85 on golden set
- Zero hallucinated endpoints reaching PR review (gate catches 100%)
- Escape-defect rate flat or better (AI must not degrade quality)

## Phase 3 — Act with supervision (bounded autonomy)

**Capabilities:** auto-quarantine tickets for proven-flaky tests, auto-rerun on
infra-classified failures, ML flaky predictor feeding test ordering.
**Reference:** `ml-qe-pipeline` champion/challenger gate governs the predictor.
**Guardrails:** allowed-action list per category; confidence threshold routes
uncertain cases to humans; weekly quality review audits every autonomous action.
**Exit criteria:**
- Precision >= 0.85 on the specific automated action classes
- Zero incidents caused by autonomous actions over the review period
- Rollback drill executed successfully

## Phase 4 — Autonomous workflows (never includes release authority)

**Capabilities:** end-to-end triage-to-ticket, multi-tool agents (BigQuery MCP
for trends, Playwright MCP for live UI verification), release-readiness reports.
**Permanent line:** merge/release authority stays with deterministic gates and
humans. This is policy, not a maturity gap.

## KPIs tracked across all phases

| KPI | Why |
|---|---|
| Mean time to triage | The core toil AI removes |
| Escape defect rate | AI must never trade quality for speed |
| Eval metrics (precision/accuracy) per release | The AI's own regression suite |
| Token/compute cost per PR | Guard against silent cost creep |
| Engineer satisfaction (quarterly pulse) | Adoption is a people problem |
