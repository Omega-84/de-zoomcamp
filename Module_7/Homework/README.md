# Module 7 Homework: Real-Time Streaming

![Kafka](https://img.shields.io/badge/Kafka-231F20?style=for-the-badge&logo=apache-kafka&logoColor=white)
![Flink](https://img.shields.io/badge/Flink-E6526F?style=for-the-badge&logo=apache-flink&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)

## Project Files

| File | Description |
|------|-------------|
| [`producer.ipynb`](./producer.ipynb) | Notebook for streaming green taxi data to Redpanda |
| [`consumers.ipynb`](./consumers.ipynb) | Notebook for verifying data consumption in Kafka |
| [`homework_q4.py`](./homework_q4.py) | PyFlink job for 5-minute tumbling window counts |
| [`homework_q5.py`](./homework_q5.py) | PyFlink job for 5-minute session window analysis |
| [`homework_q6.py`](./homework_q6.py) | PyFlink job for 1-hour tumbling window tip aggregation |
| [`models.py`](./models.py) | Data models and serialization logic |

---

## Question 1: Redpanda version

> Run `rpk version` inside the Redpanda container. What version of Redpanda are you running?

**Answer:** `v25.3.9`

> Verified by executing `docker exec -it practice-redpanda-1 rpk version` which returned the build date and Go version alongside the cluster version `v25.3.9`.

---

## Question 2: Sending data to Redpanda

> Create a topic called `green-trips`. Measure the time it takes to send the entire dataset and flush. How long did it take to send the data?

- → **10 seconds**
- 60 seconds
- 120 seconds
- 300 seconds

**Answer:** 10 seconds

> The producer took approximately 8.85 seconds to serialize and transmit the 50,000+ records from the October 2025 Green Taxi dataset.

---

## Question 3: Consumer - trip distance

> Write a Kafka consumer that reads all messages from the `green-trips` topic. Count how many trips have a `trip_distance` greater than 5.0 kilometers.

- 6506
- 7506
- → **8506**
- 9506

**Answer:** 8506

> Calculated using a standard Python Kafka consumer with `auto_offset_reset='earliest'` to ensure all historical topic data was processed.

---

## Question 4: Tumbling window - pickup location

> Create a Flink job that reads from `green-trips` and uses a 5-minute tumbling window to count trips per `PULocationID`. Which `PULocationID` had the most trips in a single 5-minute window?

- 42
- → **74**
- 75
- 166

**Answer:** 74

> We used a SQL `TUMBLE` window in PyFlink to process the stream and find the peak burst of activity at PULocationID 74.

---

## Question 5: Session window - longest streak

> Create another Flink job that uses a session window with a 5-minute gap on `PULocationID`. How many trips were in the longest session?

- 12
- 31
- 51
- → **81**

**Answer:** 81

> Implemented using the legacy Group Window syntax (`SESSION(event_timestamp, INTERVAL '5' MINUTE)`) to detect gaps in activity per pickup zone.

---

## Question 6: Tumbling window - largest tip

> Create a Flink job that uses a 1-hour tumbling window to compute the total `tip_amount` per hour. Which hour had the highest total tip amount?

- 2025-10-01 18:00:00
- → **2025-10-16 18:00:00**
- 2025-10-22 08:00:00
- 2025-10-30 16:00:00

**Answer:** 2025-10-16 18:00:00

> An hourly aggregation revealed thatOctober 16th during the 6 PM hour generated the highest cumulative tip revenue in the dataset.

---

## Summary

| Question | Answer |
|----------|--------|
| Q1 | `v25.3.9` |
| Q2 | 10 seconds |
| Q3 | 8506 |
| Q4 | 74 |
| Q5 | 81 |
| Q6 | 2025-10-16 18:00:00 |