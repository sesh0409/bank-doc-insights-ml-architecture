# 🌐 Azure Architecture — Customer Insights & Loan Process Optimization

This document describes how the solution is deployed on **Microsoft Azure**, aligned with the
code structure in this repository:

- `data_pipeline/` → Data ingestion, extraction, validation
- `ml/` → Feature engineering and ML models
- `dashboards/` → BI & reporting
- `config/` → Environment-specific configuration

The goal is to provide a **secure, scalable and governed** platform for:
- Document ingestion and digitization
- Customer 360 and loan risk analytics
- Churn, loan risk and next-best-offer ML models
- Dashboards for underwriters, CRM and executives

---

## 1. Core Azure Services Mapping

| Layer | Purpose | Azure Services |
|------|---------|----------------|
| Ingestion & Storage | Raw document landing and structured zones | Azure Blob Storage / ADLS Gen2 |
| Document AI | OCR + key-value extraction | Azure AI Document Intelligence (Form Recognizer) |
| Orchestration | Pipelines for ETL & ML | Azure Data Factory, Azure Databricks |
| Data Warehouse / Lakehouse | Curated / Gold zones | Azure Synapse Analytics, Delta Lake |
| ML Platform | Training, registry, endpoints | Azure Machine Learning |
| Serving APIs | Underwriter & CRM access | Azure Kubernetes Service (AKS) or Azure Container Apps, Azure API Management |
| Identity & Security | Authentication & authorization | Azure Active Directory, Key Vault |
| Monitoring & Logging | Observability & audit | Azure Monitor, Log Analytics, Application Insights |
| Governance | Catalog, lineage, classification | Microsoft Purview |

---

## 2. High-Level Azure Architecture (End-to-End Flow)

```mermaid
flowchart TB
    subgraph Ingestion
        A1["Bank Portals / LOS / Branch"]
        A2["Azure Blob Storage / ADLS Gen2 (Raw)"]
        A1 --> A2
    end

    subgraph DocumentAI["Document AI Layer"]
        B1["Azure AI Document Intelligence (Form Recognizer)"]
        B2["Extracted JSON (Structured Fields)"]
        A2 --> B1 --> B2
    end

    subgraph Processing["Data Processing & Validation"]
        C1["Azure Data Factory"]
        C2["Azure Databricks (ETL + Validation)"]
        B2 --> C1 --> C2
    end

    subgraph Storage["Data Lakehouse"]
        D1["ADLS Gen2 - Raw / Processed"]
        D2["Delta Tables / Synapse (Curated / Gold)"]
        C2 --> D1 --> D2
    end

    subgraph ML["ML Platform (Azure ML)"]
        E1["Feature Engineering\n(Customer 360 / Loan View)"]
        E2["Churn Model"]
        E3["Loan Risk Support Model"]
        E4["Model Registry + Endpoints"]
        D2 --> E1
        E1 --> E2
        E1 --> E3
        E2 --> E4
        E3 --> E4
    end

    subgraph Serving["Serving & Consumption"]
        F1["Azure API Management"]
        F2["Underwriter UI / LOS Integration"]
        F3["CRM / Campaign Tools"]
        F4["Power BI Service (Dashboards)"]
        E4 --> F1 --> F2
        E4 --> F3
        D2 --> F4
    end

    subgraph Security["Security & Governance"]
        G1["Azure AD (Identity)"]
        G2["Key Vault (Secrets, Keys)"]
        G3["Microsoft Purview (Catalog & Lineage)"]
        G4["Azure Monitor / Log Analytics"]
    end

    Storage -.-> Security
    ML -.-> Security
    Serving -.-> Security
```
