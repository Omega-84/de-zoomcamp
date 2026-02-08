import os
import urllib.request
from google.cloud import storage
from google.api_core.exceptions import Forbidden
import time

# Configuration
BASE_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-"
MONTHS = [f"{i:02d}" for i in range(1, 7)]
DOWNLOAD_DIR = "/tmp"
CHUNK_SIZE = 8 * 1024 * 1024
BUCKET_NAME = 'de-zoomcamp-485104-bucket'
CREDENTIALS_FILE = "/opt/airflow/keys/service-account.json"


def get_client() -> storage.Client:
    """Get authenticated GCS client."""
    return storage.Client.from_service_account_json(CREDENTIALS_FILE)


def download_parquet(month: int) -> str | None:
    """Download parquet file for given month (1-indexed)."""
    url = f"{BASE_URL}{MONTHS[month-1]}.parquet"
    file_path = os.path.join(DOWNLOAD_DIR, f"yellow_tripdata_2024-{MONTHS[month-1]}.parquet")
    try:
        urllib.request.urlretrieve(url, file_path)
        print(f"Downloaded: {file_path}")
        return file_path
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return None


def check_bucket(bucket_name: str) -> bool:
    """Check if bucket exists, create if not."""
    client = get_client()
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


def verify_upload(month: int) -> bool:
    """Check if file exists in bucket."""
    client = get_client()
    blob_name = f"yellow_tripdata_2024-{MONTHS[month-1]}.parquet"
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(blob_name)
    return blob.exists()


def push_to_gcs(month: int, max_retries: int = 3) -> bool:
    """Upload parquet file to GCS bucket. Returns True if successful."""
    client = get_client()
    blob_name = f"yellow_tripdata_2024-{MONTHS[month-1]}.parquet"
    file_path = os.path.join(DOWNLOAD_DIR, blob_name)
    
    # 1. Check if file already exists in bucket
    if verify_upload(month):
        print(f"Blob - {blob_name} already exists in bucket. Skipping.")
        # Clean up local file if it exists
        if os.path.exists(file_path):
            os.remove(file_path)
        return True
    
    # 2. Ensure local file exists (download if needed)
    if not os.path.exists(file_path):
        print(f"File {blob_name} not found locally. Downloading...")
        if download_parquet(month) is None:
            print(f"Failed to download {blob_name}. Aborting.")
            return False
    
    # 3. Ensure bucket exists
    if not check_bucket(BUCKET_NAME):
        return False
    
    # 4. Upload with retries
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(blob_name)
    blob.chunk_size = CHUNK_SIZE
    
    for attempt in range(1, max_retries + 1):
        try:
            print(f"Uploading {blob_name} (attempt {attempt}/{max_retries})...")
            blob.upload_from_filename(file_path)
            
            # Verify upload succeeded
            if verify_upload(month):
                print(f"✓ {blob_name} uploaded successfully.")
                os.remove(file_path)
                return True
            else:
                print(f"Verification failed for {blob_name}.")
                
        except Exception as e:
            print(f"Upload error for {blob_name}: {e}")
        
        if attempt < max_retries:
            print(f"Retrying in 5 seconds...")
            time.sleep(5)
    
    print(f"✗ Failed to upload {blob_name} after {max_retries} attempts.")
    return False
