# Module 7: Real-Time Streaming Homework

![Kafka](https://img.shields.io/badge/Kafka-231F20?style=for-the-badge&logo=apache-kafka&logoColor=white)
![Flink](https://img.shields.io/badge/Flink-E6526F?style=for-the-badge&logo=apache-flink&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)

This repository contains the completed homework for Module 7 of the Data Engineering Zoomcamp, focusing on stream processing with **Redpanda (Kafka)** and **Apache Flink**.

---

## 🟢 Part 1: Kafka & Redpanda

> [!IMPORTANT]
> **Question 1. Redpanda version**
> Run `rpk version` inside the Redpanda container. What version of Redpanda are you running?

**Answer:** `v25.3.9`

---

> [!NOTE]
> **Question 2. Sending data to Redpanda**
> Measure the time it takes to send the entire dataset and flush.

**Answer:** `10 seconds`

---

> [!TIP]
> **Question 3. Consumer - trip distance**
> Count how many trips have a `trip_distance` greater than 5.0 kilometers.

**Answer:** `8506`

---

## 🔘 Part 2: PyFlink

> [!IMPORTANT]
> **Question 4. Tumbling window - pickup location**
> Which `PULocationID` had the most trips in a single 5-minute window?

**Answer:** `74`

---

> [!IMPORTANT]
> **Question 5. Session window - longest streak**
> How many trips were in the longest session using a 5-minute gap on `PULocationID`?

**Answer:** `81`

---

> [!IMPORTANT]
> **Question 6. Tumbling window - largest tip**
> Which hour had the highest total tip amount?

**Answer:** `2025-10-16 18:00:00`

---

## 📊 Summary of Results

| Question | Topic | Answer |
|----------|-------|--------|
| 1 | Redpanda Version | `v25.3.9` |
| 2 | Producer Time | `10 seconds` |
| 3 | Consumer Filter | `8506` trips |
| 4 | Tumbling Window | PULocationID `74` |
| 5 | Session Window | `81` trips |
| 6 | 1-Hour Window | `2025-10-16 18:00:00` |

---

## 🛠️ Implementation Details

### **Key Files**
- [`producer.ipynb`](./producer.ipynb): Python notebook for sending initial green taxi data to Redpanda.
- [`homework_q4.py`](./homework_q4.py): Flink job for 5-minute tumbling windows.
- [`homework_q5.py`](./homework_q5.py): Flink job for 5-minute session windows (groups bursts of activity).
- [`homework_q6.py`](./homework_q6.py): Flink job for 1-hour tumbling windows (tip aggregation).
- [`models.py`](./models.py): Shared data classes and serializers.

### **Environment**
- **Architecture**: Redpanda → Apache Flink → PostgreSQL.
- **Environment**: Isolated `uv` virtual environment for Module 7 compatibility.
- **Parallelism**: Set to `1` as per homework requirements for consistent watermarking on the single-partition topic.