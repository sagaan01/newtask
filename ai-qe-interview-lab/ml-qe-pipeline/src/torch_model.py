"""PyTorch alternative: a small MLP on the same features, compared with the
sklearn champion. Demonstrates when deep learning is and is not worth it -
on 5 tabular features, a RandomForest usually matches or beats a neural net.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from sklearn.metrics import f1_score

from common import DATA_DIR, FEATURES, LABEL, load_registry

torch.manual_seed(7)


class FlakyMLP(nn.Module):
    def __init__(self, n_features: int):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(n_features, 16),
            nn.ReLU(),
            nn.Linear(16, 1),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)


def main() -> None:
    train_df = pd.read_csv(DATA_DIR / "test_history.csv")
    holdout = pd.read_csv(DATA_DIR / "eval_holdout.csv")

    # Standardize features (neural nets care; tree models don't).
    mean, std = train_df[FEATURES].mean(), train_df[FEATURES].std()
    X = torch.tensor(((train_df[FEATURES] - mean) / std).values, dtype=torch.float32)
    y = torch.tensor(train_df[LABEL].values, dtype=torch.float32).unsqueeze(1)
    X_hold = torch.tensor(((holdout[FEATURES] - mean) / std).values, dtype=torch.float32)

    model = FlakyMLP(len(FEATURES))
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
    loss_fn = nn.BCEWithLogitsLoss()

    for epoch in range(200):
        optimizer.zero_grad()
        loss = loss_fn(model(X), y)
        loss.backward()
        optimizer.step()
        if (epoch + 1) % 50 == 0:
            print(f"epoch {epoch + 1:3d}  loss={loss.item():.4f}")

    with torch.no_grad():
        preds = (torch.sigmoid(model(X_hold)) > 0.5).int().numpy().ravel()
    torch_f1 = round(f1_score(holdout[LABEL], preds), 3)

    registry = load_registry()
    champion = registry.get("champion")
    champ_f1 = (
        registry["models"][champion].get("holdout_metrics", {}).get("f1", "n/a") if champion else "n/a"
    )

    print(f"\nPyTorch MLP holdout F1:        {torch_f1}")
    print(f"sklearn champion holdout F1:   {champ_f1}")
    print("Takeaway: on small tabular data, classic ML matches deep learning at a")
    print("fraction of the complexity - model choice should follow the data, not hype.")


if __name__ == "__main__":
    main()
