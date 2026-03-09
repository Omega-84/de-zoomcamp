# Data Engineering Zoomcamp 2026

![Terraform](https://img.shields.io/badge/Terraform-7B42BC?style=for-the-badge&logo=terraform&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![GCP](https://img.shields.io/badge/Google_Cloud-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white)
![Kestra](https://img.shields.io/badge/Kestra-7B42BC?style=for-the-badge&logoColor=white)
![Airflow](https://img.shields.io/badge/Airflow-017CEE?style=for-the-badge&logo=apache-airflow&logoColor=white)
![BigQuery](https://img.shields.io/badge/BigQuery-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white)
![Bruin](https://img.shields.io/badge/Bruin-FF6B35?style=for-the-badge&logoColor=white)
![DuckDB](https://img.shields.io/badge/DuckDB-FFF000?style=for-the-badge&logo=duckdb&logoColor=black)
![dlt](https://img.shields.io/badge/dlt-FF6B35?style=for-the-badge&logoColor=white)

A comprehensive journey through the [Data Engineering Zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp) by DataTalks.Club.

---

## 📚 Course Progress

| Module | Topic | Status |
|--------|-------|--------|
| 1 | [Containerization & Infrastructure as Code](#module-1-containerization--infrastructure-as-code) | ✅ Complete |
| 2 | [Workflow Orchestration](#module-2-workflow-orchestration) | ✅ Complete |
| 3 | [Data Warehouse](#module-3-data-warehouse) | ✅ Complete |
| 4 | [Analytics Engineering](#module-4-analytics-engineering) | ✅ Complete |
| 5 | [Data Platforms](#module-5-data-platforms) | ✅ Complete |
| WS | [Workshop: dlt](#workshop-dlt-data-load-tool) | ✅ Complete |
| 6 | [Batch Processing](#module-6-batch-processing) | ✅ Complete |
| 7 | [Project](#module-7-project) | ⬜ Not Started |

---

## Module 1: Containerization & Infrastructure as Code

**Topics Covered:**
- [x] Docker basics and containerization
- [x] Docker Compose for multi-container applications
- [x] PostgreSQL and pgAdmin setup
- [x] Data ingestion pipelines with Python
- [x] Terraform fundamentals
- [x] Google Cloud Platform setup
- [x] Infrastructure as Code with variables

**Homework:** [View Homework 1](./Module_1/Homework_1/)

**Key Files:**
- [`Dockerfile`](./Module_1/Homework_1/Dockerfile) - Data ingestion container
- [`docker-compose.yaml`](./Module_1/Homework_1/docker-compose.yaml) - PostgreSQL + pgAdmin
- [`ingest_to_db.py`](./Module_1/Homework_1/ingest_to_db.py) - Click CLI ingestion script
- [`terraform/`](./Module_1/Homework_1/terraform/) - GCP infrastructure

---

## Module 2: Workflow Orchestration

**Topics Covered:**
- [x] Introduction to Kestra workflow orchestration
- [x] YAML-based flow definitions
- [x] Building ETL pipelines (Extract → Transform → Load)
- [x] PostgreSQL data ingestion with MERGE
- [x] GCP integration (GCS + BigQuery)
- [x] Scheduling and backfill
- [x] AI/RAG integration with Gemini

**Homework:** [View Homework 2](./Module_2/Homework_2/)

**Key Files:**
- [`docker-compose.yaml`](./Module_2/practice/docker-compose.yaml) - Kestra + PostgreSQL + pgAdmin
- [`learning_logs/`](./Module_2/practice/learning_logs/) - Daily learning documentation

---

## Module 3: Data Warehouse

**Topics Covered:**
- [x] BigQuery fundamentals
- [x] External vs Materialized tables
- [x] Partitioning and clustering
- [x] Query optimization and cost estimation
- [x] Apache Airflow for ETL
- [x] GCS to BigQuery data pipeline

**Homework:** [View Homework 3](./Module_3/Homework_3/)

**Key Files:**
- [`docker-compose.yaml`](./Module_3/practice/airflow/docker-compose.yaml) - Airflow cluster
- [`upload_files.py`](./Module_3/practice/airflow/dags/upload_files.py) - GCS upload DAG
- [`gcs_helpers/`](./Module_3/practice/airflow/plugins/gcs_helpers/) - Reusable GCS helpers
- [`Homework_3.sql`](./Module_3/Homework_3/Homework_3.sql) - BigQuery queries

---

## Module 4: Analytics Engineering

**Topics Covered:**
- [x] dbt (data build tool)
- [x] Data modeling (staging, intermediate, marts)
- [x] Testing (generic & singular tests)
- [x] Documentation & schemas
- [x] Dispatch & macros
- [x] Airflow ingestion pipeline for FHV data

**Homework:** [View Homework 4](./Module_4/Homework/)

**Key Files:**
- [`ny_taxi_project/`](./Module_4/practice/ny_taxi_project/) - Main dbt project
- [`fhv_taxi_pipeline.py`](./Module_4/practice/airflow/dags/fhv_taxi_pipeline.py) - FHV Ingestion DAG
- [`models/`](./Module_4/practice/ny_taxi_project/models/) - SQL transformations

---

## Module 5: Data Platforms

**Topics Covered:**
- [x] Bruin CLI for unified data pipelines
- [x] ELT pipeline architecture (ingestion → staging → reports)
- [x] Python ingestion assets (NYC Taxi parquet data)
- [x] SQL transformation & deduplication
- [x] Materialization strategies (append, time_interval)
- [x] Data quality checks (not_null, non_negative, custom)
- [x] DuckDB for local development

**Homework:** [View Homework 5](./Module_5/Homework/)

**Key Files:**
- [`my-taxi-pipeline/`](./Module_5/my-taxi-pipeline/) - Full Bruin pipeline project
- [`trips.py`](./Module_5/my-taxi-pipeline/pipeline/assets/ingestion/trips.py) - Python ingestion asset
- [`trips.sql`](./Module_5/my-taxi-pipeline/pipeline/assets/staging/trips.sql) - SQL staging asset
- [`trips_report.sql`](./Module_5/my-taxi-pipeline/pipeline/assets/reports/trips_report.sql) - SQL reporting asset

---

## Workshop: dlt (Data Load Tool)

**Topics Covered:**
- [x] dlt (Data Load Tool) for REST API ingestion
- [x] Declarative REST API sources (`RESTAPIConfig`)
- [x] Imperative REST client (`RESTClient`)
- [x] Custom paginator for non-standard APIs
- [x] Schema inference and auto-normalization
- [x] DuckDB as local destination

**Homework:** [View Workshop Homework](./Workshops/dlt/Homework/)

**Key Files:**
- [`taxi_pipeline_pipeline.py`](./Workshops/dlt/Homework/taxi_pipeline_pipeline.py) - NYC Taxi dlt pipeline with custom paginator
- [`open_library_pipeline.py`](./Workshops/dlt/open_library_pipeline.py) - Open Library search pipeline (practice)

---

## Module 6: Batch Processing

**Topics Covered:**
- [x] Apache Spark architecture (Driver, Executors, Partitioning)
- [x] PySpark DataFrame API (Read, Transform, Repartition, Write)
- [x] Spark SQL & Temporary Views
- [x] Google Cloud Dataproc cluster execution
- [x] Integrating PySpark with Google Cloud Storage
- [x] Analyzing NYC trip data via Spark SQL

**Homework:** [View Homework 6](./Module_6/Homework/)

**Key Files:**
- [`hw.ipynb`](./Module_6/Homework/hw.ipynb) - PySpark dataframe manipulation
- [`spark_sql_dataproc.py`](./Module_6/practice/scripts/spark_sql_dataproc.py) - GCP Dataproc submission script

---

## Module 7: Project

**Topics to Cover:**
- [ ] End-to-end data pipeline
- [ ] Combining all learned technologies
- [ ] Dashboard creation

---

## 📁 Repository Structure

```
de-zoomcamp/
├── Module_1/
│   ├── Homework_1/          # Docker & SQL homework
│   │   ├── Dockerfile
│   │   ├── docker-compose.yaml
│   │   ├── ingest_to_db.py
│   │   └── README.md
│   └── practice/
│       └── learning_logs/
├── Module_2/
│   ├── Homework_2/          # Kestra homework
│   │   └── README.md
│   └── practice/
│       ├── docker-compose.yaml
│       └── learning_logs/
├── Module_3/
│   ├── Homework_3/          # BigQuery homework
│   │   ├── Homework_3.sql
│   │   └── README.md
│   └── practice/
│       ├── airflow/
│       └── learning_logs/
├── Module_4/
│   ├── Homework/            # dbt homework
│   │   ├── stg_fhv_tripdata.sql
│   │   └── README.md
│   └── practice/
│       ├── airflow/         # FHV ingestion DAGs
│       ├── ny_taxi_project/ # dbt project
│       └── learning_logs/
├── Module_5/
│   ├── Homework/            # Bruin homework
│   │   └── README.md
│   ├── my-taxi-pipeline/    # Bruin ELT pipeline
│   │   ├── pipeline/
│   │   │   ├── pipeline.yml
│   │   │   └── assets/
│   │   └── README.md
│   └── practice/
│       └── learning_logs/
├── Workshops/
│   └── dlt/
│       ├── Homework/        # dlt workshop homework
│       │   ├── taxi_pipeline_pipeline.py
│       │   └── README.md
│       ├── open_library_pipeline.py
│       └── practice/
│           └── learning_logs/
├── Module_6/
│   ├── Homework/            # Spark processing homework
│   │   ├── hw.ipynb
│   │   └── README.md
│   └── practice/
│       ├── scripts/         # PySpark execution scripts
│       └── learning_logs/
└── README.md
```

---

## 🛠️ Tools & Technologies

| Category | Tools |
|----------|-------|
| **Containerization** | Docker, Docker Compose |
| **Database** | PostgreSQL, BigQuery |
| **Infrastructure** | Terraform, Google Cloud Platform |
| **Programming** | Python, SQL |
| **Orchestration** | Kestra, Apache Airflow |
| **Data Warehouse** | BigQuery |
| **Analytics Engineering** | dbt (Data Build Tool) |
| **Data Platforms** | Bruin, DuckDB |
| **Data Load Tool** | dlt |
| **Batch Processing** | Apache Spark |
| **Streaming** | Apache Kafka (upcoming) |

---

## 📖 Learning Logs

Daily learning logs documenting concepts, commands, and key takeaways:

**Module 1:**
- [Day 1-2: Docker basics](./Module_1/practice/learning_logs/learnings_2026-01-18.txt)
- [Day 3: PostgreSQL, pgcli, Dockerfile](./Module_1/practice/learning_logs/learnings_2026-01-19.txt)
- [Day 4: Docker Compose](./Module_1/practice/learning_logs/learnings_2026-01-20.txt)
- [Day 5: GCP Setup](./Module_1/practice/learning_logs/learnings_2026-01-21.txt)
- [Day 6: Terraform basics](./Module_1/practice/learning_logs/learnings_2026-01-22.txt)
- [Day 7: Homework completion](./Module_1/practice/learning_logs/learnings_2026-01-23.txt)
- [Day 8: Terraform variables](./Module_1/practice/learning_logs/learnings_2026-01-24.txt)

**Module 2:**
- [Day 9-10: Kestra setup & flows 01-07](./Module_2/practice/learning_logs/learnings_2026-01-25.txt)
- [Day 11: GCP secrets & flows](./Module_2/practice/learning_logs/learnings_2026-01-27.txt)
- [Day 12: GCP Taxi & AI/RAG (flows 08-11)](./Module_2/practice/learning_logs/learnings_2026-01-29.txt)

**Module 3:**
- [Day 13: Python GCP setup](./Module_3/practice/learning_logs/learnings_2026-02-05.txt)
- [Day 14: Airflow setup & GCS DAG](./Module_3/practice/learning_logs/learnings_2026-02-08.txt)

**Module 4:**
- [Day 15: dbt Setup & Models (Staging, Marts)](./Module_4/practice/learning_logs/learnings_2026-02-16.txt)

**Module 5:**
- [Day 16: Bruin ELT Pipeline (Ingestion, Staging, Reports)](./Module_5/practice/learning_logs/learnings_2026-02-25.txt)

**Workshop: dlt:**
- [Day 17: dlt REST API Pipelines (Open Library + NYC Taxi)](./Workshops/dlt/practice/learning_logs/learnings_2026-03-02.txt)

**Module 6:**
- [Day 18: Spark Basics & Architecture](./Module_6/practice/learning_logs/learnings_2026-03-04.txt)
- [Day 19: Spark SQL & Distributed Joins](./Module_6/practice/learning_logs/learnings_2026-03-07.txt)
- [Day 20: Google Cloud Dataproc Clusters](./Module_6/practice/learning_logs/learnings_2026-03-08.txt)
- [Day 21: Batch Processing Homework](./Module_6/practice/learning_logs/learnings_2026-03-09.txt)

---

## 🔗 Resources

- [Course Repository](https://github.com/DataTalksClub/data-engineering-zoomcamp)
- [DataTalks.Club](https://datatalks.club/)
- [Course Videos](https://www.youtube.com/playlist?list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb)
