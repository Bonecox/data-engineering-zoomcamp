#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm


## Parameters

pg_user = 'root'
pg_pass = 'root'
pg_host = 'pgdatabase-hw'
pg_port = 5432
pg_db = 'ny_taxi_hw'
target_table = 'green_ny_taxi'
lookup_table = 'taxi_zone_lookup'

engine = create_engine(f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')


df = pd.read_parquet(
    'green_tripdata_2025-11.parquet')
df.head()



df.to_sql(
    name=target_table,
    con=engine,
    if_exists='replace'
)

df_zones_lookup = pd.read_csv('taxi_zone_lookup.csv')
df_zones_lookup.to_sql(
    name=lookup_table,
    con=engine,
    if_exists='replace'
)

