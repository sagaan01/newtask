"""Data pipeline stage 1: synthesize test-execution history.

In production this would be an ETL job reading CI results from BigQuery/Jenkins.
The generator encodes a real-world signal: flaky tests tend to have high
rerun-pass rates, unstable durations, and external dependencies.

--drift simulates distribution shift (new frameworks, new infra) to demo retraining.
"""

from __future__ import annotations

import argparse

import numpy as np
import pandas as pd

from common import DATA_DIR, FEATURES, LABEL


def make_dataset(rows: int, seed: int, drift: float = 0.0) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    fail_rate = rng.beta(1.5, 8, rows)
    rerun_pass_rate = rng.beta(2, 2, rows)
    duration_std_ratio = rng.gamma(2.0, 0.15, rows)
    days_since_last_change = rng.integers(0, 60, rows).astype(float)
    external_deps = rng.integers(0, 5, rows).astype(float)

    # Latent flakiness score: rerun recovery + timing variance + external deps.
    score = (
        2.2 * rerun_pass_rate
        + 1.5 * duration_std_ratio
        + 0.25 * external_deps
        - 0.02 * days_since_last_change
        + drift * rng.normal(0.0, 0.5, rows)
        + rng.normal(0.0, 0.35, rows)
    )
    is_flaky = (score > 2.0).astype(int)

    return pd.DataFrame(
        {
            "fail_rate": fail_rate,
            "rerun_pass_rate": rerun_pass_rate,
            "duration_std_ratio": duration_std_ratio,
            "days_since_last_change": days_since_last_change,
            "external_deps": external_deps,
            LABEL: is_flaky,
        }
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rows", type=int, default=2000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--drift", type=float, default=0.0)
    parser.add_argument("--out", default="test_history.csv")
    parser.add_argument("--append", action="store_true", help="Append to existing file")
    args = parser.parse_args()

    DATA_DIR.mkdir(exist_ok=True)
    df = make_dataset(args.rows, args.seed, args.drift)
    out_path = DATA_DIR / args.out

    if args.append and out_path.exists():
        df = pd.concat([pd.read_csv(out_path), df], ignore_index=True)
    df.to_csv(out_path, index=False)

    # Fixed eval holdout: same distribution, NEVER trained on.
    holdout_path = DATA_DIR / "eval_holdout.csv"
    if not holdout_path.exists():
        make_dataset(500, seed=777).to_csv(holdout_path, index=False)

    flaky_pct = df[LABEL].mean() * 100
    print(f"Wrote {len(df)} rows to {out_path.name} ({flaky_pct:.1f}% flaky)")
    print(f"Eval holdout: {holdout_path.name} (fixed, seed=777)")
    print(f"Features: {FEATURES}")


if __name__ == "__main__":
    main()
