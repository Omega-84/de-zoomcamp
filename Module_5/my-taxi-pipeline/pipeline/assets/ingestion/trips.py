"""@bruin
name: ingestion.trips
type: python
connection: duckdb-default
depends:
  - ingestion.payment_lookup

materialization:
  type: table
  strategy: append

columns:
  - name: trip_id
    type: string
    description: "Composite key from pickup/dropoff times and locations"
    primary_key: true
    checks:
      - name: not_null
  - name: taxi_type
    type: string
    description: "Type of taxi: yellow or green"
    checks:
      - name: not_null
      - name: accepted_values
        value:
          - yellow
          - green
  - name: VendorID
    type: integer
    description: "TPEP/LPEP provider code. 1=Creative Mobile Technologies, 2=VeriFone Inc."
  - name: pickup_datetime
    type: timestamp
    description: "Date and time when the meter was engaged"
    checks:
      - name: not_null
  - name: dropoff_datetime
    type: timestamp
    description: "Date and time when the meter was disengaged"
  - name: passenger_count
    type: float
    description: "Number of passengers (driver-entered)"
  - name: trip_distance
    type: float
    description: "Elapsed trip distance in miles"
    checks:
      - name: non_negative
  - name: RatecodeID
    type: float
    description: "Rate code: 1=Standard, 2=JFK, 3=Newark, 4=Nassau/Westchester, 5=Negotiated, 6=Group"
  - name: store_and_fwd_flag
    type: string
    description: "Whether trip record was held in vehicle memory before sending"
  - name: PULocationID
    type: integer
    description: "TLC Taxi Zone where meter was engaged"
  - name: DOLocationID
    type: integer
    description: "TLC Taxi Zone where meter was disengaged"
  - name: payment_type
    type: integer
    description: "Payment method code: 1=Credit card, 2=Cash, 3=No charge, 4=Dispute, 5=Unknown, 6=Voided"
  - name: fare_amount
    type: float
    description: "Time-and-distance fare calculated by the meter"
  - name: extra
    type: float
    description: "Miscellaneous extras and surcharges"
  - name: mta_tax
    type: float
    description: "MTA tax automatically triggered based on metered rate"
  - name: tip_amount
    type: float
    description: "Tip amount (auto-populated for credit card tips)"
  - name: tolls_amount
    type: float
    description: "Total tolls paid in trip"
  - name: improvement_surcharge
    type: float
    description: "Improvement surcharge assessed at flag drop"
  - name: total_amount
    type: float
    description: "Total amount charged to passengers (excludes cash tips)"
  - name: congestion_surcharge
    type: float
    description: "Congestion surcharge for trips in congested zones"
  - name: airport_fee
    type: float
    description: "Airport fee for pickups/dropoffs at airports"

@bruin"""

import os
import json
import hashlib
import pandas as pd
import requests
from io import BytesIO
from datetime import datetime
from dateutil.relativedelta import relativedelta


BASE_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data"


def materialize(context=None):
    """Fetch NYC taxi trip data from TLC public endpoint for the given date range."""

    # Read date range from Bruin environment variables
    start_date_str = os.environ.get("BRUIN_START_DATE", "2022-01-01")
    end_date_str = os.environ.get("BRUIN_END_DATE", "2022-02-01")

    start_date = datetime.strptime(start_date_str[:10], "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str[:10], "%Y-%m-%d")

    # Read taxi_types variable from BRUIN_VARS
    bruin_vars = json.loads(os.environ.get("BRUIN_VARS", "{}"))
    taxi_types = bruin_vars.get("taxi_types", ["yellow"])

    print(f"Fetching taxi data from {start_date_str} to {end_date_str}")
    print(f"Taxi types: {taxi_types}")

    all_frames = []

    # Iterate over each month in the date range
    current = start_date.replace(day=1)
    while current < end_date:
        year = current.year
        month = current.month

        for taxi_type in taxi_types:
            file_name = f"{taxi_type}_tripdata_{year}-{month:02d}.parquet"
            url = f"{BASE_URL}/{file_name}"

            print(f"Downloading {url} ...")

            try:
                response = requests.get(url, timeout=120)
                response.raise_for_status()

                df = pd.read_parquet(BytesIO(response.content))
                print(f"  ✓ {file_name}: {len(df)} rows")

                # Standardize column names across yellow and green taxi types
                rename_map = {}
                if "tpep_pickup_datetime" in df.columns:
                    rename_map["tpep_pickup_datetime"] = "pickup_datetime"
                    rename_map["tpep_dropoff_datetime"] = "dropoff_datetime"
                elif "lpep_pickup_datetime" in df.columns:
                    rename_map["lpep_pickup_datetime"] = "pickup_datetime"
                    rename_map["lpep_dropoff_datetime"] = "dropoff_datetime"

                df = df.rename(columns=rename_map)

                # Add taxi_type column
                df["taxi_type"] = taxi_type

                # Generate a composite trip_id
                id_cols = ["pickup_datetime", "dropoff_datetime", "PULocationID", "DOLocationID", "fare_amount"]
                df["trip_id"] = df[id_cols].astype(str).agg("-".join, axis=1).apply(
                    lambda x: hashlib.md5(x.encode()).hexdigest()
                )

                all_frames.append(df)

            except requests.exceptions.HTTPError as e:
                print(f"  ✗ {file_name}: HTTP {e.response.status_code} - skipping")
            except Exception as e:
                print(f"  ✗ {file_name}: {e} - skipping")

        # Move to next month
        current += relativedelta(months=1)

    if not all_frames:
        print("No data fetched. Returning empty DataFrame.")
        return pd.DataFrame()

    # Combine all months/types and select standardized columns
    result = pd.concat(all_frames, ignore_index=True)

    # Select and order columns to match the asset schema
    keep_cols = [
        "trip_id", "taxi_type", "VendorID",
        "pickup_datetime", "dropoff_datetime",
        "passenger_count", "trip_distance",
        "RatecodeID", "store_and_fwd_flag",
        "PULocationID", "DOLocationID",
        "payment_type", "fare_amount", "extra",
        "mta_tax", "tip_amount", "tolls_amount",
        "improvement_surcharge", "total_amount",
        "congestion_surcharge", "airport_fee",
    ]

    # Only keep columns that actually exist in the data
    existing_cols = [c for c in keep_cols if c in result.columns]
    result = result[existing_cols]

    # Add missing columns with None so the schema is consistent
    for col in keep_cols:
        if col not in result.columns:
            result[col] = None

    result = result[keep_cols]

    print(f"\nTotal rows fetched: {len(result)}")
    return result
