#!/bin/env python
"""Main module for budget"""

from pathlib import Path
import psycopg2
from pyyamlconfig import load_config


class Budget:
    """Main class for budget"""
    def __init__(self):
        self.config = load_config(f'{Path.home()}/.config/budget.yaml')

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
                print(cur.fetchone())

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
                        date = lines.pop(0).strip()
                        amount = lines.pop(0).strip()
                        balance = lines.pop(0).strip()
                        print(title, date, amount, balance)
                        cur.execute(f"SELECT * FROM insert_title('{title}');")
                        (title_id,) = cur.fetchone()
                        print(title_id)
