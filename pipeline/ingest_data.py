import click
import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm


DTYPE = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}

PARSE_DATES = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]


@click.command()
@click.option('--user', default='root', help='PostgreSQL username')
@click.option('--password', default='root', help='PostgreSQL password')
@click.option('--host', default='localhost', help='PostgreSQL host')
@click.option('--port', default='5432', help='PostgreSQL port')
@click.option('--db', default='ny_taxi', help='PostgreSQL database name')
@click.option('--table', default='yellow_taxi_data', help='Target table name')
@click.option('--year', default=2021, type=int, help='Year of taxi data')
@click.option('--month', default=1, type=int, help='Month of taxi data (1-12)')
@click.option('--chunksize', default=100000, type=int, help='Chunk size for batch inserts')
def main(user, password, host, port, db, table, year, month, chunksize):
    """Ingest NYC Yellow Taxi data into PostgreSQL database."""
    
    prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/'
    url = f'{prefix}yellow_tripdata_{year}-{month:02d}.csv.gz'
    
    click.echo(f"Connecting to PostgreSQL at {host}:{port}/{db}")
    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")
    
    click.echo(f"Downloading data from: {url}")
    df_iter = pd.read_csv(
        url,
        dtype=DTYPE,
        parse_dates=PARSE_DATES,
        iterator=True,
        chunksize=chunksize
    )

    first = True
    total_rows = 0

    click.echo(f"Ingesting data into table '{table}'...")
    for df_chunk in tqdm(df_iter, desc="Processing chunks"):
        if first:
            df_chunk.to_sql(name=table, con=engine, if_exists='replace', index=False)
            first = False
        else:
            df_chunk.to_sql(name=table, con=engine, if_exists='append', index=False)
        total_rows += len(df_chunk)

    click.echo(f"✅ Successfully ingested {total_rows:,} rows into '{table}'")


if __name__ == '__main__':
    main()
