## 📌 Phase-wise Delivery Plan — Customer Insights & Loan Optimization

```mermaid
flowchart TD

    %% === STYLE CONFIG ===
    classDef phaseStyle fill:#0078D4,stroke:#003B73,stroke-width:3px,color:#ffffff,font-weight:bold
    classDef taskStyle fill:#E5F3FF,stroke:#0078D4,stroke-width:2px,color:#003B73,font-weight:bold

    %% === PHASES ===
    P1[Phase 1️⃣ — PoC<br>(4–6 Weeks)]:::phaseStyle
    P2[Phase 2️⃣ — Pilot<br>(8–12 Weeks)]:::phaseStyle
    P3[Phase 3️⃣ — Production Rollout<br>(3–6 Months)]:::phaseStyle

    %% === TASKS UNDER PHASES ===
    T11[[1 Region + 1 Product Scope]]:::taskStyle
    T12[[Document AI: Bank Statements + Loan Forms]]:::taskStyle
    T13[[Basic Churn Model + Simple Dashboard]]:::taskStyle

    T21[[Multi-template + Multi-language support]]:::taskStyle
    T22[[Underwriter UI + Role-Based Access]]:::taskStyle
    T23[[Loan Risk Support + Propensity Scoring]]:::taskStyle
    T24[[ML Monitoring: AUC + Drift Detection]]:::taskStyle

    T31[[Multi-Region Rollout + Data Residency Compliance]]:::taskStyle
    T32[[MLOps Governance + Retraining Automation]]:::taskStyle
    T33[[CRM Integration + Proactive Retention Campaigns]]:::taskStyle
    T34[[Scalable Infra + SLA Monitoring + DR]]:::taskStyle

    %% === HIERARCHY ===
    P1 -->|<b>Deliverables</b>| T11
    P1 -->|<b>Deliverables</b>| T12
    P1 -->|<b>Deliverables</b>| T13

    P2 -->|<b>Deliverables</b>| T21
    P2 -->|<b>Deliverables</b>| T22
    P2 -->|<b>Deliverables</b>| T23
    P2 -->|<b>Deliverables</b>| T24

    P3 -->|<b>Deliverables</b>| T31
    P3 -->|<b>Deliverables</b>| T32
    P3 -->|<b>Deliverables</b>| T33
    P3 -->|<b>Deliverables</b>| T34

    %% === PROCESS FLOW ===
    P1 ==> P2 ==> P3
