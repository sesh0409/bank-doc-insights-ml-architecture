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

A[Raw Data<br>ADLS Gen2] --> B[ETL<br>Azure Data Factory / Databricks]
B --> C[Curated Zone<br>Delta Tables / Synapse]
C --> D[(Azure Synapse SQL<br>Power BI DirectQuery)]
D --> E[Power BI Dashboards<br>Users & Decision Makers]

E -.-> F[Row-level Security<br>(RBAC + AAD)]
C -.-> G[Hot Storage<br>Low Latency Views]
```
