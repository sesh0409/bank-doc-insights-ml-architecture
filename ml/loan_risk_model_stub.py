"""
loan_risk_model_stub.py

Stub implementation of a loan risk support model using RandomForest.

This model is meant to **support** underwriters by:
- Highlighting higher-risk applications
- Providing a probability of early delinquency (as an example target)

In production:
- Target labels would come from loan performance data (delinquencies, defaults)
- Model would be governed by risk/compliance stakeholders
"""

from __future__ import annotations

from typing import Tuple

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, classification_report
from sklearn.model_selection import train_test_split

from .feature_engineering import load_sample_datasets, build_loan_risk_features


def train_loan_risk_model(
    features: pd.DataFrame,
    target_col: str = "early_delinquency_flag",
) -> Tuple[RandomForestClassifier, float]:
    """
    Train a simple RandomForest-based loan risk support model.

    Parameters
    ----------
    features : pd.DataFrame
        Feature table returned by build_loan_risk_features.
    target_col : str
        Column representing early delinquency indicator.

    Returns
    -------
    model : RandomForestClassifier
    auc : float
        ROC-AUC on validation set.
    """
    if target_col not in features.columns:
        raise ValueError(f"Target column '{target_col}' not found in features.")

    X = features.drop(columns=[target_col, "application_id", "customer_id"])
    y = features[target_col].astype(int)

    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=None,
        random_state=42,
        n_jobs=-1,
    )
    model.fit(X_train, y_train)

    y_proba = model.predict_proba(X_val)[:, 1]
    auc = roc_auc_score(y_val, y_proba)

    print(f"[LOAN RISK MODEL] Validation AUC: {auc:.3f}")
    print("[LOAN RISK MODEL] Classification report:")
    print(classification_report(y_val, (y_proba > 0.5).astype(int)))

    return model, auc


def score_loan_risk(
    model: RandomForestClassifier,
    features: pd.DataFrame,
) -> pd.DataFrame:
    """
    Score loan applications using the trained loan risk model.

    Returns a DataFrame with:
    - application_id
    - customer_id
    - risk_score (probability of early delinquency)
    """
    X = features.drop(columns=["early_delinquency_flag", "application_id", "customer_id"])
    risk_score = model.predict_proba(X)[:, 1]

    scored = features[["application_id", "customer_id"]].copy()
    scored["risk_score"] = risk_score
    return scored


if __name__ == "__main__":
    # Example usage: train and score on synthetic features.
    bank_df, loan_df, onboard_df = load_sample_datasets()
    loan_features = build_loan_risk_features(loan_df, bank_df)

    model, auc = train_loan_risk_model(loan_features)
    scored = score_loan_risk(model, loan_features)

    print("\n[LOAN RISK MODEL] Sample scores:")
    print(scored.head())
