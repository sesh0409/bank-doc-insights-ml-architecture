"""
Utility script to generate synthetic sample data for the document pipeline.

It creates 3 JSON files in this folder:

- bank_statement_example.json      -> 10 records, 50 features each
- loan_application_example.json    -> 10 records, 50 features each
- onboarding_form_example.json     -> 10 records, 50 features each

Run from repository root:

    python sample_data/generate_sample_data.py
"""

import json
from pathlib import Path
from datetime import date, timedelta
import random

BASE_DIR = Path(__file__).resolve().parent


def generate_bank_statement_records(n: int = 10):
    records = []
    base_date = date(2025, 1, 1)
    regions = ["APAC", "EMEA", "AMER"]
    account_types = ["SAVINGS", "CURRENT", "SALARY"]

    for i in range(1, n + 1):
        start_date = base_date + timedelta(days=30 * (i - 1))
        end_date = start_date + timedelta(days=29)

        opening_balance = 50000 + i * 1000
        total_credits = 25000 + i * 500
        total_debits = 18000 + i * 400
        closing_balance = opening_balance + total_credits - total_debits

        record = {
            # 1–10
            "document_type": "bank_statement",
            "customer_id": f"CUST{i:05d}",
            "statement_id": f"STM{i:06d}",
            "statement_period_start": start_date.isoformat(),
            "statement_period_end": end_date.isoformat(),
            "opening_balance": opening_balance,
            "closing_balance": closing_balance,
            "total_debits": total_debits,
            "total_credits": total_credits,
            "avg_daily_balance": (opening_balance + closing_balance) / 2,

            # 11–20
            "min_balance": opening_balance * 0.7,
            "max_balance": opening_balance * 1.4,
            "num_credit_transactions": 20 + i,
            "num_debit_transactions": 25 + 2 * i,
            "cash_deposits": 5000 + 100 * i,
            "cash_withdrawals": 3000 + 100 * i,
            "atm_withdrawals": 2000 + 50 * i,
            "pos_spend": 7000 + 150 * i,
            "online_spend": 6000 + 120 * i,
            "loan_emis_count": 2 + i % 3,

            # 21–30
            "loan_emis_total": 8000 + 200 * i,
            "salary_credits_count": 1,
            "salary_credits_total": total_credits * 0.7,
            "bounced_charges_count": i % 2,
            "bounced_charges_total": 300 * (i % 2),
            "charges_total": 500 + 10 * i,
            "interest_earned": 150 + 2 * i,
            "overdraft_limit": 10000,
            "overdraft_used": 2000 * (i % 2),
            "account_number": f"ACCT{i:010d}",

            # 31–40
            "account_type": random.choice(account_types),
            "currency": "INR",
            "branch_code": f"BR{i:04d}",
            "region": random.choice(regions),
            "kyc_status": random.choice(["COMPLETED", "PENDING"]),
            "risk_segment": random.choice(["LOW", "MEDIUM", "HIGH"]),
            "relationship_tenure_months": 12 + 3 * i,
            "has_credit_card": bool(i % 2),
            "has_mortgage": bool(i % 3 == 0),
            "has_auto_loan": bool(i % 4 == 0),

            # 41–50
            "has_personal_loan": bool(i % 2),
            "digital_channel_index": round(0.5 + 0.03 * i, 2),
            "last_txn_date": end_date.isoformat(),
            "first_txn_date": start_date.isoformat(),
            "avg_txn_amount": round(total_debits / (25 + 2 * i), 2),
            "median_txn_amount": round(1200 + 20 * i, 2),
            "std_txn_amount": round(300 + 10 * i, 2),
            "income_estimate": 60000 + 2000 * i,
            "expense_estimate": 40000 + 1500 * i,
            "confidence_score": round(0.9 + 0.005 * i, 3),
        }
        records.append(record)
    return records


