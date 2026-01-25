-- Module 1 Homework: SQL Queries for Questions 3-6
-- Dataset: NYC Green Taxi Trip Data (November 2025)

-- ============================================================================
-- Question 3: Counting Short Trips
-- How many trips had a trip_distance <= 1 mile in November 2025?
-- Answer: 8,007
-- ============================================================================

SELECT COUNT(*)
FROM green_taxi_trip_data 
WHERE lpep_pickup_datetime >= '2025-11-01' 
  AND lpep_pickup_datetime < '2025-12-01' 
  AND trip_distance <= 1;


-- ============================================================================
-- Question 4: Longest Trip for Each Day
-- Which pickup day had the longest trip distance? (excluding trips >= 100 miles)
-- Answer: 2025-11-14
-- ============================================================================

SELECT DATE(lpep_pickup_datetime) AS pickup_day_max_distance
FROM green_taxi_trip_data 
WHERE trip_distance < 100
ORDER BY trip_distance DESC
LIMIT 1;


-- ============================================================================
-- Question 5: Biggest Pickup Zone
-- Which pickup zone had the largest total_amount on November 18th, 2025?
-- Answer: East Harlem North
-- ============================================================================

SELECT b."Zone", SUM(a."total_amount") AS total_amount 
FROM green_taxi_trip_data AS a
INNER JOIN taxi_zone_lookup AS b
  ON a."PULocationID" = b."LocationID"
WHERE DATE(a."lpep_pickup_datetime") = '2025-11-18' 
GROUP BY b."Zone" 
ORDER BY total_amount DESC
LIMIT 1;


-- ============================================================================
-- Question 6: Largest Tip
-- For pickups in "East Harlem North" in Nov 2025, which dropoff zone had the largest tip?
-- Answer: Yorkville West
-- ============================================================================

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
