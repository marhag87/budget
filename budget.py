#!/bin/env python

import psycopg2
from pyyamlconfig import load_config
from pathlib import Path
home = str(Path.home())

config = load_config(f'{home}/.config/budget.yaml')

with psycopg2.connect(
        dbname=config.get('database'),
        user=config.get('username'),
        password=config.get('password'),
        host=config.get('hostname'),
     ) as con:
        with con.cursor() as cur:
            cur.execute("SELECT * FROM transactions_for_month(2017, 10);")
            print(cur.fetchone())

