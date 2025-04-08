import pandas as pd
import random
from datetime import datetime, timedelta
from google.cloud import storage, bigquery

def generate_data(n=100):
    data = {
        "transaction_id": [f"TX{random.randint(1000, 9999)}" for _ in range(n)],
        "customer_id": [f"C{random.randint(1, 50)}" for _ in range(n)],
        "amount": [round(random.uniform(10.0, 1000.0), 2) for _ in range(n)],
        "transaction_date": [(datetime.now() - timedelta(days=random.randint(1, 30))).date() for _ in range(n)]
    }
    return pd.DataFrame(data)


def upload_to_gcs(df, bucket_name):
    client = storage.Client.from_service_account_json(
        'C:/Users/avina/OneDrive/Desktop/banking-project/scripts/banking-project-456011-b80a729bb967.json'
    )
    bucket = client.bucket(bucket_name)
    blob = bucket.blob('transactions.csv')
    df.to_csv('transactions.csv', index=False)
    blob.upload_from_filename('transactions.csv')

def load_to_bigquery(bucket_name):
    client = bigquery.Client.from_service_account_json(
        'C:/Users/avina/OneDrive/Desktop/banking-project/scripts/banking-project-456011-b80a729bb967.json'
    )
    table_id = f"{client.project}.banking_data.transactions"
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        autodetect=True
    )
    uri = f"gs://{bucket_name}/transactions.csv"
    load_job = client.load_table_from_uri(uri, table_id, job_config=job_config)
    load_job.result()
    print("Data loaded into BigQuery")

if __name__ == "__main__":
    bucket_name = "banking-project-456011-raw-transactions"  # Replace with your bucket name
    df = generate_data()
    upload_to_gcs(df, bucket_name)
    load_to_bigquery(bucket_name)