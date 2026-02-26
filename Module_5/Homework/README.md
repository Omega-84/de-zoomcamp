# Module 5 Homework: Data Platforms with Bruin

![Bruin](https://img.shields.io/badge/Bruin-FF6B35?style=for-the-badge&logoColor=white)
![DuckDB](https://img.shields.io/badge/DuckDB-FFF000?style=for-the-badge&logo=duckdb&logoColor=black)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

## Project Files

| File | Description |
|------|-------------|
| [`my-taxi-pipeline/`](../my-taxi-pipeline/) | Full Bruin pipeline project |
| [`pipeline.yml`](../my-taxi-pipeline/pipeline/pipeline.yml) | Pipeline configuration |
| [`trips.py`](../my-taxi-pipeline/pipeline/assets/ingestion/trips.py) | Python ingestion asset |
| [`trips.sql`](../my-taxi-pipeline/pipeline/assets/staging/trips.sql) | SQL staging asset |
| [`trips_report.sql`](../my-taxi-pipeline/pipeline/assets/reports/trips_report.sql) | SQL reporting asset |

---

## Question 1: Bruin Pipeline Structure

> In a Bruin project, what are the required files/directories?

- `bruin.yml` and `assets/`
- `.bruin.yml` and `pipeline.yml` (assets can be anywhere)
- → **`.bruin.yml` and `pipeline/` with `pipeline.yml` and `assets/`**
- `pipeline.yml` and `assets/` only

**Answer:** `.bruin.yml` and `pipeline/` with `pipeline.yml` and `assets/`

> `.bruin.yml` lives at the project root for environment/connection config, `pipeline.yml` defines the pipeline, and `assets/` contains the actual data assets.

---

## Question 2: Materialization Strategies

> Which incremental strategy is best for processing a specific interval period by deleting and inserting data for that time period?

- `append` - always add new rows
- `replace` - truncate and rebuild entirely
- → **`time_interval` - incremental based on a time column**
- `view` - create a virtual table only

**Answer:** `time_interval`

> `time_interval` deletes rows within the run's time window and re-inserts the query results for that same window. This is exactly what our staging and reports layers use with `pickup_datetime` as the `incremental_key`.

---

## Question 3: Pipeline Variables

> How do you override the `taxi_types` variable to only process yellow taxis?

- `bruin run --taxi-types yellow`
- `bruin run --var taxi_types=yellow`
- → **`bruin run --var 'taxi_types=["yellow"]'`**
- `bruin run --set taxi_types=["yellow"]`

**Answer:** `bruin run --var 'taxi_types=["yellow"]'`

> Since `taxi_types` is defined as an array, the override must also be valid JSON array syntax. We used this exact flag when running our pipeline.

---

## Question 4: Running with Dependencies

> You've modified `ingestion/trips.py` and want to run it plus all downstream assets. Which command?

- `bruin run ingestion.trips --all`
- → **`bruin run ingestion/trips.py --downstream`**
- `bruin run pipeline/trips.py --recursive`
- `bruin run --select ingestion.trips+`

**Answer:** `bruin run ingestion/trips.py --downstream`

> The `--downstream` flag tells Bruin to execute the specified asset AND all assets that depend on it (staging → reports).

---

## Question 5: Quality Checks

> Which quality check ensures `pickup_datetime` never has NULL values?

- `name: unique`
- → **`name: not_null`**
- `name: positive`
- `name: accepted_values, value: [not_null]`

**Answer:** `not_null`

> We used this exact check in our `trips.py` and `trips.sql` assets for `pickup_datetime`.

---

## Question 6: Lineage and Dependencies

> Which Bruin command visualizes the dependency graph?

- `bruin graph`
- `bruin dependencies`
- → **`bruin lineage`**
- `bruin show`

**Answer:** `bruin lineage`

> Usage: `bruin lineage ./pipeline/assets/ingestion/trips.py`

---

## Question 7: First-Time Run

> What flag ensures tables are created from scratch on first run?

- `--create`
- `--init`
- → **`--full-refresh`**
- `--truncate`

**Answer:** `--full-refresh`

> We used this exact flag in our first pipeline run: `bruin run ./pipeline/pipeline.yml --full-refresh --start-date 2022-01-01 --end-date 2022-02-01`

---

## Summary

| Question | Answer |
|----------|--------|
| Q1 | `.bruin.yml` + `pipeline/` with `pipeline.yml` + `assets/` |
| Q2 | `time_interval` |
| Q3 | `--var 'taxi_types=["yellow"]'` |
| Q4 | `bruin run ingestion/trips.py --downstream` |
| Q5 | `not_null` |
| Q6 | `bruin lineage` |
| Q7 | `--full-refresh` |
