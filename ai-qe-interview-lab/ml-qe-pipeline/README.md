# ML QE Pipeline — Category 3 (ML/AI Engineering & Data Pipelines)

Flaky-test prediction with full ML CI/CD, plus a data/embedding pipeline with
retrieval optimization for RAG.

| JD requirement | Where it lives | Result |
|---|---|---|
| Scikit-Learn | `src/train.py` RandomForest flaky predictor | holdout F1 0.746 |
| PyTorch | `src/torch_model.py` MLP on same features | holdout F1 0.774 |
| NLP (NLTK) | sentence-aware chunking in `src/embedding_pipeline.py` | 5 docs -> 10 chunks |
| Data pipelines | `src/generate_data.py` (ETL stand-in) + PII redaction stage | 3 PII values redacted |
| Embedding pipelines + RAG retrieval optimization | `src/embedding_pipeline.py` stages 3-5 | precision@1 = 4/4 |
| CI/CD for ML: versioning | `models/registry.json` + versioned joblib artifacts | v1, v2 registered |
| CI/CD for ML: evaluation | `src/evaluate.py` champion/challenger gate on fixed holdout | exit 0/1 = promote/reject |
| CI/CD for ML: retraining | `src/retrain.py` new data -> train -> gate | v2 promoted over v1 |

TensorFlow/BART/OpenCV are alternates: same registry/gate pattern applies to any
framework. Interview talking points: BART for CI-log summarization, OpenCV for
visual regression testing.

## The ML CI/CD loop

```
new CI data (drift) --> train candidate vN --> registry (status: candidate)
                                                    |
                              fixed eval holdout (never trained on)
                                                    |
                         champion/challenger gate (F1 within tolerance?)
                          /                                        \
                 PROMOTED (exit 0)                          REJECTED (exit 1)
              champion pointer -> vN                     champion unchanged
```

Key principles:
- **Fixed holdout** (seed=777, never trained on): candidate and champion are
  compared on identical, untouched data - no metric gaming.
- **Training never promotes.** Promotion is owned by the evaluation gate,
  exactly like code merge is owned by CI, not by the author.
- **Exit codes are the contract**: the gate slots into any pipeline
  (GitHub Actions step fails on regression).

## Run it

```bash
pip install -r requirements.txt
pip install torch --index-url https://download.pytorch.org/whl/cpu

cd src
python generate_data.py            # 1. data pipeline (2000 rows + fixed holdout)
python train.py                    # 2. train + version candidate v1
python evaluate.py                 # 3. gate: first model auto-promotes
python retrain.py                  # 4. full loop: drifted data -> v2 -> gate
python torch_model.py              # 5. PyTorch comparison on same holdout
python embedding_pipeline.py       # 6. ingest->redact->chunk->embed->retrieve
```

## Features used by the predictor

- `rerun_pass_rate` — failures that pass on rerun (strongest flakiness smell, importance 0.35)
- `duration_std_ratio` — timing instability
- `days_since_last_change` — churn signal
- `fail_rate`, `external_deps`

In production these come from CI history (BigQuery/Jenkins API); prediction
feeds risk-based test selection and quarantine decisions - always advisory,
with the QE lead owning quarantine policy.