def generate_loan_application_records(n: int = 10):
    records = []
    regions = ["APAC", "EMEA", "AMER"]
    products = ["Personal Loan", "Auto Loan", "Home Loan"]
    channels = ["Branch", "Mobile App", "Web Portal"]
    employment_types = ["SALARIED", "SELF_EMPLOYED"]

    for i in range(1, n + 1):
        requested_amount = 200000 + 50000 * i
        income = 800000 + 50000 * i
        liabilities = 50000 + 20000 * (i % 4)
        tenor_months = 12 * (1 + i % 5)

        record = {
            # 1–10
            "document_type": "loan_application",
            "application_id": f"APP{i:06d}",
            "customer_id": f"CUST{i:05d}",
            "product_type": random.choice(products),
            "requested_amount": requested_amount,
            "tenor_months": tenor_months,
            "region": random.choice(regions),
            "application_channel": random.choice(channels),
            "application_date": f"2025-02-{min(28, 10 + i):02d}",
            "decision_status": random.choice(["Pending", "Approved", "Rejected"]),

            # 11–20
            "interest_rate_offered": round(9.5 + 0.25 * i, 2),
            "processing_fee": 1000 + 100 * i,
            "income": income,
            "liabilities": liabilities,
            "credit_score": 650 + 5 * i,
            "dti_ratio": round(liabilities / max(income, 1), 3),
            "employment_type": random.choice(employment_types),
            "employer_category": random.choice(["TIER1", "TIER2", "OTHERS"]),
            "years_in_current_job": 1 + i % 7,
            "total_work_experience_years": 3 + i,

            # 21–30
            "age": 25 + i,
            "marital_status": random.choice(["SINGLE", "MARRIED"]),
            "dependents_count": i % 4,
            "existing_relationship_years": 1 + i % 6,
            "has_existing_loan_with_bank": bool(i % 2),
            "existing_loans_total_amount": 100000 * (i % 3),
            "collateral_type": random.choice(["NONE", "PROPERTY", "VEHICLE"]),
            "collateral_value": 0 if i % 2 else 500000 + 20000 * i,
            "segment": random.choice(["MASS", "AFFLUENT", "HNI"]),
            "risk_score_internal": round(0.3 + 0.03 * i, 3),

            # 31–40
            "fraud_flag": bool(i % 7 == 0),
            "early_delinquency_flag": bool(i % 5 == 0),
            "approval_probability_model": round(0.4 + 0.04 * i, 3),
            "channel_cost_index": round(1.0 + 0.1 * (i % 3), 2),
            "priority_segment_flag": bool(i % 3 == 0),
            "preapproved_flag": bool(i % 4 == 0),
            "branch_code": f"BR{i:04d}",
            "city": f"City_{i}",
            "country": "India",
            "currency": "INR",

            # 41–50
            "campaign_id": f"CAMP{i:03d}",
            "campaign_response_flag": bool(i % 3 == 0),
            "device_type": random.choice(["MOBILE", "DESKTOP", "BRANCH"]),
            "referral_flag": bool(i % 2),
            "cross_sell_eligible": bool(i % 2 == 0),
            "upsell_eligible": bool(i % 3 == 0),
            "net_monthly_surplus": income / 12 - liabilities / 12 - 10000,
            "underwriter_manual_override": bool(i % 4 == 1),
            "model_version_used": "loan_risk_v1",
            "confidence_score": round(0.88 + 0.006 * i, 3),
        }
        records.append(record)
    return records


