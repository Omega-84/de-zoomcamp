/* @bruin

name: reports.trips_report
type: duckdb.sql

depends:
  - staging.trips

materialization:
  type: table
  strategy: time_interval
  incremental_key: pickup_date
  time_granularity: date

columns:
  - name: pickup_date
    type: date
    description: "Trip date (date part of pickup_datetime)"
    primary_key: true
    checks:
      - name: not_null
  - name: taxi_type
    type: string
    description: "Taxi type: yellow or green"
    primary_key: true
    checks:
      - name: not_null
  - name: payment_type_name
    type: string
    description: "Payment method name from lookup"
    primary_key: true
  - name: total_trips
    type: bigint
    description: "Total number of trips"
    checks:
      - name: non_negative
  - name: total_passengers
    type: float
    description: "Sum of passenger counts"
    checks:
      - name: non_negative
  - name: total_distance
    type: float
    description: "Sum of trip distances in miles"
    checks:
      - name: non_negative
  - name: total_fare
    type: float
    description: "Sum of fare amounts in USD"
  - name: total_amount
    type: float
    description: "Sum of total amounts charged"
  - name: avg_trip_distance
    type: float
    description: "Average trip distance in miles"
  - name: avg_fare
    type: float
    description: "Average fare amount in USD"
  - name: avg_tip
    type: float
    description: "Average tip amount in USD"

@bruin */

-- Reports: aggregate staging data by date, taxi_type, and payment_type
SELECT
    CAST(pickup_datetime AS DATE) AS pickup_date,
    taxi_type,
    COALESCE(payment_type_name, 'unknown') AS payment_type_name,
    COUNT(*) AS total_trips,
    COALESCE(SUM(passenger_count), 0) AS total_passengers,
    COALESCE(SUM(trip_distance), 0) AS total_distance,
    COALESCE(SUM(fare_amount), 0) AS total_fare,
    COALESCE(SUM(total_amount), 0) AS total_amount,
    AVG(trip_distance) AS avg_trip_distance,
    AVG(fare_amount) AS avg_fare,
    AVG(tip_amount) AS avg_tip
FROM staging.trips
WHERE pickup_datetime >= '{{ start_datetime }}'
  AND pickup_datetime < '{{ end_datetime }}'
GROUP BY
    CAST(pickup_datetime AS DATE),
    taxi_type,
    COALESCE(payment_type_name, 'unknown')
