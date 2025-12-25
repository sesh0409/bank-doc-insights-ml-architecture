"""
schemas.py

Shared data structures for the document pipeline:
- Document metadata
- Extraction outputs
- Validation results
- Canonical customer / loan entities

These are intentionally simple and framework-agnostic.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional


class DocumentType(str, Enum):
    """Supported document types in the pipeline."""
    BANK_STATEMENT = "bank_statement"
    LOAN_APPLICATION = "loan_application"
    ONBOARDING_FORM = "onboarding_form"


@dataclass
class DocumentMetadata:
    """
    Lightweight metadata about a single document.

    This simulates what we'd store when a file is first ingested into
    object storage / data lake.
    """
    path: Path
    customer_id: str
    document_type: DocumentType
    region: str
    source_channel: str  # e.g. "branch", "portal", "api"


@dataclass
class ExtractionResult:
    """
    Structured output from the Document AI / OCR step.

    In production this would be the cleaned/normalized JSON returned
    from Azure Form Recognizer or equivalent.
    """
    metadata: DocumentMetadata
    payload: Dict[str, Any]
    confidence: float


@dataclass
class ValidationIssue:
    """
    A single validation rule result.
    """
    field: str
    message: str
    severity: str = "ERROR"  # could be "WARNING" / "INFO"


@dataclass
class ValidationResult:
    """
    Result of running validation rules on a record.
    """
    is_valid: bool
    issues: List[ValidationIssue] = field(default_factory=list)

    def add_issue(self, field: str, message: str, severity: str = "ERROR") -> None:
        self.issues.append(ValidationIssue(field=field, message=message, severity=severity))
        if severity.upper() == "ERROR":
            self.is_valid = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "is_valid": self.is_valid,
            "issues": [asdict(issue) for issue in self.issues],
        }


# === Canonical business entities (simplified) ===

@dataclass
class CustomerRecord:
    """
    Canonical customer representation used in the curated / gold layer.
    """
    customer_id: str
    full_name: str
    region: str
    segment: Optional[str] = None
    risk_band: Optional[str] = None


@dataclass
class LoanApplicationRecord:
    """
    Canonical view of a loan application used for downstream ML and analytics.
    """
    application_id: str
    customer_id: str
    product_type: str
    requested_amount: float
    tenor_months: int
    income: float
    liabilities: float
    region: str
    decision_status: Optional[str] = None  # approved / rejected / pending


@dataclass
class OnboardingRecord:
    """
    Core fields extracted from onboarding forms.
    """
    customer_id: str
    full_name: str
    dob: str  # ISO string for simplicity
    region: str
    channel: str  # e.g. "branch", "mobile_app"
    consent_provided: bool = True
