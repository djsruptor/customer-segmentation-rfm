# Customer Segmentation with Synthetic Data
## Business Problem

Retail and e-commerce businesses accumulate large volumes of customer data but often lack a clear, actionable way to translate that data into growth, retention, and monetization strategies.

The goal of this project is to design a reproducible customer segmentation pipeline that:
- Identifies behaviorally distinct customer groups using transactional data
- Produces segments that are interpretable, actionable, and business-ready
- Can be reused by analytics teams and consumed directly by a dashboard or downstream applications

This project is framed as an internal analytics deliverable for a department store seeking to improve:
- customer retention
- targeted marketing
- prioritization of high-value customers

## Dataset

The project uses a synthetic customer dataset downloaded from Kaggle.
- Size: 100,000 records
- Grain: one row per customer (expected)
- Scope: demographic, geographic, and behavioral attributes

Each record represents a unique customer of a department store and includes:

- demographic attributes (age, gender)
- geographic information (country)
- behavioral and transactional fields (total spend, average order value, last purchase date, etc.)

The file `synthetic_customers_metadata.json` documents each field and its intended use cases.

## Data Quality Review and Improvement

A preliminary data quality review was performed before modeling.

Identified issues

1. Duplicate customer identifiers

- The customer_id field was expected to uniquely identify customers.
- 27,490 duplicated identifiers were found.
- Manual inspection confirmed these duplicates did not represent:
  - customer profile updates (e.g. country change, age progression)
  - longitudinal records
- Conclusion: identifiers were unreliable as primary keys.

2. Remediation

- A new deterministic customer_id was generated based on first purchase chronology.
- All downstream processing uses this regenerated identifier.
- The decision and rationale are documented and reproducible in the pipeline.

This step ensures:

- one row per customer
- stable joins
- consistent aggregation logic

## Approach

The project follows a pipeline-first analytics approach, separating:

- data preparation
- feature engineering
- segmentation logic
- analysis and visualization

Segmentation methodology

- RFM analysis (Recency, Frequency, Monetary)
- Quantile-based scoring (5 bins per dimension)
- Explicit, rule-based segment definitions externalized to YAML
- Deterministic, interpretable segmentation (no black-box clustering)

Segmentation rules are defined declaratively and evaluated in order of precedence, enabling:

- easy iteration
- business review
- version control of assumptions

## Deliverables

Customer-level segmentation table

`data/mart/customer_segments.parquet`

Includes:

- cleaned customer attributes
- RFM metrics and scores
- RFM code
- assigned segment
- subscription status

### Segment summary (MISSING TABLE)

Each segment is designed to support a summary view with:

|segment_id | name (human-readable)|
|-|-|
|size|% of customers|
|key traits|top 5 features|
|primary KPI deltas|vs overall population|

Recommended actions (2–3 per segment)

risks / watchouts

This structure is intended for dashboards, stakeholder reviews, and strategy discussions.

## Key Insights

_(Summarized from post-segmentation analysis)_

- A small share of customers concentrates a disproportionate amount of total monetary value.
- High-recency customers split clearly between:
  - high-frequency loyal customers
  - low-frequency but high-potential new customers
- “At risk” customers retain high historical value but show clear recency decay, making them prime targets for re-engagement.
- Premium subscription status meaningfully amplifies value within otherwise similar RFM profiles.

## Recommendations

- Protect and grow top customers
  - personalized retention programs
  - early access and loyalty incentives

- Activate new customers early
  - onboarding campaigns within the first purchase window
  - nudges to increase second purchase probability

- Re-engage at-risk customers
  - targeted win-back offers
  - time-bounded promotions triggered by recency thresholds

- Treat premium status as a modifier, not a segment
  - overlay premium benefits on behavioral segments rather than isolating them

## How to Run
1. Create and activate a virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Run the segmentation pipeline
```bash
python -m segmentation.pipeline
```

This will generate:

`data/mart/customer_segments.parquet`

4. Run the dashboard application

`python -m app.app`

5. Notebooks (optional)

`01_eda_pre_segmentation.ipynb`: data validation and exploratory analysis
`02_segment_analysis.ipynb`: segment profiling and behavioral comparison

## Repository Structure
```bash
customer_segmentation/
├── README.md
├── requirements.txt
├── configs/
│   └── default.yaml
├── data/
│   ├── raw/
│   └── mart/
├── src/
│   ├── config.py
│   ├── segmentation/
│   │   ├── pipeline.py
│   │   ├── features.py
│   │   ├── model.py
│   │   └── io.py
│   └── app/
│       └── app.py
├── notebooks/
│   ├── 01_eda_pre_segmentation.ipynb
│   └── 02_segment_analysis.ipynb
└── reports/
    └── figures/
```
