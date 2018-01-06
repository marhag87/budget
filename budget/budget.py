#!/bin/env python
"""Main module for budget"""

from pathlib import Path
import psycopg2
from pyyamlconfig import load_config


class Budget:
    """Main class for budget"""
    def __init__(self, config=None):
        if config is None:
            config = f'{Path.home()}/.config/budget.yaml'
        self.config = load_config(config)

    def get_transactions(self, year, month):
        """Example function for printing a set of transactions"""
        with psycopg2.connect(
            dbname=self.config.get('database'),
            user=self.config.get('username'),
            password=self.config.get('password'),
            host=self.config.get('hostname'),
        ) as con:
            with con.cursor() as cur:
                cur.execute(f"SELECT * FROM transactions_for_month({year}, {month});")
                return cur.fetchone()

    def insert_transactions(self, transactionfile='transactions.txt'):
        """Insert all the transactions found in the file provided"""
        with psycopg2.connect(
            dbname=self.config.get('database'),
            user=self.config.get('username_rw'),
            password=self.config.get('password_rw'),
            host=self.config.get('hostname'),
        ) as con:
            with con.cursor() as cur:
                with open(transactionfile) as file:
                    lines = file.readlines()
                    while lines:
                        title = lines.pop(0).strip()
                        cur.execute(f"SELECT * FROM insert_title('{title}');")
                        (title_id,) = cur.fetchone()
                        return title_id
