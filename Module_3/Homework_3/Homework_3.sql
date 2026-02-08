CREATE OR REPLACE EXTERNAL TABLE `de-zoomcamp-485104.demo_dataset.external_yellow_tripdata`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://de-zoomcamp-485104-bucket/yellow_tripdata_2024-*.parquet']
);

# Question 1
SELECT COUNT(*) FROM de-zoomcamp-485104.demo_dataset.external_yellow_tripdata;

CREATE OR REPLACE TABLE de-zoomcamp-485104.demo_dataset.materialized_yellow_tripdata AS
SELECT * FROM de-zoomcamp-485104.demo_dataset.external_yellow_tripdata;

# Question 2
SELECT COUNT(DISTINCT PULocationID) FROM de-zoomcamp-485104.demo_dataset.external_yellow_tripdata;
SELECT COUNT(DISTINCT PULocationID) FROM de-zoomcamp-485104.demo_dataset.materialized_yellow_tripdata;

# Question 3
SELECT PULocationID FROM de-zoomcamp-485104.demo_dataset.materialized_yellow_tripdata;
SELECT PULocationID, DOLocationID FROM de-zoomcamp-485104.demo_dataset.materialized_yellow_tripdata;

# Question 4
SELECT COUNT(*) FROM de-zoomcamp-485104.demo_dataset.external_yellow_tripdata WHERE fare_amount = 0;

# Question 5
CREATE OR REPLACE TABLE de-zoomcamp-485104.demo_dataset.yellow_tripdata_partitioned_clustered
PARTITION BY DATE(tpep_dropoff_datetime )
CLUSTER BY VendorID AS
SELECT * FROM de-zoomcamp-485104.demo_dataset.external_yellow_tripdata;

# Question 6
SELECT DISTINCT(VendorID) FROM de-zoomcamp-485104.demo_dataset.materialized_yellow_tripdata
WHERE tpep_dropoff_datetime >= '2024-03-01' AND tpep_dropoff_datetime <= '2024-03-15';

SELECT DISTINCT(VendorID) FROM de-zoomcamp-485104.demo_dataset.yellow_tripdata_partitioned_clustered
WHERE tpep_dropoff_datetime >= '2024-03-01' AND tpep_dropoff_datetime <= '2024-03-15';

# Question 9
SELECT COUNT(*) FROM de-zoomcamp-485104.demo_dataset.materialized_yellow_tripdata;
