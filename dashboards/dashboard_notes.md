# 📊 Dashboards & Analytics — Business Intelligence Layer

This document describes how analytics insights are exposed to end users such as:
- 🧑‍💼 Underwriters (risk support, decision confidence)
- 🎯 CRM / Marketing (next-best-offer targeting, retention tracking)
- 🧑‍⚖️ Executives (operational KPIs & business outcomes)

---

## 🎯 Objectives

- Provide a **single pane of glass** for customer intelligence
- Support **loan decisioning** through risk scores + explainability
- Enable **proactive retention** and **new customer acquisition**
- Measure **pipeline health**, **SLAs**, and **customer experience KPIs**

---

## 🧩 Data Flow into Power BI (Azure Cloud)

Data ingestion into Power BI follows governed access from the **Curated (Gold) Zone**:

```mermaid
flowchart TB
    A["Raw Data - ADLS Gen2"] --> B["ETL - Azure Data Factory / Databricks"]
    B --> C["Curated Zone - Delta Tables / Synapse"]
    C --> D[["Azure Synapse SQL / Power BI DirectQuery"]]
    D --> E["Power BI Dashboards - Users & Decision Makers"]
    
    E -.-> F["Row-level Security (RBAC & Azure AD)"]
    C -.-> G["Hot Storage - Low Latency Views"]

```

## 🧩 Data Flow into Power BI (Azure Cloud)

Operational and ML-derived insights are consumed through secure and governed dashboards in Power BI.
Only validated and privacy-compliant data from the Curated (Gold) Zone is exposed to business users.

Access is tightly controlled using:

Azure AD authentication

Role-Based Access Control (RBAC)

Row-Level Security (RLS) → users only see authorized region/customers

Data masking for high-risk PII fields (e.g., account numbers)

Audit logs for dashboard views & data access

This ensures analytics helps accelerate decisioning without compromising financial data security.

```mermaid
flowchart TB

%% LAYER STYLES
classDef data fill:#CDE6F7,stroke:#0078D4,stroke-width:2px,color:#003B73,font-weight:bold
classDef process fill:#EDE7F6,stroke:#6C33A3,stroke-width:2px,color:#3D1A5A,font-weight:bold
classDef bi fill:#FFF2CC,stroke:#CC9900,stroke-width:2px,color:#4D3D00,font-weight:bold
classDef security fill:#FDE7E7,stroke:#A61C1C,stroke-width:2px,color:#7A0000,font-weight:bold

%% DATA FLOW
A[Raw Storage<br>Azure Data Lake Gen2]:::data
B[Data Processing<br>ADF / Databricks ETL]:::process
C[Curated Zone<br>Synapse / Delta Tables]:::data
D[(Semantic Model<br>Power BI DirectQuery)]:::bi
E[Dashboards & Reports<br>Power BI Service]:::bi

%% FLOW CONNECTIONS
A --> B --> C --> D --> E

%% GOVERNANCE + SECURITY
E -.-> F[RBAC + Row-Level Security<br>Azure AD]:::security
C -.-> G[Secure Views for Low-Latency Access<br>Controlled Exposure]:::security
```
