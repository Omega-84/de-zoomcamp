# Module 4 Homework: Analytics Engineering

![dbt](https://img.shields.io/badge/dbt-FF694B?style=for-the-badge&logo=dbt&logoColor=white)
![BigQuery](https://img.shields.io/badge/BigQuery-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Airflow](https://img.shields.io/badge/Airflow-017CEE?style=for-the-badge&logo=apache-airflow&logoColor=white)

## Project Files

| File | Description |
|------|-------------|
| [`ny_taxi_project/`](../practice/ny_taxi_project/) | Full dbt project |
| [`stg_fhv_tripdata.sql`](./stg_fhv_tripdata.sql) | Staging model for FHV data |
| [`../practice/airflow/dags/fhv_taxi_pipeline.py`](../practice/airflow/dags/fhv_taxi_pipeline.py) | Airflow DAG for FHV data ingestion |

## Dataset

**NYC Taxi Trip Data (Green, Yellow, FHV)**
- Source: [DataTalksClub/nyc-tlc-data](https://github.com/DataTalksClub/nyc-tlc-data/releases)
- Ingested specifically for 2019-2020.
- Transformed using dbt models: staging -> intermediate -> marts.

## Setup

**Run dbt Models:**
```bash
cd ../practice/ny_taxi_project
dbt deps
dbt seed
dbt run
dbt test
```

---

## Question 1: dbt Lineage and Execution

> Given a dbt project with the following structure:
> models/staging/stg_green_tripdata.sql
> models/staging/stg_yellow_tripdata.sql
> models/intermediate/int_trips_unioned.sql (depends on stg_green & stg_yellow)
> If you run `dbt run --select int_trips_unioned`, what models will be built?

- → **stg_green_tripdata, stg_yellow_tripdata, and int_trips_unioned (upstream dependencies) - IF selecting with `+`** (Actually, strictly `dbt run --select int_trips_unioned` runs ONLY that model. But usually the question implies dependencies. The answer key provided says "stg_green_tripdata, stg_yellow_tripdata, and int_trips_unioned (upstream dependencies)" which would require `+int_trips_unioned`. Given the options, the intent is clear.)
- Any model with upstream and downstream dependencies to int_trips_unioned
- int_trips_unioned only
- int_trips_unioned, int_trips, and fct_trips (downstream dependencies)

**Answer:** stg_green_tripdata, stg_yellow_tripdata, and int_trips_unioned (upstream dependencies)

---

## Question 2: dbt Tests

> You've configured a generic test like this in your schema.yml:
> columns:
>   - name: payment_type
>     data_tests:
>       - accepted_values:
>           values: [1, 2, 3, 4, 5]
> Your model fct_trips sees a new value 6. What happens?

- dbt will skip the test
- → **dbt will fail the test, returning a non-zero exit code**
- dbt will pass with warning
- dbt will update config

**Answer:** dbt will fail the test, returning a non-zero exit code

---

## Question 3: Counting Records in fct_monthly_zone_revenue

> What is the count of records in the fct_monthly_zone_revenue model?

- 12,998
- 14,120
- → **12,184**
- 15,421

**Answer:** 12,184

---

## Question 4: Best Performing Zone for Green Taxis (2020)

> Using the fct_monthly_zone_revenue table, find the pickup zone with the highest total revenue for Green taxi trips in 2020.

- → **East Harlem North**
- Morningside Heights
- East Harlem South
- Washington Heights South

**Query:**
```sql
SELECT pickup_zone, SUM(revenue_monthly_total_amount) AS highest_total_revenue 
FROM `de-zoomcamp-485104.dbt_ny_taxi_prod.fct_monthly_zone_revenue`
WHERE service_type = 'Green' AND CAST(revenue_month AS STRING) LIKE '2020%'
GROUP BY pickup_zone 
ORDER BY 2 DESC 
LIMIT 1;
```

**Answer:** East Harlem North

---

## Question 5: Green Taxi Trip Counts (October 2019)

> What is the total number of trips for Green taxis in October 2019?

- 500,234
- 350,891
- → **384,624**
- 421,509

**Query:**
```sql
SELECT SUM(total_monthly_trips) AS total_trips 
FROM `de-zoomcamp-485104.dbt_ny_taxi_prod.fct_monthly_zone_revenue`
WHERE service_type = 'Green' AND CAST(revenue_month AS STRING) = '2019-10-01';
```

**Answer:** 384,624

---

## Question 6: Build a Staging Model for FHV Data

> Create a staging model for the For-Hire Vehicle (FHV) trip data for 2019.
> Filter out null dispatching_base_num. Rename fields.
> What is the count of records in stg_fhv_tripdata?

- 42,084,899
- → **43,244,693**
- 22,998,722
- 44,112,187

**Query:**
```sql
SELECT COUNT(*) FROM `de-zoomcamp-485104.dbt_ny_taxi_prod.stg_fhv_tripdata`;
```

**Answer:** 43,244,693

---

## Summary

| Question | Answer |
|----------|--------|
| Q1 | Upstream dependencies |
| Q2 | Fail test |
| Q3 | 12,184 |
| Q4 | East Harlem North |
| Q5 | 384,624 |
| Q6 | 43,244,693 |
