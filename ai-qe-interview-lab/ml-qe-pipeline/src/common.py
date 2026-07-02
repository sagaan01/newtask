"""Shared: feature schema and the model registry (versioning + champion pointer)."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
MODELS_DIR = ROOT / "models"
REGISTRY_PATH = MODELS_DIR / "registry.json"

# The feature contract: every model version trains on exactly these columns.
FEATURES = [
    "fail_rate",            # historical failure rate of the test
    "rerun_pass_rate",      # share of failures that passed on rerun (flakiness smell)
    "duration_std_ratio",   # run-duration variance / mean (timing instability)
    "days_since_last_change",  # recent churn in the test or its target code
    "external_deps",        # number of external services the test touches
]
LABEL = "is_flaky"


def load_registry() -> dict:
    if REGISTRY_PATH.exists():
        with open(REGISTRY_PATH, encoding="utf-8") as f:
            return json.load(f)
    return {"champion": None, "models": {}}


def save_registry(registry: dict) -> None:
    MODELS_DIR.mkdir(exist_ok=True)
    with open(REGISTRY_PATH, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=2)


def next_version(registry: dict) -> str:
    return f"v{len(registry['models']) + 1}"