def generate_onboarding_records(n: int = 10):
    records = []
    regions = ["APAC", "EMEA", "AMER"]
    channels = ["Branch", "Mobile App", "Web Portal"]
    kyc_methods = ["VIDEO_KYC", "IN_PERSON", "EKYC"]

    for i in range(1, n + 1):
        record = {
            # 1–10
            "document_type": "onboarding_form",
            "customer_id": f"CUST{i:05d}",
            "full_name": f"Customer {i}",
            "gender": random.choice(["Male", "Female", "Other"]),
            "dob": f"19{70 + i % 25}-06-{min(28, 5 + i):02d}",
            "national_id": f"ID{i:08d}",
            "region": random.choice(regions),
            "country": "India",
            "city": f"City_{i}",
            "residential_status": random.choice(["OWNED", "RENTED"]),

            # 11–20
            "mobile_number": f"+91-9{random.randint(100000000, 999999999)}",
            "email": f"customer{i}@example.com",
            "account_opening_channel": random.choice(channels),
            "primary_account_type": random.choice(["SAVINGS", "CURRENT"]),
            "segment": random.choice(["MASS", "AFFLUENT", "HNI"]),
            "source_of_funds": random.choice(["SALARY", "BUSINESS", "INVESTMENT"]),
            "occupation": random.choice(["ENGINEER", "MANAGER", "SELF_EMPLOYED", "OTHER"]),
            "annual_income": 500000 + 50000 * i,
            "pep_flag": bool(i % 10 == 0),
            "risk_rating_initial": random.choice(["LOW", "MEDIUM", "HIGH"]),

            # 21–30
            "fatca_declaration": bool(i % 2),
            "crs_declaration": bool(i % 3 == 0),
            "tax_residency_country": "India",
            "consent_marketing": bool(i % 2),
            "consent_data_sharing": bool(i % 3 == 0),
            "kyc_completed": bool(i % 2 == 0),
            "kyc_method": random.choice(kyc_methods),
            "kyc_completion_date": f"2025-01-{min(28, 10 + i):02d}",
            "welcome_kit_opt_in": bool(i % 2),
            "debit_card_opt_in": bool(i % 2),

            # 31–40
            "net_banking_opt_in": bool(i % 2 == 0),
            "mobile_banking_opt_in": True,
            "preferred_language": random.choice(["EN", "HI"]),
            "referral_code_used": f"REF{i:04d}" if i % 3 == 0 else "",
            "family_bank_relation": bool(i % 3 == 0),
            "has_existing_relationship": bool(i % 4 == 0),
            "existing_products_count": i % 5,
            "wealth_flag": bool(i % 5 == 0),
            "rm_assigned_flag": bool(i % 3 == 0),
            "rm_id": f"RM{i:03d}" if i % 3 == 0 else "",

            # 41–50
            "onboarding_date": f"2025-01-{min(28, 1 + i):02d}",
            "onboarding_status": random.choice(["COMPLETED", "PENDING", "ON_HOLD"]),
            "onboarding_sla_met": bool(i % 4 != 0),
            "channel_latency_seconds": 10 + 2 * i,
            "document_upload_count": 3 + i % 4,
            "document_reupload_required": bool(i % 5 == 0),
            "initial_funding_amount": 10000 + 2000 * i,
            "rm_segment_tag": random.choice(["STANDARD", "PRIORITY", "WEALTH"]),
            "feedback_score_initial": random.randint(3, 5),
            "confidence_score": round(0.9 + 0.004 * i, 3),
        }
        records.append(record)
    return records


def main():
    bank_file = BASE_DIR / "bank_statement_example.json"
    loan_file = BASE_DIR / "loan_application_example.json"
    onboard_file = BASE_DIR / "onboarding_form_example.json"

    bank_data = generate_bank_statement_records()
    loan_data = generate_loan_application_records()
    onboard_data = generate_onboarding_records()

    bank_file.write_text(json.dumps(bank_data, indent=4), encoding="utf-8")
    loan_file.write_text(json.dumps(loan_data, indent=4), encoding="utf-8")
    onboard_file.write_text(json.dumps(onboard_data, indent=4), encoding="utf-8")

    print(f"[WRITE] {bank_file} ({len(bank_data)} records)")
    print(f"[WRITE] {loan_file} ({len(loan_data)} records)")
    print(f"[WRITE] {onboard_file} ({len(onboard_data)} records)")


if __name__ == "__main__":
    main()
