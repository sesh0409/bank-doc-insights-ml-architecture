# ML Model Lifecycle & MLOps Governance

This document describes how ML models (e.g., **churn**, **loan risk support**, **next-best-offer**) move from
**idea → production → monitoring → retraining** in a governed way suitable for a regulated bank.

The goal is to avoid “one-off notebooks” and instead have **repeatable, auditable ML pipelines**.

---

## 1. Objectives of the ML Lifecycle

- **Traceability**: Every model version can be traced back to data, code, config, and approvers.
- **Reproducibility**: Training runs are reproducible using stored code, parameters, and dataset snapshots.
- **Governance & Risk**: Business, Risk, and Compliance have clear checkpoints before models go live.
- **Operational Reliability**: Models are deployed via automated pipelines with monitoring and rollback.
- **Continuous Improvement**: Performance drift is detected and triggers **controlled retraining**.

---

## 2. Lifecycle Phases (Conceptual)

1. **Business Problem & KPI Definition**
   - Define the use case (e.g., churn reduction, NPL reduction, upsell uplift).
   - Agree on **success metrics**: AUC, conversion uplift, delinquency reduction, onboarding TAT, etc.
   - Clarify constraints: explainability, fairness, geography, product scope.

2. **Data & Feature Management**
   - Source labeled data from curated / gold layer (Synapse / Delta).
   - Define **feature views** (e.g., customer 360, loan application view).
   - Track data lineage: which tables, time windows, and transformation logic.
   - Apply DQ checks and reject bad training data early.

3. **Model Experimentation & Training**
   - Use Azure ML / Databricks for experiments.
   - Log:
     - Code version (git commit)
     - Hyperparameters
     - Training dataset snapshot
     - Metrics (AUC, recall@K, calibration, etc.)
   - Compare multiple candidate models (baseline vs advanced).

4. **Review, Risk, and Approval**
   - Generate **model cards**:
     - Purpose, data, algorithms, metrics, limitations.
   - Review by:
     - Data Science Lead (technical)
     - Risk / Model Risk Management (governance)
     - Business Owner (fit-for-purpose)
   - Only **approved** model versions are allowed to move to deployment.

5. **Deployment & Serving**
   - Register approved model in **Model Registry**.
   - Deploy behind a **versioned endpoint** (Azure ML / Databricks serving).
   - Put API Management in front for:
     - AuthN/AuthZ
     - Throttling
     - Central logging / tracing
   - Integrate with:
     - Underwriter UI
     - LOS / CRM
     - Batch scoring (for nightly refreshes).

6. **Monitoring & Alerting**
   - Monitor at multiple levels:
     - **Data drift**: feature distribution vs training baseline.
     - **Prediction drift**: score distribution, class balance.
     - **Outcome performance**: AUC, delinquency rate, churn rate, conversion uplift.
     - **Operational**: latency, error rates, throughput.
   - Define thresholds and automatic alerts to team channels / ticketing.

7. **Retraining, Rollback & Decommissioning**
   - Schedule **periodic retraining** (e.g., monthly/quarterly) OR event-based retraining upon drift.
   - New model versions must go through the same approval pipeline.
   - If degradation or defects are detected:
     - Roll back to previous stable model version.
   - Decommission models that are:
     - Outdated, superseded, or no longer aligned with business policy.

---

## 3. Vertical ML Lifecycle Flow (Mermaid Diagram)

```mermaid
flowchart TB

%% === STYLES ===
classDef phase fill:#0078D4,stroke:#003B73,stroke-width:2px,color:#ffffff,font-weight:bold
classDef step fill:#E5F3FF,stroke:#0078D4,stroke-width:1.5px,color:#003B73,font-weight:bold
classDef gov fill:#FDE7E7,stroke:#B22222,stroke-width:1.5px,color:#7A0000,font-weight:bold

%% === PHASES (TOP → BOTTOM) ===
P0["1. Business Problem & KPIs"]:::phase
P1["2. Data & Feature Management"]:::phase
P2["3. Model Training & Experimentation"]:::phase
P3["4. Review & Approval"]:::phase
P4["5. Deployment & Serving"]:::phase
P5["6. Monitoring & Alerting"]:::phase
P6["7. Retraining & Rollback"]:::phase

%% === KEY STEPS UNDER EACH PHASE ===
S01["Define use case\nand target metric"]:::step
S11["Build feature views\n(customer 360, loan view)"]:::step
S12["Validate data quality\nand lineage"]:::step

S21["Run experiments\n(Log metrics + params)"]:::step
S22["Compare models\nagainst baseline"]:::step

S31["Create model card\nand documentation"]:::step
S32["Risk / Compliance\nreview and sign-off"]:::step

S41["Register model in\nModel Registry"]:::step
S42["Deploy endpoint\nbehind API Management"]:::step

S51["Monitor data & prediction drift"]:::step
S52["Track business KPIs\n(churn, NPL, TAT)"]:::step

S61["Trigger retraining\non schedule / drift"]:::step
S62["Rollback or promote\nnew model version"]:::step

%% === MAIN FLOW ===
P0 --> S01 --> P1
P1 --> S11 --> S12 --> P2
P2 --> S21 --> S22 --> P3
P3 --> S31 --> S32 --> P4
P4 --> S41 --> S42 --> P5
P5 --> S51 --> S52 --> P6
P6 --> S61 --> S62 --> P2

%% === GOVERNANCE OVERLAY ===
subgraph Governance
G1["Model Registry\n(versioned models)"]:::gov
G2["Audit Trail\n(data, code, approvals)"]:::gov
G3["Access Control\n(RBAC, AAD)"]:::gov
end

P2 -.-> G1
P3 -.-> G2
P4 -.-> G3
