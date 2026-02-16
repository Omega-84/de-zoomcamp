import os
import requests
from datetime import datetime
from google.cloud import storage, bigquery
from google.api_core.exceptions import Forbidden
import time

# Configuration
BASE_URL = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download"
DOWNLOAD_DIR = "/tmp"
CHUNK_SIZE = 8 * 1024 * 1024
PROJECT_ID = "de-zoomcamp-485104"
BUCKET_NAME = "de-zoomcamp-485104-bucket"
DATASET_NAME = "demo_dataset"
CREDENTIALS_FILE = "/opt/airflow/keys/service-account.json"


def get_gcs_client() -> storage.Client:
    """Get authenticated GCS client."""
    return storage.Client.from_service_account_json(CREDENTIALS_FILE)


def get_bq_client() -> bigquery.Client:
    """Get authenticated BigQuery client."""
    return bigquery.Client.from_service_account_json(CREDENTIALS_FILE)


def download_file(taxi: str, month: int, year: int) -> bool:
    """Download CSV gz file for given taxi type, month, and year."""
    file_name = f"{taxi}_tripdata_{datetime(year, month, 1).strftime('%Y-%m')}.csv.gz"
    url = f"{BASE_URL}/{taxi}/{file_name}"
    file_path = os.path.join(DOWNLOAD_DIR, file_name)
    try:
        response = requests.get(url)
        response.raise_for_status()

        with open(file_path, "wb") as f:
            f.write(response.content)
        print(f"Successfully downloaded '{file_name}'")
        return True

    except requests.exceptions.RequestException as e:
        print(f"Error during download: {e}")
        return False


def check_bucket(bucket_name: str) -> bool:
    """Check if bucket exists, create if not."""
    client = get_gcs_client()
    all_buckets = [b.id for b in client.list_buckets()]
    if bucket_name in all_buckets:
        print(f"Bucket - {bucket_name} already exists.")
        return True
    try:
        client.create_bucket(bucket_name)
        print(f"Created bucket '{bucket_name}'")
        return True
    except Forbidden:
        print(f"Bucket name already taken. Please try with a different name.")
        return False


def verify_upload(taxi: str, month: int, year: int) -> bool:
    """Check if file exists in bucket."""
    client = get_gcs_client()
    file_name = f"{taxi}_tripdata_{datetime(year, month, 1).strftime('%Y-%m')}.csv.gz"
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(file_name)
    return blob.exists()


def push_to_gcs(taxi: str, month: int, year: int, max_retries: int = 3) -> bool:
    """Upload file to GCS bucket. Returns True if successful."""
    file_name = f"{taxi}_tripdata_{datetime(year, month, 1).strftime('%Y-%m')}.csv.gz"
    file_path = os.path.join(DOWNLOAD_DIR, file_name)

    # 1. Check if file already exists in bucket
    if verify_upload(taxi, month, year):
        print(f"Blob - {file_name} already exists in bucket. Skipping.")
        if os.path.exists(file_path):
            os.remove(file_path)
        return True

    # 2. Ensure local file exists (download if needed)
    if not os.path.exists(file_path):
        print(f"File {file_name} not found locally. Downloading...")
        if not download_file(taxi, month, year):
            print(f"Failed to download {file_name}. Aborting.")
            return False

    # 3. Ensure bucket exists
    if not check_bucket(BUCKET_NAME):
        return False

    # 4. Upload with retries
    client = get_gcs_client()
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(file_name)
    blob.chunk_size = CHUNK_SIZE

    for attempt in range(1, max_retries + 1):
        try:
            print(f"Uploading {file_name} (attempt {attempt}/{max_retries})...")
            blob.upload_from_filename(file_path)

            if verify_upload(taxi, month, year):
                print(f"✓ {file_name} uploaded successfully.")
                os.remove(file_path)
                return True
            else:
                print(f"Verification failed for {file_name}.")

        except Exception as e:
            print(f"Upload error for {file_name}: {e}")

        if attempt < max_retries:
            print("Retrying in 5 seconds...")
            time.sleep(5)

    print(f"✗ Failed to upload {file_name} after {max_retries} attempts.")
    return False


# ─────────────────────────────────────────────────────────────────────────────
# BigQuery Table Creation
# ─────────────────────────────────────────────────────────────────────────────

