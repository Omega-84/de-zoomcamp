# Module 7: Real-Time Streaming Practice

![Redpanda](https://img.shields.io/badge/Redpanda-241F21?style=for-the-badge&logo=redpanda&logoColor=white)
![Flink](https://img.shields.io/badge/Flink-E6526F?style=for-the-badge&logo=apache-flink&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)

This repository contains the practice work and experimentation for Module 7, focusing on **Redpanda** (Kafka API) and **Apache Flink** for stream processing.

---

## 🛠️ Practice Overview

The goal was to build a robust streaming pipeline which:
1.  **Generates events** using a custom Python producer with simulated lateness.
2.  **Buffers data** in a Redpanda topic named `rides`.
3.  **Processes streams** using PyFlink to compute hourly windowed aggregations.
4.  **Sinks results** into a PostgreSQL database for persistent storage.

---

## 🏗️ Architecture

### **Data Source: Real-Time Taxi Trips**
- We used `producer_realtime.py` to generate simulated NYC yellow taxi data.
- **Simulated Lateness**: To test Flink's **Watermarking** logic, we programmed the producer to send approximately 20% of events with a 3-10 second delay.

### **Steam Engine: Apache Flink (PyFlink)**
- **Table API**: Defined sources and sinks through SQL DDL.
- **Tumble Windows**: Grouped data into 1-hour fixed windows to calculate `total_revenue` and `num_trips` per zone.
- **Sink (Postgres)**: Data was written to the `processed_events_aggregated` table via a JDBC connector.

---

## 📁 Project Structure

```
Module_7/practice/
├── Dockerfile.flink        # Custom image with PyFlink and JDBC drivers
├── docker-compose.yaml     # Redpanda, Flink, and Postgres stack
├── flink-config.yaml       # Flink cluster configuration
├── pyproject.flink.toml    # Flink-specific Python dependencies
├── src/
│   ├── producers/          # Producers for Kafka topics
│   │   ├── producer_realtime.py
│   │   └── models.py
│   └── job/                # PyFlink stream processing jobs
│       ├── aggregation_job.py
│       └── pass_through_job.py
└── notebooks/              # Early prototyping with Kafka-python
    ├── producer.ipynb
    └── consumer.ipynb
```

## 🚀 How to Run

1.  **Start Infrastructure**:
    ```bash
    docker compose up -d
    ```

2.  **Start the Real-time Producer**:
    ```bash
    uv run python src/producers/producer_realtime.py
    ```

3.  **Submit the Flink Job**:
    ```bash
    docker exec -it practice-jobmanager-1 flink run -py /opt/src/job/aggregation_job.py
    ```

4.  **Monitor via Flink UI**: Visit [http://localhost:8081](http://localhost:8081).
