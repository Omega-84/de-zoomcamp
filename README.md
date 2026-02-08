# Data Engineering Zoomcamp 2026

![Terraform](https://img.shields.io/badge/Terraform-7B42BC?style=for-the-badge&logo=terraform&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![GCP](https://img.shields.io/badge/Google_Cloud-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white)
![Kestra](https://img.shields.io/badge/Kestra-7B42BC?style=for-the-badge&logoColor=white)
![Airflow](https://img.shields.io/badge/Airflow-017CEE?style=for-the-badge&logo=apache-airflow&logoColor=white)
![BigQuery](https://img.shields.io/badge/BigQuery-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white)

A comprehensive journey through the [Data Engineering Zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp) by DataTalks.Club.

---

## 📚 Course Progress

| Module | Topic | Status |
|--------|-------|--------|
| 1 | [Containerization & Infrastructure as Code](#module-1-containerization--infrastructure-as-code) | ✅ Complete |
| 2 | [Workflow Orchestration](#module-2-workflow-orchestration) | ✅ Complete |
| 3 | [Data Warehouse](#module-3-data-warehouse) | ✅ Complete |
| 4 | [Analytics Engineering](#module-4-analytics-engineering) | ⬜ Not Started |
| 5 | [Batch Processing](#module-5-batch-processing) | ⬜ Not Started |
| 6 | [Streaming](#module-6-streaming) | ⬜ Not Started |
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

**Topics to Cover:**
- [ ] dbt (data build tool)
- [ ] Data modeling
- [ ] Testing and documentation

---

## Module 5: Batch Processing

**Topics to Cover:**
- [ ] Apache Spark
- [ ] DataFrames and SQL
- [ ] Spark internals

---

## Module 6: Streaming

**Topics to Cover:**
- [ ] Apache Kafka
- [ ] Stream processing
- [ ] Real-time data pipelines

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
├── Module_4/                # Coming soon
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

---

## 🔗 Resources

- [Course Repository](https://github.com/DataTalksClub/data-engineering-zoomcamp)
- [DataTalks.Club](https://datatalks.club/)
- [Course Videos](https://www.youtube.com/playlist?list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb)
