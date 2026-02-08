# Module 3 Homework: Data Warehouse

![BigQuery](https://img.shields.io/badge/BigQuery-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white)
![GCS](https://img.shields.io/badge/Cloud_Storage-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Airflow](https://img.shields.io/badge/Airflow-017CEE?style=for-the-badge&logo=apache-airflow&logoColor=white)

## Project Files

| File | Description |
|------|-------------|
| [`Homework_3.sql`](./Homework_3.sql) | All SQL queries for this homework |
| [`../practice/airflow/`](../practice/airflow/) | Airflow DAG for data loading |

## Dataset

**NYC Yellow Taxi Trip Data (2024)**
- Source: `https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-*.parquet`
- Loaded via Airflow DAG to GCS bucket
- External and Materialized tables in BigQuery

## Setup

**Create External Table:**
```sql
CREATE OR REPLACE EXTERNAL TABLE `de-zoomcamp-485104.demo_dataset.external_yellow_tripdata`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://de-zoomcamp-485104-bucket/yellow_tripdata_2024-*.parquet']
);
```

**Create Materialized Table:**
```sql
CREATE OR REPLACE TABLE de-zoomcamp-485104.demo_dataset.materialized_yellow_tripdata AS
SELECT * FROM de-zoomcamp-485104.demo_dataset.external_yellow_tripdata;
```

---

## Question 1: Counting Records

> What is the count of records for the 2024 Yellow Taxi Data?

- 65,623
- 840,402
- → **20,332,093**
- 85,431,289

**Query:**
```sql
SELECT COUNT(*) FROM de-zoomcamp-485104.demo_dataset.external_yellow_tripdata;
```

**Answer:** 20,332,093

---

## Question 2: Data Read Estimation

> Write a query to count the distinct number of PULocationIDs for the entire dataset on both tables. What is the estimated amount of data that will be read when this query is executed on the External Table and the Materialized Table?

- 18.82 MB for the External Table and 47.60 MB for the Materialized Table
- → **0 MB for the External Table and 155.12 MB for the Materialized Table**
- 2.14 GB for the External Table and 0MB for the Materialized Table
- 0 MB for the External Table and 0MB for the Materialized Table

**Query:**
```sql
SELECT COUNT(DISTINCT PULocationID) FROM de-zoomcamp-485104.demo_dataset.external_yellow_tripdata;
SELECT COUNT(DISTINCT PULocationID) FROM de-zoomcamp-485104.demo_dataset.materialized_yellow_tripdata;
```

**Answer:** 0 MB for the External Table and 155.12 MB for the Materialized Table

---

## Question 3: Understanding Columnar Storage

> Write a query to retrieve the PULocationID from the table (not external). Now write a query to retrieve both PULocationID and DOLocationID. Why are the estimated bytes different?

- → **BigQuery is a columnar database, and it only scans the specific columns requested in the query. Querying two columns (PULocationID, DOLocationID) requires reading more data than querying one column (PULocationID), leading to a higher estimated number of bytes processed.**
- BigQuery duplicates data across multiple storage partitions, so selecting two columns instead of one requires scanning the table twice, doubling the estimated bytes processed.
- BigQuery automatically caches the first queried column, so adding a second column increases processing time but does not affect the estimated bytes scanned.
- When selecting multiple columns, BigQuery performs an implicit join operation between them, increasing the estimated bytes processed.

**Query:**
```sql
SELECT PULocationID FROM de-zoomcamp-485104.demo_dataset.materialized_yellow_tripdata;
SELECT PULocationID, DOLocationID FROM de-zoomcamp-485104.demo_dataset.materialized_yellow_tripdata;
```

**Answer:** BigQuery is a columnar database, and it only scans the specific columns requested in the query.

---

## Question 4: Counting Zero Fare Trips

> How many records have a fare_amount of 0?

- 128,210
- 546,578
- 20,188,016
- → **8,333**

**Query:**
```sql
SELECT COUNT(*) FROM de-zoomcamp-485104.demo_dataset.external_yellow_tripdata 
WHERE fare_amount = 0;
```

**Answer:** 8,333

---

## Question 5: Partitioning and Clustering

> What is the best strategy to make an optimized table in BigQuery if your query will always filter based on tpep_dropoff_datetime and order the results by VendorID?

- → **Partition by tpep_dropoff_datetime and Cluster on VendorID**
- Cluster on tpep_dropoff_datetime and Cluster on VendorID
- Cluster on tpep_dropoff_datetime Partition by VendorID
- Partition by tpep_dropoff_datetime and Partition by VendorID

**Query:**
```sql
CREATE OR REPLACE TABLE de-zoomcamp-485104.demo_dataset.yellow_tripdata_partitioned_clustered
PARTITION BY DATE(tpep_dropoff_datetime)
CLUSTER BY VendorID AS
SELECT * FROM de-zoomcamp-485104.demo_dataset.external_yellow_tripdata;
```

**Answer:** Partition by tpep_dropoff_datetime and Cluster on VendorID

---

## Question 6: Partition Benefits

> Write a query to retrieve distinct VendorIDs between tpep_dropoff_datetime 2024-03-01 and 2024-03-15 (inclusive). Compare estimated bytes for non-partitioned vs partitioned table.

- 12.47 MB for non-partitioned table and 326.42 MB for the partitioned table
- → **310.24 MB for non-partitioned table and 26.84 MB for the partitioned table**
- 5.87 MB for non-partitioned table and 0 MB for the partitioned table
- 310.31 MB for non-partitioned table and 285.64 MB for the partitioned table

**Query:**
```sql
-- Non-partitioned (materialized)
SELECT DISTINCT(VendorID) FROM de-zoomcamp-485104.demo_dataset.materialized_yellow_tripdata
WHERE tpep_dropoff_datetime >= '2024-03-01' AND tpep_dropoff_datetime <= '2024-03-15';

-- Partitioned & Clustered
SELECT DISTINCT(VendorID) FROM de-zoomcamp-485104.demo_dataset.yellow_tripdata_partitioned_clustered
WHERE tpep_dropoff_datetime >= '2024-03-01' AND tpep_dropoff_datetime <= '2024-03-15';
```

**Answer:** 310.24 MB for non-partitioned table and 26.84 MB for the partitioned table

---

## Question 7: External Table Storage

> Where is the data stored in the External Table you created?

- Big Query
- Container Registry
- → **GCP Bucket**
- Big Table

**Answer:** GCP Bucket

---

## Question 8: Clustering Best Practices

> It is best practice in BigQuery to always cluster your data:

- True
- → **False**

**Answer:** False (Clustering is beneficial for large tables with frequent filtered queries, but adds overhead for small tables or full scans)

---

## Question 9: Understanding Table Scans (No Points)

> Write a SELECT count(*) query FROM the materialized table. How many bytes does it estimate will be read? Why?

**Query:**
```sql
SELECT COUNT(*) FROM de-zoomcamp-485104.demo_dataset.materialized_yellow_tripdata;
```

**Answer:** 0 bytes - BigQuery stores table metadata including row counts, so COUNT(*) doesn't require scanning actual data.

---

## Summary

| Question | Answer |
|----------|--------|
| Q1 | 20,332,093 |
| Q2 | 0 MB / 155.12 MB |
| Q3 | Columnar storage |
| Q4 | 8,333 |
| Q5 | Partition by datetime, Cluster by VendorID |
| Q6 | 310.24 MB / 26.84 MB |
| Q7 | GCP Bucket |
| Q8 | False |
| Q9 | 0 bytes (metadata) |
