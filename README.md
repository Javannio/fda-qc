# FDA Food Safety Inspection Data Validation & Analysis

A Python data validation and exploratory pipeline for processing, schema enforcing, and testing FDA food safety inspection datasets.

The project uses Pydantic/dataclasses for schema enforcement, automated unit testing with `pytest`, and modular scripts to ingest raw inspection logs into clean analytical data.

---

## Repository Architecture

fda-food-qc/
├── raw_data/         # Input raw FDA inspection and food sample datasets
├── results/          # Cleaned, validated, and processed output reports
├── tests/            # Automated unit and schema validation test suite
├── explore.py        # Exploratory Data Analysis (EDA) and summary metrics
├── schema.py         # Data validation rules, column types, and schema models
├── validate.py       # Pipeline execution logic for dataset validation
├── pytest.ini        # Configuration settings for pytest suite
└── LICENSE           # MIT License


---

## Core Capabilities & Workflow

1. **Schema Validation (`schema.py`):**
   * Enforces strict data types, required fields, and acceptable ranges for FDA inspection and compliance metrics.
   * Handles missing values, date formatting, and record cleaning.

2. **Data Processing Pipeline (`validate.py`):**
   * Reads raw inspection records from `raw_data/`.
   * Applies schema rules to filter out corrupt or non-compliant records.
   * Exports validated outputs to `results/`.

3. **Exploratory Analysis (`explore.py`):**
   * Computes summary statistics on compliance rates, common violations, and regional inspection breakdowns.

4. **Automated Testing (`tests/`):**
   * Unit tests covering edge cases, invalid data handling, and schema compliance.

---

##  Usage Instructions

### 1. Run the Validation Pipeline
Execute the main script to process and validate raw inspection files:

```bash
python validate.py
2. Run Exploratory Analysis
Generate summary statistics and inspect processed data:

Bash

python explore.py
3. Run Test Suite
Execute unit tests to verify schema compliance and validation logic:

Bash

pytest
License
Distributed under the MIT License.
