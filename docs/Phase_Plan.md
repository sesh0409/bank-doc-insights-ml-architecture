## Phase-wise Delivery Plan — Customer Insights & Loan Optimization

```mermaid
flowchart TB

    %% === STYLE CONFIG ===
    classDef phaseStyle fill:#0078D4,stroke:#003B73,stroke-width:3px,color:#ffffff,font-weight:bold;
    classDef taskStyle fill:#E5F3FF,stroke:#0078D4,stroke-width:2px,color:#003B73,font-weight:bold;

    %% === PHASES (Top to Bottom) ===
    P1["Phase 1 - Proof of Concept\n(4-6 Weeks)"]:::phaseStyle
    P2["Phase 2 - Pilot\n(8-12 Weeks)"]:::phaseStyle
    P3["Phase 3 - Production Rollout\n(3-6 Months)"]:::phaseStyle

    %% === TASKS UNDER EACH PHASE ===
    T11["Scope: 1 Region, 1 Product"]:::taskStyle
    T12["Document AI for Bank Statements + Loan Forms"]:::taskStyle
    T13["Basic Churn Model + Simple Dashboard"]:::taskStyle

    T21["Support Multi-template + Multi-language Documents"]:::taskStyle
    T22["Underwriter UI with RBAC + Low-Latency Access"]:::taskStyle
    T23["Loan Risk Support + Propensity Models"]:::taskStyle
    T24["ML Monitoring: Accuracy + Drift"]:::taskStyle

    T31["Multi-Region Rollout + Data Residency Compliance"]:::taskStyle
    T32["MLOps Governance + Automated Retraining"]:::taskStyle
    T33["CRM Integration for Retention Campaigns"]:::taskStyle
    T34["Scalable Infrastructure + SLAs + DR"]:::taskStyle

    %% === HIERARCHICAL RELATIONSHIP ===
    P1 --> T11 --> T12 --> T13 --> P2
    P2 --> T21 --> T22 --> T23 --> T24 --> P3
    P3 --> T31 --> T32 --> T33 --> T34
