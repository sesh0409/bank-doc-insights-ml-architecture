"""
churn_model_stub.py

A minimal churn prediction model stub using LogisticRegression.

This is NOT meant to be a production-ready model, but to:
- Show where churn modeling fits in the architecture
- Demonstrate typical ML steps (train/val split, metrics)
- Connect with feature_engineering outputs
"""

from __future__ import annotations

from typing import Tuple

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, classification_report
from sklearn.model_selection import train_test_split

from .feature_engineering import load_sample_datasets, build_churn_features


def train_churn_model(
    features: pd.DataFrame,
    target_col: str = "churn_flag",
) -> Tuple[LogisticRegression, float]:
    """
    Train a simple logistic regression churn model.

    Parameters
    ----------
    features : pd.DataFrame
        Feature table returned by build_churn_features.
    target_col : str
        Column name for the churn flag.

    Returns
    -------
    model : LogisticRegression
    auc : float
        ROC-AUC on validation set.
    """
    X = features.drop(columns=[target_col, "customer_id"])
    y = features[target_col].astype(int)

    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )

    model = LogisticRegression(
        max_iter=500,
        solver="lbfgs",
    )
    model.fit(X_train, y_train)

    # Predict probabilities for positive class
    y_proba = model.predict_proba(X_val)[:, 1]
    auc = roc_auc_score(y_val, y_proba)

    print(f"[CHURN MODEL] Validation AUC: {auc:.3f}")
    print("[CHURN MODEL] Classification report:")
    print(classification_report(y_val, (y_proba > 0.5).astype(int)))

    return model, auc


def score_churn(
    model: LogisticRegression,
    features: pd.DataFrame,
) -> pd.DataFrame:
    """
    Score a feature table using the trained churn model.

    Returns a DataFrame with:
    - customer_id
    - churn_score (probability)
    """
    X = features.drop(columns=["churn_flag", "customer_id"])
    churn_score = model.predict_proba(X)[:, 1]

    scored = features[["customer_id"]].copy()
    scored["churn_score"] = churn_score
    return scored


if __name__ == "__main__":
    # Example usage: train and score on the synthetic feature view.
    bank_df, loan_df, onboard_df = load_sample_datasets()
    churn_features = build_churn_features(bank_df, loan_df, onboard_df)

    model, auc = train_churn_model(churn_features)
    scored_df = score_churn(model, churn_features)

    print("\n[CHURN MODEL] Sample scores:")
    print(scored_df.head())
