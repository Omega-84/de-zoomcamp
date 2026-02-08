from airflow.decorators import dag, task
from datetime import datetime

# Import from plugin (Airflow auto-discovers plugins/ folder)
from gcs_helpers import (
    download_parquet,
    check_bucket,
    verify_upload,
    push_to_gcs,
    BUCKET_NAME,
)


@dag(
    dag_id="upload_yellow_taxi_to_gcs",
    description="Uploads yellow taxi data to GCS",
    catchup=False,
    tags=["yellow", "gcs"],
)
def upload_files():

    @task
    def ensure_bucket():
        check_bucket(BUCKET_NAME)
        return True

    @task
    def download_files(bucket_ready: bool):
        for i in range(1, 7):
            download_parquet(i)
        return True

    @task
    def upload_to_gcs(files_downloaded: bool):
        for i in range(1, 7):
            push_to_gcs(i)
        return True

    # Define task dependencies
    bucket_ready = ensure_bucket()
    files_downloaded = download_files(bucket_ready)
    upload_to_gcs(files_downloaded)


# Instantiate the DAG
upload_files()