"""ML CI/CD gate: champion/challenger evaluation on the fixed holdout set.

The newest candidate is promoted to champion ONLY if it does not regress
(F1 within tolerance of the current champion). Exit 0 = promoted, 1 = rejected.
"""

from __future__ import annotations

import sys

import joblib
import pandas as pd
from sklearn.metrics import f1_score, precision_score, recall_score

from common import DATA_DIR, FEATURES, LABEL, MODELS_DIR, load_registry, save_registry

TOLERANCE = 0.01  # candidate may not be worse than champion by more than this


def holdout_metrics(model_path: str, df: pd.DataFrame) -> dict:
    model = joblib.load(MODELS_DIR / model_path)
    preds = model.predict(df[FEATURES])
    return {
        "f1": round(f1_score(df[LABEL], preds), 3),
        "precision": round(precision_score(df[LABEL], preds), 3),
        "recall": round(recall_score(df[LABEL], preds), 3),
    }


def main() -> None:
    registry = load_registry()
    candidates = [v for v, m in registry["models"].items() if m["status"] == "candidate"]
    if not candidates:
        print("No candidate models to evaluate.")
        sys.exit(0)
    candidate = candidates[-1]

    holdout = pd.read_csv(DATA_DIR / "eval_holdout.csv")
    cand_metrics = holdout_metrics(registry["models"][candidate]["path"], holdout)
    registry["models"][candidate]["holdout_metrics"] = cand_metrics

    champion = registry["champion"]
    print(f"Candidate {candidate} holdout metrics: {cand_metrics}")

    if champion is None:
        promote = True
        print("No champion exists - first model auto-promotes.")
    else:
        champ_metrics = holdout_metrics(registry["models"][champion]["path"], holdout)
        print(f"Champion  {champion} holdout metrics: {champ_metrics}")
        promote = cand_metrics["f1"] >= champ_metrics["f1"] - TOLERANCE

    if promote:
        if champion:
            registry["models"][champion]["status"] = "retired"
        registry["models"][candidate]["status"] = "champion"
        registry["champion"] = candidate
        save_registry(registry)
        print(f"DECISION: PROMOTED - {candidate} is the new champion")
        sys.exit(0)
    else:
        registry["models"][candidate]["status"] = "rejected"
        save_registry(registry)
        print(f"DECISION: REJECTED - {candidate} regressed beyond tolerance; {champion} stays champion")
        sys.exit(1)


if __name__ == "__main__":
    main()
