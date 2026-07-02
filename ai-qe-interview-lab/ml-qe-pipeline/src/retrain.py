"""ML CI/CD stage: scheduled retraining workflow.

Simulates the production loop: new CI data arrives (with drift) -> append to
training set -> train new candidate -> champion/challenger gate decides.
In production this runs nightly/weekly from a scheduler (GitHub Actions cron,
Airflow, Step Functions).
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent


def run(script: str, *args: str) -> int:
    print(f"\n=== {script} {' '.join(args)} ===")
    return subprocess.call([sys.executable, str(SRC / script), *args])


def main() -> None:
    print("RETRAINING WORKFLOW: new data -> train candidate -> evaluation gate")

    # 1. New batch of CI results arrives (moderate distribution drift).
    run("generate_data.py", "--rows", "1000", "--seed", "99", "--drift", "0.4", "--append")

    # 2. Train a new candidate on the grown dataset.
    run("train.py")

    # 3. Champion/challenger gate: promote or reject.
    code = run("evaluate.py")

    print("\nWORKFLOW RESULT:", "candidate promoted" if code == 0 else "candidate rejected, champion unchanged")
    sys.exit(code)


if __name__ == "__main__":
    main()
