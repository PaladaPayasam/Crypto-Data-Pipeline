# Crypto Analytics ELT Pipeline

An automated, modular data orchestration pipeline built natively in Python to extract live market cap metrics from the CoinGecko API and load them directly into a Google BigQuery data warehouse.

## 🏗️ Architecture Overview

The pipeline utilizes a decoupled, block-based orchestration model inspired by modern data engineering tools like Mage.ai:

1. **Data Loader (Extract):** Hits the CoinGecko API asynchronously, extracts raw pricing/volume metrics for specified crypto assets, filters the matrix, and compiles a clean `pandas` DataFrame.
2. **Data Exporter (Load):** Authorizes a secure handshake with Google Cloud Platform via a Service Account, handles schema serialization, and writes the data to BigQuery using a `WRITE_TRUNCATE` design pattern for clean, idempotent re-runs.
3. **Pipeline Orchestrator:** A custom programmatic engine (`run_pipeline.py`) that manages sequential module execution, system path injections, tracking logs, and execution error handlings.

## 📁 Project Structure

```text
Crypto Analytics/
│
├── crypto_pipeline/
│   ├── data_loaders/
│   │   └── fetch_crypto_api.py     # API ingestion block
│   └── data_exporters/
│       └── load_to_bigquery.py     # BigQuery loading block
│
├── .gitignore                      # Safeguards private GCP keys and caches
├── README.md                       # Documentation
└── run_pipeline.py                 # Core orchestration execution engine