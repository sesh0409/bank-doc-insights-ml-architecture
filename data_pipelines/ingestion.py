"""
ingestion.py

Simple local "ingestion" layer that simulates:
- Discovering documents on disk
- Building DocumentMetadata for each file
- Copying files into a landing zone (as if into ADLS / Blob)

This is intentionally lightweight so the repository can be cloned
and understood without any cloud credentials.
"""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import List, Optional

from .schemas import DocumentMetadata, DocumentType


def infer_metadata_from_filename(path: Path, default_region: str = "APAC") -> Optional[DocumentMetadata]:
    """
    Infer basic metadata from a filename convention:

        <customer_id>__<document_type>__<region>.<ext>

    Example:
        CUST00123__bank_statement__APAC.json
        CUST00999__loan_application__EMEA.pdf

    If parsing fails, returns None.
    """
    stem_parts = path.stem.split("__")
    if len(stem_parts) < 2:
        # Not following the convention; skip or handle separately
        return None

    customer_id = stem_parts[0]
    doc_type_raw = stem_parts[1]
    region = stem_parts[2] if len(stem_parts) >= 3 else default_region

    try:
        document_type = DocumentType(doc_type_raw)
    except ValueError:
        # Unknown document type for our pipeline
        return None

    # For demo, assume everything comes via "portal"
    source_channel = "portal"

    return DocumentMetadata(
        path=path,
        customer_id=customer_id,
        document_type=document_type,
        region=region,
        source_channel=source_channel,
    )


def discover_documents(input_dir: Path) -> List[Path]:
    """
    Recursively discover all files in the given directory.

    In real life we'd filter by extension (.pdf, .tif, .png, etc).
    """
    if not input_dir.exists():
        raise FileNotFoundError(f"Input directory does not exist: {input_dir}")

    return [p for p in input_dir.rglob("*") if p.is_file()]


def ingest_to_landing(
    source_dir: Path,
    landing_dir: Path,
    default_region: str = "APAC",
) -> List[DocumentMetadata]:
    """
    Discover documents in source_dir, copy them to landing_dir,
    and return a list of DocumentMetadata objects.

    This mimics landing into ADLS Gen2 / Blob Storage.
    """
    landing_dir.mkdir(parents=True, exist_ok=True)

    docs = discover_documents(source_dir)
    metadata_items: List[DocumentMetadata] = []

    for src in docs:
        meta = infer_metadata_from_filename(src, default_region=default_region)
        if meta is None:
            print(f"[INGEST] Skipping file with unknown pattern: {src.name}")
            continue

        dest = landing_dir / src.name
        shutil.copy2(src, dest)

        # Update path in metadata to reflect landing location
        meta.path = dest
        metadata_items.append(meta)

        print(f"[INGEST] {src.name} -> {dest} | "
              f"{meta.document_type.value} | customer={meta.customer_id} | region={meta.region}")

    return metadata_items


if __name__ == "__main__":
    # Example usage (local):
    # python -m data_pipeline.ingestion
    src = Path("./sample_data")
    landing = Path("./landing_zone")

    ingested = ingest_to_landing(src, landing)
    print(f"[INGEST] Total ingested: {len(ingested)}")
