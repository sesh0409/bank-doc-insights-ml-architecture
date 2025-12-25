## Phase-wise Delivery Plan — Customer Insights & Loan Optimization

```mermaid
flowchart TD

    %% === STYLE CONFIG ===
    classDef phaseStyle fill:#0078D4,stroke:#003B73,stroke-width:3px,color:#ffffff,font-weight:bold;
    classDef taskStyle fill:#E5F3FF,stroke:#0078D4,stroke-width:2px,color:#003B73,font-weight:bold;

    %% === PHASES ===
    P1["Phase 1 - Proof of Concept (4-6 Weeks)"]:::phaseStyle
    P2["Phase 2 - Pilot (8-12 Weeks)"]:::phaseStyle
    P3["Phase 3 - Production Rollout (3-6 Months)"]:::phaseStyle

    %% === TASKS UNDER PHASES ===
    T11["Scope: 1 Region, 1 Product"]:::taskStyle
    T12["Document AI for Bank Statements + Loan Forms"]:::taskStyle
    T13["Basic Churn Model + Simple Dashboard"]:::taskStyle

    T21["Support Multi-template + Multi-language Documents"]:::taskStyle
    T22["Underwriter UI with RBAC"]:::taskStyle
    T23["Loan Risk Support + Propensity Models"]:::taskStyle
    T24["ML Monitoring: Accuracy + Drift"]:::taskStyle

    T31["Multi-Region Rollout + Data Residency Compliance"]:::taskStyle
    T32["MLOps Governance + Retraining Automation"]:::taskStyle
    T33["CRM Integration for Retention Campaigns"]:::taskStyle
    T34["Scalable Infra + SLAs + Disaster Recovery"]:::taskStyle

    %% === PHASE BREAKDOWN ===
    P1 --> T11
    P1 --> T12
    P1 --> T13

    P2 --> T21
    P2 --> T22
    P2 --> T23
    P2 --> T24

    P3 --> T31
    P3 --> T32
    P3 --> T33
    P3 --> T34
    %% === TIMELINE FLOW ===
    P1 ==> P2 ==> P3
