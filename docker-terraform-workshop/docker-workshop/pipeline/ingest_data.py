#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm
import click
# Just for verbose of the df insert

dtype = {
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

parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]


def run(pg_user, pg_pass, pg_host, pg_port, pg_db, year, month, target_table, chunk):


    engine = create_engine(f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')

    prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/'

    df_iter = pd.read_csv(
        prefix + f'yellow_tripdata_{year}-{month:02d}.csv.gz',
        # nrows=100,
        dtype=dtype,
        parse_dates=parse_dates,
        iterator=True,
        chunksize=chunk
    )

    first = True
    for df_chunk in tqdm(df_iter):
        if first:
            df_chunk.head(n=0).to_sql(
                name=target_table, 
                con=engine,
                  if_exists='replace'
            )
            first=False
        else:
            df_chunk.to_sql(name=target_table,
                             con=engine, 
                             if_exists='append'
            )

@click.command()
@click.option('--pg-user', default='root', show_default=True, help='Postgres user')
@click.option('--pg-pass', default='root', show_default=True, help='Postgres password')
@click.option('--pg-host', default='localhost', show_default=True, help='Postgres host')
@click.option('--pg-port', default=5432, show_default=True, help='Postgres port')
@click.option('--pg-db', default='ny_taxi', show_default=True, help='Postgres database')
@click.option('--year', default=2021, show_default=True, type=int, help='Year of the dataset')
@click.option('--month', default=1, show_default=True, type=int, help='Month of the dataset (1-12)')
@click.option('--target-table', default='yellow_taxi_data', show_default=True, help='Target table name')
@click.option('--chunk', default=100000, show_default=True, type=int, help='Chunk size for CSV iterator')


def run_click(pg_user, pg_pass, pg_host, pg_port, pg_db, year, month, target_table, chunk):
    run(pg_user, pg_pass, pg_host, pg_port, pg_db, year, month, target_table, chunk)


if __name__ == '__main__':
    run_click()