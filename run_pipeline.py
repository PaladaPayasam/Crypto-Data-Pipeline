import sys
import logging
from datetime import datetime


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] (PipelineOrchestrator) %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

def run_crypto_pipeline():
    start_time = datetime.now()
    logging.info("==================================================")
    logging.info("STARTING PIPELINE RUN: crypto_load_job")
    logging.info("==================================================")

    
    try:
        logging.info("[Block: fetch_crypto_api] Initializing Data Loader...")
        
        
        sys.path.append(r'C:\Datalytics Centre\Crypto Analytics\crypto_pipeline\data_loaders')
        import fetch_crypto_api
        
        
        df = fetch_crypto_api.load_data_from_api()
        
        logging.info(f"[Block: fetch_crypto_api] Success! Extracted {len(df)} rows from CoinGecko API.")
    except Exception as e:
        logging.error(f"[Block: fetch_crypto_api] CRITICAL FAILED: {str(e)}")
        sys.exit(1)

   
    try:
        logging.info("[Block: load_to_bigquery] Initializing Data Exporter...")
        
        sys.path.append(r'C:\Datalytics Centre\Crypto Analytics\crypto_pipeline\data_exporters')
        import load_to_bigquery
        
       
        load_to_bigquery.export_data(df)
        
        logging.info("[Block: load_to_bigquery] Success! Target table updated smoothly.")
    except Exception as e:
        logging.error(f"[Block: load_to_bigquery] CRITICAL FAILED: {str(e)}")
        sys.exit(1)


    duration = datetime.now() - start_time
    logging.info("==================================================")
    logging.info(f"PIPELINE RUN SUCCESSFUL | Total Execution Time: {duration}")
    logging.info("==================================================")

if __name__ == "__main__":
    run_crypto_pipeline()