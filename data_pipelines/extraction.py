"""
extraction.py

Simulated Document AI extraction step.

In a real system this would:
- Call Azure Form Recognizer (or equivalent) per document type
- Handle model selection by region/template
- Normalize the response into a canonical JSON payload

Here we:
- Read JSON files from the landing zone (acting as "already OCR'd")
- Wrap them in ExtractionResult objects
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import List

from .schemas import DocumentMetadata, ExtractionResult


def _load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def extract_from_metadata_items(metadata_items: List[DocumentMetadata]) -> List[ExtractionResult]:
    """
    For each DocumentMetadata object, read its JSON file and
    build an ExtractionResult.

    Assumptions for this demo:
    - Files are already JSON (e.g., output of OCR step)
    - Confidence is a dummy value; in real life comes from Document AI
    """
    results: List[ExtractionResult] = []

    for meta in metadata_items:
        if meta.path.suffix.lower() != ".json":
            print(f"[EXTRACT] Skipping non-JSON file: {meta.path.name}")
            continue

        try:
            payload = _load_json(meta.path)
        except json.JSONDecodeError as exc:
            print(f"[EXTRACT] Failed to parse JSON for {meta.path.name}: {exc}")
            continue

        confidence = float(payload.get("confidence_score", 0.9))

        result = ExtractionResult(
            metadata=meta,
            payload=payload,
            confidence=confidence,
        )
        results.append(result)

        print(f"[EXTRACT] Loaded payload for {meta.path.name} | "
              f"type={meta.document_type.value} | confidence={confidence:.2f}")

    return results


if __name__ == "__main__":
    # Example usage:
    # Run ingestion first to populate landing_zone, then:
    from .ingestion import ingest_to_landing

    source_dir = Path("./sample_data")
    landing_dir = Path("./landing_zone")

    metas = ingest_to_landing(source_dir, landing_dir)
    extracted = extract_from_metadata_items(metas)
    print(f"[EXTRACT] Total extracted: {len(extracted)}")