def create_green_tables(year: int, month: int) -> bool:
    """Create BQ tables for green taxi data: master → external → tmp → merge."""
    bq_client = get_bq_client()
    file_name = f"green_tripdata_{datetime(year, month, 1).strftime('%Y-%m')}.csv.gz"
    dataset_id = f"{PROJECT_ID}.{DATASET_NAME}"
    master_table = f"{dataset_id}.green_tripdata"
    tmp_table = f"{dataset_id}.green_tripdata_{datetime(year, month, 1).strftime('%Y-%m')}"
    ext_table = f"{tmp_table}_ext"

    # 1. Create master table (if not exists)
    master_table_query = f"""
        CREATE TABLE IF NOT EXISTS `{master_table}`
        (
            unique_row_id BYTES OPTIONS (description = 'A unique identifier for the trip, generated by hashing key trip attributes.'),
            filename STRING OPTIONS (description = 'The source filename from which the trip data was loaded.'),
            VendorID STRING OPTIONS (description = 'A code indicating the LPEP provider that provided the record. 1= Creative Mobile Technologies, LLC; 2= VeriFone Inc.'),
            lpep_pickup_datetime TIMESTAMP OPTIONS (description = 'The date and time when the meter was engaged'),
            lpep_dropoff_datetime TIMESTAMP OPTIONS (description = 'The date and time when the meter was disengaged'),
            store_and_fwd_flag STRING OPTIONS (description = 'This flag indicates whether the trip record was held in vehicle memory before sending to the vendor'),
            RatecodeID STRING OPTIONS (description = 'The final rate code in effect at the end of the trip. 1= Standard rate 2=JFK 3=Newark 4=Nassau or Westchester 5=Negotiated fare 6=Group ride'),
            PULocationID STRING OPTIONS (description = 'TLC Taxi Zone in which the taximeter was engaged'),
            DOLocationID STRING OPTIONS (description = 'TLC Taxi Zone in which the taximeter was disengaged'),
            passenger_count INT64 OPTIONS (description = 'The number of passengers in the vehicle. This is a driver-entered value.'),
            trip_distance NUMERIC OPTIONS (description = 'The elapsed trip distance in miles reported by the taximeter.'),
            fare_amount NUMERIC OPTIONS (description = 'The time-and-distance fare calculated by the meter'),
            extra NUMERIC OPTIONS (description = 'Miscellaneous extras and surcharges'),
            mta_tax NUMERIC OPTIONS (description = '$0.50 MTA tax that is automatically triggered based on the metered rate in use'),
            tip_amount NUMERIC OPTIONS (description = 'Tip amount. This field is automatically populated for credit card tips. Cash tips are not included.'),
            tolls_amount NUMERIC OPTIONS (description = 'Total amount of all tolls paid in trip.'),
            ehail_fee NUMERIC,
            improvement_surcharge NUMERIC OPTIONS (description = '$0.30 improvement surcharge assessed on hailed trips at the flag drop.'),
            total_amount NUMERIC OPTIONS (description = 'The total amount charged to passengers. Does not include cash tips.'),
            payment_type INTEGER OPTIONS (description = 'A numeric code signifying how the passenger paid for the trip. 1= Credit card 2= Cash 3= No charge 4= Dispute 5= Unknown 6= Voided trip'),
            trip_type STRING OPTIONS (description = 'A code indicating whether the trip was a street-hail or a dispatch. 1= Street-hail 2= Dispatch'),
            congestion_surcharge NUMERIC OPTIONS (description = 'Congestion surcharge applied to trips in congested zones')
        )
        PARTITION BY DATE(lpep_pickup_datetime);
    """

    print("Step 1: Creating master table...")
    bq_client.query(master_table_query).result()
    print(f"✓ Master table `{master_table}` ready.")

    # 2. Create external table for this month/year
    ext_table_query = f"""
        CREATE OR REPLACE EXTERNAL TABLE `{ext_table}`
        (
            VendorID STRING OPTIONS (description = 'A code indicating the LPEP provider that provided the record. 1= Creative Mobile Technologies, LLC; 2= VeriFone Inc.'),
            lpep_pickup_datetime TIMESTAMP OPTIONS (description = 'The date and time when the meter was engaged'),
            lpep_dropoff_datetime TIMESTAMP OPTIONS (description = 'The date and time when the meter was disengaged'),
            store_and_fwd_flag STRING OPTIONS (description = 'This flag indicates whether the trip record was held in vehicle memory before sending to the vendor'),
            RatecodeID STRING OPTIONS (description = 'The final rate code in effect at the end of the trip. 1= Standard rate 2=JFK 3=Newark 4=Nassau or Westchester 5=Negotiated fare 6=Group ride'),
            PULocationID STRING OPTIONS (description = 'TLC Taxi Zone in which the taximeter was engaged'),
            DOLocationID STRING OPTIONS (description = 'TLC Taxi Zone in which the taximeter was disengaged'),
            passenger_count INT64 OPTIONS (description = 'The number of passengers in the vehicle. This is a driver-entered value.'),
            trip_distance NUMERIC OPTIONS (description = 'The elapsed trip distance in miles reported by the taximeter.'),
            fare_amount NUMERIC OPTIONS (description = 'The time-and-distance fare calculated by the meter'),
            extra NUMERIC OPTIONS (description = 'Miscellaneous extras and surcharges'),
            mta_tax NUMERIC OPTIONS (description = '$0.50 MTA tax that is automatically triggered based on the metered rate in use'),
            tip_amount NUMERIC OPTIONS (description = 'Tip amount. This field is automatically populated for credit card tips. Cash tips are not included.'),
            tolls_amount NUMERIC OPTIONS (description = 'Total amount of all tolls paid in trip.'),
            ehail_fee NUMERIC,
            improvement_surcharge NUMERIC OPTIONS (description = '$0.30 improvement surcharge assessed on hailed trips at the flag drop.'),
            total_amount NUMERIC OPTIONS (description = 'The total amount charged to passengers. Does not include cash tips.'),
            payment_type INTEGER OPTIONS (description = 'A numeric code signifying how the passenger paid for the trip. 1= Credit card 2= Cash 3= No charge 4= Dispute 5= Unknown 6= Voided trip'),
            trip_type STRING OPTIONS (description = 'A code indicating whether the trip was a street-hail or a dispatch. 1= Street-hail 2= Dispatch'),
            congestion_surcharge NUMERIC OPTIONS (description = 'Congestion surcharge applied to trips in congested zones')
        )
        OPTIONS (
            format = 'CSV',
            uris = ['gs://{BUCKET_NAME}/{file_name}'],
            skip_leading_rows = 1,
            ignore_unknown_values = TRUE
        );
    """

    print("Step 2: Creating external table...")
    bq_client.query(ext_table_query).result()
    print(f"✓ External table `{ext_table}` ready.")

    # 3. Create tmp table with unique_row_id and filename
    tmp_table_query = f"""
        CREATE OR REPLACE TABLE `{tmp_table}`
        AS
        SELECT
            MD5(CONCAT(
                COALESCE(CAST(VendorID AS STRING), ''),
                COALESCE(CAST(lpep_pickup_datetime AS STRING), ''),
                COALESCE(CAST(lpep_dropoff_datetime AS STRING), ''),
                COALESCE(CAST(PULocationID AS STRING), ''),
                COALESCE(CAST(DOLocationID AS STRING), '')
            )) AS unique_row_id,
            '{file_name}' AS filename,
            *
        FROM `{ext_table}`;
    """

    print("Step 3: Creating tmp table...")
    bq_client.query(tmp_table_query).result()
    print(f"✓ Tmp table `{tmp_table}` ready.")

    # 4. Merge tmp into master
    merge_query = f"""
        MERGE INTO `{master_table}` T
        USING `{tmp_table}` S
        ON T.unique_row_id = S.unique_row_id
        WHEN NOT MATCHED THEN
            INSERT (unique_row_id, filename, VendorID, lpep_pickup_datetime, lpep_dropoff_datetime, store_and_fwd_flag, RatecodeID, PULocationID, DOLocationID, passenger_count, trip_distance, fare_amount, extra, mta_tax, tip_amount, tolls_amount, ehail_fee, improvement_surcharge, total_amount, payment_type, trip_type, congestion_surcharge)
            VALUES (S.unique_row_id, S.filename, S.VendorID, S.lpep_pickup_datetime, S.lpep_dropoff_datetime, S.store_and_fwd_flag, S.RatecodeID, S.PULocationID, S.DOLocationID, S.passenger_count, S.trip_distance, S.fare_amount, S.extra, S.mta_tax, S.tip_amount, S.tolls_amount, S.ehail_fee, S.improvement_surcharge, S.total_amount, S.payment_type, S.trip_type, S.congestion_surcharge);
    """

    print("Step 4: Merging into master table...")
    bq_client.query(merge_query).result()
    print(f"✓ Merged `{tmp_table}` into `{master_table}`.")

    return True


