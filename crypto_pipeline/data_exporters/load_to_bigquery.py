from mage_ai.data_preparation.decorators import data_exporter
from google.cloud import bigquery
import os

@data_exporter
def export_data(df, *args, **kwargs):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Datalytics Centre\Crypto Analytics\google_creds.json"
    
    client = bigquery.Client()
    table_id = "de-zero-to-hero.crypto_dw.raw_market_data"
    
    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_TRUNCATE"
    )
    
    print("Mage running: Shipping data to BigQuery...")
    job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
    job.result()
    print("Success! Data loaded cleanly via programmatic orchestrator.")