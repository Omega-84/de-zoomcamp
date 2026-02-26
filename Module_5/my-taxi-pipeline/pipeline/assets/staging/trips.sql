/* @bruin

name: staging.trips
type: duckdb.sql

depends:
  - ingestion.trips
  - ingestion.payment_lookup

materialization:
  type: table
  strategy: time_interval
  incremental_key: pickup_datetime
  time_granularity: timestamp

columns:
  - name: trip_id
    type: string
    description: "Unique trip identifier (MD5 hash of composite key)"
    primary_key: true
    nullable: false
    checks:
      - name: not_null
  - name: taxi_type
    type: string
    description: "Taxi type: yellow or green"
    primary_key: true
    checks:
      - name: not_null
  - name: pickup_datetime
    type: timestamp
    description: "When the trip started"
    primary_key: true
    checks:
      - name: not_null
  - name: dropoff_datetime
    type: timestamp
    description: "When the trip ended"
  - name: pu_location_id
    type: integer
    description: "Pickup TLC Taxi Zone ID"
  - name: do_location_id
    type: integer
    description: "Dropoff TLC Taxi Zone ID"
  - name: passenger_count
    type: float
    description: "Number of passengers"
  - name: trip_distance
    type: float
    description: "Trip distance in miles"
    checks:
      - name: non_negative
  - name: fare_amount
    type: float
    description: "Meter fare in USD"
  - name: total_amount
    type: float
    description: "Total charged to passenger"
  - name: payment_type
    type: integer
    description: "Payment method code"
  - name: payment_type_name
    type: string
    description: "Human-readable payment method from lookup"

custom_checks:
  - name: no_duplicate_trips
    description: "Ensure no duplicate trip_id values exist in the time window"
    query: |
      SELECT COUNT(*) - COUNT(DISTINCT trip_id)
      FROM staging.trips
    value: 0

@bruin */

-- Staging: clean, deduplicate, and enrich raw trip data
WITH deduplicated AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY trip_id, taxi_type
            ORDER BY pickup_datetime
        ) AS row_num
    FROM ingestion.trips
    WHERE pickup_datetime >= '{{ start_datetime }}'
      AND pickup_datetime < '{{ end_datetime }}'
      AND pickup_datetime IS NOT NULL
      AND trip_distance >= 0
)

SELECT
    d.trip_id,
    d.taxi_type,
    d.vendor_id,
    d.pickup_datetime,
    d.dropoff_datetime,
    d.passenger_count,
    d.trip_distance,
    d.ratecode_id,
    d.store_and_fwd_flag,
    d.pu_location_id,
    d.do_location_id,
    d.payment_type,
    p.payment_type_name,
    d.fare_amount,
    d.extra,
    d.mta_tax,
    d.tip_amount,
    d.tolls_amount,
    d.improvement_surcharge,
    d.total_amount,
    d.congestion_surcharge,
    d.airport_fee
FROM deduplicated d
LEFT JOIN ingestion.payment_lookup p
    ON d.payment_type = p.payment_type_id
WHERE d.row_num = 1
