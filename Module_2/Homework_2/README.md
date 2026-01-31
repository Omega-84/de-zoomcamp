# Module 2 Homework: Workflow Orchestration

![Kestra](https://img.shields.io/badge/Kestra-1.1-7B42BC?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PC9zdmc+&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![BigQuery](https://img.shields.io/badge/BigQuery-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white)
![GCS](https://img.shields.io/badge/Cloud_Storage-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)


## Project Files

| File | Description |
|------|-------------|
| [`../practice/docker-compose.yaml`](../practice/docker-compose.yaml) | Kestra + PostgreSQL + pgAdmin services |
| [`../practice/learning_logs/`](../practice/learning_logs/) | Daily learning logs |

## Dataset

**NYC Taxi Trip Data**
- Yellow & Green taxi data (2019-2021)
- Source: `https://github.com/DataTalksClub/nyc-tlc-data/releases/`

---

## Question 1: File Size

> Within the execution for `Yellow` Taxi data for the year `2020` and month `12`: what is the uncompressed file size (i.e. the output file `yellow_tripdata_2020-12.csv` of the `extract` task)?

- → **128.3 MiB**
- 134.5 MiB
- 364.7 MiB
- 692.6 MiB

**Answer:** 128.3 MiB

---

## Question 2: Variable Rendering

> What is the rendered value of the variable `file` when the inputs `taxi` is set to `green`, `year` is set to `2020`, and `month` is set to `04` during execution?

- `{{inputs.taxi}}_tripdata_{{inputs.year}}-{{inputs.month}}.csv`
- → **`green_tripdata_2020-04.csv`**
- `green_tripdata_04_2020.csv`
- `green_tripdata_2020.csv`

**Answer:** `green_tripdata_2020-04.csv`

---

## Question 3: Yellow 2020 Total Rows

> How many rows are there for the `Yellow` Taxi data for all CSV files in the year 2020?

- 13,537,299
- → **24,648,499**
- 18,324,219
- 29,430,127

**Query:**
```sql
SELECT COUNT(*) 
FROM demo_dataset.yellow_tripdata 
WHERE filename LIKE '%2020%';
```

**Answer:** 24,648,499

---

## Question 4: Green 2020 Total Rows

> How many rows are there for the `Green` Taxi data for all CSV files in the year 2020?

- 5,327,301
- 936,199
- → **1,734,051**
- 1,342,034

**Query:**
```sql
SELECT COUNT(*) 
FROM demo_dataset.green_tripdata 
WHERE filename LIKE '%2020%';
```

**Answer:** 1,734,051

---

## Question 5: Yellow March 2021 Rows

> How many rows are there for the `Yellow` Taxi data for the March 2021 CSV file?

- 1,428,092
- 706,911
- → **1,925,152**
- 2,561,031

**Query:**
```sql
SELECT COUNT(*) 
FROM demo_dataset.yellow_tripdata 
WHERE filename LIKE '%2021-03%';
```

**Answer:** 1,925,152

---

## Question 6: Timezone Configuration

> How would you configure the timezone to New York in a Schedule trigger?

- Add a `timezone` property set to `EST` in the `Schedule` trigger configuration
- → **Add a `timezone` property set to `America/New_York` in the `Schedule` trigger configuration**
- Add a `timezone` property set to `UTC-5` in the `Schedule` trigger configuration
- Add a `location` property set to `New_York` in the `Schedule` trigger configuration


**Answer:** Add a `timezone` property set to `America/New_York` in the `Schedule` trigger configuration

---

## Summary

| Question | Answer |
|----------|--------|
| Q1 | 128.3 MiB |
| Q2 | `green_tripdata_2020-04.csv` |
| Q3 | 24,648,499 |
| Q4 | 1,734,051 |
| Q5 | 1,925,152 |
| Q6 | `America/New_York` |
