provider "google" {
  project = var.project_id
  region  = var.region
  credentials = file("C:/Users/avina/OneDrive/Desktop/banking-project/terraform/banking-project-456011-b80a729bb967.json") # Path to your key
}

resource "google_storage_bucket" "raw_data_bucket" {
  name     = "${var.project_id}-raw-transactions"
  location = var.region
}

resource "google_bigquery_dataset" "banking_dataset" {
  dataset_id = "banking_data"
  location   = var.region
}

resource "google_bigquery_table" "transactions_table" {
  dataset_id = google_bigquery_dataset.banking_dataset.dataset_id
  table_id   = "transactions"
  schema     = <<EOF
[
  {"name": "transaction_id", "type": "STRING"},
  {"name": "customer_id", "type": "STRING"},
  {"name": "amount", "type": "FLOAT"},
  {"name": "transaction_date", "type": "DATE"}
]
EOF
}