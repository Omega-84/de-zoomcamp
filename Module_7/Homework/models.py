from dataclasses import dataclass
import json 
import dataclasses

@dataclass
class Trip:
    lpep_pickup_datetime: str
    lpep_dropoff_datetime: str
    PULocationID: int
    DOLocationID: int
    passenger_count: int
    trip_distance: float
    tip_amount: float
    total_amount: float

def trip_from_row(row):
    return Trip(
        lpep_pickup_datetime = str(row['lpep_pickup_datetime']),
        lpep_dropoff_datetime = str(row['lpep_dropoff_datetime']),
        PULocationID=int(row['PULocationID']),
        DOLocationID=int(row['DOLocationID']),
        passenger_count = int(row['passenger_count']),
        trip_distance=float(row['trip_distance']),
        tip_amount=float(row['tip_amount']),
        total_amount=float(row['total_amount']),
        )

def trip_serializer(trip):
    trip_dict = dataclasses.asdict(trip)
    json_str = json.dumps(trip_dict)
    return json_str.encode('utf-8')

def trip_deserializer(data):
    json_str = data.decode('utf-8')
    trip_dict = json.loads(json_str)
    return Trip(**trip_dict)