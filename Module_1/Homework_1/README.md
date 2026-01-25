# Module 1 Homework: Docker & SQL

![Terraform](https://img.shields.io/badge/Terraform-7B42BC?style=for-the-badge&logo=terraform&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Python](https://img.shields.io/badge/Python_3.13-3776AB?style=for-the-badge&logo=python&logoColor=white)
![GCP](https://img.shields.io/badge/Google_Cloud-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white)


## Project Files

| File | Description |
|------|-------------|
| [`Dockerfile`](./Dockerfile) | Container image for data ingestion pipeline |
| [`docker-compose.yaml`](./docker-compose.yaml) | PostgreSQL and pgAdmin services |
| [`ingest_to_db.py`](./ingest_to_db.py) | Python CLI script for data ingestion |
| [`pyproject.toml`](./pyproject.toml) | Python dependencies |
| [`terraform/`](./terraform/) | Terraform configuration for GCP resources |

## Dataset

**NYC Green Taxi Trip Data (November 2025)**
- Trip data: `green_tripdata_2025-11.parquet`
- Zone lookup: `taxi_zone_lookup.csv`

---

## Question 1: Understanding Docker Images

> Run docker with the `python:3.13` image. Use an entrypoint bash to interact with the container. What's the version of pip in the image?

- → **25.3**
- 24.3.1
- 24.2.1
- 23.3.1

**Command:**
```bash
docker run -it --rm --entrypoint=bash python:3.13
pip --version
```

**Answer:** 25.3

---

## Question 2: Understanding Docker Networking

> Given the following docker-compose.yaml, what is the hostname and port that pgadmin should use to connect to the postgres database?

```yaml
services:
  db:
    container_name: postgres
    image: postgres:17-alpine
    environment:
      POSTGRES_USER: 'postgres'
      POSTGRES_PASSWORD: 'postgres'
      POSTGRES_DB: 'ny_taxi'
    ports:
      - '5433:5432'
    volumes:
      - vol-pgdata:/var/lib/postgresql/data

  pgadmin:
    container_name: pgadmin
    image: dpage/pgadmin4:latest
    environment:
      PGADMIN_DEFAULT_EMAIL: "pgadmin@pgadmin.com"
      PGADMIN_DEFAULT_PASSWORD: "pgadmin"
    ports:
      - "8080:80"
    volumes:
      - vol-pgadmin_data:/var/lib/pgadmin

volumes:
  vol-pgdata:
    name: vol-pgdata
  vol-pgadmin_data:
    name: vol-pgadmin_data
```

- postgres:5433
- localhost:5432
- db:5433
- postgres:5432
- → **db:5432**

**Answer:** db:5432

---

## Question 3: Counting Short Trips

> For the trips in November 2025 (lpep_pickup_datetime between '2025-11-01' and '2025-12-01', exclusive of the upper bound), how many trips had a trip_distance of less than or equal to 1 mile?

- 7,853
- → **8,007**
- 8,254
- 8,421

**Query:**
```sql
SELECT COUNT(*)
FROM green_taxi_trip_data 
WHERE lpep_pickup_datetime >= '2025-11-01' 
  AND lpep_pickup_datetime < '2025-12-01' 
  AND trip_distance <= 1;
```

**Answer:** 8,007

---

## Question 4: Longest Trip for Each Day

> Which was the pick up day with the longest trip distance? Only consider trips with trip_distance less than 100 miles (to exclude data errors).

- → **2025-11-14**
- 2025-11-20
- 2025-11-23
- 2025-11-25

**Query:**
```sql
SELECT DATE(lpep_pickup_datetime) AS pickup_day_max_distance
FROM green_taxi_trip_data 
WHERE trip_distance < 100
ORDER BY trip_distance DESC
LIMIT 1;
```

**Answer:** 2025-11-14

---

## Question 5: Biggest Pickup Zone

> Which was the pickup zone with the largest total_amount (sum of all trips) on November 18th, 2025?

- → **East Harlem North**
- East Harlem South
- Morningside Heights
- Forest Hills

**Query:**
```sql
SELECT b."Zone", SUM(a."total_amount") AS total_amount 
FROM green_taxi_trip_data AS a
INNER JOIN taxi_zone_lookup AS b
  ON a."PULocationID" = b."LocationID"
WHERE DATE(a."lpep_pickup_datetime") = '2025-11-18' 
GROUP BY b."Zone" 
ORDER BY total_amount DESC
LIMIT 1;
```

**Answer:** East Harlem North

---

## Question 6: Largest Tip

> For the passengers picked up in the zone named "East Harlem North" in November 2025, which was the drop off zone that had the largest tip?

- JFK Airport
- → **Yorkville West**
- East Harlem North
- LaGuardia Airport

**Query:**
```sql
SELECT dropoff."Zone" AS dropoff_zone
FROM green_taxi_trip_data AS a
INNER JOIN taxi_zone_lookup AS pickup
  ON a."PULocationID" = pickup."LocationID"
INNER JOIN taxi_zone_lookup AS dropoff
  ON a."DOLocationID" = dropoff."LocationID"
WHERE EXTRACT(MONTH FROM a.lpep_pickup_datetime) = 11 
  AND pickup."Zone" = 'East Harlem North'
ORDER BY a."tip_amount" DESC
LIMIT 1;
```

**Answer:** Yorkville West

---

## Question 7: Terraform Workflow

> Which of the following sequences, respectively, describes the workflow for:
> 1. Downloading the provider plugins and setting up backend
> 2. Generating proposed changes and auto-executing the plan
> 3. Remove all resources managed by Terraform

- terraform import, terraform apply -y, terraform destroy
- teraform init, terraform plan -auto-apply, terraform rm
- terraform init, terraform run -auto-approve, terraform destroy
- → **terraform init, terraform apply -auto-approve, terraform destroy**
- terraform import, terraform apply -y, terraform rm

**Answer:** terraform init, terraform apply -auto-approve, terraform destroy

---

## Summary

| Question | Answer |
|----------|--------|
| Q1 | 25.3 |
| Q2 | db:5432 |
| Q3 | 8,007 |
| Q4 | 2025-11-14 |
| Q5 | East Harlem North |
| Q6 | Yorkville West |
| Q7 | terraform init, terraform apply -auto-approve, terraform destroy |
