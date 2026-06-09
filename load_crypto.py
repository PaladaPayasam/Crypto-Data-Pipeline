import os
from google.cloud import bigquery
from extract_crypto import fetch_crypto_data

PROJECT_ID ="de-zero-to-hero"
DATASET_ID="crypto_dw"
TABLE_ID="raw_market_data"
CREDS_FILE="google_creds.json"

def load_data_to_bigquery():
    
    print("Loading data to BigQuery...")
    if not os.path.exists(CREDS_FILE):
        print(f"Credentials file {CREDS_FILE} not found.")
        return
    client = bigquery.Client.from_service_account_json(CREDS_FILE, project=PROJECT_ID)
    
    df=fetch_crypto_data()
    if df is None or df.empty:
        print("No data to load.")
        return

    dataset_ref=client.dataset(DATASET_ID)
    
    try:
        client.get_dataset(dataset_ref)
        print(f"Dataset {DATASET_ID} already exists.")
    except Exception:
        print(f"Dataset {DATASET_ID} not found. Creating dataset...")
        dataset=bigquery.Dataset(dataset_ref)
        dataset.location="asia-south1"
        client.create_dataset(dataset)
        print(f"Dataset {DATASET_ID} created.")
    
    job_config=bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND,)
    
    table_ref=dataset_ref.table(TABLE_ID)
    print(f"Loading {len(df)} rows into {PROJECT_ID}.{DATASET_ID}.{TABLE_ID}...")
    
    try:
        job = client.load_table_from_dataframe(df, table_ref, job_config=job_config)
        job.result()
        print("Data loaded successfully.")
    except Exception as e:
        print(f"Error loading data: {e}")
        return
    
if __name__ == "__main__":
    load_data_to_bigquery()
    