# Data Engineering Zoomcamp 2025

![Terraform](https://img.shields.io/badge/Terraform-7B42BC?style=for-the-badge&logo=terraform&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![GCP](https://img.shields.io/badge/Google_Cloud-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white)

A comprehensive journey through the [Data Engineering Zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp) by DataTalks.Club.

---

## 📚 Course Progress

| Module | Topic | Status |
|--------|-------|--------|
| 1 | [Containerization & Infrastructure as Code](#module-1-containerization--infrastructure-as-code) | ✅ Complete |
| 2 | [Workflow Orchestration](#module-2-workflow-orchestration) | 🔄 In Progress |
| 3 | [Data Warehouse](#module-3-data-warehouse) | ⬜ Not Started |
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

**Topics to Cover:**
- [ ] Introduction to workflow orchestration
- [ ] Mage/Prefect/Airflow basics
- [ ] Building ETL pipelines
- [ ] Scheduling and monitoring

---

## Module 3: Data Warehouse

**Topics to Cover:**
- [ ] BigQuery fundamentals
- [ ] Partitioning and clustering
- [ ] Best practices for data warehousing

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
│   ├── Homework_1/          # Completed homework
│   │   ├── Dockerfile
│   │   ├── docker-compose.yaml
│   │   ├── ingest_to_db.py
│   │   ├── queries.sql
│   │   ├── terraform/
│   │   └── README.md
│   └── practice/            # Practice exercises
│       ├── pipeline/
│       ├── terraform/
│       └── learning_logs/
├── Module_2/                # Coming soon
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
| **Orchestration** | Mage/Prefect/Airflow (upcoming) |
| **Processing** | Apache Spark (upcoming) |
| **Streaming** | Apache Kafka (upcoming) |

---

## 📖 Learning Logs

Daily learning logs documenting concepts, commands, and key takeaways:

- [Day 1-2: Docker basics](./Module_1/practice/learning_logs/learnings_2026-01-18.txt)
- [Day 3: PostgreSQL, pgcli, Dockerfile](./Module_1/practice/learning_logs/learnings_2026-01-19.txt)
- [Day 4: Docker Compose](./Module_1/practice/learning_logs/learnings_2026-01-20.txt)
- [Day 5: GCP Setup](./Module_1/practice/learning_logs/learnings_2026-01-21.txt)
- [Day 6: Terraform basics](./Module_1/practice/learning_logs/learnings_2026-01-22.txt)
- [Day 7: Homework completion](./Module_1/practice/learning_logs/learnings_2026-01-23.txt)
- [Day 8: Terraform variables](./Module_1/practice/learning_logs/learnings_2026-01-24.txt)

---

## 🔗 Resources

- [Course Repository](https://github.com/DataTalksClub/data-engineering-zoomcamp)
- [DataTalks.Club](https://datatalks.club/)
- [Course Videos](https://www.youtube.com/playlist?list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb)