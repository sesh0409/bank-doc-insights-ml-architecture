"""
feature_engineering.py

Feature engineering utilities for:
- Customer churn prediction
- Loan risk support

This module is intentionally simple and uses:
- sample_data/*.json as inputs
- pandas to build ML-ready feature tables

In a real implementation, features would be built from the curated / gold
zone (e.g. Synapse / Delta tables) rather than JSON files.
"""

from __future__ import annotations

from pathlib import Path
from typing import Tuple

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
SAMPLE_DATA_DIR = BASE_DIR / "sample_data"


def _load_json_records(path: Path) -> pd.DataFrame:
    """
    Load a JSON file in the format:
    {
        "description": "...",
        "sample_records": N,
        "schema_support": 50,
        "records": [ {...}, {...}, ... ]
    }
    """
    data = pd.read_json(path)
    # The 'records' field is a list of dicts → normalize into rows
    df_records = pd.json_normalize(data["records"])
    return df_records


def load_sample_datasets() -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Load the three sample JSON files as DataFrames:

    - bank_statement_example.json
    - loan_application_example.json
    - onboarding_form_example.json
    """
    bank_path = SAMPLE_DATA_DIR / "bank_statement_example.json"
    loan_path = SAMPLE_DATA_DIR / "loan_application_example.json"
    onboard_path = SAMPLE_DATA_DIR / "onboarding_form_example.json"

    df_bank = _load_json_records(bank_path)
    df_loan = _load_json_records(loan_path)
    df_onboard = _load_json_records(onboard_path)

    return df_bank, df_loan, df_onboard


def build_churn_features(
    df_bank: pd.DataFrame,
    df_loan: pd.DataFrame,
    df_onboard: pd.DataFrame,
) -> pd.DataFrame:
    """
    Construct a simple churn modeling feature table at customer level.

    This is illustrative only. Real churn features would include:
    - Product holdings & balances
    - Relationship tenure
    - Engagement & transaction activity
    - Complaints, service interactions, etc.

    Output schema (example):
    - customer_id
    - region
    - segment
    - income_estimate
    - relationship_tenure_months
    - has_loans_with_bank
    - total_loans_amount
    - digital_channel_index
    - risk_segment_encoded
    - target (synthetic churn_flag for demo)
    """
    # Take a subset of relevant columns from each table
    bank_cols = [
        "customer_id",
        "region",
        "segment",
        "income_estimate",
        "relationship_tenure_months",
        "digital_channel_index",
        "risk_segment",
    ]
    bank_features = df_bank[bank_cols].drop_duplicates(subset=["customer_id"])

    loan_agg = df_loan.groupby("customer_id", as_index=False).agg(
        has_loans_with_bank=("application_id", lambda x: (len(x) > 0)),
        total_loans_amount=("requested_amount", "sum"),
        avg_internal_risk_score=("risk_score_internal", "mean"),
        any_early_delinquency=("early_delinquency_flag", "max"),
    )

    onboard_cols = [
        "customer_id",
        "annual_income",
        "pep_flag",
        "risk_rating_initial",
        "segment",
    ]
    onboard_features = df_onboard[onboard_cols].drop_duplicates(subset=["customer_id"])

    # Merge everything on customer_id
    df = bank_features.merge(loan_agg, on="customer_id", how="left")
    df = df.merge(
        onboard_features,
        on=["customer_id", "segment"],  # join on segment as well to show awareness
        how="left",
        suffixes=("_bank", "_onboard"),
    )

    # Fill NaNs for boolean-like features
    df["has_loans_with_bank"] = df["has_loans_with_bank"].fillna(False)
    df["any_early_delinquency"] = df["any_early_delinquency"].fillna(False)
    df["total_loans_amount"] = df["total_loans_amount"].fillna(0.0)
    df["avg_internal_risk_score"] = df["avg_internal_risk_score"].fillna(0.0)

    # Encode a very simple synthetic churn_flag:
    # Example heuristic:
    # - Higher churn risk if risk_segment is HIGH or
    #   digital usage is low or relationship is short.
    df["risk_segment_encoded"] = df["risk_segment"].map(
        {"LOW": 0, "MEDIUM": 1, "HIGH": 2}
    ).fillna(1)

    df["short_relationship_flag"] = df["relationship_tenure_months"] < 12
    df["low_digital_engagement_flag"] = df["digital_channel_index"] < 0.6

    df["churn_flag"] = (
        (df["risk_segment_encoded"] >= 1)
        & (df["short_relationship_flag"] | df["low_digital_engagement_flag"])
    ).astype(int)

    return df


def build_loan_risk_features(
    df_loan: pd.DataFrame,
    df_bank: pd.DataFrame,
) -> pd.DataFrame:
    """
    Construct a loan-level feature view for a loan risk support model.

    Output schema (example):
    - application_id
    - customer_id
    - requested_amount
    - tenor_months
    - income
    - liabilities
    - dti_ratio
    - credit_score
    - existing_loans_total_amount
    - risk_score_internal
    - region
    - segment
    - early_delinquency_flag (as example target)
    """
    loan_core_cols = [
        "application_id",
        "customer_id",
        "product_type",
        "requested_amount",
        "tenor_months",
        "income",
        "liabilities",
        "dti_ratio",
        "credit_score",
        "existing_loans_total_amount",
        "risk_score_internal",
        "early_delinquency_flag",
        "region",
        "segment",
    ]
    df_loan_core = df_loan[loan_core_cols].copy()

    # Optionally enrich with derived ratios
    df_loan_core["loan_to_income_ratio"] = (
        df_loan_core["requested_amount"] / df_loan_core["income"].clip(lower=1)
    )
    df_loan_core["loan_to_existing_loans_ratio"] = df_loan_core[
        "requested_amount"
    ] / (df_loan_core["existing_loans_total_amount"].replace(0, 1))

    # Enrich with simple customer-level info from bank statements
    bank_customer_cols = [
        "customer_id",
        "relationship_tenure_months",
        "risk_segment",
        "income_estimate",
        "digital_channel_index",
    ]
    df_bank_cust = df_bank[bank_customer_cols].drop_duplicates(subset=["customer_id"])

    df_features = df_loan_core.merge(df_bank_cust, on="customer_id", how="left")

    return df_features


if __name__ == "__main__":
    # Simple manual test: load and build both feature sets.
    bank_df, loan_df, onboard_df = load_sample_datasets()
    churn_features = build_churn_features(bank_df, loan_df, onboard_df)
    loan_risk_features = build_loan_risk_features(loan_df, bank_df)

    print("[FEATURES] Churn feature view:")
    print(churn_features.head())

    print("\n[FEATURES] Loan risk feature view:")
    print(loan_risk_features.head())
