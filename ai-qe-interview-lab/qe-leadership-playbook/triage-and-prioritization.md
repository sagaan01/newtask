# Defect Triage Process & Prioritization Framework

## Defect triage (AI-assisted, human-decided)

Daily 15-minute triage, QE lead chairs. The AI prepares; humans decide.

```
overnight failures
      |
qe-copilot pre-triage (before the meeting):
  - clusters similar failures          (50 failures -> ~5 root causes)
  - classifies each cluster            (product-defect / flaky / infra / locator)
  - cites similar past incidents
  - drafts recommended actions
      |
triage meeting (humans):
  - validate classifications (spot-check, not rubber-stamp)
  - set priority by BLAST RADIUS: customers affected x revenue path x workaround
  - assign owners; product-defects get dev owner, test issues get QE owner
      |
outcomes tracked:
  - misclassifications feed back into the golden eval set
  - confirmed root causes appended to the RAG knowledge base
```

Priority rubric:
- **P1:** revenue path broken, no workaround — swarm now
- **P2:** feature broken, workaround exists — this sprint
- **P3:** edge case / cosmetic — backlog, batched

## Feature prioritization (for the QE platform itself)

Score = (Impact x Feasibility x Risk-reduction) / Cost, each 1-5.

Worked examples (from this repo's own roadmap decisions):

| Candidate feature | Impact | Feas. | Risk-red. | Cost | Score | Decision |
|---|---|---|---|---|---|---|
| Failure summarization (Phase 1) | 4 | 5 | 3 | 1 | 60 | Ship first |
| AI test generation w/ gates | 4 | 3 | 4 | 2 | 24 | Phase 2 |
| Flaky predictor + quarantine ranking | 3 | 4 | 4 | 2 | 24 | Phase 2-3 |
| Fully autonomous test authoring | 5 | 2 | 2 | 5 | 4 | Defer |

Rules of use:
- Scores are debate anchors, not verdicts — the argument the table forces is the value.
- Any pilot that can't beat its baseline metric in 4-6 weeks is killed. Killing
  pilots cheaply is a feature of the process, not a failure.

## Quality reviews

Per-sprint: escape defects root-caused (test gap? env gap? process gap?),
flaky quarantine queue reviewed, eval metrics trended. Findings become backlog
items with owners — a review without resulting actions didn't happen.