def create_yellow_tables(year: int, month: int) -> bool:
    """Create BQ tables for yellow taxi data: master → external → tmp → merge."""
    bq_client = get_bq_client()
    file_name = f"yellow_tripdata_{datetime(year, month, 1).strftime('%Y-%m')}.csv.gz"
    dataset_id = f"{PROJECT_ID}.{DATASET_NAME}"
    master_table = f"{dataset_id}.yellow_tripdata"
    tmp_table = f"{dataset_id}.yellow_tripdata_{datetime(year, month, 1).strftime('%Y-%m')}"
    ext_table = f"{tmp_table}_ext"

    # 1. Create master table (if not exists)
    master_table_query = f"""
        CREATE TABLE IF NOT EXISTS `{master_table}`
        (
            unique_row_id BYTES OPTIONS (description = 'A unique identifier for the trip, generated by hashing key trip attributes.'),
            filename STRING OPTIONS (description = 'The source filename from which the trip data was loaded.'),
            VendorID STRING OPTIONS (description = 'A code indicating the TPEP provider that provided the record. 1= Creative Mobile Technologies, LLC; 2= VeriFone Inc.'),
            tpep_pickup_datetime TIMESTAMP OPTIONS (description = 'The date and time when the meter was engaged'),
            tpep_dropoff_datetime TIMESTAMP OPTIONS (description = 'The date and time when the meter was disengaged'),
            passenger_count INTEGER OPTIONS (description = 'The number of passengers in the vehicle. This is a driver-entered value.'),
            trip_distance NUMERIC OPTIONS (description = 'The elapsed trip distance in miles reported by the taximeter.'),
            RatecodeID STRING OPTIONS (description = 'The final rate code in effect at the end of the trip. 1= Standard rate 2=JFK 3=Newark 4=Nassau or Westchester 5=Negotiated fare 6=Group ride'),
            store_and_fwd_flag STRING OPTIONS (description = 'This flag indicates whether the trip record was held in vehicle memory before sending to the vendor. TRUE = store and forward trip, FALSE = not a store and forward trip'),
            PULocationID STRING OPTIONS (description = 'TLC Taxi Zone in which the taximeter was engaged'),
            DOLocationID STRING OPTIONS (description = 'TLC Taxi Zone in which the taximeter was disengaged'),
            payment_type INTEGER OPTIONS (description = 'A numeric code signifying how the passenger paid for the trip. 1= Credit card 2= Cash 3= No charge 4= Dispute 5= Unknown 6= Voided trip'),
            fare_amount NUMERIC OPTIONS (description = 'The time-and-distance fare calculated by the meter'),
            extra NUMERIC OPTIONS (description = 'Miscellaneous extras and surcharges. Currently, this only includes the $0.50 and $1 rush hour and overnight charges'),
            mta_tax NUMERIC OPTIONS (description = '$0.50 MTA tax that is automatically triggered based on the metered rate in use'),
            tip_amount NUMERIC OPTIONS (description = 'Tip amount. This field is automatically populated for credit card tips. Cash tips are not included.'),
            tolls_amount NUMERIC OPTIONS (description = 'Total amount of all tolls paid in trip.'),
            improvement_surcharge NUMERIC OPTIONS (description = '$0.30 improvement surcharge assessed on hailed trips at the flag drop. The improvement surcharge began being levied in 2015.'),
            total_amount NUMERIC OPTIONS (description = 'The total amount charged to passengers. Does not include cash tips.'),
            congestion_surcharge NUMERIC OPTIONS (description = 'Congestion surcharge applied to trips in congested zones')
        )
        PARTITION BY DATE(tpep_pickup_datetime);
    """

    print("Step 1: Creating master table...")
    bq_client.query(master_table_query).result()
    print(f"✓ Master table `{master_table}` ready.")

    # 2. Create external table for this month/year
    ext_table_query = f"""
        CREATE OR REPLACE EXTERNAL TABLE `{ext_table}`
        (
            VendorID STRING OPTIONS (description = 'A code indicating the TPEP provider that provided the record. 1= Creative Mobile Technologies, LLC; 2= VeriFone Inc.'),
            tpep_pickup_datetime TIMESTAMP OPTIONS (description = 'The date and time when the meter was engaged'),
            tpep_dropoff_datetime TIMESTAMP OPTIONS (description = 'The date and time when the meter was disengaged'),
            passenger_count INTEGER OPTIONS (description = 'The number of passengers in the vehicle. This is a driver-entered value.'),
            trip_distance NUMERIC OPTIONS (description = 'The elapsed trip distance in miles reported by the taximeter.'),
            RatecodeID STRING OPTIONS (description = 'The final rate code in effect at the end of the trip. 1= Standard rate 2=JFK 3=Newark 4=Nassau or Westchester 5=Negotiated fare 6=Group ride'),
            store_and_fwd_flag STRING OPTIONS (description = 'This flag indicates whether the trip record was held in vehicle memory before sending to the vendor. TRUE = store and forward trip, FALSE = not a store and forward trip'),
            PULocationID STRING OPTIONS (description = 'TLC Taxi Zone in which the taximeter was engaged'),
            DOLocationID STRING OPTIONS (description = 'TLC Taxi Zone in which the taximeter was disengaged'),
            payment_type INTEGER OPTIONS (description = 'A numeric code signifying how the passenger paid for the trip. 1= Credit card 2= Cash 3= No charge 4= Dispute 5= Unknown 6= Voided trip'),
            fare_amount NUMERIC OPTIONS (description = 'The time-and-distance fare calculated by the meter'),
            extra NUMERIC OPTIONS (description = 'Miscellaneous extras and surcharges. Currently, this only includes the $0.50 and $1 rush hour and overnight charges'),
            mta_tax NUMERIC OPTIONS (description = '$0.50 MTA tax that is automatically triggered based on the metered rate in use'),
            tip_amount NUMERIC OPTIONS (description = 'Tip amount. This field is automatically populated for credit card tips. Cash tips are not included.'),
            tolls_amount NUMERIC OPTIONS (description = 'Total amount of all tolls paid in trip.'),
            improvement_surcharge NUMERIC OPTIONS (description = '$0.30 improvement surcharge assessed on hailed trips at the flag drop. The improvement surcharge began being levied in 2015.'),
            total_amount NUMERIC OPTIONS (description = 'The total amount charged to passengers. Does not include cash tips.'),
            congestion_surcharge NUMERIC OPTIONS (description = 'Congestion surcharge applied to trips in congested zones')
        )
        OPTIONS (
            format = 'CSV',
            uris = ['gs://{BUCKET_NAME}/{file_name}'],
            skip_leading_rows = 1,
            ignore_unknown_values = TRUE
        );
    """

    print("Step 2: Creating external table...")
    bq_client.query(ext_table_query).result()
    print(f"✓ External table `{ext_table}` ready.")

    # 3. Create tmp table with unique_row_id and filename
    tmp_table_query = f"""
        CREATE OR REPLACE TABLE `{tmp_table}`
        AS
        SELECT
            MD5(CONCAT(
                COALESCE(CAST(VendorID AS STRING), ''),
                COALESCE(CAST(tpep_pickup_datetime AS STRING), ''),
                COALESCE(CAST(tpep_dropoff_datetime AS STRING), ''),
                COALESCE(CAST(PULocationID AS STRING), ''),
                COALESCE(CAST(DOLocationID AS STRING), '')
            )) AS unique_row_id,
            '{file_name}' AS filename,
            *
        FROM `{ext_table}`;
    """

    print("Step 3: Creating tmp table...")
    bq_client.query(tmp_table_query).result()
    print(f"✓ Tmp table `{tmp_table}` ready.")

    # 4. Merge tmp into master
    merge_query = f"""
        MERGE INTO `{master_table}` T
        USING `{tmp_table}` S
        ON T.unique_row_id = S.unique_row_id
        WHEN NOT MATCHED THEN
            INSERT (unique_row_id, filename, VendorID, tpep_pickup_datetime, tpep_dropoff_datetime, passenger_count, trip_distance, RatecodeID, store_and_fwd_flag, PULocationID, DOLocationID, payment_type, fare_amount, extra, mta_tax, tip_amount, tolls_amount, improvement_surcharge, total_amount, congestion_surcharge)
            VALUES (S.unique_row_id, S.filename, S.VendorID, S.tpep_pickup_datetime, S.tpep_dropoff_datetime, S.passenger_count, S.trip_distance, S.RatecodeID, S.store_and_fwd_flag, S.PULocationID, S.DOLocationID, S.payment_type, S.fare_amount, S.extra, S.mta_tax, S.tip_amount, S.tolls_amount, S.improvement_surcharge, S.total_amount, S.congestion_surcharge);
    """

    print("Step 4: Merging into master table...")
    bq_client.query(merge_query).result()
    print(f"✓ Merged `{tmp_table}` into `{master_table}`.")

    return True
