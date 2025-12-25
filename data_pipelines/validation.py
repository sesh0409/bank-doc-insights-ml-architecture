"""
validation.py

Data quality and business rule checks on extracted payloads.

This helps:
- Demonstrate governance for ML inputs
- Separate concerns (extraction vs validation vs modeling)
"""

from __future__ import annotations

from typing import List

from .schemas import ExtractionResult, ValidationResult


def validate_bank_statement(result: ExtractionResult) -> ValidationResult:
    vr = ValidationResult(is_valid=True)
    p = result.payload

    if not p.get("customer_id"):
        vr.add_issue("customer_id", "Missing customer_id")

    if "closing_balance" in p and "opening_balance" in p:
        if p["closing_balance"] < 0:
            vr.add_issue("closing_balance", "Closing balance cannot be negative")
    else:
        vr.add_issue("closing_balance", "Missing balance fields", severity="WARNING")

    if not p.get("currency"):
        vr.add_issue("currency", "Currency not provided", severity="WARNING")

    return vr


def validate_loan_application(result: ExtractionResult) -> ValidationResult:
    vr = ValidationResult(is_valid=True)
    p = result.payload

    if not p.get("application_id"):
        vr.add_issue("application_id", "Missing application_id")

    for field in ("requested_amount", "tenor_months", "income"):
        if field not in p:
            vr.add_issue(field, f"Missing {field}")
        elif p[field] is not None and p[field] < 0:
            vr.add_issue(field, f"{field} cannot be negative")

    return vr


def validate_onboarding_form(result: ExtractionResult) -> ValidationResult:
    vr = ValidationResult(is_valid=True)
    p = result.payload

    if not p.get("full_name"):
        vr.add_issue("full_name", "Missing full_name")

    if not p.get("dob"):
        vr.add_issue("dob", "Missing date of birth", severity="WARNING")

    if not p.get("region"):
        vr.add_issue("region", "Missing region")

    return vr


def route_validation(result: ExtractionResult) -> ValidationResult:
    """
    Route to the correct validator based on document type.
    """
    doc_type = result.metadata.document_type

    if doc_type.value == "bank_statement":
        return validate_bank_statement(result)
    if doc_type.value == "loan_application":
        return validate_loan_application(result)
    if doc_type.value == "onboarding_form":
        return validate_onboarding_form(result)

    # Default: no specific rules, consider valid
    return ValidationResult(is_valid=True)


def validate_batch(results: List[ExtractionResult]) -> List[ValidationResult]:
    """
    Run validation for a batch of extraction results.
    """
    validations: List[ValidationResult] = []

    for r in results:
        vr = route_validation(r)
        status = "OK" if vr.is_valid else "FAILED"
        print(f"[VALIDATE] {r.metadata.path.name} -> {status} "
              f"(issues={len(vr.issues)})")
        validations.append(vr)

    return validations


if __name__ == "__main__":
    # Example demo pipeline when this module is run directly
    from pathlib import Path
    from .ingestion import ingest_to_landing
    from .extraction import extract_from_metadata_items

    source_dir = Path("./sample_data")
    landing_dir = Path("./landing_zone")

    metas = ingest_to_landing(source_dir, landing_dir)
    extracted = extract_from_metadata_items(metas)
    validate_batch(extracted)
