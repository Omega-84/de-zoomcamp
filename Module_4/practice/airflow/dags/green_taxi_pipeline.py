from airflow.decorators import dag, task
from datetime import datetime
from pendulum import timezone

from taxi_helpers import (
    download_file,
    check_bucket,
    push_to_gcs,
    create_green_tables,
    BUCKET_NAME,
)

EST = timezone("America/New_York")


@dag(
    dag_id="green_taxi_pipeline",
    description="Downloads green taxi CSV data, uploads to GCS, and creates BigQuery tables",
    schedule="0 9 1 * *",  # 1st of every month at 9 AM EST
    start_date=datetime(2019, 1, 1, tzinfo=EST),
    catchup=False,
    max_active_runs=1,
    tags=["green", "gcs", "bigquery"],
)
def green_taxi_pipeline():

    @task
    def ensure_bucket():
        """Ensure the GCS bucket exists."""
        check_bucket(BUCKET_NAME)
        return True

    @task
    def upload_to_gcs(bucket_ready: bool, **context):
        """Download green taxi file and upload to GCS for this execution month."""
        execution_date = context["data_interval_start"]
        year = execution_date.year
        month = execution_date.month
        print(f"Processing green taxi data for {year}-{month:02d}")

        if not push_to_gcs("green", month, year):
            raise Exception(f"Failed to upload green taxi data for {year}-{month:02d}")
        return True

    @task
    def create_bq_tables(upload_done: bool, **context):
        """Create BigQuery external table, tmp table, and merge into master."""
        execution_date = context["data_interval_start"]
        year = execution_date.year
        month = execution_date.month
        print(f"Creating BQ tables for green taxi {year}-{month:02d}")

        if not create_green_tables(year, month):
            raise Exception(f"Failed to create BQ tables for green taxi {year}-{month:02d}")
        return True

    # Task dependencies
    bucket_ready = ensure_bucket()
    upload_done = upload_to_gcs(bucket_ready)
    create_bq_tables(upload_done)


# Instantiate the DAG
green_taxi_pipeline()
