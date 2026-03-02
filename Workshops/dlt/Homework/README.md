# Workshop: dlt (Data Load Tool) — NYC Taxi Pipeline

![dlt](https://img.shields.io/badge/dlt-FF6B35?style=for-the-badge&logoColor=white)
![DuckDB](https://img.shields.io/badge/DuckDB-FFF000?style=for-the-badge&logo=duckdb&logoColor=black)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

## Project Files

| File | Description |
|------|-------------|
| [`taxi_pipeline_pipeline.py`](./taxi_pipeline_pipeline.py) | dlt pipeline with custom paginator for NYC taxi REST API |
| [`requirements.txt`](./requirements.txt) | Python dependencies |

---

## Question 1: What is the start date and end date of the dataset?

> Run the pipeline and query the loaded data date range.

- `2009-01-01` to `2009-01-31`
- → **`2009-06-01` to `2009-07-01`**
- `2024-01-01` to `2024-02-01`
- `2024-06-01` to `2024-07-01`

**Answer:** `2009-06-01` to `2009-07-01`

```sql
SELECT
    MIN(trip_pickup_date_time) AS start_date,
    MAX(trip_pickup_date_time) AS end_date
FROM taxi_data.rides;
```

> **Result:** `2009-06-01 07:33:00` → `2009-06-30 19:58:00`

---

## Question 2: What proportion of trips are paid with credit card?

> Calculate the percentage of credit card payments.

- `16.66%`
- → **`26.66%`**
- `36.66%`
- `46.66%`

**Answer:** `26.66%`

```sql
SELECT
    payment_type,
    COUNT(*) AS cnt,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) AS pct
FROM taxi_data.rides
GROUP BY payment_type
ORDER BY cnt DESC;
```

> **Result:**
> | payment_type | cnt | pct |
> |---|---|---|
> | CASH | 7,235 | 72.35% |
> | Credit | 2,666 | **26.66%** |
> | Cash | 97 | 0.97% |
> | No Charge | 1 | 0.01% |
> | Dispute | 1 | 0.01% |

---

## Question 3: What is the total amount of money generated in tips?

> Sum the tip amounts across all rides.

- `$4,063.41`
- → **`$6,063.41`**
- `$8,063.41`
- `$10,063.41`

**Answer:** `$6,063.41`

```sql
SELECT ROUND(SUM(tip_amt), 2) AS total_tips
FROM taxi_data.rides;
```

> **Result:** `$6,063.41`

---

## Pipeline Details

### API Configuration

| Config | Value |
|--------|-------|
| **Base URL** | `https://us-central1-dlthub-analytics.cloudfunctions.net/` |
| **Endpoint** | `data_engineering_zoomcamp_api` |
| **Data format** | Flat JSON array (1,000 records per page) |
| **Pagination** | Custom `StopOnEmptyPaginator` — stops when empty `[]` returned |
| **Destination** | DuckDB |
| **Total records** | 10,000 (10 pages × 1,000) |

### Custom Paginator

The built-in `PageNumberPaginator` expects a JSON object with a `total` field, but this API returns a bare JSON array. A custom `StopOnEmptyPaginator` was implemented to handle this:

```python
class StopOnEmptyPaginator(BasePaginator):
    def update_state(self, response, data=None):
        if not response.json():
            self._has_next_page = False
        else:
            self._page += 1
            self._has_next_page = True
```

---

## Summary

| Question | Answer |
|----------|--------|
| Q1 — Date range | `2009-06-01` to `2009-07-01` |
| Q2 — Credit card % | `26.66%` |
| Q3 — Total tips | `$6,063.41` |
