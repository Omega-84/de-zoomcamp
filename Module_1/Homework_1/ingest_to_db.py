import click
import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm

date_col_trip = [
    "lpep_pickup_datetime",
    "lpep_dropoff_datetime"
]

dtype_trip = {'VendorID': 'Int64',
 'store_and_fwd_flag': 'str',
 'RatecodeID': 'Int64',
 'PULocationID': 'Int64',
 'DOLocationID': 'Int64',
 'passenger_count': 'Int64',
 'trip_distance': 'float64',
 'fare_amount': 'float64',
 'extra': 'float64',
 'mta_tax': 'float64',
 'tip_amount': 'float64',
 'tolls_amount': 'float64',
 'ehail_fee': 'float64',
 'improvement_surcharge': 'float64',
 'total_amount': 'float64',
 'payment_type': 'Int64',
 'trip_type': 'Int64',
 'congestion_surcharge': 'float64',
 'cbd_congestion_fee': 'float64'}

dtype_lookup = {
    "LocationID" : "int32",
    "Borough" : "str",
    "Zone" : "str",
    "service_zone" : "str"
}

@click.command()
@click.option('--user', default='root', help='PostgreSQL username')
@click.option('--password', default='root', help='PostgreSQL password')
@click.option('--host', default='localhost', help='PostgreSQL host')
@click.option('--port', default='5432', help='PostgreSQL port')
@click.option('--table', default='yellow_taxi_data', help='Target table name')
@click.option('--db', default='ny_taxi_db', help='PostgreSQL database name')
@click.option('--chunksize', default=10000, type=int, help='Chunk size for batch inserts')
def main(user, password, host, port, table, db, chunksize):
    """
    Ingest trip and lookup data into PostgreSQL database.
    """
    click.echo(f"Connecting to PostgreSQL at {host}:{port}/{db}")
    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")

    lookup = pd.read_csv('taxi_zone_lookup.csv', dtype=dtype_lookup)
    lookup.to_sql(name='taxi_zone_lookup', con=engine, if_exists='replace', index=False)
    click.echo(f"✅ Successfully ingested lookup data into 'taxi_zone_lookup'")

    trip = pd.read_parquet("green_tripdata_2025-11.parquet")
    for i in date_col_trip:
        trip[i] = pd.to_datetime(trip[i],errors='coerce')
    trip = trip.astype(dtype_trip)

    first = True
    total_rows = 0
    click.echo(f"Ingesting trip data into table '{table}'...")
    for start in tqdm(range(0, len(trip), chunksize), desc="Processing chunks"):
        df_chunk = trip.iloc[start:start + chunksize]
        if first:
            df_chunk.to_sql(name=table, con=engine, if_exists='replace', index=False)
            first = False
        else:
            df_chunk.to_sql(name=table, con=engine, if_exists='append', index=False)
        total_rows += len(df_chunk)

    click.echo(f"✅ Successfully ingested trip data {total_rows:,} rows into '{table}'")

if __name__ == '__main__':
    main()
