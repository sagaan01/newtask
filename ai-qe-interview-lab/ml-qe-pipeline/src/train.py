"""ML CI/CD stage: train a candidate model and register it (versioned artifact).

Training does NOT promote - evaluate.py owns promotion (champion/challenger).
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split

from common import DATA_DIR, FEATURES, LABEL, MODELS_DIR, load_registry, next_version, save_registry


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default="test_history.csv")
    args = parser.parse_args()

    df = pd.read_csv(DATA_DIR / args.data)
    X_train, X_val, y_train, y_val = train_test_split(
        df[FEATURES], df[LABEL], test_size=0.2, random_state=7, stratify=df[LABEL]
    )

    model = RandomForestClassifier(n_estimators=150, max_depth=8, random_state=7)
    model.fit(X_train, y_train)
    preds = model.predict(X_val)

    registry = load_registry()
    version = next_version(registry)
    MODELS_DIR.mkdir(exist_ok=True)
    artifact = MODELS_DIR / f"flaky_predictor_{version}.joblib"
    joblib.dump(model, artifact)

    registry["models"][version] = {
        "path": artifact.name,
        "algorithm": "RandomForestClassifier",
        "trained_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "train_rows": len(X_train),
        "training_metrics": {
            "f1": round(f1_score(y_val, preds), 3),
            "precision": round(precision_score(y_val, preds), 3),
            "recall": round(recall_score(y_val, preds), 3),
        },
        "status": "candidate",
    }
    save_registry(registry)

    importances = sorted(zip(FEATURES, model.feature_importances_), key=lambda x: -x[1])
    print(f"Registered candidate {version} -> {artifact.name}")
    print(f"Training metrics: {registry['models'][version]['training_metrics']}")
    print("Top features:", ", ".join(f"{name}={imp:.2f}" for name, imp in importances[:3]))


if __name__ == "__main__":
    main()
