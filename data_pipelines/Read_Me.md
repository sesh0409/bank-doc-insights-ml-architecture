# ▶️ Data Pipeline — Example Execution Snippets

The following examples demonstrate the execution of each stage in this pipeline
using the sample JSON data already included in the repository.

---

## 1️⃣ Ingestion — Discover + Move to Landing Zone

```python
from pathlib import Path
from data_pipeline.ingestion import ingest_to_landing

source_dir = Path("./sample_data")
landing_dir = Path("./landing_zone")

metadata_items = ingest_to_landing(source_dir, landing_dir)
print(f"Total ingested: {len(metadata_items)}")
```
## 2️⃣ Extraction — Simulated Document AI → Structured JSON


from pathlib import Path
from data_pipeline.ingestion import ingest_to_landing
from data_pipeline.extraction import extract_from_metadata_items

source_dir = Path("./sample_data")
landing_dir = Path("./landing_zone")

metas = ingest_to_landing(source_dir, landing_dir)
extracted = extract_from_metadata_items(metas)

print(f"Total extracted: {len(extracted)}")
for r in extracted:
    print(r.metadata.document_type, r.confidence)

## 3️⃣ Validation — Quality Checks + Business Rules

from pathlib import Path
from data_pipeline.ingestion import ingest_to_landing
from data_pipeline.extraction import extract_from_metadata_items
from data_pipeline.validation import validate_batch

source_dir = Path("./sample_data")
landing_dir = Path("./landing_zone")

metas = ingest_to_landing(source_dir, landing_dir)
extracted = extract_from_metadata_items(metas)
validations = validate_batch(extracted)

for vr in validations:
    print(vr.to_dict())


##4️⃣ Schemas — Canonical Structured Entities

from data_pipeline.schemas import CustomerRecord, LoanApplicationRecord

customer = CustomerRecord(
    customer_id="CUST00999",
    full_name="Sample User",
    region="APAC",
)

loan = LoanApplicationRecord(
    application_id="APP11111",
    customer_id="CUST00999",
    product_type="Personal Loan",
    requested_amount=500000,
    tenor_months=48,
    income=1200000,
    liabilities=300000,
    region="APAC",
)

print(customer)
print(loan)

